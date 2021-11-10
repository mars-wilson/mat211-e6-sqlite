
import csv

with open('data/coffees.csv','r') as fv:
    # fv = open('data/coffees.csv','r')
    coffees = csv.reader(fv, delimiter='\t')
    try:
        while True:
            line = next(coffees)
            print(line)
    except StopIteration:
        print('done')