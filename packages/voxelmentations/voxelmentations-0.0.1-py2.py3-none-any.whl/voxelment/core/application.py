import torch
import random

from voxelment.core.utils import get_shortest_class_fullname

class Apply(torch.nn.Module):
    """Root class for single and compound augmentations
    """

    REPR_INDENT_STEP=2

    def __init__(self, is_trainable, p):
        """
            :args:
                is_trainable: bool
                    the flag of trainable behaviour
                p: float
                    the probability of application
        """
        super().__init__()

        self.is_trainable = is_trainable
        self.p = p

    def whether_apply(self, force_apply):
        return force_apply or (random.random() < self.p)

    def forward(self, *args, **data):
        raise NotImplementedError

    def get_class_name(self):
        """
            :return:
                output: str
                    the name of class
        """
        return self.__class__.__name__

    @classmethod
    def get_class_fullname(cls):
        """
            :return:
                output: str
                    the full name of class
        """
        return get_shortest_class_fullname(cls)

    def get_base_init_args(self):
        """
            :return:
                output: dict
                    initialization parameters
        """
        return {'is_trainable': self.is_trainable, 'p': self.p}
