import os
import json
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import directory_config as dconf
import file_load

def clusterize(df, epsilon, min_t, date_range):
    t, c_id = 0, 0
    clusters = {}
    clusters_pos = {}

    while t+1 < len(date_range):
        start, end = date_range[t], date_range[t+1]
        mask = (df['timestamp'] > start) & (df['timestamp'] <= end)
        tmp_df = df.loc[mask]

        pos_data = tmp_df.loc[:, ['lon', 'lat']]
        positions = np.array(pos_data.values.tolist())

        density_clusters = DBSCAN(eps=epsilon, min_samples=min_t).fit(positions)

        serie = pd.Series(density_clusters.labels_, index=tmp_df.index)
        tmp_df.loc[:, 'cluster'] = serie

        grps = tmp_df.groupby("cluster")
        for i in grps.indices:

            grp = grps.get_group(i)
            grp_pos = grp.loc[:, ['lon', 'lat']]
            grp_pos = np.array(grp_pos.values.tolist())
            clusters_pos[c_id] = [np.mean(grp_pos[:, 0]), np.mean(grp_pos[:, 1])]

            clusters[c_id] = {
                'c_time': t,
                'time_start': start,
                'time_end': end,
                'obj_ids':grp['obj_id'].unique()
            }

            c_id += 1
        t += 1

    c_id, tag2id = 0, {}
    for tag in df['obj_id'].unique():
        tag2id[tag] = c_id
        c_id += 1
    return clusters, clusters_pos, tag2id

def prepare_jgetmove(df, clusters, tag_2_id):
    """Prepare file for jGetMove"""
    data_table = [[] for i in range(len(np.unique(df['obj_id'])))]
    time_index_table = []
    for clu in clusters:
        for b in clusters[clu]["obj_ids"]:
            data_table[tag_2_id[b]].append(clu)

    for clu in clusters:
        time_index_table.append([clusters[clu]["c_time"], clu])
    time_index_table = sorted(time_index_table,
                              key=lambda a_entry: a_entry[0])

    np.savetxt(dconf.WORKING_DIR + "/objectstimeindex.dat", np.array(time_index_table, dtype=int), fmt='%d')

    input_data = ""
    for l in data_table:
        if l != []:
            input_data += "\t".join([str(i) for i in l]) + "\n"
    input_data = input_data.strip()
    open(dconf.WORKING_DIR + "/objects.dat", 'w').write(input_data)

def jgetmove():
    os.system("java -jar " + dconf.JGETMOVE_DIR + "/jGetMove.jar " + dconf.WORKING_DIR + "/objects.dat " + dconf.WORKING_DIR + "/objectstimeindex.dat -o " + dconf.WORKING_DIR + "/results.json -p 2 -s 2 -t 1")

    return json.load(open("" + dconf.WORKING_DIR + "/results.json"))

def get_data(df, epsilon, min_t, date_range):
    clstrs, clstrs_pos, tag_2_id = clusterize(df, epsilon, min_t, date_range)
    prepare_jgetmove(df, clstrs, tag_2_id)
    results = jgetmove()

    json_data = file_load.get_raw_data(df)

    json_data['clusters'] = []
    nodes = results['nodes']
    for node in nodes:
        json_data['clusters'].append({
            'lon':clstrs_pos[node["id"]][0],
            'lat':clstrs_pos[node["id"]][1],
            'time_start':clstrs[node["id"]]["time_start"].value,
            'time_end':clstrs[node["id"]]["time_end"].value,
            'objects':clstrs[node["id"]]["obj_ids"].tolist()
        })

    for pattern_nb in range(0, len(results["patterns"])):
        pattern_name = str(results['patterns'][pattern_nb]["name"]).lower()
        json_data[pattern_name] = []

        links = pd.DataFrame(results['patterns'][pattern_nb]['links'])
        for l_idx, l_row in links.iterrows():
            arr_s = np.array(clstrs[l_row["source"]]["obj_ids"])
            arr_t = np.array(clstrs[l_row["target"]]["obj_ids"])
            l_start = clstrs[l_row["source"]]["time_start"]
            l_end = clstrs[l_row["target"]]["time_end"]
            ids = np.intersect1d(arr_s, arr_t)
            to_append = {
                'start_date':l_start.value,
                'end_date':l_end.value,
                'source_id':int(l_row["source"]),
                'target_id':int(l_row["target"]),
                'objects':ids.tolist()
            }
            json_data[pattern_name].append(to_append)

    return json_data
