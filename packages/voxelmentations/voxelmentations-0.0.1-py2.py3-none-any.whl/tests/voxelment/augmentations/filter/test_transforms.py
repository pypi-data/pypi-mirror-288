# import pytest

# import torch
# import exgment as E

# @pytest.mark.filter
# def test_LowPassFilter_CASE_is_trainable_AND_true():
#     transform = E.LowPassFilter(is_trainable=True)
#     transform.train()

#     parameters = dict(transform.named_parameters())
#     assert 'cutoff_frequency' in parameters

#     input = torch.rand(1, 12, 5000)

#     ouput = transform(exg=input)['exg']
#     loss = ouput.sum()

#     loss.backward()

#     assert parameters['cutoff_frequency'].grad is not None

# @pytest.mark.filter
# def test_LowPassFilter_CASE_is_trainable_AND_false():
#     transform = E.LowPassFilter(is_trainable=False)
#     transform.train()

#     parameters = dict(transform.named_parameters())
#     assert 'cutoff_frequency' not in parameters
