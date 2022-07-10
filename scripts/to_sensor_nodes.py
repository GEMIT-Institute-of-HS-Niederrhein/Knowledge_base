import pandas as pd

df = pd.read_csv('neo4j_import.csv')
test_list = []
for data in df['Components']:
    #print(list(data))
    test_list.extend([x.strip("\' \'") for x in data[1:-1].split(',')])

to_csv = dict()
to_csv['Sensor'] = []
to_list = [x for x in set(test_list)]
for data in to_list[1:]:
    to_csv['Sensor'].append(data)


df = pd.DataFrame.from_dict(to_csv)
df.to_csv("sensor_nodes.csv")