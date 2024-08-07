from ..models.base import BaseComparison
import numpy as np
from typing import Union, List, Tuple

def ensureVector(v: Union[List, np.ndarray, int, float, str]) -> np.ndarray:
    return np.array([ord(c) for c in v]) if isinstance(v, str) else np.array([v]) if isinstance(v, (int, float)) else np.asarray(v)

def padVectors(v1: np.ndarray, v2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    maxLen = max(len(v1), len(v2))
    return (np.pad(v1, (0, maxLen - len(v1)), 'constant'),
            np.pad(v2, (0, maxLen - len(v2)), 'constant'))

class VectorComparison(BaseComparison):
    def __call__(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> Union[float, List[float]]:
        if isinstance(target, list) and not isinstance(target[0], (int, float)):
            return [self.compare(ref, t) for t in target]
        return self.compare(ref, target)

@BaseComparison.register("euclidean")
class EuclideanComparison(VectorComparison):
    def compare(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> float:
        refVec, targetVec = map(ensureVector, (ref, target))
        refVec, targetVec = padVectors(refVec, targetVec)
        distance = np.linalg.norm(refVec - targetVec)
        maxDist = np.linalg.norm(np.maximum(refVec, targetVec) - np.minimum(refVec, targetVec))
        return float(1 - (distance / maxDist) if maxDist else 1.0)

    def explain(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Euclidean",
            "score": score,
            "explanation": f"Normalized Euclidean similarity: {score:.2f}. Inverse of normalized Euclidean distance."
        }

@BaseComparison.register("manhattan")
class ManhattanComparison(VectorComparison):
    def compare(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> float:
        refVec, targetVec = map(ensureVector, (ref, target))
        refVec, targetVec = padVectors(refVec, targetVec)
        distance = np.sum(np.abs(refVec - targetVec))
        maxDist = np.sum(np.abs(np.maximum(refVec, targetVec) - np.minimum(refVec, targetVec)))
        return float(1 - (distance / maxDist) if maxDist else 1.0)

    def explain(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Manhattan",
            "score": score,
            "explanation": f"Normalized Manhattan similarity: {score:.2f}. Inverse of normalized Manhattan distance."
        }

@BaseComparison.register("cosine")
class CosineVectorComparison(VectorComparison):
    def compare(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> float:
        refVec, targetVec = map(ensureVector, (ref, target))
        refVec, targetVec = padVectors(refVec, targetVec)
        dotProd = np.dot(refVec, targetVec)
        normRef, normTarget = np.linalg.norm(refVec), np.linalg.norm(targetVec)
        return float(dotProd / (normRef * normTarget) if normRef * normTarget != 0 else 0.0)

    def explain(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Cosine Vector",
            "score": score,
            "explanation": f"Cosine similarity: {score:.2f}. Cosine of the angle between the vectors."
        }

@BaseComparison.register("jaccard")
class JaccardVectorComparison(VectorComparison):
    def compare(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> float:
        refVec, targetVec = map(ensureVector, (ref, target))
        refVec, targetVec = padVectors(refVec, targetVec)
        intersection = np.sum(np.minimum(refVec, targetVec))
        union = np.sum(np.maximum(refVec, targetVec))
        return float(intersection / union if union != 0 else 0.0)

    def explain(self, ref: Union[List, np.ndarray, int, float, str], target: Union[List, np.ndarray, int, float, str]) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Jaccard Vector",
            "score": score,
            "explanation": f"Jaccard similarity: {score:.2f}. Intersection over union of vector elements."
        }

'''
TODO: Consider implementing more advanced vector comparison methods such as:
1. Mahalanobis distance
2. Earth Mover's Distance (EMD) / Wasserstein metric
3. Kullback-Leibler divergence (for probability distributions)
These methods might require additional dependencies like scipy.
'''
