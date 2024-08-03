import csv


def proc(filename: str, index: list[int]):
    with open('output.csv', 'w', newline='') as writefile:
        with open(filename, newline='') as readfile:
            reader = csv.reader(readfile, delimiter=',', quotechar='"')
            writer = csv.writer(writefile, delimiter=',', quotechar='"')
            for row in reader:
                writer.writerow(list(map(lambda x: row[x], index)))
