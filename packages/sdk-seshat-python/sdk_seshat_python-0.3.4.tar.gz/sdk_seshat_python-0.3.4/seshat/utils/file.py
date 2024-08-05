import csv


def save_to_csv(data, file_name):
    keys = data[0].keys()
    with open(file_name, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
