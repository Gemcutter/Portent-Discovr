import csv
import json
        

def save(name, data, logs, raw_cloud_response_dict):
    if len(data)>1:
        with open(f'{name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([x.split(", ") for x in data.split("\n")])

    with open(f'{name}_full_log.txt', 'w') as file:
        file.write(logs)

    if raw_cloud_response_dict != None:
        with open(f'{name}_full_AWS_results.json', 'w') as jfile:
            json.dump(raw_cloud_response_dict, jfile, default=str, indent=4)

    else:
        with open(f'you dun goofed.txt', 'w') as fufile:
            fufile.write("hahahahahahahahah end me now")
