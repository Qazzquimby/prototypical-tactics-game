import abc


class TtsEntity(abc.ABC):
    def as_dict(self):
        raise NotImplementedError
