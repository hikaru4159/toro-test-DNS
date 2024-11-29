
ロール作成⇒ウェブサービス⇒作成したIDプロバイダの設定を使う　
ロール名: hikaru_OIDC_test 
ARN: arn:aws:iam::157094121738:role/hikaru_OIDC_test
エンティティ
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::157094121738:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:hikaru4159/*"
                }
            }
        }
    ]
}
___ 
1. OIDCプロバイダーの作成
まず、AWSにGitHubのOIDCプロバイダーを作成します。

AWS Management Consoleにログインします。
IAMサービスに移動します。
左側のメニューから「アイデンティティプロバイダー」を選択し、「プロバイダーを追加」をクリックします。
「プロバイダータイプ」として「OpenID Connect」を選択します。
プロバイダーのURLとして次のURLを使用します（GitHubのOIDCエンドポイント）:
https://token.actions.githubusercontent.com
「プロバイダー名」を設定し、作成します。
2. IAMロールの作成
OIDCプロバイダーを使用してAWSリソースにアクセスするためのIAMロールを作成します。

IAMの「ロール」を選択し、「ロールを作成」をクリックします。
「信頼関係の設定」で「外部IDを使用する」を選択します。
「信頼されたエンティティのタイプ」として「Web サービス」を選択します。
「信頼されたエンティティの詳細」で、以下のように設定します。
プロバイダー: 先ほど作成したOIDCプロバイダーを選択。
条件: GitHub Actionsからのアクセスを制御する条件を設定します。例えば、特定のリポジトリからのアクセスを許可する場合は、以下のように設定します。
{
  "StringEquals": {
    "token.actions.githubusercontent.com:sub": "repo:<GITHUB_USERNAME>/<REPO_NAME>:ref:refs/heads/<BRANCH_NAME>"
  }
}
ここで <GITHUB_USERNAME>、<REPO_NAME>、<BRANCH_NAME> はそれぞれGitHubのユーザー名、リポジトリ名、ブランチ名に置き換えてください。

必要なアクセス権限を持つポリシーをアタッチします。例えば、S3バケットへのアクセスを許可する場合は、以下のようなポリシーを作成し、アタッチします。
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    }
  ]
}