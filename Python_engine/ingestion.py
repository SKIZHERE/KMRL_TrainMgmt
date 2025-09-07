import csv

def load_trainsets():
    trainsets = []
    with open("data/trainsets.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trainsets.append(row)
    return trainsets
