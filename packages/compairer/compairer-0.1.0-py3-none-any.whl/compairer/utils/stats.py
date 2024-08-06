import numpy as np
from typing import List, Union

def normalize(scores: List[float], method: str = "minmax") -> List[float]:
    """
    Normalize a list of scores.
    
    Args:
    scores (List[float]): List of scores to normalize
    method (str): Normalization method. Options: "minmax", "zscore"
    
    Returns:
    List[float]: Normalized scores
    """
    if method == "minmax":
        minScore, maxScore = min(scores), max(scores)
        if minScore == maxScore:
            return [1.0] * len(scores)
        return [(score - minScore) / (maxScore - minScore) for score in scores]
    elif method == "zscore":
        mean, std = np.mean(scores), np.std(scores)
        if std == 0:
            return [0.0] * len(scores)
        return [(score - mean) / std for score in scores]
    else:
        raise ValueError("Unsupported normalization method")

def meanScore(scores: List[float]) -> float:
    """Calculate the mean of a list of scores."""
    return np.mean(scores)

def medianScore(scores: List[float]) -> float:
    """Calculate the median of a list of scores."""
    return np.median(scores)

def varianceScore(scores: List[float]) -> float:
    """Calculate the variance of a list of scores."""
    return np.var(scores)

def standardDeviation(scores: List[float]) -> float:
    """Calculate the standard deviation of a list of scores."""
    return np.std(scores)

def confidenceInterval(scores: List[float], confidence: float = 0.95) -> tuple:
    """
    Calculate the confidence interval for a list of scores.
    
    Args:
    scores (List[float]): List of scores
    confidence (float): Confidence level (default: 0.95 for 95% CI)
    
    Returns:
    tuple: (lower bound, upper bound) of the confidence interval
    """
    return tuple(np.percentile(scores, [(1 - confidence) / 2 * 100, (1 + confidence) / 2 * 100]))

"""
TODO: 
1. Implement more advanced statistical measures (e.g., skewness, kurtosis)
2. Add functionality for hypothesis testing (e.g., t-test, ANOVA)
3. Consider implementing bootstrapping methods for more robust confidence intervals
4. Add visualization functions (e.g., histograms, box plots) for score distributions
"""