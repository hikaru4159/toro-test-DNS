import json
import yaml

def change_yaml(input_json, output_yaml):
    # JSONファイルを読み込む
    with open(input_json, 'r') as json_file:
        data = json.load(json_file)

    # YAML形式で書き込む
    with open(output_yaml, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False, allow_unicode=True)

change_yaml(".\\maasapis.com\\idx_maasapi-com.json", ".\\maasapis.com\\2-idx_maasapi-com.yaml")