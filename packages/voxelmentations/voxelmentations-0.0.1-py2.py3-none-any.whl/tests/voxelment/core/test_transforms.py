import pytest

import torch
import voxelment as V

@pytest.mark.core
def test_Identity_CASE_repr():
    transform = V.Identity(p=1.0)
    transform.eval()

    repr = str(transform)

    assert 'Identity' in repr
    assert 'is_trainable' in repr
    assert 'p' in repr

@pytest.mark.core
def test_Identity_CASE_call():
    input = torch.ones((1, 1, 32, 32, 32))
    expected = input

    transform = V.Identity(p=1.0)
    transform.eval()

    with torch.no_grad():
        output = transform(voxel=input)['voxel']

    assert torch.allclose(output, expected)
