import json
import yaml

# JSONファイルを開く
with open('1119-test-toro.json', 'r') as json_file:
    data = json.load(json_file)

# YAMLファイルに書き込む
with open('1119-test-toro.yml', 'w') as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=False)