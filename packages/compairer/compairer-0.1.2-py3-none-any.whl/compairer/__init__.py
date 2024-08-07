from . import core, models, methods, utils
from .core import compare, ComparisonResult
from .models import BaseComparison, IncrementalComparison
from .methods import (
    LevenshteinComparison, JaccardComparison, CosineComparison, FuzzComparison, RegexComparison,
    EuclideanComparison, ManhattanComparison, CosineVectorComparison, JaccardVectorComparison,
    CustomComparison
)
from .utils import normalize, meanScore, medianScore, varianceScore, standardDeviation, confidenceInterval

__all__ = [
    'compare', 'ComparisonResult',
    'BaseComparison', 'IncrementalComparison',
    'LevenshteinComparison', 'JaccardComparison', 'CosineComparison', 'FuzzComparison', 'RegexComparison',
    'EuclideanComparison', 'ManhattanComparison', 'CosineVectorComparison', 'JaccardVectorComparison',
    'CustomComparison',
    'normalize', 'meanScore', 'medianScore', 'varianceScore', 'standardDeviation', 'confidenceInterval'
]

compare.levenshtein = LevenshteinComparison()
compare.jaccard = JaccardComparison()
compare.cosine = CosineComparison()
compare.fuzz = FuzzComparison()
compare.regex = RegexComparison()
compare.euclidean = EuclideanComparison()
compare.manhattan = ManhattanComparison()
compare.cosineVector = CosineVectorComparison()
compare.jaccardVector = JaccardVectorComparison()

__version__ = '0.1.0'
