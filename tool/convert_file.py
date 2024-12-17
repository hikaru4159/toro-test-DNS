import json
import yaml
import os
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import chardet

def upload_convert():
    input_file = filedialog.askopenfilename(title="変換するYAMLファイルを選択", filetypes=[("YAML files", "*.yaml")], initialdir=os.getcwd())
    
    if input_file:
        convert_yaml(input_file)


def detect_encoding(file_path):
    # ファイルのエンコーディングを検出する
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding

def convert_yaml(input_file):
    encoding = detect_encoding(input_file)
    
    # YAMLファイルを読み込む
    with open(input_file, 'r', encoding=encoding) as file:
        data = yaml.safe_load(file)

    # デバッグ: データの構造を確認
    print("Data loaded from YAML:")
    print(data)

    # 新しい形式に変換
    changes = []

    # 'ResourceRecordSets'キーのリストを処理
    if 'ResourceRecordSets' in data:
        for record in data['ResourceRecordSets']:
            # デバッグ: 各レコードの内容を確認
            print("Processing record:")
            print(record)

            # レコードが辞書型であることを確認
            if isinstance(record, dict):
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
            else:
                print("Warning: Record is not a dictionary:", record)

    # 最終的な辞書を作成
    output_data = {'Changes': changes}

    # 出力ファイル名を生成
    output_file = os.path.join(os.path.dirname(input_file), f"upconv-{os.path.basename(input_file)}")

    # 新しいYAML形式で出力
    with open(output_file, 'w', encoding='utf-8') as outfile:
        yaml.dump(output_data, outfile, allow_unicode=True)

    messagebox.showinfo("完了", f"変換が完了しました:\n{output_file}")

def change_yaml_to_json(input_yaml, output_json):
    encoding = detect_encoding(input_yaml)
    with open(input_yaml, 'r', encoding=encoding) as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def change_json_to_yaml(input_json, output_yaml):
    encoding = detect_encoding(input_json)
    with open(input_json, 'r', encoding=encoding) as json_file:
        data = json.load(json_file)

    with open(output_yaml, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False, allow_unicode=True)

def convert_to_csv(input_file, output_csv):
    encoding = detect_encoding(input_file)
    
    with open(input_file, 'r', encoding=encoding) as file:
        if input_file.endswith('.json'):
            data = json.load(file)
        elif input_file.endswith('.yaml'):
            data = yaml.load(file, Loader=yaml.FullLoader)
        else:
            messagebox.showerror("エラー", "サポートされていないファイル形式です。")
            return

    # データをCSV形式で出力
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        if isinstance(data, dict):
            writer.writerow(data.keys())
            writer.writerow(data.values())
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    writer.writerow(item.values())
                else:
                    writer.writerow([item])
        else:
            messagebox.showerror("エラー", "データが辞書またはリスト形式ではありません。")

    messagebox.showinfo("完了", f"ファイルをCSV形式に変換しました:\n{output_csv}")

def process_file(input_file):
    _, file_extension = os.path.splitext(input_file)
    output_file = os.path.join(os.path.dirname(input_file), f"conv-{os.path.basename(input_file).replace(file_extension, '')}")

    if file_extension.lower() == '.yaml':
        output_file += '.json'
        change_yaml_to_json(input_file, output_file)
        messagebox.showinfo("完了", f"YAMLファイルをJSONファイルに変換しました:\n{output_file}")
    elif file_extension.lower() == '.json':
        output_file += '.yaml'
        change_json_to_yaml(input_file, output_file)
        messagebox.showinfo("完了", f"JSONファイルをYAMLファイルに変換しました:\n{output_file}")
    else:
        messagebox.showerror("エラー", "サポートされていないファイル形式です。")

def select_file():
    input_file = filedialog.askopenfilename(title="ファイルを選択", filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml")], initialdir=os.getcwd())
    
    if input_file:
        process_file(input_file)

def convert_file_to_csv():
    input_file = filedialog.askopenfilename(title="ファイルを選択", filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml")], initialdir=os.getcwd())
    
    if input_file:
        output_csv = os.path.join(os.path.dirname(input_file), f"table-{os.path.basename(input_file).replace(os.path.splitext(input_file)[1], '.csv')}")
        convert_to_csv(input_file, output_csv)

def create_gui():
    root = tk.Tk()
    root.title("JSON/YAML変換ツール")

    # YAML変換ボタン
    upload_button = tk.Button(root, text="upload変換", command=upload_convert)
    upload_button.pack(pady=10)

    # JSON/YAML変換ボタン
    select_button = tk.Button(root, text="ファイルを選択して変換", command=select_file)
    select_button.pack(pady=10)

    # CSV変換ボタン
    csv_button = tk.Button(root, text="CSV形式に変換", command=convert_file_to_csv)
    csv_button.pack(pady=10)

    # 終了ボタン
    exit_button = tk.Button(root, text="終了", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
