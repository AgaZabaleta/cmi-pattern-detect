import sys
from os.path import basename
import pandas as pd
import file_load
import clusters

def main():
    if len(sys.argv) != 7:
        sys.exit()

    start = sys.argv[1]
    end = sys.argv[2]
    time_interval = sys.argv[3]
    eps = float(sys.argv[4])
    mint = int(sys.argv[5])
    file_path = sys.argv[6]
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

    raws_json = file_load.get_raw_data(df)
    raws_json["filename"] = file_name

    file_load.write_json(raws_json, name="raws_"+file_name)

    patterns_json = clusters.get_patterns(df, eps, mint, date_range)

    file_load.write_json(patterns_json, name="patterns_"+file_name)

if __name__ == '__main__':
    main()
