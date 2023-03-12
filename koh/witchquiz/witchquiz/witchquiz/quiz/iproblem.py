import abc

class IProblem(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def score(self, stage: int, answer: list[int]) -> int:
        raise NotImplementedError()
    