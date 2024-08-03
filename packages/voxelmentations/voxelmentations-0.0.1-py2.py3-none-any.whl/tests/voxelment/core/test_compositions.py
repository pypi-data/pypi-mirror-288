import pytest

import torch
import voxelment as V

@pytest.mark.core
def test_Sequential_CASE_create_AND_list_error():
    with pytest.raises(RuntimeError, match=r'transforms is type of <.+> that is not list'):
        transform = V.Sequential(
            V.ZFlip()
        )

@pytest.mark.core
def test_Sequential_CASE_create_AND_subtype_error():
    with pytest.raises(RuntimeError, match=r'object at \d+ position is not subtype of Apply'):
        transform = V.Sequential([
            V.ZFlip(),
            object()
        ])

@pytest.mark.core
def test_Sequential_CASE_call_AND_no_transfroms():
    input = torch.ones((1, 1, 32, 32, 32))

    transform = V.Sequential([
    ], p=1.0)
    transform.eval()

    with torch.no_grad():
        transformed = transform(voxel=input)

    output = transformed['voxel']

    assert torch.allclose(output, input)

@pytest.mark.core
def test_Sequential_CASE_call_AND_one_flip():
    input = torch.rand((1, 1, 32, 32, 32))

    transform = V.Sequential([
        V.ZFlip(p=1.0)
    ], p=1.0)
    transform.eval()

    with torch.no_grad():
        transformed = transform(voxel=input)

    output = transformed['voxel']

    assert not torch.allclose(output, input)

@pytest.mark.core
def test_Sequential_CASE_call_AND_double_flip():
    input = torch.rand((1, 1, 32, 32, 32))

    transform = V.Sequential([
        V.ZFlip(p=1.0),
        V.ZFlip(p=1.0)
    ], p=1.0)
    transform.eval()

    with torch.no_grad():
        transformed = transform(voxel=input)

    output = transformed['voxel']

    assert torch.allclose(output, input)
