from typing import Any, Dict, List
import inspect

def generateBasicExplanation(method: str, score: float, ref: Any, target: Any) -> Dict[str, Any]:
    """
    Generate a basic explanation for a comparison result.
    
    Args:
    method (str): Name of the comparison method
    score (float): Comparison score
    ref (Any): Reference object
    target (Any): Target object
    
    Returns:
    Dict[str, Any]: Explanation dictionary
    """
    return {
        "method": method,
        "score": score,
        "explanation": f"The {method} similarity between the reference and target is {score:.2f}."
    }

def generateDetailedExplanation(comparisonObj: Any, ref: Any, target: Any) -> Dict[str, Any]:
    """
    Generate a detailed explanation for a comparison result.
    
    Args:
    comparisonObj (Any): Comparison object
    ref (Any): Reference object
    target (Any): Target object
    
    Returns:
    Dict[str, Any]: Detailed explanation dictionary
    """
    method = comparisonObj.__class__.__name__
    score = comparisonObj.compare(ref, target)
    params = comparisonObj.params
    
    explanation = {
        "method": method,
        "score": score,
        "parameters": params,
        "reference": str(ref),
        "target": str(target),
        "explanation": f"The {method} similarity between the reference and target is {score:.2f}.",
        "method_description": inspect.getdoc(comparisonObj.compare)
    }
    
    if hasattr(comparisonObj, 'explain'):
        explanation.update(comparisonObj.explain(ref, target))
    
    return explanation

# TODO: Implement more specific explanation generators for different types of comparisons (e.g., text, vector, image)
# TODO: Add support for generating explanations in different formats (e.g., HTML, Markdown)
# TODO: Implement a mechanism for customizing explanation templates