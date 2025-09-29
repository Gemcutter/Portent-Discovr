import csv
def save(name, data, logs):
    if len(data)>1:
        with open(f'{name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([x.split(", ") for x in data.split("\n")])

    with open(f'{name}_full_log.txt', 'w') as file:
        file.write(logs)