import sys
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
    file_name = sys.argv[6]
    df = file_load.import_file(file_name)

    date_range = pd.date_range(start=start, end=end, freq=time_interval)

    json_data = clusters.get_data(df, eps, mint, date_range)

    file_load.write_json(json_data)

if __name__ == '__main__':
    main()
