# bbml.ensemble / BijanClassifier

## Motivation

The `bbml.ensemble` library is a Python tool designed for classification problems where accuracy is not the primary concern. This novel classification approach focuses on fitting models based on weights or costs associated with different types of errors. In addition to addressing classification problems by assigning labels according to a specified weight/cost matrix, this library serves as an efficient tool for decision-making scenarios. One significant application is in industrial settings, such as manufacturing systems, where misclassifying a good item as a bad item, or vice versa, incurs asymmetric costs depending on the error type. Thus, the contribution of this model lies in fitting classification models based on a predefined weight/cost matrix. In this release, the `BijanClassifier` utilizes four base classification models: decision tree, random forest, gradient boosting, and logistic regression.

For binary classification problems, standard models aim to maximize the accuracy of the fitted model on the training set, treating Type I and Type II errors (FN and FP) with equal weight (symmetrical cost). However, `BijanClassifier` assigns asymmetrical cost values to each error type.


## Instructions

1. Install:

    ```
    pip install bbml
    ```


2. Import:

    ```
    from bbml.ensemble import BijanClassifier
    ```


3. Call:

    class bbml.ensemble.BijanClassifier(*, model_type='RF', cost_matrix=None, criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.0, monotonic_cst=None)


------------------------------------------------------------


4. Parameters:

    **model_type :** {“RF”, “DT”, “GB”, “LR”}, default=”RF”

    This parameter specifies the base classification model, including: RF (Random Forest), DT (Decision Tree), GB (Gradient Boosting), and LR (Logistic Regression).


    **cost_matrix :** array of cost matrix, or “None”  default=None

    Weights/Costs associated with the error types are provided in the format of an array. If set to None, only the basic/standard classification model is fitted without considering the error cost matrix.


    **thresholds :** int or array-like, default=100

    The number of decision threshold to use when discretizing the output of the classifier method. Pass an array-like to manually specify the thresholds to use.


    **cv :** int, float, cross-validation generator, iterable or “prefit”, default=None

    Determines the cross-validation splitting strategy to train classifier.


    **greater_is_better :** bool, default=True

    Whether score_func is a score function (default), meaning high is good, or a loss function, meaning low is good. In the latter case, the scorer object will sign-flip the outcome of the score_func.






    
    **Note :**

    Based on selected `model_type`, the other parameters can be modified and defined. For tree-based methods following parameters can be tuned. All other parameters, such as n_estimators (for RF and GB), bootstrap, n_jobs, and etc. , can be set and tuned in the same manner as the basic models in the scikit-learn library.


    **criterion :** {“gini”, “entropy”, “log_loss”}, default=”gini”
    
    The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “log_loss” and “entropy” both for the Shannon information gain, see Mathematical formulation.


    **max_depth :** int, default=None
    
    The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.


    **min_samples_leaf :** int or float, default=1

    The minimum number of samples required to be at a leaf node. A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches. This may have the effect of smoothing the model, especially in regression.


    **max_features :** int, float or {“sqrt”, “log2”}, default=None

    The number of features to consider when looking for the best split.


    **random_state :** int, RandomState instance or None, default=None
    
    Controls the randomness of the estimator. The features are always randomly permuted at each split, even if splitter is set to "best". When max_features < n_features, the algorithm will select max_features at random at each split before finding the best split among them. But the best found split may vary across different runs, even if max_features=n_features. That is the case, if the improvement of the criterion is identical for several splits and one split has to be selected at random. To obtain a deterministic behaviour during fitting, random_state has to be fixed to an integer. See Glossary for details.


------------------------------------------------------------

5. Attributes:

    **fit(X, y, **params) :**
    
    Fit the classifier. X{array-like, sparse matrix} of shape (n_samples, n_features) Training data. y array-like of shape (n_samples,) Target values.

   **predict(X) :**

    Predict the target of new samples. X{array-like, sparse matrix} of shape (n_samples, n_features)

   **predict_proba(X) :**

    Predict class probabilities for X using the fitted estimator. X{array-like, sparse matrix} of shape (n_samples, n_features)

   **accuracy(X, y, sample_weight=None) :**

    Return the mean accuracy on the given test data and labels.

   **cost(y, y_pred) :**

    Return the misclassification cost based on cost matrix. y_pred is prediction values.

   **estimator_ :**

    estimator instance. The fitted classifier used when predicting.

   **best_params_ :**

    Parameter setting that gave the best results on the hold out data for multi class problems.

   **best_threshold_ :**

    The new decision threshold for binary classification problems.

   **best_score_ :**

    The optimal score of the objective metric, evaluated at best_threshold_.

   **cv_results_ :**

    A dictionary containing the scores and thresholds computed during the cross-validation process. Only exist if store_cv_results=True. The keys are "thresholds" and "scores".

   **n_features_in_ :**

    Number of features seen during fit. Only defined if the underlying estimator exposes such an attribute when fit.

   **feature_names_in_ :**

    Names of features seen during fit. Only defined if the underlying estimator exposes such an attribute when fit.

   **coef_ :** ndarray of shape (1, n_features) or (n_classes, n_features)

    Coefficient of the features in the decision function for logistic regression. coef_ is of shape (1, n_features) when the given problem is binary. In particular, when multi_class='multinomial', coef_ corresponds to outcome 1 (True) and -coef_ corresponds to outcome 0 (False).

   **intercept_ :** ndarray of shape (1,) or (n_classes,)

    Intercept (a.k.a. bias) added to the decision function for logistic regression. If fit_intercept is set to False, the intercept is set to zero. intercept_ is of shape (1,) when the given problem is binary. In particular, when multi_class='multinomial', intercept_ corresponds to outcome 1 (True) and -intercept_ corresponds to outcome 0 (False).

------------------------------------------------------------


6. Sample Code:

    ```python
    import numpy as np
    from bbml.ensemble import BijanClassifier
    from sklearn.datasets import make_classification
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split

    # Step 1: Generate a binary dataset
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, n_clusters_per_class=1, random_state=42)

    # Step 2: Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 3: Define the cost matrix and basic model
    CM = np.array([[0, 20], [80, 0]])
    BM = "DT"

    # Step 4: Fit a BijanClassifier on the training set
    clf = BijanClassifier(model_type='DT', cost_matrix=CM, max_depth=2, random_state=42)
    clf.fit(X_train, y_train)

    # Step 5: Evaluate the classifier on the testing set
    y_pred = clf.predict(X_test)

    # Calculate accuracy
    accuracy = clf.accuracy(y_test, y_pred)

    # Calculate the associated cost with error types
    cost = clf.cost(y_test, y_pred)

    # Print accuracy and classification report
    print(f"Accuracy: {accuracy}")
    print(f"Cost: {cost}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    ```
