import torch

def flip(voxel, dims):
    return torch.flip(voxel, dims)

def rot90(voxel, plane, times):
    return torch.rot90(voxel, times, plane)

# def amplitude_invert(exg):
#     return torch.neg(exg)

# def channel_shuffle(exg, channel_order):
#     return exg[..., channel_order, :]

# def channel_dropout(exg, channels_to_drop, fill_value):
#     exg = torch.clone(exg)
#     exg[..., channels_to_drop, :] = fill_value

#     return exg

# def amplitude_scale(exg, scaling_factor):
#     return exg * scaling_factor
