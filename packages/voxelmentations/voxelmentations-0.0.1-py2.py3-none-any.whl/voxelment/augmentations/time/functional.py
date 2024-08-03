# import torch
# import torch.nn.functional as F

# from exgment.augmentations.enum import BorderType

# def time_reverse(exg):
#     return torch.flip(exg, dims=(-1, ))

# def pad(exg, left_pad, rigth_pad, border_mode, fill_value):
#     if border_mode == BorderType.CONSTANT:
#         border_mode = 'constant'
#     else:
#         raise ValueError('Get invalide border_mode: {}'.format(border_mode))

#     exg = F.pad(exg, (left_pad, rigth_pad), border_mode, fill_value)

#     return exg

# def time_shift(exg, shift, border, fill_value):
#     length = exg.shape[-1]

#     pad_ = int(length*shift)

#     if pad_ > 0:
#         exg = pad(exg, pad_, 0, border, fill_value)
#         exg = exg[..., :-pad_]
#     elif pad_ < 0:
#         exg = pad(exg, 0, -pad_, border, fill_value)
#         exg = exg[..., -pad_:]

#     return exg

# def time_segment_swap(exg, segment_order):
#     length = exg.shape[-1]
#     num_segments = len(segment_order)

#     time_point_order = torch.arange(length)
#     time_point_order = torch.tensor_split(time_point_order, num_segments)
#     time_point_order = [ time_point_order[idx] for idx in segment_order ]
#     time_point_order = torch.cat(time_point_order, dim=0)

#     exg = exg[..., time_point_order]

#     return exg

# def time_cutout(exg, cutouts, fill_value):
#     exg = torch.clone(exg)

#     for cutout_start, cutout_length in cutouts:
#         exg[..., cutout_start: cutout_start+cutout_length] = fill_value

#     return exg

# def time_crop(exg, left_bound, crop_length):
#     length = exg.shape[-1]

#     if length < crop_length:
#         raise ValueError(
#             'Requested crop length {crop_length} is '
#             'larger than the exg length {length}'.format(
#                 crop_length=crop_length, length=length
#             )
#         )

#     t1 = int((length - crop_length) * left_bound)
#     t2 = t1 + crop_length

#     return exg[..., t1:t2]
