from functools import singledispatch
from typing import Any, Callable, Dict, List, Union, Tuple
from .models.base import BaseComparison
from .utils.stats import normalize as normalizeScores, confidenceInterval
from .methods.strings import LevenshteinComparison, JaccardComparison, CosineComparison, FuzzComparison, RegexComparison
from .methods.vectors import EuclideanComparison, ManhattanComparison, CosineVectorComparison, JaccardVectorComparison
import numpy as np

class ComparisonResult:
    def __init__(self, scores: List[float], targets: List[Any], method: str):
        self.scores, self.targets, self.method = scores, targets, method

    def normalize(self): return ComparisonResult(normalizeScores(self.scores), self.targets, f"{self.method} (normalized)")
    def filter(self, threshold: float): return ComparisonResult(*zip(*[(s, t) for s, t in zip(self.scores, self.targets) if s >= threshold]) or ([], []), f"{self.method} (filtered)")
    def top(self, n: int = 1): return sorted(zip(self.scores, self.targets), reverse=True)[0][1] if n == 1 else [t for _, t in sorted(zip(self.scores, self.targets), reverse=True)[:n]]
    def isMatch(self, threshold: float = 0.8): return max(self.scores) >= threshold
    def aboveThreshold(self, threshold: float): return [t for s, t in zip(self.scores, self.targets) if s >= threshold]
    def stats(self): return {stat: func(self.scores) for stat, func in [("mean", np.mean), ("median", np.median), ("std", np.std), ("min", min), ("max", max)]}
    def confInt(self, confidence: float = 0.95): return confidenceInterval(self.scores, confidence)
    def explain(self): return f"Comparison using {self.method} method resulted in scores ranging from {min(self.scores):.2f} to {max(self.scores):.2f}"
    def __str__(self): return f"ComparisonResult(method={self.method}, scores={self.scores}, targets={self.targets})"
    __repr__ = __str__

def getComparisonMethod(method: Union[str, BaseComparison, Callable]) -> BaseComparison:
    if isinstance(method, BaseComparison): return method
    if isinstance(method, str):
        comparisonClass = globals().get(f"{method.capitalize()}Comparison")
        if not comparisonClass: raise ValueError(f"Unknown comparison method: {method}")
        return comparisonClass()
    if callable(method): return method
    raise ValueError("Invalid comparison method")

@singledispatch
def compare(ref: Any, targets: Union[Any, List[Any]], method: Union[str, BaseComparison, Callable] = "levenshtein", **kwargs) -> ComparisonResult:
    raise NotImplementedError(f"Comparison not implemented for type {type(ref)}")

@compare.register(str)
def _(ref: str, targets: Union[str, List[str]], method: Union[str, BaseComparison, Callable] = "levenshtein", **kwargs) -> ComparisonResult:
    targets = [targets] if isinstance(targets, str) else targets
    compMethod = getComparisonMethod(method)
    scores = compMethod(ref, targets)
    return ComparisonResult(normalizeScores(scores) if kwargs.get("normalize", False) else scores, targets, str(compMethod))

@compare.register(list)
def _(ref: list, targets: Union[list, List[list]], method: Union[str, BaseComparison, Callable] = "euclidean", **kwargs) -> ComparisonResult:
    targets = [targets] if isinstance(targets[0], (int, float)) else targets
    compMethod = getComparisonMethod(method)
    scores = compMethod(ref, targets)
    return ComparisonResult(normalizeScores(scores) if kwargs.get("normalize", False) else scores, targets, str(compMethod))

@compare.register(dict)
def _(ref: Dict[str, Any], target: Dict[str, Any], fields: List[str], method: Union[str, BaseComparison, Callable] = "levenshtein", **kwargs) -> ComparisonResult:
    compMethod = getComparisonMethod(method)
    scores = [compMethod(ref.get(field), target.get(field)) for field in fields if field in ref or field in target]
    return ComparisonResult(scores, [target], str(compMethod))

def compareItems(items: Union[Tuple[Dict[str, Any], Dict[str, Any]], List[Dict[str, Any]]],
                 fields: List[str] = None,
                 method: Union[str, BaseComparison, Callable] = "fuzz",
                 crossreference: bool = False,
                 **kwargs) -> Union[ComparisonResult, List[Tuple[int, int, ComparisonResult]]]:
    '''
    Compare items, supporting both tuples of two dictionaries and lists of dictionaries.

    Args:
    items: Either a tuple of two dictionaries to compare, or a list of dictionaries for cross-referencing.
    fields: List of fields to compare. If None, compares all keys.
    method: Comparison method to use.
    crossreference: Whether to perform cross-reference comparison for lists.

    Returns:
    ComparisonResult for tuple input, or list of ComparisonResults for list input with crossreference=True.
    '''

    if isinstance(items, tuple) and len(items) == 2 and all(isinstance(item, dict) for item in items):
        dict1, dict2 = items
        if fields is None:
            fields = list(set(dict1.keys()) | set(dict2.keys()))

        compFunc = method if isinstance(method, BaseComparison) else globals().get(f"{method.capitalize()}Comparison")()

        scores = []
        for field in fields:
            val1 = str(dict1.get(field, ''))
            val2 = str(dict2.get(field, ''))
            scores.append(compFunc(val1, val2))

        return ComparisonResult(scores, fields, str(compFunc))

    elif isinstance(items, list) and all(isinstance(item, dict) for item in items):
        if not crossreference:
            raise ValueError("For list input, crossreference must be True")

        results = []
        for i, item1 in enumerate(items):
            for j, item2 in enumerate(items[i+1:], start=i+1):
                result = compareItems((item1, item2), fields=fields, method=method, **kwargs)
                results.append((i, j, result))

        return results

    else:
        raise ValueError("Invalid input: expected a tuple of two dictionaries or a list of dictionaries")


compare.items = compareItems
