import json
import yaml
import sys
import os

def convert_record_sets_to_changes(record_sets, action):
    changes = []
    for record in record_sets:
        if 'AliasTarget' in record:
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

def convert_yaml(input_file_name, output_yaml_file_name, output_json_file_name):
    # Actionの決定
    action_prefix = "DELETE" if input_file_name.startswith("DELETE") else "UPSERT"

    # DELETEの場合の処理
    if action_prefix == "DELETE":
        # maasapis.com/maasapis-com.yamlファイルを読み込む
        reference_yaml_file = "maasapis.com/maasapis-com.yaml"
        with open(reference_yaml_file, 'r', encoding='utf-8') as ref_file:
            reference_data = yaml.safe_load(ref_file)

        # 入力ファイルからデータを読み込む
        with open(input_file_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # 入力データ内のレコードを削除
        for record in data["ResourceRecordSets"]:
            record_name = record["Name"]
            record_type = record["Type"]

            # reference_dataから削除する
            reference_data["ResourceRecordSets"] = [
                ref_record for ref_record in reference_data["ResourceRecordSets"]
                if not (ref_record["Name"] == record_name and ref_record["Type"] == record_type)
            ]

        # 削除後のレコードを確認
        print(f"Updated ResourceRecordSets: {reference_data['ResourceRecordSets']}")

        # 更新されたreference_dataをYAML形式で出力
        with open(output_yaml_file_name, 'w', encoding='utf-8') as yaml_outfile:
            yaml.dump(reference_data, yaml_outfile, default_flow_style=False, allow_unicode=True)

        print(f"{output_yaml_file_name} has been updated.")  # 更新確認の出力

        # 新しい形式に変換（共通関数を使用）
        changes = convert_record_sets_to_changes(reference_data["ResourceRecordSets"], 'DELETE')

        # 最終的な辞書を作成
        output_data = {'Changes': changes}

        # JSON形式で出力
        with open(output_json_file_name, 'w', encoding='utf-8') as json_outfile:
            json.dump(output_data, json_outfile, indent=2)

        print(f"{output_json_file_name} has been created.")  # 更新確認の出力

    else:  # UPSERTの場合の処理
        # JSONデータを直接YAML形式に変換して出力
        with open(input_file_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # JSONデータを直接YAML形式に変換して出力
        with open(output_yaml_file_name, 'w', encoding='utf-8') as yaml_outfile:
            yaml.dump(data, yaml_outfile, default_flow_style=False, allow_unicode=True)

        print(f"{output_yaml_file_name} has been updated.")  # 更新確認の出力

        # 新しい形式に変換（動的データ取得の部分）
        changes = convert_record_sets_to_changes(data["ResourceRecordSets"], action_prefix)

        # 最終的な辞書を作成
        output_data = {'Changes': changes}

        # JSON形式で出力
        with open(output_json_file_name, 'w', encoding='utf-8') as json_outfile:
            json.dump(output_data, json_outfile, indent=2)

        print(f"{output_json_file_name} has been created.")  # 更新確認の出力

    # YAMLファイルの内容を標準出力に出力（GitHub Actionsで取得できるように）
    print("---")
    print(yaml.dump(reference_data if action_prefix == "DELETE" else data, allow_unicode=True))  # 元のデータのYAML出力

    # 最終的なJSONデータを標準出力に出力
    print("---")
    print(json.dumps(output_data, indent=2))  # 最終的なJSONデータの出力

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_yaml_file_name = sys.argv[2]
    output_json_file_name = sys.argv[3]
    convert_yaml(input_file_name, output_yaml_file_name, output_json_file_name)
