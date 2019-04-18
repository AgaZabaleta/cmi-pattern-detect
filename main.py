import sys, getopt
from os.path import basename
import pandas as pd
import file_load
import clusters

def getmove(argv):
    start = argv[0]
    end = argv[1]
    time_interval = argv[2]
    eps = float(argv[3])
    mint = int(argv[4])
    file_path = argv[5]
    file_name = basename(file_path)
    df = file_load.import_file(file_path)

    if start.upper().isupper():
        start = df['timestamp'].min()
        print(start)
    elif start.isdigit():
        sys.exit("error:start date should be a timestamp YYYY-MM-DD or 's' to select the earliest date")

    if end.upper().isupper():
        end = df['timestamp'].max()
    elif end.isdigit():
        sys.exit("error:end date should be a timestamp YYYY-MM-DD or 'e' to select the latest date")

    date_range = pd.date_range(start=start, end=end, freq=time_interval)

    patterns_json = clusters.get_patterns(df, eps, mint, date_range)

    file_load.write_json(patterns_json, name="patterns_"+file_name)

def raws(file_path):
    file_name = basename(file_path)
    df = file_load.import_file(file_path)

    raws_json = file_load.get_raw_data(df)
    raws_json["filename"] = file_name

    file_load.write_json(raws_json, name="raws_"+file_name)

def main(argv):
    if len(argv) < 2:
        sys.exit("Missing arguments: please check documentation on how to use this script")

    if argv[0] == "getmove":
        if len(argv[1:]) == 6:
            getmove(argv[1:])
    elif argv[0] == "raws":
        raws(argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])
