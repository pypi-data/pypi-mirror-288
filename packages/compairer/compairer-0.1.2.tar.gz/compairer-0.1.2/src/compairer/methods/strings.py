from ..models.base import BaseComparison
from collections import Counter
import math
import re
from fuzzywuzzy import fuzz
from typing import Optional


@BaseComparison.register("fuzz")
class FuzzComparison(BaseComparison):
    '''DOCS NEEDED'''
    def __init__(self, method: str = "ratio"):
        super().__init__()
        self.method = method
        self.fuzz_func = getattr(fuzz, method)

    def compare(self, ref: str, target: str) -> float:
        return self.fuzz_func(ref, target) / 100.0  # fuzzywuzzy returns scores 0-100, we normalize to 0-1

    def explain(self, ref: str, target: str) -> dict:
        score = self.compare(ref, target)
        return {
            "method": f"Fuzz ({self.method})",
            "score": score,
            "explanation": f"The fuzzy similarity between '{ref}' and '{target}' using {self.method} method is {score:.2f}. "
                           f"This represents the normalized fuzzy match score between the strings."
        }

@BaseComparison.register("regex")
class RegexComparison(BaseComparison):
    def __init__(self, pattern: str = None, flags: int = 0):
        super().__init__()
        self.pattern = pattern
        self.flags = flags

    def compare(self, ref: str, target: str) -> float:
        pattern = self.pattern or ref
        try:
            regex = re.compile(pattern, self.flags)
            match = regex.search(target)
            if match:
                # Return a score based on the length of the match relative to the target string
                return len(match.group()) / len(target)
            return 0.0
        except re.error:
            return 0.0

    def explain(self, ref: str, target: str) -> dict:
        score = self.compare(ref, target)
        pattern = self.pattern or ref
        return {
            "method": "Regex",
            "score": score,
            "explanation": f"The regex match between pattern '{pattern}' and string '{target}' resulted in a score of {score:.2f}. "
                           f"This represents the proportion of the target string matched by the regex pattern."
        }


@BaseComparison.register("levenshtein")
class LevenshteinComparison(BaseComparison):
    def compare(self, ref: Optional[str], target: Optional[str]) -> float:
        if ref is None or target is None:
            return 0.0 if ref != target else 1.0
        m, n = len(ref), len(target)
        if m < n:
            return self.compare(target, ref)
        if not n:
            return 1.0 if not m else 0.0
        prev = list(range(n + 1))
        for i, c1 in enumerate(ref):
            curr = [i + 1]
            for j, c2 in enumerate(target):
                curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
            prev = curr
        return 1 - (prev[-1] / max(m, n))

    def explain(self, ref: str, target: str) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Levenshtein",
            "score": score,
            "explanation": f"The Levenshtein similarity between '{ref}' and '{target}' is {score:.2f}. "
                           f"This represents the normalized edit distance between the strings."
        }

@BaseComparison.register("jaccard")
class JaccardComparison(BaseComparison):
    def compare(self, ref: str, target: str) -> float:
        set1, set2 = set(ref), set(target)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union else 0

    def explain(self, ref: str, target: str) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Jaccard",
            "score": score,
            "explanation": f"The Jaccard similarity between '{ref}' and '{target}' is {score:.2f}. "
                           f"This represents the size of the intersection divided by the size of the union of the character sets."
        }

@BaseComparison.register("cosine")
class CosineComparison(BaseComparison):
    def compare(self, ref: str, target: str) -> float:
        vec1, vec2 = Counter(ref), Counter(target)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return numerator / denominator if denominator else 0

    def explain(self, ref: str, target: str) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Cosine",
            "score": score,
            "explanation": f"The Cosine similarity between '{ref}' and '{target}' is {score:.2f}. "
                           f"This represents the cosine of the angle between the vector representations of the strings."
        }

@BaseComparison.register("longestCommonSubsequence")
class LCSComparison(BaseComparison):
    def compare(self, ref: str, target: str) -> float:
        m, n = len(ref), len(target)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if ref[i-1] == target[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n] / max(m, n)  # Normalize to [0, 1]

    def explain(self, ref: str, target: str) -> dict:
        score = self.compare(ref, target)
        return {
            "method": "Longest Common Subsequence",
            "score": score,
            "explanation": f"The normalized LCS similarity between '{ref}' and '{target}' is {score:.2f}. "
                           f"This represents the length of the longest common subsequence divided by the length of the longer string."
        }
