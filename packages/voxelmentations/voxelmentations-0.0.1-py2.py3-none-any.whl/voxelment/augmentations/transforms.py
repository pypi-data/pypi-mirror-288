# import torch

# from random import uniform, randint, choices

from random import randint

# import exgment.augmentations.misc as M
import voxelment.augmentations.functional as F

from voxelment.core.transforms import VoxelOnlyTransform, DualTransform

class Flip(DualTransform):
    """Flip the input voxel along a dim.
    """
    def __init__(
            self,
            is_trainable=False,
            p=0.5,
        ):
        """
        """
        super(Flip, self).__init__(is_trainable, p)

        self.dims = (-3, -2, -1)

    def apply(self, voxel, dims, **params):
        return F.flip(voxel, dims)

    def get_params(self):
        code = randint(1, 2**len(self.dims)-1)

        dims = tuple()

        for dim in self.dims:
            if code % 2 == 1:
                dims = (*dims, dim)

            code = code / 2

        return {'dims': dims}

    def get_transform_init_args_names(self):
        return tuple()

class XYFlip(Flip):
    """Flip the input voxel in x-y plane.
    """
    def __init__(
            self,
            is_trainable=False,
            p=0.5,
        ):
        """
        """
        super(XYFlip, self).__init__(is_trainable, p)

        self.dims = (-3, -2)

class ZFlip(Flip):
    """Flip the input voxel in z dim.
    """
    def __init__(
            self,
            is_trainable=False,
            p=0.5,
        ):
        """
        """
        super(ZFlip, self).__init__(is_trainable, p)

        self.dims = (-1, )

class RandomRotate90(DualTransform):
    """Random rotate the input voxel in a plane.
    """
    def __init__(
            self,
            is_trainable=False,
            p=0.5,
        ):
        """
        """
        super(RandomRotate90, self).__init__(is_trainable, p)

        self.planes = ((-3, -2), (-3, -1), (-2, -1))

    def apply(self, voxel, plane, times, **params):
        return F.rot90(voxel, plane, times)

    def get_params(self):
        code = randint(0, len(self.planes)-1)

        plane = self.planes[code]
        times = randint(1, 3)

        return {'plane': plane, 'times': times}

    def get_transform_init_args_names(self):
        return tuple()


class RandomXYRotate90(RandomRotate90):
    """Random rotate the input voxel in x-y plane.
    """
    def __init__(
            self,
            is_trainable=False,
            p=0.5,
        ):
        """
        """
        super(RandomXYRotate90, self).__init__(is_trainable, p)

        self.planes = ((-3, -2), )

# 1, 2, 4

# 001 - x
# 010 - y
# 011 - xy
# 100 - z
# 101 - zx
# 110 - zy 
# 111 - zxy

# class AmplitudeInvert(ExgOnlyTransform):
#     """Invert the input exg.
#     """
#     def apply(self, exg, **params):
#         return F.amplitude_invert(exg)

#     def get_transform_init_args_names(self):
#         return tuple()

# class ChannelShuffle(ExgOnlyTransform):
#     """Randomly rearrange channels of the input exg.
#     """
#     def apply(self, exg, channel_order, **params):
#         return F.channel_shuffle(exg, channel_order)

#     @property
#     def targets_as_params(self):
#         return ['exg']

#     def get_params_dependent_on_targets(self, params):
#         channel_order = torch.randperm(params['exg'].shape[1])

#         return {'channel_order': channel_order}

#     def get_transform_init_args_names(self):
#         return ()

# class ChannelDropout(ExgOnlyTransform):
#     """Randomly drop channels in the input exg.
#     """
#     def __init__(
#             self,
#             channel_drop_range=(1, 1),
#             fill_value=0,
#             is_trainable=False,
#             p=0.5,
#         ):
#         """
#             :args:
#                 channel_drop_range: (int, int)
#                     range for select the number of dropping channels
#                 fill_value: int
#                     fill value for dropped channels
#         """
#         super(ChannelDropout, self).__init__(is_trainable, p)

#         self.channel_drop_range = M.prepare_int_asymrange(channel_drop_range, 'channel_drop_range', 1)

#         self.min_drop_channels = channel_drop_range[0]
#         self.max_drop_channels = channel_drop_range[1]

#         self.fill_value = M.prepare_float(fill_value, 'fill_value')

#     def apply(self, exg, channels_to_drop, **params):
#         return F.channel_dropout(exg, channels_to_drop, self.fill_value)

#     @property
#     def targets_as_params(self):
#         return ['exg']

#     def get_params_dependent_on_targets(self, params):
#         num_channels = params['exg'].shape[1]

#         if num_channels == 1:
#             raise NotImplementedError('exg has one channel. ChannelDropout is not defined.')

#         if not ( self.max_drop_channels < num_channels ):
#             raise ValueError('Can not drop all channels in ChannelDropout.')

#         num_drop_channels = randint(self.min_drop_channels, self.max_drop_channels + 1)
#         channels_to_drop = choices(range(num_channels), k=num_drop_channels)

#         return {'channels_to_drop': channels_to_drop}

#     def get_transform_init_args_names(self):
#         return ('channel_drop_range', 'fill_value')

# class AmplitudeScale(ExgOnlyTransform):
#     """Scale amplitude of the input exg.
#     """
#     def __init__(
#             self,
#             scaling_range=(-0.05, 0.05),
#             is_trainable=False,
#             p=0.5,
#         ):
#         """
#             :args:
#                 scaling_range: (float, float)
#                     range for selecting scaling factor
#         """
#         super(AmplitudeScale, self).__init__(is_trainable, p)

#         self.scaling_range = M.prepare_float_symrange(scaling_range, 'scaling_range')

#         self.min_scaling_range = self.scaling_range[0]
#         self.max_scaling_range = self.scaling_range[1]

#     def apply(self, exg, scaling_factor, **params):
#         return F.amplitude_scale(exg, scaling_factor)

#     def get_params(self):
#         scaling_factor = 1 + uniform(self.min_scaling_range, self.max_scaling_range)

#         return {'scaling_factor': scaling_factor}

#     def get_transform_init_args_names(self):
#         return ('scaling_range', )
