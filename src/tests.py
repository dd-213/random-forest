import random_forest


def testing(forest, test):
    predictions = list()
    for instance in test:
        classification = [predict_tree(instance, tree) for tree in forest]
        instance_prediction = max(set(classification), key=classification.count)
        predictions.append(instance_prediction)
    return predictions


def predict_tree(test, tree_node):
    if test[tree_node['feature']] < tree_node['value']:
        if isinstance(tree_node['lesser'], dict):
            return predict_tree(test, tree_node['lesser'])
        else:
            return tree_node['lesser']
    else:
        if isinstance(tree_node['greater'], dict):
            return predict_tree(test, tree_node['greater'])
        else:
            return tree_node['greater']


def evaluate_forest(forest, test_set):
    predictions = testing(forest, test_set)
    actual = [row[-1] for row in test_set]
    return accuracy_metric(actual, predictions)


def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0


def tests_forest(filename):
    n_folds = 4
    fold_it = 0
    select_limit = 1
    n_features = 1
    n_for_tournament = 2
    n_trees = 5
    max_depth = 7
    sample_size = 1.0
    score_forest = 0
    score_forest_trnmnt = 0

    n_features_rand = [[] for x in range(n_folds)]
    n_features_const = [[] for x in range(n_folds)]

    data = random_forest.data_in(filename)
    max_features = len(data[0])
    random_forest.str_to_float(data)
    folds, classes = random_forest.data_prep(data, n_folds)
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set, [])
        test_set = list()
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)

        for n_features in range(2, max_features):
            n_features_rand[fold_it].append(test_n_features(train_set, test_set, classes, n_features, 0))
            n_features_const[fold_it].append(test_n_features(train_set, test_set, classes, n_features, 1))
        fold_it += 1
    for fold_it in range(n_folds - 1):
        for instance in range(len(n_features_rand[fold_it])):
            for single_test in range(len(n_features_rand[fold_it][instance])):
                n_features_rand[n_folds - 1][instance][single_test]['score_forest'] += \
                n_features_rand[fold_it][instance][single_test]['score_forest']
                n_features_rand[n_folds - 1][instance][single_test]['score_trnmnt'] += \
                n_features_rand[fold_it][instance][single_test]['score_trnmnt']

                n_features_const[n_folds - 1][instance][single_test]['score_forest'] += \
                n_features_const[fold_it][instance][single_test][
                    'score_forest']
                n_features_const[n_folds - 1][instance][single_test]['score_trnmnt'] += \
                n_features_const[fold_it][instance][single_test][
                    'score_trnmnt']

    for instance in range(len(n_features_rand[n_folds - 1])):
        for single_test in range(len(n_features_rand[n_folds - 1][instance])):
            n_features_rand[n_folds - 1][instance][single_test]['score_forest'] /= n_folds
            n_features_rand[n_folds - 1][instance][single_test]['score_trnmnt'] /= n_folds
            n_features_const[n_folds - 1][instance][single_test]['score_forest'] /= n_folds
            n_features_const[n_folds - 1][instance][single_test]['score_trnmnt'] /= n_folds

    return [n_features_rand[n_folds - 1], n_features_const[n_folds - 1]]


def test_n_features(train_set, test_set, classes, n_features, flag):
    max_depth = 7
    test_features = list()
    for select_limit in [0.5]:    #for select_limit in [0.2, 0.5, 0.9]:
        for n_for_tournament in [2]:  #for n_for_tournament in [2, 3, 5]:
            for n_trees in [5]:     #for n_trees in [5, 10, 15]:
                for sample_size in [0.2]:     #for sample_size in [0.2, 0.5, 1.0]:
                    forest = random_forest.forest_init(train_set, classes, max_depth, sample_size, n_trees, n_features,
                                                      flag, 1, 1)
                    accuracy_forest = evaluate_forest(forest, test_set)

                    forest_trnmnt = random_forest.forest_init(train_set, classes, max_depth, sample_size, n_trees,
                                                             n_features, flag, n_for_tournament, select_limit)
                    accuracy_trnmnt = evaluate_forest(forest_trnmnt, test_set)

                    instance = {
                        'select_limit': select_limit,
                        'n_features': n_features,
                        'n_for_tournament': n_for_tournament,
                        'n_trees': n_trees,
                        'max_depth': max_depth,
                        'sample_size': sample_size,
                        'score_forest': accuracy_forest,
                        'score_trnmnt': accuracy_trnmnt
                    }
                    # print("wokring")
                    test_features.append(instance)
    return test_features
