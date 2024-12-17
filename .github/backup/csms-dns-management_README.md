# csms-dns-management
csms環境用のDNS管理用リポジトリです。
# DNS設定管理 - maasapis.com


このリポジトリは、AWS Route 53におけるmaasapis.comのDNS設定を管理するためのものです。以下のルールに従って運用します。


## 運用ルール

1. **リポジトリとroute53の更新**  
   git pushにより自動でリポジトリとroute53のデータを更新するので、ユーザーは更新作業を行う必要はありません。
   自動更新が正常に機能するためには、適切な設定と権限が必要です。変更内容が意図した通りに反映されているかを確認をしてください。

2. **ネームサーバ情報の管理**  
   このリポジトリでは、ネームサーバ情報のIPアドレス先の環境までの管理は行いません。ネームサーバの設定はAWS Route 53の管理コンソールで直接行ってください。

3. **csms環境のレコード管理**  
   このリポジトリには、csms環境に関連するDNSレコードのみを含めます。その他の環境に関するレコードは追加しないでください。

4. **不要なレコードの削除**  
   不要になったDNSレコードは随時削除を行います。削除した場合は、その理由をコミットメッセージに明記してください。

5. **環境差分の優先**  
   DNS環境とリポジトリ環境に差分が生じた場合は、リポジトリ環境を優先し、リポジトリの内容をDNS環境に反映します。これにより、リポジトリの状態が最新の正しい情報を保持することを保証します。

6. **yamlファイルで管理**  
   DNS環境データはyamlファイルで管理

7. **更新内容はjsonファイルで編集・更新**
   git push時にホームディレクトリ直下に置いたjsonファイルを自動取得して、記載内容のレコードデータ状態へと更新
   actionが成功すればjsonファイルは自動で削除されるが、不具合等で削除されなかった場合は手動で削除をお願いします。
   
## gitでのRoute 53設定更新方法

### 1. 権限の設定

以下のコマンドを実行して、AWSの認証情報を環境変数に設定します。

```bash
export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
export AWS_SESSION_TOKEN="your_session_token"
```

### 2. 復元先のホストゾーンIDを調べる

復元先のホストゾーンIDを確認するために、次のコマンドを実行します。(ホストゾーンが削除、新規作成されない限りIDは変わらない)

```bash
aws route53 list-hosted-zones
```

### 3. ファイル形式の変換(変換前のyaml型式ではデータの編集を行わない事)

修正した`maasapi-com.yml`をyamlからjsonへ型式を変更
[convert_file.py](tool\convert_file.py)を実行し
表示されるメニューに従い変換を行う。(｢ファイルを選択して変換｣⇒ファイル名ボックス横の｢ファイル形式設定｣をyamlへ変更⇒変換ファイルを選択(maasapis.com\maasapi-com.yaml))
出力ファイル名は"conv-***.jsonで出力される

### 4. jsonファイル内のレコードデータを編集

編集の概要
任意の内容でJSON内のレコードデータを編集できます。ただし、更新処理は次のように行われます：

現在のデータを全て削除します。
更新後の状態を新たに上書きします。
このため、以下のような操作が可能です。

更新: レコードの項目は維持したまま、値の内容を修正します。
削除: 削除したいレコードデータ一式を削除し、更新後の希望するレコード状態にします。
注意点
gitのactionsが*maasapis-com.jsonでファイル名を自動取得する為、jsonファイル名は変更しないか記載の名前に適合する様にしてください。
JSONフォーマットが正しいことを確認してください。フォーマットが不正な場合、エラーが発生する可能性があります。
更新後のデータは、必ず適切に確認し、意図した状態になっていることを確認してください。

例
以下は、JSONファイル内のレコードデータを編集する際の例です。
```bash
{
    "ResourceRecordSets": [
        {
            "Name": "example.com",
            "Type": "A",
            "TTL": 300,
            "ResourceRecords": [
                "192.0.2.1"
            ]
        },
        {
            "Name": "www.example.com",
            "Type": "CNAME",
            "TTL": 300,
            "ResourceRecords": [
                "example.com"
            ]
        }
    ]
}
```
この例では、example.comのAレコードを更新したり、www.example.comのCNAMEレコードを削除したりすることができます。



### 5. Route 53の更新
ホストゾーンに設定を反映します。

リポジトリ：csms-dns-managementに対してpushを行います。

git hub actionsの自動処理で更新に必要なデータの追記やawsコマンド処理を行い
DNS設定をroute53へ反映させます。

## 注意事項

- 変更履歴は全てコミットメッセージに記録されますので、変更の内容が明確になるように心がけてください。
- 不明点や問題が発生した場合は、リポジトリのIssuesタブを利用して報告してください。

```

```
## 補足
---

# GitHubとCloud ShellでのGit操作手順

## 1. GitHub パーソナルトークンの作成

### 初回および更新時のみ実施

1. **GitHub アカウントメニュー**
   - 右上のプロフィールアイコンをクリックし、`Settings`を選択します。

2. **Developer settings**
   - 左側のメニューから`Developer settings`を選択します。
   
3. **Personal access tokens**
   - `Personal access tokens` > `Token (classic)`を選択します。

4. **新しいトークンの生成**
   - `Generate new token`をクリックし、`Generate new token (classic)`を選択します。

5. **二段階認証**
   - トークンのスコープを設定します。DNSバックアップ修正の場合は、`repo`を選択すれば十分です。
   - トークンの有効期限を設定します。

6. **トークンコードのメモ**
   - 必ずトークンコードをメモしておいてください。後で必要になります。

## 2. Cloud Shellの事前準備

1. **ユーザー情報の設定**
   ```bash
   git config --global user.name "あなたの名前"
   git config --global user.email "あなたのメールアドレス"
   ```

2. **設定確認**
   ```bash
   git config --global --list
   ```

## 3. リポジトリのクローン

1. **HTTPSリンクの取得**
   - 作成済みのGitリポジトリの`Code`からHTTPSリンクをコピーします。

2. **クローン**
   ```bash
   git clone HTTPSリンク先
   ```
   - ユーザー名: GitHubに登録した名前
   - パスワード: パーソナルアクセストークンを入力します（入力中は表示されませんが、`Ctrl + V`で貼り付け可能です）。

3. **初回のエラー対処**
   - 初回は「remote: To access this repository, visit https://○○」というメッセージが表示される場合があります。その場合、メッセージ内の`https://○○`から`and`までをコピーして別タブで開きます。

4. **再度クローン**
   - 再度以下のコマンドを実行します。
   ```bash
   git clone HTTPSリンク先
   ```

## 4. Gitリポジトリへのプッシュ

1. **リポジトリのクローン**
   ```bash
   git clone https://○○
   ```

2. **リポジトリディレクトリへ移動**
   ```bash
   cd リポジトリ名
   ```

3. **ファイルをコピー**
   ```bash
   cp ~/リポジトリに追加したいファイル ./
   ```

4. **変更をステージ(リポジトリ全体をステージング)**
   ```bash
   git add .
   ```

5. **コミット**
   ```bash
   git commit -m "コミットメッセージ"
   ```

6. **プッシュ**
(初回userとpass入力から15分だけ再入力を行わなくていいおまじない)
   git config --global credential.helper cache
   
   ```bash
   git push origin develop  # または master, main
   ```

## 5. Gitリポジトリからのプル
1.  **リポジトリのディレクトリに移動**

```bash
cd /path/to/your/repo
```

2. **リモートリポジトリを確認**

```bash
git remote -v
```

3. **git pullを実行**

```bash
git pull
```

---