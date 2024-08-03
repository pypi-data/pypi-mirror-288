# import pytest

# import torch
# import exgment.augmentations.functional as F

# def test_amplitude_invert_CASE_default():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], ]])
#     expected = torch.tensor([[[-1, -2, -3, -4, -5, -6], ]])

#     with torch.no_grad():
#         output = F.amplitude_invert(input)

#     assert torch.allclose(output, expected)

# def test_channel_shuffle_CASE_direct_order():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])

#     with torch.no_grad():
#         output = F.channel_shuffle(input, (0, 1))

#     assert torch.allclose(output, expected)

# def test_channel_shuffle_CASE_inverse_order():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6]]])

#     with torch.no_grad():
#         output = F.channel_shuffle(input, (1, 0))

#     assert torch.allclose(output, expected)

# def test_channel_dropout_CASE_default():
#     input = torch.tensor([[[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]]])
#     expected = torch.tensor([[[0, 0, 0, 0, 0, 0], [6, 5, 4, 3, 2, 1]]])

#     channels_to_drop = (0, )
#     fill_value = 0

#     with torch.no_grad():
#         output = F.channel_dropout(input, channels_to_drop, fill_value)

#     assert torch.allclose(output, expected)
