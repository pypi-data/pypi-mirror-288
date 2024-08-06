from typing import Any, List, Dict
from .base import BaseComparison

class IncrementalComparison:
    def __init__(self, comparisonMethod: BaseComparison, initialRef: Any = None):
        self.comparisonMethod = comparisonMethod
        self.ref = initialRef
        self.currentScore = 0
        self.count = 0
        self.history: List[Dict[str, Any]] = []

    def update(self, newData: Any) -> float:
        """
        Update the comparison with new data.
        
        Args:
        newData (Any): New data to compare against the reference
        
        Returns:
        float: Updated comparison score
        """
        if self.ref is None:
            self.ref = newData
            self.currentScore = 1.0
        else:
            newScore = self.comparisonMethod.compare(self.ref, newData)
            self.currentScore = (self.currentScore * self.count + newScore) / (self.count + 1)
        
        self.count += 1
        self.history.append({"data": newData, "score": self.currentScore})
        
        return self.currentScore

    def getCurrentScore(self) -> float:
        """Get the current comparison score."""
        return self.currentScore

    def getHistory(self) -> List[Dict[str, Any]]:
        """Get the history of comparisons."""
        return self.history

    def reset(self, newRef: Any = None):
        """
        Reset the incremental comparison.
        
        Args:
        newRef (Any, optional): New reference to use. If None, keeps the current reference.
        """
        if newRef is not None:
            self.ref = newRef
        self.currentScore = 0
        self.count = 0
        self.history = []

# TODO: Implement methods for analyzing the trend of comparison scores over time
# TODO: Add support for different aggregation methods (e.g., exponential moving average)
# TODO: Implement a mechanism for detecting significant changes in the comparison scores
# TODO: Add support for handling streaming data in real-time