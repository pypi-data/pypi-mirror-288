import torch
import torch.nn as nn
import zlib
import numpy as np
from torch import Tensor
from torchvision.transforms import ToPILImage
from compressai.layers import GDN1, conv1x1, conv3x3, AttentionBlock
from compressai.models import CompressionModel
from compressai.models.utils import deconv
from compressai.entropy_models import EntropyBottleneck
from diffusers.models.autoencoders.autoencoder_kl import Encoder, Decoder

class NormClip(nn.Module):
    def __init__(self, min_val, max_val):
        super(NormClip, self).__init__()
        self.max_val = max_val
        self.hardtanh = nn.Hardtanh(min_val=min_val, max_val=max_val)
    def forward(self, x):
        norm = x.norm(dim=1, keepdim=True)
        direction = x / (norm + 1e-8)  # Add epsilon to avoid division by zero
        clipped_norm = self.hardtanh(norm)
        return direction * clipped_norm

class ResidualBottleneckBlock(nn.Module):

    def __init__(self, in_ch: int, out_ch: int):
        super().__init__()
        mid_ch = min(in_ch, out_ch) // 2
        self.conv1 = conv1x1(in_ch, mid_ch)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(mid_ch, mid_ch)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = conv1x1(mid_ch, out_ch)
        self.skip = conv1x1(in_ch, out_ch) if in_ch != out_ch else nn.Identity()

    def forward(self, x: Tensor) -> Tensor:
        identity = self.skip(x)

        out = x
        out = self.conv1(out)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)

        return out + identity
        
