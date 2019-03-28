"""
Script to serialize trajectories csv into json
"""
import json
import pandas as pd
import directory_config as dconf

def import_file(file_name):
    """Run script"""
    pd.options.mode.chained_assignment = None  # default='warn'
    original_data = pd.read_csv(file_name)
    original_data = original_data[["object-id", "timestamp", "visible", "longitude", "latitude"]]
    original_data = original_data[(original_data.visible == True)]

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

    to_file = {'raw':{}}

    for i, grp in grps:
        for _, row in grp.iterrows():
            if not i in to_file['raw']:
                id_data = {'positions':[]}
                to_file['raw'][i] = id_data

            current_data = {
                'lon': row['lon'],
                'lat': row['lat'],
                'timestamp': row['timestamp'].value
            }

            to_file['raw'][i]['positions'].append(current_data)

    return to_file

def write_json(data, name="data"):
    """Create data.json"""

    with open(dconf.WORKING_DIR + "/" + name + ".json", "w") as dest_file:
        json.dump(data, dest_file)
