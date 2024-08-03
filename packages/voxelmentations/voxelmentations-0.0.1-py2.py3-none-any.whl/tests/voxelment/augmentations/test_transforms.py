import pytest

import torch
import voxelment as V

SHAPE_PRESERVED_TRANSFORMS = [
    V.Flip,
    V.ZFlip,
    V.XYFlip,
    V.RandomRotate90,
    V.RandomXYRotate90,
#     E.ChannelShuffle,
#     E.ChannelDropout,
#     E.AmplitudeScale,
#     E.TimeReverse,
#     E.TimeShift,
#     E.TimeSegmentShuffle,
#     E.TimeCutout,
#     E.LowPassFilter,
]

SHAPE_UNPRESERVED_TRANSFORMS = [
#     E.TimeCrop,
#     E.RandomTimeCrop,
#     E.CenterTimeCrop,
]

@pytest.mark.parametrize('transform', SHAPE_PRESERVED_TRANSFORMS + SHAPE_UNPRESERVED_TRANSFORMS)
def test_Transform_CASE_repr(transform):
    transform = transform(p=1.0)
    transform.eval()

    repr = str(transform)

    assert 'is_trainable' in repr
    assert 'p' in repr

@pytest.mark.parametrize('transform', SHAPE_PRESERVED_TRANSFORMS)
def test_Transform_CASE_call(transform):
    input = torch.rand(size=(1, 1, 32, 32, 32))
    imask = torch.zeros((1, 1, 32, 32, 32))

    transform = transform(p=1.0)
    transform.eval()

    with torch.no_grad():
        transformed = transform(voxel=input, mask=imask)

    output, omask = transformed['voxel'], transformed['mask']

    assert output.shape == input.shape
    assert not torch.allclose(output, input)

    assert omask.shape == imask.shape

    if isinstance(transform, V.VoxelOnlyTransform):
        assert torch.all(omask == imask)
