# Random forest implementation 
> With added selection limit (for Gini index) and randomized tree division

## Table of Contents
* [General Info](#general-information)
* [Usage](#usage)
* [Acknowledgements](#acknowledgements)

## General Information
Random forest implementation with optional futher randomization of tree divsion. After selection limit, splits (with gini indexes) are randomly picked and the smallest index becomes the deciding split.
Folds for cross validation have been set in _tests_.
Data sets should be numerics followed by class in last column.

## Usage
_random_forest_:
def forest_init(train, classes, max_depth, sample_size, n_trees, n_features, n_feat_const_flag=1, n_for_tournament=1, select_limit=1):
>- train - training subset
>- classes - list of classes in set
>- max_depth - maximal depth of trees
>- sample_size - maximal size of subsets of train used for one tree ((0.09,1])
>- n_trees - number of trees
>- n_features - maximal number of features used for one tree
>- n_feat_const_flag=1 - whetever n_features is constant for every tree or randomized
>- n_for_tournament=1 - number of randomly choosen splits 
>- select_limit=1 - selection limit for Gini index

def data_prep(data, n_folds):
>- data - data set, last column treated as classes, atributes as floats
>- n_folds - number of folds for cross validation

_tests_:
	 def tests_forest(filename):
>- filename - file
>- n_folds set as = 4
Every last instance is the mean of results of all iterations for specified conditions.

_to_file_:
Added module for saving results.

## Acknowledgements
Random forest implementation based on [this implementation](https://machinelearningmastery.com/implement-random-forest-scratch-python/).
