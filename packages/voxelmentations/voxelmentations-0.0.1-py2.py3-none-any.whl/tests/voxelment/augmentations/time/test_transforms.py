# import pytest

# import torch
# import exgment as E

# @pytest.mark.time
# def test_TimeCrop_CASE_rigth_crop():
#     input = torch.rand(12, 5000)
#     imask = torch.zeros((1, 5000))

#     expected_length = 4000

#     transform = E.TimeCrop(length=expected_length, position='left', p=1.0)
#     transform.eval()

#     with torch.no_grad():
#         transformed = transform(exg=input, mask=imask)

#     output, omask = transformed['exg'], transformed['mask']

#     assert output.shape == (input.shape[0], expected_length)
#     assert omask.shape == (imask.shape[0], expected_length)

#     assert torch.allclose(output, input[:, :expected_length])

# @pytest.mark.time
# def test_TimeCutout_CASE_mask_fill_value():
#     input = torch.rand(12, 5000)
#     imask = torch.zeros((1, 5000))

#     mask_fill_value = 0

#     transform = E.TimeCutout(mask_fill_value=mask_fill_value, p=1.0)
#     transform.eval()

#     with torch.no_grad():
#         transformed = transform(exg=input, mask=imask)

#     output, omask = transformed['exg'], transformed['mask']

#     assert torch.all(omask[imask != omask], mask_fill_value)
