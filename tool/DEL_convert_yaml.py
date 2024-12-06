import json
import yaml
import sys

def convert_yaml(input_file_name, output_yaml_file_name, output_json_file_name):
    with open(input_file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # JSONデータを直接YAML形式に変換して出力
    with open(output_yaml_file_name, 'w', encoding='utf-8') as yaml_outfile:
        yaml.dump(data, yaml_outfile, default_flow_style=False, allow_unicode=True)

    print(f"{output_yaml_file_name} has been updated.")  # 更新確認の出力

    # 新しい形式に変換
    changes = []
    for record in data["ResourceRecordSets"]:
        if 'AliasTarget' in record:
            changes.append({
                'Action': 'DELETE',
                'ResourceRecordSet': record
            })
        else:
            changes.append({
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': record['Name'],
                    'ResourceRecords': record['ResourceRecords'],
                    'TTL': record['TTL'],
                    'Type': record['Type']
                }
            })

    # 最終的な辞書を作成
    output_data = {'Changes': changes}

    # JSON形式で出力
    with open(output_json_file_name, 'w', encoding='utf-8') as json_outfile:
        json.dump(output_data, json_outfile, indent=2)

    print(f"{output_json_file_name} has been created.")  # 更新確認の出力

    # YAMLファイルの内容を標準出力に出力（GitHub Actionsで取得できるように）
    print("---")
    print(yaml.dump(data, allow_unicode=True))  # 元のデータのYAML出力

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_yaml_file_name = sys.argv[2]
    output_json_file_name = sys.argv[3]
    convert_yaml(input_file_name, output_yaml_file_name, output_json_file_name)
