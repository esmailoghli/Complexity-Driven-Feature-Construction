from sklearn.feature_selection import SelectKBest
import numpy as np

map_fold2ranking = {}

class WrapperBestK(SelectKBest):
	def __init__(self, selection, k=10):
		self.k = k
		self.selection = selection
		#map_fold2ranking[self.selection.score_func.__name__] = {}

	def fit(self, X, y=None):

		if hasattr(y, 'index'):
			hash_for_fold_ids = np.sum(y.index.values)
			if hash_for_fold_ids in map_fold2ranking[self.selection.score_func.__name__]:
				self.scores_ = map_fold2ranking[self.selection.score_func.__name__][hash_for_fold_ids]
				return self
		self.selection.fit(X,y)
		if hasattr(y, 'index'):
			map_fold2ranking[self.selection.score_func.__name__][hash_for_fold_ids] = self.selection.scores_
		self.scores_ = self.selection.scores_

		return self