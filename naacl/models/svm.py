__author__='thiagocastroferreira'

from sklearn import svm
from sklearn.grid_search import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression

class Model():
    # Machine Learning
    def train_svm(self, trainvectors, labels, c='1.0', kernel='linear', gamma='0.1', degree='1', class_weight='balanced', iterations=10, jobs=1):
        parameters = ['C', 'kernel', 'gamma', 'degree']
        if len(class_weight.split(':')) > 1: # dictionary
            class_weight = dict([label_weight.split(':') for label_weight in class_weight.split()])
        c_values = [0.001, 0.005, 0.01, 0.5, 1, 5, 10, 50, 100, 500, 1000] if c == 'search' else [float(x) for x in c.split()]
        kernel_values = ['linear', 'poly'] if kernel == 'search' else [k for  k in kernel.split()]
        gamma_values = [0.0005, 0.002, 0.008, 0.032, 0.128, 0.512, 1.024, 2.048] if gamma == 'search' else [float(x) for x in gamma.split()]
        degree_values = [1, 2] if degree == 'search' else [int(x) for x in degree.split()]
        grid_values = [c_values, kernel_values, gamma_values, degree_values]
        if not False in [len(x) == 1 for x in grid_values]: # only sinle parameter settings
            settings = {}
            for i, parameter in enumerate(parameters):
                settings[parameter] = grid_values[i][0]
        else:
            param_grid = {}
            for i, parameter in enumerate(parameters):
                param_grid[parameter] = grid_values[i]
            model = svm.SVC(probability=True)

            paramsearch = RandomizedSearchCV(model, param_grid, cv = 5, verbose = 2, n_iter = iterations, n_jobs = jobs, pre_dispatch = 4)
            paramsearch.fit(trainvectors, labels)
            settings = paramsearch.best_params_
        # train an SVC classifier with the settings that led to the best performance
        self.model = svm.SVC(
            probability = True,
            C = settings[parameters[0]],
            kernel = settings[parameters[1]],
            gamma = settings[parameters[2]],
            degree = settings[parameters[3]],
            class_weight = class_weight,
            cache_size = 1000,
            verbose = 2
        )
        self.model.fit(trainvectors, labels)


    def train_regression(self, trainvectors, labels, c='1.0', penalty='l1', tol='1e-4', solver='saga', iterations=10, jobs=1):
        parameters = ['C', 'penalty', 'tol']
        c_values = [0.001, 0.005, 0.01, 0.5, 1, 5, 10, 50, 100, 500, 1000] if c == 'search' else [float(x) for x in c.split()]
        penalty_values = ['l1', 'l2'] if penalty == 'search' else [k for  k in penalty.split()]
        tol_values = [1, 0.1, 0.01, 0.001, 0.0001] if tol == 'search' else [float(x) for x in tol.split()]
        grid_values = [c_values, penalty_values, tol_values]
        if not False in [len(x) == 1 for x in grid_values]: # only sinle parameter settings
            settings = {}
            for i, parameter in enumerate(parameters):
                settings[parameter] = grid_values[i][0]
        else:
            param_grid = {}
            for i, parameter in enumerate(parameters):
                param_grid[parameter] = grid_values[i]
            model = LogisticRegression(solver=solver)

            paramsearch = RandomizedSearchCV(model, param_grid, cv = 5, verbose = 2, n_iter = iterations, n_jobs = jobs, pre_dispatch = 4)
            paramsearch.fit(trainvectors, labels)
            settings = paramsearch.best_params_
        # train an SVC classifier with the settings that led to the best performance
        self.model = LogisticRegression(
            C = settings[parameters[0]],
            penalty = settings[parameters[1]],
            tol = settings[parameters[2]],
            solver= solver,
            verbose = 2
        )
        self.model.fit(trainvectors, labels)

    def score(self, X):
        score = self.model.decision_function([X])[0]
        pred_label = self.model.predict([X])[0]
        return score, pred_label