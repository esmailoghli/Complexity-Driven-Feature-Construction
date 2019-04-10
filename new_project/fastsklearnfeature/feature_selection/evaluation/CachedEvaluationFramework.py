from typing import List, Dict, Set
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score
from fastsklearnfeature.configuration.Config import Config
from fastsklearnfeature.candidate_generation.feature_space.explorekit_transformations import get_transformation_for_feature_space
from fastsklearnfeature.feature_selection.evaluation.EvaluationFramework import EvaluationFramework
from fastsklearnfeature.candidates.RawFeature import RawFeature
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
import time
from fastsklearnfeature.candidates.CandidateFeature import CandidateFeature
import itertools
from sklearn.base import ClassifierMixin
from sklearn.base import RegressorMixin

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class CachedEvaluationFramework(EvaluationFramework):
    def __init__(self, dataset_config, classifier=LogisticRegression, grid_search_parameters={'penalty': ['l2'],
                                                                                                'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                                                                                                'solver': ['lbfgs'],
                                                                                                'class_weight': ['balanced'],
                                                                                                'max_iter': [10000],
                                                                                                'multi_class':['auto']
                                                                                                },
                 transformation_producer=get_transformation_for_feature_space
                 ):
        super(CachedEvaluationFramework, self).__init__(dataset_config, classifier, grid_search_parameters, transformation_producer)


    def generate_target(self):
        current_target = self.dataset.splitted_target['train']

        if isinstance(self.classifier(), ClassifierMixin):
            label_encoder = LabelEncoder()
            label_encoder.fit(current_target)

            current_target = label_encoder.transform(current_target)

            if Config.get_default('score.test', 'False') == 'True':
                self.test_target = label_encoder.transform(self.dataset.splitted_target['test'])
                self.train_y_all_target = label_encoder.transform(self.train_y_all)


            self.preprocessed_folds = []
            for train, test in StratifiedKFold(n_splits=self.folds, random_state=42).split(self.dataset.splitted_values['train'],
                                                                                   current_target):
                self.preprocessed_folds.append((train, test))
        elif isinstance(self.classifier(), RegressorMixin):

            if Config.get_default('score.test', 'False') == 'True':
                self.test_target = self.dataset.splitted_target['test']
                self.train_y_all_target = self.train_y_all

            self.preprocessed_folds = []
            for train, test in KFold(n_splits=self.folds, random_state=42).split(
                    self.dataset.splitted_values['train'],
                    current_target):
                self.preprocessed_folds.append((train, test))
        else:
            pass

        self.target_train_folds = [None] * self.folds
        self.target_test_folds = [None] * self.folds

        for fold in range(len(self.preprocessed_folds)):
            self.target_train_folds[fold] = current_target[self.preprocessed_folds[fold][0]]
            self.target_test_folds[fold] = current_target[self.preprocessed_folds[fold][1]]





    def grid_search(self, train_transformed, test_transformed, training_all, one_test_set_transformed):

        hyperparam_to_score_list = {}

        my_keys = list(self.grid_search_parameters.keys())

        for parameter_combination in itertools.product(*[self.grid_search_parameters[k] for k in my_keys]):
            parameter_set = hashabledict(zip(my_keys, parameter_combination))
            hyperparam_to_score_list[parameter_set] = []
            for fold in range(len(train_transformed)):
                clf = self.classifier(**parameter_set)
                clf.fit(train_transformed[fold], self.target_train_folds[fold])
                y_pred = clf.predict(test_transformed[fold])
                hyperparam_to_score_list[parameter_set].append(self.score._sign * self.score._score_func(self.target_test_folds[fold], y_pred, **self.score._kwargs))

        best_param = None
        best_mean_cross_val_score = -float("inf")
        for parameter_config, score_list in hyperparam_to_score_list.items():
            mean_score = np.mean(score_list)
            if mean_score > best_mean_cross_val_score:
                best_param = parameter_config
                best_mean_cross_val_score = mean_score

        test_score = None
        if Config.get_default('score.test', 'False') == 'True':
            # refit to entire training and test on test set
            clf = self.classifier(**best_param)
            clf.fit(training_all, self.train_y_all_target)
            y_pred = clf.predict(one_test_set_transformed)
            test_score = self.score._sign * self.score._score_func(self.test_target, y_pred, **self.score._kwargs)

            #np.save('/tmp/true_predictions', self.test_target)


        return best_mean_cross_val_score, test_score, best_param, y_pred





    def evaluate(self, candidate: CandidateFeature):

        if type(self.max_timestamp) != type(None) and time.time() >= self.max_timestamp:
            raise RuntimeError('Out of time!')

        result = {}
        train_transformed = [None] * len(self.preprocessed_folds)
        test_transformed = [None] * len(self.preprocessed_folds)

        #test
        training_all = None
        one_test_set_transformed = None

        result['train_transformed'] = None
        result['test_transformed'] = None
        result['one_test_set_transformed'] = None

        if isinstance(candidate, RawFeature):

            if Config.get_default('score.test', 'False') == 'True':
                result['training_all'] = training_all = self.name_to_training_all[str(candidate)]
                result['one_test_set_transformed'] = one_test_set_transformed = self.name_to_one_test_set_transformed[str(candidate)]

            result['train_transformed'] = train_transformed = self.name_to_train_transformed[str(candidate)]
            result['test_transformed'] = test_transformed = self.name_to_test_transformed[str(candidate)]

        else:

            #print(self.name_to_train_transformed.keys())

            #merge columns from parents
            for fold in range(len(self.preprocessed_folds)):
                train_transformed_input = np.hstack([self.name_to_train_transformed[str(p)][fold] for p in candidate.parents])
                test_transformed_input = np.hstack([self.name_to_test_transformed[str(p)][fold] for p in candidate.parents])

                candidate.transformation.fit(train_transformed_input)
                train_transformed[fold] = candidate.transformation.transform(train_transformed_input)
                test_transformed[fold] = candidate.transformation.transform(test_transformed_input)

            if Config.get_default('score.test', 'False') == 'True':
                training_all_input = np.hstack(
                    [self.name_to_training_all[str(p)] for p in candidate.parents])
                one_test_set_transformed_input = np.hstack(
                    [self.name_to_one_test_set_transformed[str(p)] for p in candidate.parents])

                candidate.transformation.fit(training_all_input)
                training_all = candidate.transformation.transform(training_all_input)
                one_test_set_transformed = candidate.transformation.transform(one_test_set_transformed_input)

        candidate.runtime_properties['score'], candidate.runtime_properties['test_score'], candidate.runtime_properties['hyperparameters'], y_pred = self.grid_search(train_transformed, test_transformed, training_all, one_test_set_transformed)

        if Config.get_default('store.predictions', 'False') == 'True':
            candidate.runtime_properties['predictions'] = y_pred

        if not isinstance(candidate, RawFeature):
            #only save the transformed data if we need it in the future
            max_parent = np.max([p.runtime_properties['score'] for p in candidate.parents])
            accuracy_delta = candidate.runtime_properties['score'] - max_parent
            if accuracy_delta / self.complexity_delta > self.epsilon:

                result['train_transformed'] = train_transformed
                result['test_transformed'] = test_transformed

                result['training_all'] = training_all
                result['one_test_set_transformed'] = one_test_set_transformed

                # derive properties
                if not isinstance(candidate, RawFeature):
                    candidate.derive_properties(result['train_transformed'][0])


        return result















