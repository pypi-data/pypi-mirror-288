import torch, torch.nn as nn

from voxelment.core.application import Apply
from voxelment.core.utils import format_args, get_shortest_class_fullname

class Compose(Apply):
    def __init__(self, transforms, p):
        """
            :args:
                transforms: list of Apply
                    list of operations to compose
                p: float
                    the probability of application
        """
        super(Compose, self).__init__(False, p)

        if not isinstance(transforms, list):
            raise RuntimeError(
                'transforms is type of {} that is not list'.format(type(transforms))
            )
        elif not all(isinstance(t, Apply) for t in transforms):
            for idx, t in enumerate(transforms):
                if not isinstance(t, Apply):
                    raise RuntimeError(
                        'object at {} position is not subtype of Apply'.format(idx)
                    )

        self.transforms = nn.ModuleList(transforms)

    def __len__(self):
        return len(self.transforms)

    def __getitem__(self, idx):
        return self.transforms[idx]

    def __repr__(self):
        return self.repr()

    def repr(self, indent=Apply.REPR_INDENT_STEP):
        args = self.get_base_init_args()

        repr_string = self.get_class_name() + '(['

        for t in self.transforms:
            repr_string += '\n'

            if hasattr(t, 'repr'):
                t_repr = t.repr(indent + self.REPR_INDENT_STEP)
            else:
                t_repr = repr(t)

            repr_string += ' ' * indent + t_repr + ','

        repr_string += '\n' + ' ' * (indent - self.REPR_INDENT_STEP) + '], {args})'.format(args=format_args(args))

        return repr_string

    @classmethod
    def get_class_fullname(cls):
        return get_shortest_class_fullname(cls)

class Sequential(Compose):
    """Compose transforms to apply sequentially.
    """
    def __init__(self, transforms, p=1.0):
        """
            :args:
                transforms: list of Apply
                    list of operations to apply sequentially
                p: float
                    the probability of application
        """
        super(Sequential, self).__init__(transforms, p)

    def __call__(self, *args, force_apply=False, **data):
        if self.whether_apply(force_apply):
            for transform in self.transforms:
                data = transform(**data)

        return data
