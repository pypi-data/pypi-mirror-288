import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TunedThresholdClassifierCV
from sklearn.metrics import confusion_matrix, make_scorer, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

class BijanClassifier:
    def __init__(self, model_type='RF', cost_matrix=None, greater_is_better=False, thresholds=100, cv=5, random_state=None, **model_params):
        self.model_type = model_type
        self.model_params = model_params
        self.cost_matrix = cost_matrix
        self.greater_is_better = greater_is_better
        self.thresholds = thresholds
        self.random_state = random_state
        self.cv = cv
        self.model = self._create_model()
        self.is_binary = None
        self.cmm = cost_matrix

    def _create_model(self):
        if self.model_type == 'RF':
            return RandomForestClassifier(random_state=self.random_state, **self.model_params)
        elif self.model_type == 'DT':
            return DecisionTreeClassifier(random_state=self.random_state, **self.model_params)
        elif self.model_type == 'GB':
            return GradientBoostingClassifier(random_state=self.random_state, **self.model_params)
        elif self.model_type == 'LR':
            return LogisticRegression(random_state=self.random_state, **self.model_params)
        else:
            raise ValueError("Model type not supported. Choose 'RF' for RandomForest or 'DT' for DecisionTree or 'GB' for GradientBoosting.")


    def _create_default_cost_matrix(self, num_classes):
        # Create a cost matrix with zeros on the diagonal and ones elsewhere
        cost_matrix = np.ones((num_classes, num_classes)) - np.eye(num_classes)
        return cost_matrix

    
    def cost_function(self, y, y_pred):
        cm = confusion_matrix(y, y_pred)
        return float(np.sum(cm * self.cost_matrix))

    def fit(self, X_train, y_train):
        num_classes = len(np.unique(y_train))
        self.is_binary = len(np.unique(y_train)) == 2
        cost_scorer = make_scorer(self.cost_function, greater_is_better=self.greater_is_better)

        if self.cost_matrix is None:
            self.cost_matrix = self._create_default_cost_matrix(num_classes)
            self.fitted_model = self.model.fit(X_train, y_train)

        elif self.is_binary:
            tuned_model = TunedThresholdClassifierCV(self.model, thresholds=self.thresholds, random_state=self.random_state, cv=self.cv, scoring=cost_scorer, store_cv_results=True)
            self.fitted_model = tuned_model.fit(X_train, y_train)
        elif self.model_type == 'DT':
            param_grid = {
                'max_depth': [2, 3, 4, 6, 8, 10],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            grid_search = GridSearchCV(self.model, param_grid, scoring=cost_scorer, cv=self.cv, verbose=1, n_jobs=-1)
            self.fitted_model = grid_search.fit(X_train, y_train)
            
        elif self.model_type == 'RF' or self.model_type == 'GB':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 2, 4, 8, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'max_features': ["sqrt", "log2", None],
            }
            grid_search = GridSearchCV(self.model, param_grid, scoring=cost_scorer, cv=self.cv, verbose=1, n_jobs=-1)
            self.fitted_model = grid_search.fit(X_train, y_train)

        elif self.model_type == 'LR':
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'solver': ['newton-cg', 'lbfgs', 'liblinear'],
                'max_iter': [100, 200, 300],
            }
            grid_search = GridSearchCV(self.model, param_grid, scoring=cost_scorer, cv=self.cv, verbose=1, n_jobs=-1)
            self.fitted_model = grid_search.fit(X_train, y_train)

        return self.fitted_model

    def predict(self, X):
        return self.fitted_model.predict(X)

    def predict_proba(self, X):
        return self.fitted_model.predict_proba(X)

    def accuracy(self, y, y_pred):
        return accuracy_score(y, y_pred)

    def cost(self, y, y_pred):
        return self.cost_function(y, y_pred)

    def estimator_(self):
        if self.is_binary or self.cmm is None:
            return self.fitted_model.estimator_
        else:
            return self.fitted_model.best_estimator_

    def best_params_(self):
        return self.fitted_model.best_params_ if not self.is_binary else None

    def best_threshold_(self):
        return float(self.fitted_model.best_threshold_) if self.is_binary else None

    def best_score_(self):
        return float(self.fitted_model.best_score_) if self.is_binary else self.fitted_model.best_score_

    def cv_results_(self):
        return self.fitted_model.cv_results_

    def n_features_in_(self):
        return self.fitted_model.n_features_in_

    def feature_names_in_(self):
        return self.fitted_model.feature_names_in_

    def score(self, X, y):
        return self.fitted_model.score(X, y)

    def coef_(self):
        if self.model_type == 'LR' and self.is_binary:
            return self.fitted_model.estimator_.coef_
        elif not self.is_binary and hasattr(self.fitted_model.best_estimator_, 'coef_'):
            return self.fitted_model.best_estimator_.coef_
        else:
            raise AttributeError(f"Model type '{self.model_type}' does not have a 'coef_' attribute.")

    def intercept_(self):
        if self.model_type == 'LR' and self.is_binary:
            return self.fitted_model.estimator_.intercept_
        elif not self.is_binary and hasattr(self.fitted_model.best_estimator_, 'intercept_'):
            return self.fitted_model.best_estimator_.intercept_
        else:
            raise AttributeError(f"Model type '{self.model_type}' does not have an 'intercept_' attribute.")