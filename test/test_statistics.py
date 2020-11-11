from experiments.utils import statistics


def test_sem(): 
    quad_list = [[0.1, 0.3, 0.5, 0.7], [0.3, 0.2, 1.0, 0.5], [0.2, 0.2, 0.2, 0.2]]
    sem = statistics.sem(quad_list)

    print(sem)


def test_mean(): 
    quad_list = [[0.1, 0.3, 0.5, 0.7], [0.3, 0.2, 1.0, 0.5], [0.2, 0.2, 0.2, 0.2]]
    mean = statistics.mean(quad_list)

    print(mean)    


if __name__ == "__main__":
    test_sem()
    test_mean()


