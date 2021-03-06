import autograd.numpy as anp
import numpy as np
from pymoo.util.misc import stack
from pymoo.model.problem import Problem
import numpy as np
import pickle
from fastsklearnfeature.candidates.CandidateFeature import CandidateFeature
from fastsklearnfeature.candidates.RawFeature import RawFeature
from fastsklearnfeature.interactiveAutoML.feature_selection.ForwardSequentialSelection import ForwardSequentialSelection
from fastsklearnfeature.transformations.OneHotTransformation import OneHotTransformation
from typing import List, Dict, Set
from fastsklearnfeature.interactiveAutoML.CreditWrapper import run_pipeline
from pymoo.algorithms.so_genetic_algorithm import GA
from pymoo.factory import get_crossover, get_mutation, get_sampling
from pymoo.optimize import minimize
from pymoo.algorithms.nsga2 import NSGA2
import matplotlib.pyplot as plt
from fastsklearnfeature.interactiveAutoML.Runner import Runner
import copy
from sklearn.linear_model import LogisticRegression
from fastsklearnfeature.candidates.CandidateFeature import CandidateFeature
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import make_scorer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
from fastsklearnfeature.transformations.IdentityTransformation import IdentityTransformation
from fastsklearnfeature.transformations.MinMaxScalingTransformation import MinMaxScalingTransformation
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
import argparse
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import time

from art.metrics import RobustnessVerificationTreeModelsCliqueMethod
from art.metrics import loss_sensitivity
from art.metrics import empirical_robustness
from sklearn.pipeline import FeatureUnion


from xgboost import XGBClassifier
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier

from art.classifiers import XGBoostClassifier, LightGBMClassifier, SklearnClassifier
from art.attacks import HopSkipJump


from fastsklearnfeature.interactiveAutoML.feature_selection.RunAllKBestSelection import RunAllKBestSelection
from fastsklearnfeature.interactiveAutoML.feature_selection.fcbf_package import fcbf
from fastsklearnfeature.interactiveAutoML.feature_selection.fcbf_package import variance
from fastsklearnfeature.interactiveAutoML.feature_selection.fcbf_package import model_score
from fastsklearnfeature.interactiveAutoML.feature_selection.BackwardSelection import BackwardSelection
from sklearn.model_selection import train_test_split

from fastsklearnfeature.interactiveAutoML.new_bench import my_global_utils1
from fastsklearnfeature.interactiveAutoML.new_bench.multiobjective.robust_measure import unit_test_score

from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC

from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import chi2
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer

from fastsklearnfeature.interactiveAutoML.new_bench.multiobjective.robust_measure import robust_score_test

from fastsklearnfeature.configuration.Config import Config

from skrebate import ReliefF
from fastsklearnfeature.interactiveAutoML.feature_selection.fcbf_package import my_fisher_score

from skrebate import ReliefF
from fastsklearnfeature.interactiveAutoML.feature_selection.fcbf_package import my_fisher_score
from functools import partial
from hyperopt import fmin, hp, tpe, Trials, space_eval, STATUS_OK

from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import chi2

from sklearn.model_selection import cross_val_score
from fastsklearnfeature.interactiveAutoML.fair_measure import true_positive_rate_score

from fastsklearnfeature.interactiveAutoML.feature_selection.MaskSelection import MaskSelection


def forward_floating_selection(X_train, X_validation, X_test, y_train, y_validation, y_test, names, sensitive_ids, ranking_functions= [], clf=None, min_accuracy = 0.0, min_fairness=0.0, min_robustness=0.0, max_number_features=None, max_search_time=np.inf, log_file=None):
	return forward_floating_selection_lib(X_train, X_validation, X_test, y_train, y_validation, y_test, names, sensitive_ids, ranking_functions= [], clf=clf, min_accuracy = min_accuracy, min_fairness=min_fairness, min_robustness=min_robustness, max_number_features=max_number_features, max_search_time=max_search_time, log_file=log_file, floating=True)

def forward_selection(X_train, X_validation, X_test, y_train, y_validation, y_test, names, sensitive_ids, ranking_functions= [], clf=None, min_accuracy = 0.0, min_fairness=0.0, min_robustness=0.0, max_number_features=None, max_search_time=np.inf, log_file=None):
	return forward_floating_selection_lib(X_train, X_validation, X_test, y_train, y_validation, y_test, names, sensitive_ids, ranking_functions= [], clf=clf, min_accuracy = min_accuracy, min_fairness=min_fairness, min_robustness=min_robustness, max_number_features=max_number_features, max_search_time=max_search_time, log_file=log_file, floating=False)


