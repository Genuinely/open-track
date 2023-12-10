from os import getcwd
from json import loads, dumps
from datetime import datetime, timedelta
from csv import writer

TIME = "time"

def load_json_objects(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield loads(line)

def format_data(in_file, out_file, out_csv):
    in_file = open("%s/%s" % (getcwd(), in_file), "r")
    out_file = open("%s/%s" % (getcwd(), out_file), "w+")

    last_time = ""
    for line in in_file.readlines():
        line_obj = loads(line)

        if not last_time:
            original_time_str = line_obj[TIME]
            parsed_time = datetime.strptime(original_time_str, '%a %b %d %I:%M:%S %p')
            last_time = datetime(year=2023, month=parsed_time.month, day=parsed_time.day, 
                                      hour=parsed_time.hour, minute=parsed_time.minute, 
                                      second=parsed_time.second)
            
        else:
            last_time += timedelta(seconds=5)

        line_obj[TIME] = last_time.strftime('%Y-%m-%dT%H:%M:%S')
        out_file.write("%s\n" % dumps(line_obj))
            
    in_file.close()
    out_file.close()

    with open(out_csv, 'w', newline='') as csv_file:
        csv_writer = None

        for json_object in load_json_objects(out_file):
            if csv_writer is None:
                csv_writer = writer(csv_file)
                csv_writer.writerow(json_object.keys())

            csv_writer.writerow(json_object.values())

if __name__ == "__main__":
    format_data("data.json", "data_new.json", "output.csv")