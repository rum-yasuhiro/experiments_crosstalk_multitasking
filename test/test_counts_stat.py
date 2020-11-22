from pprint import pprint
from experiments.utils import counts_stat


def test_counts_stat(): 
    testdata = [
        {"00": 50, "11": 50}, 
        {"00": 25, "01": 25, "10": 25, "11": 25},
    ]
    mean, sem = counts_stat(testdata, 2)
    pprint(mean)
    pprint(sem)

if __name__ == "__main__":
    test_counts_stat()