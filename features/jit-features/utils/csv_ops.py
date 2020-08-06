import csv


def parse_csv(datafile):
    data = []
    with open(datafile, "rb") as sd:
        r = csv.DictReader(sd)
        for line in r:
            data.append(line)
    return data


def write_csv(file_path, data_dict_list, headers):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for d in data_dict_list:
            writer.writerow(d)

if __name__ == '__main__':
    pass