class RateDistortionAutoEncoder(CompressionModel):
    def __init__(self, N=128, channels=3):
        super().__init__()
        self.entropy_bottleneck = EntropyBottleneck(N)
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            nn.AvgPool2d(stride=2, kernel_size=2),
            nn.Conv2d(channels, 8, stride=2, kernel_size=5, padding=2),
            GDN1(8),
            nn.Conv2d(8, 24, stride=2, kernel_size=5, padding=2),
            GDN1(24),
            nn.Conv2d(24, 72, stride=2, kernel_size=5, padding=2),
            GDN1(72),
            nn.Conv2d(72, N, stride=2, kernel_size=5, padding=2),
        )
        self.decode = nn.Sequential(
            AttentionBlock(N),
            deconv(N, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, N, kernel_size=5, stride=2),
            AttentionBlock(N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, channels, kernel_size=5, stride=2),
            nn.Upsample(scale_factor=2,mode="bilinear"),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
        
    def forward(self, x):
        y = self.encode(x)
        y_hat, y_likelihoods = self.entropy_bottleneck(y)
        x_hat = self.decode(y_hat)
        return x_hat, y_likelihoods
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self

class RDAEVQ(CompressionModel):
    def __init__(self, N=192, latent_dim=8, channels=3):
        super().__init__()

        self.entropy_bottleneck = EntropyBottleneck(latent_dim)
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            nn.AvgPool2d(stride=2, kernel_size=2),
            nn.Conv2d(channels, N//4, stride=2, kernel_size=5, padding=2),
            GDN1(N//4),
            nn.Conv2d(N//4, N, stride=2, kernel_size=5, padding=2),
            GDN1(N),
            nn.Conv2d(N, N, stride=2, kernel_size=5, padding=2),
            GDN1(N),
            nn.Conv2d(N, latent_dim, stride=1, kernel_size=1, padding=0),
            torch.nn.Hardtanh(min_val=-8.49, max_val=7.49),
        )
        self.decode = nn.Sequential(
            AttentionBlock(latent_dim),
            deconv(latent_dim, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, N, kernel_size=5, stride=2),
            AttentionBlock(N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, channels, kernel_size=5, stride=2),
            nn.Upsample(scale_factor=2,mode="bilinear"),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
        
    def forward(self, x):
        y = self.encode(x)
        y_hat, y_likelihoods = self.entropy_bottleneck(y)
        x_hat = self.decode(y_hat)
        return x_hat, y_likelihoods
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self
        
class LLIC_v0p3(CompressionModel):
    def __init__(self, N=394, latent_dim=16, channels=3):
        super().__init__()
        channel_factor = (N/channels)**(1/4)
        C1 = int((channel_factor**1)*channels)
        C2 = int((channel_factor**2)*channels)
        C3 = int((channel_factor**3)*channels)
        C4 = int((channel_factor**4)*channels)
        self.entropy_bottleneck = EntropyBottleneck(latent_dim)
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            nn.Conv2d(channels, C1, stride=2, kernel_size=5, padding=2),
            GDN1(C1),
            nn.Conv2d(C1, C2, stride=2, kernel_size=5, padding=2),
            GDN1(C2),
            nn.Conv2d(C2, C3, stride=2, kernel_size=5, padding=2),
            GDN1(C3),
            nn.Conv2d(C3, C4, stride=2, kernel_size=5, padding=2),
            GDN1(C4),
            nn.Conv2d(C4, latent_dim, stride=1, kernel_size=5, padding=2),
            torch.nn.Hardtanh(min_val=-8.49, max_val=7.49),
        )
        self.decode = nn.Sequential(
            AttentionBlock(latent_dim),
            deconv(latent_dim, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, N, kernel_size=5, stride=2),
            AttentionBlock(N),
            deconv(N, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            ResidualBottleneckBlock(N, N),
            deconv(N, channels, kernel_size=5, stride=2),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
        
    def forward(self, x):
        y = self.encode(x)
        y_hat, y_likelihoods = self.entropy_bottleneck(y)
        x_hat = self.decode(y_hat)
        return x_hat, y_likelihoods
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self

def subpel_conv5x5(in_ch: int, out_ch: int, r: int = 1) -> nn.Sequential:
    return nn.Sequential(
        nn.Conv2d(in_ch, out_ch * r**2, kernel_size=5, padding=2), nn.PixelShuffle(r)
    )

class LLIC_v0p4(CompressionModel):
    def __init__(self, N=384, latent_dim=4, channels=3):
        super().__init__()
        channel_factor = (N/channels)**(1/3)
        C1 = int((channel_factor**1)*channels)
        C2 = int((channel_factor**2)*channels)
        C3 = int((channel_factor**3)*channels)
        self.entropy_bottleneck = EntropyBottleneck(latent_dim)
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            nn.Conv2d(channels, C1, stride=2, kernel_size=5, padding=2),
            GDN1(C1),
            nn.Conv2d(C1, C2, stride=2, kernel_size=5, padding=2),
            GDN1(C2),
            nn.Conv2d(C2, C3, stride=2, kernel_size=5, padding=2),
            GDN1(C3),
            nn.Conv2d(C3, latent_dim, stride=1, kernel_size=5, padding=2),
            torch.nn.Hardtanh(min_val=-8.49, max_val=7.49),
        )
        self.decode = nn.Sequential(
            AttentionBlock(latent_dim),
            deconv(latent_dim, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            AttentionBlock(N),
            deconv(N, N, kernel_size=5, stride=2),
            ResidualBottleneckBlock(N, N),
            subpel_conv5x5(N, channels, 2),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
        
        
    def forward(self, x):
        y = self.encode(x)
        y_hat, y_likelihoods = self.entropy_bottleneck(y)
        x_hat = self.decode(y_hat)
        return x_hat, y_likelihoods
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self


class LLIC_v0p7(CompressionModel):
    def __init__(self, N=512, latent_dim=8, channels=3, max_norm=3.3):
        super().__init__()
        self.entropy_bottleneck = EntropyBottleneck(latent_dim)
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            Encoder(
                in_channels = channels,
                out_channels = latent_dim,
                down_block_types = ('DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                double_z = False,
                mid_block_add_attention=True,
            ),
            NormClip(0.0, max_norm),
        )
        self.decode = nn.Sequential(
            Decoder(
                in_channels = latent_dim,
                out_channels = channels,
                up_block_types = ('UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                mid_block_add_attention=True,
            ),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
           
    def forward(self, x):
        y = self.encode(x)
        y_hat, y_likelihoods = self.entropy_bottleneck(y)
        x_hat = self.decode(y_hat)
        return x_hat, y_likelihoods
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self

class LLIC_v0p7_ste(CompressionModel):
    def __init__(self, N=512, latent_dim=8, channels=3, max_norm=3.3):
        super().__init__()
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            Encoder(
                in_channels = channels,
                out_channels = latent_dim,
                down_block_types = ('DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                double_z = False,
                mid_block_add_attention=True,
            ),
            NormClip(max_norm),
        )
        self.decode = nn.Sequential(
            Decoder(
                in_channels = latent_dim,
                out_channels = channels,
                up_block_types = ('UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                mid_block_add_attention=True,
            ),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
        
    def forward(self, x):
        y = self.encode(x)
        y_hat = y + y.round().detach() - y.detach()
        x_hat = self.decode(y_hat)
        return x_hat
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self

class LLIC_v0p8(CompressionModel):
    def __init__(self, N=512, latent_dim=8, channels=3, min_norm=4.0-1e8, max_norm=4.0):
        super().__init__()
        self.entropy_bottleneck = EntropyBottleneck(latent_dim)
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            Encoder(
                in_channels = channels,
                out_channels = latent_dim,
                down_block_types = ('DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                double_z = False,
                mid_block_add_attention=True,
            ),
            NormClip(min_norm,max_norm),
        )
        self.decode = nn.Sequential(
            Decoder(
                in_channels = latent_dim,
                out_channels = channels,
                up_block_types = ('UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                mid_block_add_attention=True,
            ),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )        
        
    def forward(self, x):
        y = self.encode(x)
        y_hat, y_likelihoods = self.entropy_bottleneck(y)
        x_hat = self.decode(y_hat)
        return x_hat, y_likelihoods
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self

class LLIC_v0p8_ste(CompressionModel):
    def __init__(self, N=512, latent_dim=8, channels=3, min_norm=4.0-1e8, max_norm=4.0):
        super().__init__()
        self.device = torch.device('cpu')
        self.encode = nn.Sequential(
            Encoder(
                in_channels = channels,
                out_channels = latent_dim,
                down_block_types = ('DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D','DownEncoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                double_z = False,
                mid_block_add_attention=True,
            ),
            NormClip(min_norm, max_norm),
        )
        self.decode = nn.Sequential(
            Decoder(
                in_channels = latent_dim,
                out_channels = channels,
                up_block_types = ('UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D','UpDecoderBlock2D',),
                block_out_channels = (N//4,N//2,N,N),
                layers_per_block = 2,
                norm_num_groups = 32,
                act_fn = 'silu',
                mid_block_add_attention=True,
            ),
            torch.nn.Hardtanh(min_val=-0.5, max_val=0.5),
        )
        
    def forward(self, x):
        y = self.encode(x)
        y_hat = y + y.round().detach() - y.detach()
        x_hat = self.decode(y_hat)
        return x_hat
        
    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def cuda(self, device=None):
        super().cuda(device)
        self.device = torch.device('cuda' if device is None else device)
        return self

    def cpu(self):
        super().cpu()
        self.device = torch.device('cpu')
        return self
        
def lossy_analysis_transform(x, model):
    z = model.encode(x).round().to(torch.int8).detach().cpu().numpy()
    return z
    
def lossless_entropy_encode(z):
    original_shape = z.shape
    compressed_img = zlib.compress(z.tobytes(), level=9)
    return compressed_img, original_shape

def compress(img, model):
    z = lossy_analysis_transform(img, model)
    compressed_img, original_shape = lossless_entropy_encode(z)
    return compressed_img, original_shape

def entropy_decoder(compressed_img, original_shape):
    decompressed = zlib.decompress(compressed_img)
    ẑ = np.frombuffer(decompressed, dtype=np.int8)
    ẑ = ẑ.reshape(original_shape)
    return ẑ
    
def synthesis_transform(ẑ, model):
    ẑ = torch.tensor(ẑ).to(torch.float).to(model.device)
    x̂ = model.decode(ẑ).detach().cpu()
    return x̂
    
def decompress(compressed_img, original_shape, model):
    ẑ = entropy_decoder(compressed_img,original_shape)
    x̂ = synthesis_transform(ẑ, model)
    return x̂

import torch
import numpy as np

def vector_quantize_encode(z, codebook, device='cpu'):
    batch_size, C, H, W = z.shape
    z = z.to(device)
    codebook = codebook.to(device)
    z_reshaped = z.permute(0, 2, 3, 1).contiguous().view(-1, C)
    distances = torch.cdist(z_reshaped, codebook)
    nearest_codebook_indices = torch.argmin(distances, axis=1)
    code_indices = nearest_codebook_indices.view(batch_size, H, W)
    return code_indices.cpu()

def vector_quantize_reversal(code_indices, codebook, device='cpu'):
    C = codebook.shape[1]
    batch_size, H, W = code_indices.shape
    code_indices = code_indices.to(device)
    codebook = codebook.to(device)
    flattened_indices = code_indices.view(-1)
    recovered_vectors = codebook[flattened_indices]
    recovered_latents = recovered_vectors.view(batch_size, H, W, C).permute(0, 3, 1, 2).contiguous()
    return recovered_latents.cpu()


def preprocess(img_or_batch, device="cpu"):
    if img_or_batch.ndim == 3:
        x = img_or_batch.unsqueeze(0)
    else:
        x = img_or_batch

    x = x.to(torch.float)
    x = x/255
    x = x-0.5
    x = x.to(device)
        
    return x

def postprocess(img_or_batch, batch=False):
    if batch:
        batch = img_or_batch
        return [ToPILImage()(img+0.5) for img in batch]
    else:
        img = img_or_batch
        return ToPILImage()(img+0.5)