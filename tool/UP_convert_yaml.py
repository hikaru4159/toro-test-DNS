import json
import yaml
import sys
import os

def convert_record_sets_to_changes(record_sets, action):
    changes = []
    for record in record_sets:
        # SOAレコードとNSレコードを除外
        if record['Type'] in ['SOA', 'NS']:
            continue

        elif 'AliasTarget' in record:
            changes.append({
                'Action': action,
                'ResourceRecordSet': record
            })
        else:
            changes.append({
                'Action': action,
                'ResourceRecordSet': {
                    'Name': record['Name'],
                    'ResourceRecords': record['ResourceRecords'],
                    'TTL': record['TTL'],
                    'Type': record['Type']
                }
            })
    return changes

def convert_yaml(input_file_name, output_yaml_file_name, output_DEL_json_name, output_UP_json_name):
    # reference YAMLファイルを読み込む
    reference_yaml_file = "maasapis.com/maasapis-com.yaml"
    with open(reference_yaml_file, 'r', encoding='utf-8') as ref_file:
        reference_data = yaml.safe_load(ref_file)
    # JSONファイルからデータを読み込む
    with open(input_file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # すべてのレコードを削除するための変更を作成
    delete_changes = convert_record_sets_to_changes(reference_data["ResourceRecordSets"], 'DELETE')
    # データが空でない場合にのみ削除処理を行う
    if delete_changes:
    # 最終的な削除データを作成
        delete_output_data = {'Changes': delete_changes}

        # 削除アクションをJSON形式で出力
        with open(output_DEL_json_name, 'w', encoding='utf-8') as json_outfile:
            json.dump(delete_output_data, json_outfile, indent=2)

        print(f"{output_DEL_json_name} has been created for DELETE action.") # 更新確認の出力
    else:
        print(" empty delete_changes data")
        return  # 何も削除しない場合は処理を中断
    # その後、UPSERTのための変更を作成
    changes = convert_record_sets_to_changes(data["ResourceRecordSets"], 'UPSERT')
    # 更新予定の内容がNSとSOAのみの場合は更新処理を行わない
    if all(record['Type'] in ['NS', 'SOA'] for record in data["ResourceRecordSets"]):
        print("Update data contains only NS and SOA records; skipping update action.")
        return
    
    # 最終的なUPSERTデータを作成
    output_data = {'Changes': changes}

    # JSON形式で出力
    with open(output_UP_json_name, 'a', encoding='utf-8') as json_outfile:
        json.dump(output_data, json_outfile, indent=2)

    print(f"{output_UP_json_name} has been updated for UPSERT action.") # 更新確認の出力

    # YAML形式で出力
    with open(output_yaml_file_name, 'w', encoding='utf-8') as yaml_outfile:
        yaml.dump(data, yaml_outfile, default_flow_style=False, allow_unicode=True)

    print(f"{output_yaml_file_name} has been updated.") # 更新確認の出力

    # YAMLファイルの内容を標準出力に出力
    print("---")
    print(yaml.dump(data, allow_unicode=True)) # 元のデータのYAML出力

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_yaml_file_name = sys.argv[2]
    output_DEL_json_name = sys.argv[3]
    output_UP_json_name = sys.argv[4]
    convert_yaml(input_file_name, output_yaml_file_name, output_DEL_json_name, output_UP_json_name)
