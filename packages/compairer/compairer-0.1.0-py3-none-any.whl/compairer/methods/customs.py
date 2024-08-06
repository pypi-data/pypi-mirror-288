from ..models.base import BaseComparison

@BaseComparison.register("custom")
class CustomComparison(BaseComparison):
    '''DOCS NEEDED'''
    def __init__(self, compareFunc, explainFunc=None, **kwargs):
        super().__init__(**kwargs)
        self.compareFunc = compareFunc
        self.explainFunc = explainFunc

    def compare(self, ref, target):
        return self.compareFunc(ref, target)

    def explain(self, ref, target):
        if self.explainFunc:
            return self.explainFunc(ref, target)
        score = self.compare(ref, target)
        return {
            "method": "Custom",
            "score": score,
            "explanation": f"Custom comparison method resulted in a score of {score:.2f}."
        }
