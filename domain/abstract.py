import abc
from functools import cached_property

from tts.transform import Transform


class DomainEntity(abc.ABC):
    @cached_property
    def transform(self):
        return Transform.from_size_and_coords(1)

    def as_dict(self):
        raise NotImplementedError
