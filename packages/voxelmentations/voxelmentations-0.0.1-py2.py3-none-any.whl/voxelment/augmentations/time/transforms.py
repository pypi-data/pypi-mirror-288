# import torch

# from random import randint, random

# import exgment.augmentations.misc as M
# import exgment.augmentations.time.functional as F

# from exgment.augmentations.enum import BorderType, PositionType
# from exgment.core.transforms import ExgOnlyTransform, DualTransform

# class TimeReverse(DualTransform):
#     """Reverse the input exg.
#     """
#     def apply(self, exg, **params):
#         return F.time_reverse(exg)

#     def get_transform_init_args_names(self):
#         return tuple()

# class TimeShift(DualTransform):
#     """Shift the input exg along time axis.
#     """
#     def __init__(
#             self,
#             shift_limit=0.05,
#             border=BorderType.CONSTANT,
#             fill_value=0.,
#             fill_mask_value=0,
#             is_trainable=False,
#             p=0.5,
#         ):
#         """
#             :args:
#                 shift_limit: float
#                     limit of shifting
#                 border: BorderType or str
#                     border type of exg
#                 fill_value: int or float or None
#                     padding value if border_mode is cv2.BORDER_CONSTANT
#                 fill_mask_value: int or None
#                     padding value for mask if border_mode is cv2.BORDER_CONSTANT
#         """
#         super(TimeShift, self).__init__(is_trainable, p)

#         self.shift_limit = M.prepare_non_negative_float(shift_limit, 'shift_limit')

#         self.border = border
#         self.fill_value = M.prepare_float(fill_value, 'fill_value')
#         self.fill_mask_value = M.prepare_int(fill_mask_value, 'fill_mask_value')

#     def apply(self, exg, shift, **params):
#         return F.time_shift(exg, shift, self.border, self.fill_value)

#     def apply_to_mask(self, mask, shift, **params):
#         return F.time_shift(mask, shift, self.border, self.fill_mask_value)

#     def get_params(self):
#         shift = random() * self.shift_limit

#         return {'shift': shift}

#     def get_transform_init_args_names(self):
#         return ('shift_limit', 'border', 'fill_value', 'fill_mask_value')

# class TimeSegmentShuffle(DualTransform):
#     """Randomly shuffle of the input exg segments
#     """
#     def __init__(
#             self,
#             num_segments=5,
#             is_trainable=False,
#             p=0.5,
#         ):
#         """
#             :args:
#                 num_segments: int
#                     count of grid cells on the exg
#         """
#         super(TimeSegmentShuffle, self).__init__(is_trainable, p)

#         self.num_segments = M.prepare_non_negative_int(num_segments, 'num_segments')

#     def apply(self, exg, segment_order, **params):
#         return F.time_segment_swap(exg, segment_order)

#     def get_params(self):
#         segment_order = torch.randperm(self.num_segments)

#         return {'segment_order': segment_order}

#     def get_transform_init_args_names(self):
#         return ('num_segments', )

# class TimeCutout(DualTransform):
#     """Randomly cutout time ranges in the input exg.
#     """
#     def __init__(
#             self,
#             num_ranges=(1, 5),
#             length_range=(0, 50),
#             fill_value=0.,
#             mask_fill_value=None,
#             is_trainable=False,
#             p=0.5,
#         ):
#         """
#             :args:
#                 num_ranges: (int, int)
#                     number of cutout ranges
#                 length_range: (int, int)
#                     range for selecting cutout length
#                 fill_value: float
#                     value to fill cutouted ranges in the input exg
#                 mask_fill_value: int or None
#                     value to fill cutouted ranges in the mask. if value is None, mask is not affected
#         """
#         super(TimeCutout, self).__init__(is_trainable, p)

#         self.num_ranges = M.prepare_int_asymrange(num_ranges, 'num_ranges', 0)

#         self.min_num_ranges = num_ranges[0]
#         self.max_num_ranges = num_ranges[1]

#         self.length_range = M.prepare_int_asymrange(length_range, 'length_range', 0)

#         self.min_length_range = length_range[0]
#         self.max_length_range = length_range[1]

#         self.fill_value = M.prepare_float(fill_value, 'fill_value')
#         self.mask_fill_value = mask_fill_value

#     def apply(self, exg, cutouts, **params):
#         return F.time_cutout(exg, cutouts, self.fill_value)

#     def apply_to_mask(self, mask, cutouts, **params):
#         if self.mask_fill_value is None:
#             return mask
#         else:
#             return F.time_cutout(mask, cutouts, self.mask_fill_value)

#     @property
#     def targets_as_params(self):
#         return ['exg']

#     def get_params_dependent_on_targets(self, params):
#         length = params['exg'].shape[-1]

#         cutouts = []

#         for _ in range(randint(self.min_num_ranges, self.max_num_ranges + 1)):
#             cutout_length = randint(self.min_length_range, self.max_length_range + 1)
#             cutout_start = randint(0, length - cutout_length + 1)

#             cutouts.append((cutout_start, cutout_length))

#         return {'cutouts': cutouts}

#     def get_transform_init_args_names(self):
#         return ('num_ranges', 'length_range', 'fill_value', 'mask_fill_value')

# class TimeCrop(DualTransform):
#     """Crop time segment from the input exg.
#     """
#     def __init__(
#             self,
#             length=5000,
#             position=PositionType.RANDOM,
#             is_trainable=False,
#             p=1.0,
#         ):
#         """
#             :NOTE:
#                 position sets up the position of cropped segment

#             :args:
#                 length: int
#                     the length of cropped time segment
#                 position: PositionType or str
#                     position of cropped time segment
#         """
#         super(TimeCrop, self).__init__(is_trainable, p)

#         self.length = M.prepare_int(length, 'length')
#         self.position = PositionType(position)

#     def apply(self, exg, left_bound, **params):
#         return F.time_crop(exg, left_bound, self.length)

#     def get_params(self):
#         if self.position == PositionType.LEFT:
#             left_bound = 0.0
#         elif self.position == PositionType.CENTER:
#             left_bound = 0.5
#         elif self.position == PositionType.RIGHT:
#             left_bound = 1.0
#         else:
#             left_bound = random()

#         return {'left_bound': left_bound}

#     def get_transform_init_args_names(self):
#         return ('length', 'position')

# class CenterTimeCrop(TimeCrop):
#     """Crop time segment to the center of the input exg.
#     """
#     def __init__(
#             self,
#             length=5000,
#             is_trainable=False,
#             p=1.0,
#         ):
#         """
#             :args:
#                 length: int
#                     the length of cropped region
#         """
#         super(CenterTimeCrop, self).__init__(length, PositionType.CENTER, is_trainable, p)

#     def get_transform_init_args_names(self):
#         return ('length', )

# class RandomTimeCrop(TimeCrop):
#     """Crop a random time segment of the input exg.
#     """
#     def __init__(
#             self,
#             length=5000,
#             is_trainable=False,
#             p=1.0,
#         ):
#         """
#             :args:
#                 length: int
#                     the length of cropped region
#         """
#         super(RandomTimeCrop, self).__init__(length, PositionType.RANDOM, is_trainable, p)

#     def get_transform_init_args_names(self):
#         return ('length', )
