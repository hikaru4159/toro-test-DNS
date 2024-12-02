import json
import yaml
import sys

def convert_yaml(input_file_name, output_file_name):

    with open(input_file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    yaml_data = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    loaded_data = yaml.safe_load(yaml_data)

    print("Loaded Data:", loaded_data)  # デバッグ用の出力

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
    
    print("Output Data:", output_data)  # デバッグ用の出力

    # 新しいYAML形式で出力
    with open(output_file_name, 'w', encoding='utf-8') as outfile:
        yaml.dump(output_data, outfile, allow_unicode=True)
    
    print(f"{output_file_name} has been updated.")  # 更新確認の出力

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    convert_yaml(input_file_name, output_file_name)
