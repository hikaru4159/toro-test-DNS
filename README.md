ACM検証完了後にCNAMEを削除しても、ステータスが失敗にならない(５ｈ程度待っても同様)、定期検証の時間が設定あるかも？
ACM検証完了⇒CNAME削除⇒ACM設定を一度削除⇒ACM同ドメインで再設定(検証待ち状態)⇒awscliでCNAMEを再復元⇒ACMは検証完了となる
ACM自動更新時に引き継がれるかは不明だが、少なくともこの結果からCNAME設定のみでDNSの検証を行っているものと思われる。
