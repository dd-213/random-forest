import tests

filename = 'iris.data'
[test_rand, test_const] = tests.tests_forest(filename)

with open('Iris_scores.txt', 'w') as f:
    n_features = 2
    print("Test - losowa liczba argumentów:  \n", file=f)
    for instance in test_rand:
        print("N_features       ", n_features, "\n", file=f)
        for test in instance:
            print(test, "\n", file=f)
        print("\n", file=f)
        n_features += 1

    n_features = 2
    print("Test - stała liczba argumentów:  \n", file=f)
    for instance in test_const:
        print("N_features       ", n_features, "\n", file=f)
        for test in instance:
            print(test, "\n", file=f)
        print("\n", file=f)
        n_features += 1

f.close()

filename = 'wine.data'
[test_rand, test_const] = tests.tests_forest(filename)
with open('Wine_scores.txt', 'w') as f:
    n_features = 2
    print("Test - losowa liczba argumentów:  \n", file=f)
    for instance in test_rand:
        print("N_features       ", n_features, "\n", file=f)
        for test in instance:
            print(test, "\n", file=f)
        print("\n", file=f)
        n_features += 1

    n_features = 2
    print("Test - stała liczba argumentów:  \n", file=f)
    for instance in test_const:
        print("N_features       ", n_features, "\n", file=f)
        for test in instance:
            print(test, "\n", file=f)
        print("\n", file=f)
        n_features += 1

f.close()