import json
import yaml

def change_json(input_yaml, output_json):
    # YAMLファイルを読み込む
    with open(input_yaml, 'r') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # JSON形式で書き込む
    with open(output_json, 'w') as json_file:
        json.dump(data, json_file, indent=4)

change_json(".\\1119-test-toro.yaml", ".\\exch_1119-test-toro.json")