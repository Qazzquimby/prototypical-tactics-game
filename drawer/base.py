import abc

from pygame import Surface


class BaseDrawer(abc.ABC):
    def draw(self, object) -> Surface:
        raise NotImplementedError
