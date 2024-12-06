import json
import yaml
import sys

def convert_yaml(input_file_name, output_yaml_file_name, output_json_file_name):
    with open(input_file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    yaml_data = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    loaded_data = yaml.safe_load(yaml_data)

    # 新しい形式に変換
    changes = []
    for record in loaded_data["ResourceRecordSets"]:
        if 'AliasTarget' in record:
            changes.append({
                'Action': 'UPSERT',
                'ResourceRecordSet': record
            })
        else:
            changes.append({
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record['Name'],
                    'ResourceRecords': record['ResourceRecords'],
                    'TTL': record['TTL'],
                    'Type': record['Type']
                }
            })

    # 最終的な辞書を作成
    output_data = {'Changes': changes}

    # YAML形式で出力
    with open(output_yaml_file_name, 'w', encoding='utf-8') as yaml_outfile:
        yaml.dump(output_data, yaml_outfile, allow_unicode=True)

    print(f"{output_yaml_file_name} has been updated.")  # 更新確認の出力

    # JSON形式で出力
    with open(output_json_file_name, 'w', encoding='utf-8') as json_outfile:
        json.dump(output_data, json_outfile, indent=2)

    print(f"{output_json_file_name} has been created.")  # 更新確認の出力

    # YAMLファイルの内容を標準出力に出力（GitHub Actionsで取得できるように）
    print("---")
    print(yaml.dump(output_data, allow_unicode=True))

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_yaml_file_name = sys.argv[2]
    output_json_file_name = sys.argv[3]
    convert_yaml(input_file_name, output_yaml_file_name, output_json_file_name)
