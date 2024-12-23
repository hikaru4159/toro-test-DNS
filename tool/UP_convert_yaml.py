import json
import yaml
import sys

def convert_record_sets_to_changes(record_sets, action, zone_name):
    changes = []
    for record in record_sets:
        # SOAレコードとNSレコードを除外する条件を厳密にする
        if record['Type'] in ['SOA', 'NS'] and record['Name'] == zone_name:
            continue

        changes.append({
            'Action': action,
            'ResourceRecordSet': record if 'AliasTarget' in record else {
                'Name': record['Name'],
                'ResourceRecords': record['ResourceRecords'],
                'TTL': record['TTL'],
                'Type': record['Type']
            }
        })
    return changes

def write_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)
    print(f"{filename} has been created/updated.")

def convert_yaml(input_file_name, bf_maasapis_yaml, output_DEL_json_name, output_UP_json_name, zone_name):
    # bf_maasapis_yamlの内容を表示デバッグ
    with open(bf_maasapis_yaml, 'r', encoding='utf-8') as ref_file:
        reference_data = yaml.safe_load(ref_file)
        # 内容を表示
        print("Contents of bf_maasapis_yaml:")
        print(reference_data) 

    with open(bf_maasapis_yaml, 'r', encoding='utf-8') as ref_file:
        reference_data = yaml.safe_load(ref_file)

    with open(input_file_name, 'r', encoding='utf-8') as new_record_file:
        data = yaml.safe_load(new_record_file)

    # DELETE changes
    delete_changes = convert_record_sets_to_changes(reference_data["ResourceRecordSets"], 'DELETE', zone_name)
    if delete_changes:
        write_json_file(output_DEL_json_name, {'Changes': delete_changes})
    else:
        print("No changes for DELETE action.")

    # UPSERT changes
    changes = convert_record_sets_to_changes(data["ResourceRecordSets"], 'UPSERT', zone_name)
    if not all(record['Type'] in ['NS', 'SOA'] for record in data["ResourceRecordSets"]):
        write_json_file(output_UP_json_name, {'Changes': changes})

    # Write YAML
    # with open("maasapis-com.yaml", 'w', encoding='utf-8') as yaml_outfile:
    #     yaml.dump(data, yaml_outfile, default_flow_style=False, allow_unicode=True)
    print("maasapis-update.yaml created echo data under.")

# Output YAML content to standard output
    print("---")
    print(yaml.dump(data, allow_unicode=True))

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: script.py <input_json> <output_yaml> <output_del_json> <output_up_json> <zone_name>")
        sys.exit(1)

    convert_yaml(*sys.argv[1:])
