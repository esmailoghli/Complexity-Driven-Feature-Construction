from fastsklearnfeature.transformations.Transformation import Transformation
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from fastsklearnfeature.candidates.CandidateFeature import CandidateFeature
from fastsklearnfeature.candidates.RawFeature import RawFeature
from typing import List
import sympy
import numpy

class impute(sympy.Function):
    @classmethod
    def eval(cls, x):
        if isinstance(x, impute): #idempotent
            return x

class ImputationTransformation(BaseEstimator, TransformerMixin, Transformation):
    def __init__(self, strategy='mean'):
        name = strategy + 'Imputation'
        self.imputer = SimpleImputer(strategy=strategy)
        Transformation.__init__(self, name,
                                number_parent_features=1,
                                output_dimensions=1,
                                parent_feature_order_matters=True,
                                parent_feature_repetition_is_allowed=False)

    def fit(self, X, y=None):
        self.imputer.fit(X)
        return self

    def transform(self, X):
        return self.imputer.transform(X)

    def is_applicable(self, feature_combination: List[CandidateFeature]):
        if not super(ImputationTransformation, self).is_applicable(feature_combination):
            return False
        if isinstance(feature_combination[0].transformation, ImputationTransformation):
            return False
        if isinstance(feature_combination[0], RawFeature) and 'missing_values' in feature_combination[0].properties and feature_combination[0].properties['missing_values']:
            return True

        return False

    def get_sympy_representation(self, input_attributes):
        return impute(input_attributes[0])

    def derive_properties(self, training_data, parents: List[CandidateFeature]):
        properties = {}
        # type properties
        properties['type'] = training_data.dtype

        try:
            properties['missing_values'] = False

            # range properties
            properties['has_zero'] = parents[0].properties['has_zero']

            #might not work for constant
            properties['min'] = parents[0].properties['min']
            properties['max'] = parents[0].properties['max']
        except:
            # was nonnumeric data
            pass
        #approximation (could be +1)
        properties['number_distinct_values'] = parents[0].properties['number_distinct_values']
        return properties