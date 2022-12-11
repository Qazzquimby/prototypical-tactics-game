import abc


class DomainEntity(abc.ABC):
    def to_tts(self):
        raise NotImplementedError