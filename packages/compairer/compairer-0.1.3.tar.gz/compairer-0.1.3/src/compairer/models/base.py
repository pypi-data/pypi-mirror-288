from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

class BaseComparison(ABC):
    def __init__(self, **kwargs):
        self.params = kwargs

    @abstractmethod
    def compare(self, ref: Any, target: Any) -> float:
        """Perform comparison between reference and target."""
        pass

    def batchCompare(self, ref: Any, targets: List[Any]) -> List[float]:
        return [self.compare(ref, target) for target in targets]

    def explain(self, ref: Any, target: Any) -> Dict[str, Any]:
        """Provide explanation for the comparison."""
        return {"method": self.__class__.__name__, "score": self.compare(ref, target)}

    def __call__(self, ref: Any, target: Union[Any, List[Any]]) -> Union[float, List[float]]:
        if isinstance(target, List):
            return self.batchCompare(ref, target)
        return self.compare(ref, target)

    @classmethod
    def register(cls, name: str):
        def decorator(subclass):
            setattr(cls, name, subclass)
            return subclass
        return decorator

    # TODO: Implement a method for serialization/deserialization of comparison objects
    # TODO: Add a method for parameter optimization (e.g., using grid search or other optimization techniques)
    # TODO: Implement a method for generating a detailed report of the comparison process
    # TODO: Consider adding support for async comparisons for large-scale operations