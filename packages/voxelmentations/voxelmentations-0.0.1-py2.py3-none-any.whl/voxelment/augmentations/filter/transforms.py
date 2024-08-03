# import torch

# import exgment.augmentations.misc as M
# import exgment.augmentations.filter.functional as F

# from exgment.core.transforms import ExgOnlyTransform

# class _STE(torch.autograd.Function):
#     @staticmethod
#     def forward(ctx, input_forward, input_backward):
#         ctx.shape = input_backward.shape
#         return input_forward

#     @staticmethod
#     def backward(ctx, grad_in):
#         return None, grad_in.sum_to_size(ctx.shape)

# def ste(input_forward, input_backward):
#     return _STE.apply(input_forward, input_backward).clone()

# class LowPassFilter(ExgOnlyTransform):
#     """Apply low-pass filter to the input exg.
#     """
#     def __init__(
#             self,
#             exg_frequency=500.,
#             cutoff_frequency=47.,
#             is_trainable=False,
#             p=1.0,
#         ):
#         """
#             :NOTE:
#                 cutoff_frequency:
#                     47 Hz (default for ecg) "Effective Data Augmentation, Filters, and Automation Techniques for Automatic 12-Lead ECG Classification Using Deep Residual"

#             :args:
#                 exg_frequency: float
#                     frequency of the input exg
#                 cutoff_frequency: float
#                     cutoff frequency for filter
#         """
#         super(LowPassFilter, self).__init__(is_trainable, p)

#         self.exg_frequency = M.prepare_non_negative_float(exg_frequency, 'exg_frequency')

#         cutoff_frequency = M.prepare_non_negative_float(cutoff_frequency, 'cutoff_frequency')

#         if self.is_trainable:
#             self.cutoff_frequency = torch.nn.Parameter(
#                 torch.tensor(cutoff_frequency)
#             )
#         else:
#             self.cutoff_frequency = cutoff_frequency

#     def apply(self, exg, **params):
#         exg = F.lowpass_filter(exg, self.exg_frequency, self.cutoff_frequency)

#         if self.is_trainable:
#             return ste(exg, self.cutoff_frequency)
#         else:
#             return exg

#     def get_transform_init_args_names(self):
#         return ('exg_frequency', 'cutoff_frequency')
