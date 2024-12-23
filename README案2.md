# Route53 DNS Management

このリポジトリは、AWS Route53のDNS設定を管理するためのツールです。不要なレコードや不明なレコードを残さないようにし、DNSデータを簡単に更新することができます。

## 概要

- Route53のDNS設定を管理
- 不要なレコード、不明レコードの削除
- GitHub Actionsを使用してDNSデータを自動更新
- DNSデータはリポジトリ内の `.\maasapis.com\maasapis-com.yaml` に保存

## 使用方法

### DNSデータの更新

1. **YAMLファイルの編集**  
   リポジトリ内の `.\maasapis.com\maasapis-com.yaml` ファイルを開き、必要なレコードを追加、更新します。

2. **YAMLからJSONへの変換**  
   YAMLファイルをJSON形式に変換します。この際、全てのレコードを含むJSONファイルを生成する必要があります。()

3. **更新ファイルの配置**  
   更新したJSONファイルを `DELETE-maasapis-com.json` という名前で、リポジトリのホーム直下のディレクトリに置きます。このファイルには、更新しないデータも含めた全レコードが必要です。

4. **変更のコミットとプッシュ**  
   変更をコミットし、リポジトリにプッシュします。GitHub Actionsがトリガーされ、Route53のDNS設定が更新されます。

### レコードの削除

1. **削除するレコードの記載**  
   削除したいレコードのみを記載したJSONファイルを作成します。このファイルも `DELETE-maasapis-com.json` という名前で、リポジトリのホーム直下のディレクトリに置きます。

2. **変更のコミットとプッシュ**  
   削除ファイルをリポジトリにプッシュします。これにより、記載されたレコードのみがRoute53から削除されます。

## 注意事項

- DNSデータの変更は慎重に行ってください。誤った設定は、ドメインの可用性に影響を与える可能性があります。
- GitHub Actionsを使用するため、リポジトリの設定でActionsが有効になっていることを確認してください。

## ライセンス

このリポジトリはMITライセンスのもとで公開されています。詳細はLICENSEファイルを参照してください。
