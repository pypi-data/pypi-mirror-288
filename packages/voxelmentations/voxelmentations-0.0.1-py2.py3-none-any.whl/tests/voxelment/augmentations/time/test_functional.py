# import pytest

# import torch

# import exgment.augmentations.time.functional as F
# from exgment.augmentations.enum import BorderType

# @pytest.mark.time
# def test_time_reverse_CASE_default():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], ]])
#     expected = torch.tensor([[[6, 5, 4, 3, 2, 1], ]])

#     with torch.no_grad():
#         output = F.time_reverse(input)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_shift_CASE_zero_shift():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], ]])
#     expected = torch.tensor([[[1, 2, 3, 4, 5, 6], ]])

#     with torch.no_grad():
#         output = F.time_shift(input, 0., BorderType.CONSTANT, 0.)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_shift_CASE_positive_shift():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], ]])
#     expected = torch.tensor([[[0, 1, 2, 3, 4, 5], ]])

#     with torch.no_grad():
#         output = F.time_shift(input, 0.167, BorderType.CONSTANT, 0.)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_shift_CASE_negative_shift():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], ]])
#     expected = torch.tensor([[[2, 3, 4, 5, 6, 0], ]])

#     with torch.no_grad():
#         output = F.time_shift(input, -0.167, BorderType.CONSTANT, 0.)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_segment_swap_CASE_default():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[5, 6, 1, 2, 3, 4], [2, 1, 6, 5, 4, 3]]])

#     segment_order = [2, 0, 1]

#     with torch.no_grad():
#         output = F.time_segment_swap(input, segment_order)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_cutout_CASE_default():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[0, 0, 3, 4, 5, 6], [0, 0, 4, 3, 2, 1]]])

#     cutouts = [(0, 2)]
#     fill_value = 0

#     with torch.no_grad():
#         output = F.time_cutout(input, cutouts, fill_value)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_crop_CASE_default():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[2, 3], [5, 4]]])

#     left_bound = 1 / 4
#     crop_length = 2

#     with torch.no_grad():
#         output = F.time_crop(input, left_bound, crop_length)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_crop_CASE_equal_legth():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])

#     left_bound = 1 / 6
#     crop_length = 6

#     with torch.no_grad():
#         output = F.time_crop(input, left_bound, crop_length)

#     assert torch.allclose(output, expected)

# @pytest.mark.time
# def test_time_crop_CASE_large_length():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])

#     left_bound = 1 / 6
#     crop_length = 8

#     with torch.no_grad():
#         with pytest.raises(ValueError):
#             F.time_crop(input, left_bound, crop_length)

# @pytest.mark.time
# def test_pad_CASE_border_constant():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[0, 0, 1, 2, 3, 4, 5, 6, 0, 0], [0, 0, 6, 5, 4, 3, 2, 1, 0, 0]]])

#     left_pad = 2
#     rigth_pad = 2

#     with torch.no_grad():
#         output = F.pad(input, left_pad, rigth_pad, BorderType.CONSTANT, 0.)

#     assert torch.allclose(output, expected)
