from random import randrange
import random as random2
from random import uniform
from random import SystemRandom


def data_in(filename):
    data = list()
    with open(filename, 'r') as file:
        for line in file:
            if not line:
                continue
            line = line[:-1]  # /n
            data.append(list(line.split(",")))
    return data


def str_to_float(data):
    for line in data:
        for index in range(len(line) - 1):
            line[index] = float(line[index].strip())


def data_prep(data, n_folds):
    fold = list()
    data_folds = list()
    data_copy = data
    classes = list()
    fold_size = int(len(data) / n_folds)

    for i in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(data_copy))
            classes.append(data_copy[index][-1])
            fold.append(data_copy.pop(index))
        data_folds.append(fold)
    classes = list(set(classes))
    return [data_folds, classes]


def subset_data(data, subset_size):
    subset = list()
    data_copy = data
    rand_size = uniform(0.09, subset_size)
    for i in range(round(len(data) * rand_size)):
        index = randrange(len(data_copy))
        subset.append(data_copy[index])
    return subset


def gini_index(subset, classes, index, value):
    instances = float(len(subset))
    gini = 0.0
    classes_lesser = {i: 0 for i in classes}
    classes_lesser.update({'sum': 0})
    classes_greater = {i: 0 for i in classes}
    classes_greater.update({'sum': 0})
    for inst in subset:
        if instances == 0:
            continue

        for item in classes:
            if item == inst[len(inst) - 1]:
                if inst[index] < value:
                    classes_lesser[item] += 1
                    classes_lesser['sum'] += 1
                else:
                    classes_greater[item] += 1
                    classes_greater['sum'] += 1
    gini_less = 1
    gini_great = 1
    for item in classes:
        if classes_lesser['sum'] > 0:
            gini_less -= (classes_lesser[item] / classes_lesser['sum']) ** 2
        if classes_greater['sum'] > 0:
            gini_great -= (classes_greater[item] / classes_greater['sum']) ** 2
    gini = (gini_less * classes_lesser['sum'] + gini_great * classes_greater['sum']) / instances
    return gini


def tournament(candidates, select_limit):
    if len(candidates) > 1:
        srand = SystemRandom()
        n_for_draw = len(candidates) - 1
        for index in range(len(candidates) - 1):
            if candidates[index][0] > select_limit:
                n_for_draw = index - 1
                break
        if n_for_draw < 1:
            candidates[0][0] = 1  # gini
            candidates[0][3] = 0.0  # value
            return candidates[0]

        candidate = list()

        candidate = random2.sample(range(n_for_draw + 1), 2)
        if candidates[candidate[0]][0] > candidates[candidate[1]][0]:
            return candidates[candidate[0]]
        else:
            return candidates[candidate[1]]
    else:
        return candidates[0]


def node_init(dataset, n_features, classes, select_limit, n_for_tournament):
    gini_max = 1
    row = 0
    feature = 0
    value = 999
    trnmt_list = [[gini_max, row, feature, value]] * n_for_tournament
    features = list()
    copy_features = list(range(len(dataset[0]) - 1))
    while len(features) < n_features:
        random_index = random2.choice(copy_features)
        if random_index not in features:
            features.append(random_index)
    for feature in features:
        for row in range(len(dataset)):
            current_gini = gini_index(dataset, classes, feature, dataset[row][feature])
            for lead in range(n_for_tournament):
                if current_gini < trnmt_list[lead][0]:
                    actual = trnmt_list[lead]
                    trnmt_list[lead] = [current_gini, feature, row, dataset[row][feature]]
                    for i in range(len(trnmt_list[lead + 1:])):
                        actual_loop = trnmt_list[lead + i + 1]
                        trnmt_list[lead + i + 1] = actual
                        actual = actual_loop
                    break
    node_gini, node_feature, row, node_value = tournament(trnmt_list, select_limit)
    node_lesser = list()
    node_greater = list()
    for row in range(len(dataset)):
        instance = dataset[row]

        if instance[node_feature] < node_value:
            node_lesser.append(dataset[row])
        else:
            node_greater.append(dataset[row])
    return {'feature': node_feature, 'value': node_value, 'gini': node_gini, 'lesser': node_lesser,
            'greater': node_greater}


def leaf_node(instances):
    classifiaction = [row[-1] for row in instances]
    return max(set(classifiaction), key=classifiaction.count)


def new_nodes(node, max_depth, n_features, curr_depth, classes, select_limit, n_for_tournament):
    if not node['lesser'] or not node['greater']:
        node['lesser'] = node['greater'] = leaf_node(node['lesser'] + node['greater'])
        return
    if curr_depth >= max_depth:
        node['lesser'] = leaf_node(node['lesser'])
        node['greater'] = leaf_node(node['greater'])
        return
    node['lesser'] = node_init(node['lesser'], n_features, classes, select_limit, n_for_tournament)
    new_nodes(node['lesser'], max_depth, n_features, curr_depth + 1, classes, select_limit, n_for_tournament)
    node['greater'] = node_init(node['greater'], n_features, classes, select_limit, n_for_tournament)
    new_nodes(node['greater'], max_depth, n_features, curr_depth + 1, classes, select_limit, n_for_tournament)


def tree_init(dataset, max_depth, n_features, classes, select_limit, n_for_tournament, n_feat_const_flag):
    if not n_feat_const_flag:
        n_features = randrange(1, n_features)
    root = node_init(dataset, n_features, classes, select_limit, n_for_tournament)
    new_nodes(root, max_depth, n_features, 1, classes, select_limit, n_for_tournament)
    return root


def forest_init(train, classes, max_depth, sample_size, n_trees, n_features, n_feat_const_flag=1, n_for_tournament=1,
                select_limit=1):
    trees = list()
    for i in range(n_trees):
        subset = subset_data(train, sample_size)
        tree = tree_init(subset, max_depth, n_features, classes, select_limit, n_for_tournament, n_feat_const_flag)
        trees.append(tree)
    return trees
