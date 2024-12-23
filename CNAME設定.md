以下に、`hikaru-test.maasapis.com`のホストゾーン内に設定するDNSレコードの一覧を、ホストゾーンの区分けを明確にして見やすく表示します。

### ホストゾーン設定一覧

---

#### ホストゾーン: `hikaru-test.maasapis.com`

| ドメイン名                       | レコードタイプ | 値                           | 説明                                                                 |
|----------------------------------|----------------|------------------------------|----------------------------------------------------------------------|
| `hikaru-test.maasapis.com`       | A              | `192.0.2.5`                 | `hikaru-test.maasapis.com`へのリクエストはこのIPアドレスに解決される。 |
| `sub.hikaru-test.maasapis.com`   | CNAME          | `link.hikaru-test.maasapis.com` | `sub.hikaru-test.maasapis.com`は`link.hikaru-test.maasapis.com`にリダイレクトされる。 |

---

#### ホストゾーン: `link.hikaru-test.maasapis.com`（必要に応じて）

| ドメイン名                       | レコードタイプ | 値                           | 説明                                                                 |
|----------------------------------|----------------|------------------------------|----------------------------------------------------------------------|
| `link.hikaru-test.maasapis.com`  | A              | `192.0.2.5`                 | `link.hikaru-test.maasapis.com`へのリクエストはこのIPアドレスに解決される。 |

---

### 動作の流れ
1. ユーザーが`sub.hikaru-test.maasapis.com`にアクセス。
2. DNSはCNAMEレコードを見つけ、リクエストを`link.hikaru-test.maasapis.com`にリダイレクト。
3. `link.hikaru-test.maasapis.com`がAレコードとして存在し、`192.0.2.5`に解決される。
4. 最終的に、ユーザーは`192.0.2.5`に接続され、目的のリソースにアクセスできる。

### まとめ
- `hikaru-test.maasapis.com`のホストゾーン内に`sub.hikaru-test.maasapis.com`のCNAMEレコードを設定することで、`link.hikaru-test.maasapis.com`の名前解決が行われます。これにより、`sub.hikaru-test.maasapis.com`を介して`link.hikaru-test.maasapis.com`にアクセスできるようになります。