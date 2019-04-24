"""
Script to serialize trajectories csv into json
"""
import json
import pandas as pd
import numpy as np
import directory_config as dconf

def import_file(file_name):
    """Run script"""
    pd.options.mode.chained_assignment = None  # default='warn'
    original_data = pd.read_csv(file_name)
    original_data = original_data[["object-id", "timestamp", "longitude", "latitude"]]

    raw_new_data = {
        'timestamp':[],
        'lon':  [],
        'lat':  [],
        'obj_id':  []
    }

    i = 0

    for _, row in original_data.iterrows():
        raw_new_data['obj_id'].append(int(row["object-id"]))
        raw_new_data['timestamp'].append(pd.to_datetime(row["timestamp"]))
        raw_new_data['lon'].append(row["longitude"])
        raw_new_data['lat'].append(row["latitude"])

    return pd.DataFrame(raw_new_data)

def get_raw_data(df):
    """Extracts the raw positions and timestamps from file and prepare the base json structure"""
    grps = df.groupby("obj_id")

    raws = {
        'start': df['timestamp'].min().value,
        'end': df['timestamp'].max().value,
        'objects': {}
    }

    delta = grps['timestamp'].diff().dropna().mean()

    rest = delta
    d_days = rest / np.timedelta64(1, 'D')
    rest = rest - np.timedelta64(int(d_days), 'D')
    d_hours = rest / np.timedelta64(1, 'h')
    rest = rest - np.timedelta64(int(d_hours), 'h')
    d_minutes = rest / np.timedelta64(1, 'm')
    rest = rest - np.timedelta64(int(d_minutes), 'm')
    d_seconds = rest / np.timedelta64(1, 's')

    raws['timestep'] = {
        'days': int(d_days),
        'hours': int(d_hours),
        'minutes': int(d_minutes),
        'seconds': int(d_seconds)
    }

    for i, grp in grps:
        for _, row in grp.iterrows():
            if not i in raws['objects']:
                id_data = {'positions':[]}
                raws['objects'][i] = id_data

            current_data = {
                'lon': row['lon'],
                'lat': row['lat'],
                'timestamp': row['timestamp'].value
            }

            raws['objects'][i]['positions'].append(current_data)

    return raws

def write_json(data, name="data"):
    """Create data.json"""

    with open(dconf.WORKING_DIR + "/" + name + ".json", "w") as dest_file:
        json.dump(data, dest_file)