def forward_floating_selection_lib(X_train, X_validation, X_test, y_train, y_validation, y_test, names, sensitive_ids, ranking_functions= [], clf=None, min_accuracy = 0.0, min_fairness=0.0, min_robustness=0.0, max_number_features=None, max_search_time=np.inf, log_file=None, floating=True):
	f_log = open(log_file, 'wb+')
	min_loss = np.inf
	start_time = time.time()

	auc_scorer = make_scorer(roc_auc_score, greater_is_better=True, needs_threshold=True)

	fair_validation = None
	fair_test = None
	if type(sensitive_ids) != type(None):
		fair_validation = make_scorer(true_positive_rate_score, greater_is_better=True,
									  sensitive_data=X_validation[:, sensitive_ids[0]])
		fair_test = make_scorer(true_positive_rate_score, greater_is_better=True,
								sensitive_data=X_test[:, sensitive_ids[0]])

	def f_clf1(hps):
		mask = np.zeros(len(hps), dtype=bool)
		for k, v in hps.items():
			mask[int(k.split('_')[1])] = v

		#repair number of features if neccessary
		max_k = max(int(max_number_features * X_train.shape[1]), 1)
		if np.sum(mask) > max_k:
			id_features_used = np.nonzero(mask)[0]  # indices where features are used
			np.random.shuffle(id_features_used)  # shuffle ids
			ids_tb_deactived = id_features_used[max_k:]  # deactivate features
			for item_to_remove in ids_tb_deactived:
				mask[item_to_remove] = False

		for mask_i in range(len(mask)):
			hps['f_' + str(mask_i)] = mask[mask_i]

		model = Pipeline([
			('selection', MaskSelection(mask)),
			('clf', clf)
		])

		return model, hps

	def f_to_min1(hps):
		pipeline, hps = f_clf1(hps)

		if np.sum(pipeline.named_steps['selection'].mask) == 0:
			return {'loss': 4, 'status': STATUS_OK, 'model': pipeline, 'cv_fair': 0.0, 'cv_acc': 0.0, 'cv_robust': 0.0, 'cv_number_features': 1.0}

		pipeline.fit(X_train, pd.DataFrame(y_train))

		validation_number_features = float(np.sum(pipeline.named_steps['selection']._get_support_mask())) / float(X_train.shape[1])
		validation_acc = auc_scorer(pipeline, X_validation, pd.DataFrame(y_validation))

		validation_fair = 0.0
		if type(sensitive_ids) != type(None) and min_fairness > 0.0:
			validation_fair = 1.0 - fair_validation(pipeline, X_validation, pd.DataFrame(y_validation))
		validation_robust = 0.0
		if min_robustness > 0.0:
			validation_robust = 1.0 - robust_score_test(eps=0.1, X_test=X_validation, y_test=y_validation,
														model=pipeline.named_steps['clf'],
														feature_selector=pipeline.named_steps['selection'],
														scorer=auc_scorer)

		loss = 0.0
		if min_fairness > 0.0 and validation_fair < min_fairness:
			loss += (min_fairness - validation_fair) ** 2
		if min_accuracy > 0.0 and validation_acc < min_accuracy:
			loss += (min_accuracy - validation_acc) ** 2
		if min_robustness > 0.0 and validation_robust < min_robustness:
			loss += (min_robustness - validation_robust) ** 2

		current_time = time.time() - start_time

		return {'loss': loss,
				'status': STATUS_OK,
				'model': pipeline,
				'cv_fair': validation_fair,
				'cv_acc': validation_acc,
				'cv_robust': validation_robust,
				'cv_number_features': validation_number_features,
				'time': current_time,
				'updated_parameters': hps}

	def execute_feature_combo(feature_combo, number_of_evaluations):
		hps = {}
		for f_i in range(X_train.shape[1]):
			if f_i in feature_combo:
				hps['f_' + str(f_i)] = 1
			else:
				hps['f_' + str(f_i)] = 0

		result = f_to_min1(hps)

		cv_fair = result['cv_fair']
		cv_acc = result['cv_acc']
		cv_robust = result['cv_robust']
		cv_number_features = result['cv_number_features']

		my_result = result
		my_result['number_evaluations'] = number_of_evaluations
		if cv_fair >= min_fairness and cv_acc >= min_accuracy and cv_robust >= min_robustness and cv_number_features <= max_number_features:
			model = result['model']

			X_train_val = np.vstack((X_train, X_validation))
			y_train_val = np.append(y_train, y_validation)
			model.fit(X_train_val, pd.DataFrame(y_train_val))

			test_acc = 0.0
			if min_accuracy > 0.0:
				test_acc = auc_scorer(model, X_test, pd.DataFrame(y_test))
			test_fair = 0.0
			if min_fairness > 0.0:
				test_fair = 1.0 - fair_test(model, X_test, pd.DataFrame(y_test))
			test_robust = 0.0
			if min_robustness > 0.0:
				test_robust = 1.0 - robust_score_test(eps=0.1, X_test=X_test, y_test=y_test,
													  model=model.named_steps['clf'],
													  feature_selector=model.named_steps['selection'],
													  scorer=auc_scorer)

			my_result['test_fair'] = test_fair
			my_result['test_acc'] = test_acc
			my_result['test_robust'] = test_robust
			my_result['final_time'] = time.time() - start_time
			my_result['Finished'] = True

			success = False
			if test_fair >= min_fairness and test_acc >= min_accuracy and test_robust >= min_robustness:
				success = True

			my_result['success_test'] = success
			pickle.dump(my_result, f_log)

			return result, {'success': success}

		return result, {}




	space = {}
	for f_i in range(X_train.shape[1]):
		space['f_' + str(f_i)] = hp.randint('f_' + str(f_i), 2)

	cv_fair = 0
	cv_acc = 0
	cv_robust = 0
	cv_number_features = 1.0

	number_of_evaluations = 0

	max_k = max(int(max_number_features * X_train.shape[1]), 1)

	current_feature_set = []
	remaining_features = list(range(X_train.shape[1]))

	history = {}
	while (len(current_feature_set) < max_k):
		# select best feature
		best_feature_id = -1
		lowest_loss = np.inf
		for new_feature in remaining_features:

			feature_combo = [new_feature]
			feature_combo.extend(current_feature_set)

			# book-keeping to avoid infinite loops
			if frozenset(feature_combo) in history:
				continue
			number_of_evaluations += 1

			my_result, combo_result = execute_feature_combo(feature_combo, number_of_evaluations)
			if min_loss > my_result['loss']:
				min_loss = my_result['loss']
				pickle.dump(my_result, f_log)
			if len(combo_result) > 0:
				f_log.close()
				return combo_result
			combo_loss = my_result['loss']
			print(combo_loss)

			history[frozenset(feature_combo)] = my_result['loss']
			if combo_loss < lowest_loss:
				best_feature_id = new_feature
				lowest_loss = combo_loss

		if best_feature_id == -1:
			break

		current_feature_set.append(best_feature_id)
		remaining_features.remove(best_feature_id)

		if floating:
			# select worst feature
			while True:
				best_feature_id = -1
				lowest_loss_new = np.inf
				for i in range(len(current_feature_set)-1,-1,-1):
					new_feature = current_feature_set[i]
					feature_combo = copy.deepcopy(current_feature_set)
					feature_combo.remove(new_feature)

					#book-keeping to avoid infinite loops
					if frozenset(feature_combo) in history:
						continue
					number_of_evaluations += 1

					my_result, combo_result = execute_feature_combo(feature_combo, number_of_evaluations)
					if min_loss > my_result['loss']:
						min_loss = my_result['loss']
						pickle.dump(my_result, f_log)
					if len(combo_result) > 0:
						f_log.close()
						return combo_result
					combo_loss = my_result['loss']
					print(combo_loss)

					history[frozenset(feature_combo)] = combo_loss
					if combo_loss < lowest_loss_new:
						best_feature_id = new_feature
						lowest_loss_new = combo_loss

				if lowest_loss_new > lowest_loss:
					break
				else:
					lowest_loss = lowest_loss_new

					current_feature_set.remove(best_feature_id)
					remaining_features.append(best_feature_id)

	my_result = {'number_evaluations': number_of_evaluations, 'success_test': False, 'time': time.time() - start_time,
				 'Finished': True}
	pickle.dump(my_result, f_log)
	f_log.close()
	return {'success': False}






