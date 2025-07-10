# DICOM Store SCP for AWS HealthImaging デプロイメントガイド

## このガイドについて

このガイドは、医療機関でDICOM画像を扱う方々が、AWS上でDICOM画像受信システムを構築するための完全なデプロイメント手順書です。AWS初心者の方でも安心してご利用いただけるよう、各ステップを詳しく説明しています。

## DICOM Store SCP for AWS HealthImagingとは

### 製品概要
DICOM Store SCP for AWS HealthImaging（StoreSCP）は、医療機関のDICOM画像を安全にクラウドで管理するためのソリューションです。

**主な機能：**
- **DICOM画像の受信**: CT、MRI、X線などの医療画像を標準的なDICOMプロトコルで受信
- **自動クラウド保存**: 受信した画像をAWS HealthImagingに自動的に長期保存
- **セキュアな通信**: 医療データに適したセキュリティ機能を標準装備
- **スケーラブル**: 病院の規模に応じて自動的にシステム容量を調整

### 対象ユーザー
- 医療機関のIT管理者
- 放射線科システム管理者
- DICOM画像管理システムの導入を検討している方
- クラウド移行を検討している医療機関

## デプロイ前の準備

### 1. AWS環境の準備

#### AWSアカウントの作成
1. [AWS公式サイト](https://aws.amazon.com/jp/)にアクセス
2. 「AWSアカウントを作成」をクリック
3. メールアドレス、パスワード、アカウント名を設定
4. 連絡先情報と支払い情報を入力
5. 電話認証を完了

#### 必要なIAM権限
以下の権限を持つIAMユーザーまたはロールが必要です：
- CloudFormation: フルアクセス
- ECS: フルアクセス
- Lambda: フルアクセス
- S3: フルアクセス
- VPC: 読み取り権限
- IAM: ロール作成権限

**権限設定手順：**
1. AWS Management Console → IAM
2. 「ユーザー」→「ユーザーを追加」
3. 「既存のポリシーを直接アタッチ」を選択
4. 上記権限に対応するポリシーを選択

### 2. ネットワーク環境の理解と準備

#### VPC（Virtual Private Cloud）とは
VPCは、AWS上に作成する仮想的なプライベートネットワークです。病院内のネットワークをクラウド上に再現するイメージです。

#### 必要なネットワーク構成

**パブリックサブネット（2つ以上）**
- 用途: インターネットからアクセス可能な領域
- 配置: Network Load Balancer（外部からの接続受付）
- 要件: 異なるアベイラビリティゾーン（AZ）に配置

**プライベートサブネット（2つ以上）**
- 用途: 外部から直接アクセスできない安全な領域
- 配置: DICOM処理サーバー（実際の画像処理）
- 要件: 異なるアベイラビリティゾーンに配置

**NAT Gateway（必須）**
- 用途: プライベートサブネット内のサーバーがインターネットにアクセスするための中継点
- 必要な理由: DICOM処理サーバーがECR（Elastic Container Registry）からコンテナイメージをダウンロードするため
- 配置: 最低限1つのパブリックサブネットに1つ設置
- 重要性: NAT Gatewayがないとシステムが正常に起動しません

**アベイラビリティゾーン（AZ）とは**
AWSデータセンターの物理的に分離された場所。災害対策のため、異なるAZに分散配置します。

#### ネットワーク設定の確認方法
1. AWS Management Console → VPC
2. 「VPC」メニューで既存VPCのIDを確認
3. 「サブネット」メニューでパブリック/プライベートサブネットのIDを確認
4. 「NAT ゲートウェイ」メニューで最低限1つのパブリックサブネットにNAT Gatewayが設置されていることを確認
5. 「セキュリティグループ」でアクセス制御設定を確認

**NAT Gatewayがない場合の作成方法：**
1. VPCコンソール → 「NAT ゲートウェイ」
2. 「NAT ゲートウェイの作成」をクリック
3. パブリックサブネットを選択し、Elastic IPを割り当て
4. プライベートサブネットのルートテーブルでNAT Gatewayへのルートを追加

### 3. セキュリティ要件の理解

#### セキュリティグループとは
AWS上のファイアウォール機能。VPC内および院内に割り当てられたインターネット上（グローバル）のどのIPアドレスからどのポートへのアクセスを許可するかを制御します。

#### DICOM通信用セキュリティグループの設定

**VPC内からのアクセス設定例：**
```
タイプ: カスタムTCP
ポート: 11112（DICOMの標準ポート）
ソース: 10.0.0.0/16（VPC内のIPアドレス範囲）
説明: VPC内のDICOM SCP接続用
```
*VpcCIDRパラメータを指定することで自動的に設定されます。

**インターネット上からのアクセス設定例：**
```
タイプ: カスタムTCP
ポート: 11112（DICOMの標準ポート）
ソース: 203.0.113.0/24（病院のグローバルIPアドレス範囲）
説明: インターネット経由のDICOM SCP接続用
```
*PeerCIDR1/PeerCIDR2/PeerCIDR3パラメータを指定することで設定されます。

#### TLS証明書（オプション）
**TLS証明書とは**: 通信を暗号化するためのデジタル証明書
**必要な場合**: インターネット経由でDICOM通信を行う場合
**取得方法**: AWS Certificate Manager（ACM）で無料取得可能

## デプロイ手順

### ステップ1: AWS Marketplaceでの購読

1. **AWS Marketplaceにアクセス**
   - AWS Management Consoleにログイン
   - AWS Marketplaceを開く

2. **StoreSCPを検索**
   - 検索バーに「DICOM Store SCP」または「StoreSCP」と入力
   - 該当するプロダクトを選択

3. **購読手続き**
   - 「Continue to Subscribe」をクリック
   - 利用規約を確認し、「Accept Terms」をクリック
   - 購読処理の完了を待つ

### ステップ2: 設定とデプロイ

1. **設定画面への移動**
   - 「Continue to Configuration」をクリック

2. **基本設定**
   - **Region**: デプロイするリージョンを選択
   - **Version**: 最新バージョンを選択
   - 「Continue to Launch」をクリック

3. **起動設定**
   - **Action**: 「Launch CloudFormation」を選択
   - 「Launch」をクリック

### ステップ3: CloudFormationパラメータ設定

#### CloudFormationとは
AWSリソースを自動的に作成・設定するサービス。複雑なシステム構成を一度に構築できます。

#### 必須パラメータの詳細説明

**ネットワーク設定**

| パラメータ | 説明 | 設定例 | 確認方法 |
|-----------|------|--------|----------|
| VpcID | 使用するVPCのID | vpc-xxxxxxxxx | VPCコンソール→「VPC」 |
| PublicSubnetIDs | パブリックサブネットのID（カンマ区切り） | subnet-xxxxxxxx,subnet-yyyyyyyy | VPCコンソール→「サブネット」 |
| PrivateSubnetIDs | プライベートサブネットのID（カンマ区切り） | subnet-aaaaaaaa,subnet-bbbbbbbb | VPCコンソール→「サブネット」 |
| AvailabilityZones | アベイラビリティゾーン（カンマ区切り） | us-east-1a,us-east-1b | サブネット詳細で確認 |
| SecurityGroupID | セキュリティグループのID | sg-xxxxxxxxx | EC2コンソール→「セキュリティグループ」 |
| VpcCIDR | VPCのIPアドレス範囲 | 10.0.0.0/16 | VPC詳細で確認 |

**DICOM設定**

| パラメータ | 説明 | 設定例 | 推奨値 |
|-----------|------|--------|--------|
| SCPAETitle | DICOM機器の識別名 | MYHOSPITAL | 病院名の略称（16文字以内） |
| SCPPort | DICOM通信ポート | 11112 | 標準値のまま |
| PeerCIDR1 | 接続を許可するIPアドレス範囲1 | 203.0.113.0/24 | 病院のグローバルIP範囲 |
| PeerCIDR2 | 接続を許可するIPアドレス範囲2 | "" | 追加のIP範囲（オプション） |
| PeerCIDR3 | 接続を許可するIPアドレス範囲3 | "" | 追加のIP範囲（オプション） |
| RequireCalledAETitle | AE Title検証の有効化 | false | 通常はfalse |
| RequireCallingAETitle | 許可するクライアントAE Title | "" | 特定機器のみ許可する場合に設定 |

**AE Title（Application Entity Title）とは**
DICOM機器を識別するための名前。病院内の各機器（CT、MRI等）が持つ固有の識別子です。

#### オプションパラメータ

**パフォーマンス設定**

| パラメータ | 説明 | デフォルト値 | 推奨値 |
|-----------|------|-------------|--------|
| TaskCPU | ECSタスクのCPUユニット数 | 1024 | 2048 |
| TaskMemoryLimit | ECSタスクのメモリ制限（MiB） | 2048 | 4096 |
| TaskDesiredCount | 希望するECSタスク数 | 1 | 2 |
| AutoscaleMaxCapacity | オートスケーリング最大容量 | 3 | 5 |

**セキュリティ設定**

| パラメータ | 説明 | デフォルト値 | 設定例 |
|-----------|------|-------------|--------|
| TLSCertificateARN | TLS証明書のARN（オプション） | "" | arn:aws:acm:us-east-1:123456789012:certificate/xxxxxxxx |

**DICOM詳細設定**

| パラメータ | 説明 | デフォルト値 | 推奨値 |
|-----------|------|-------------|--------|
| DIMSETimeout | DIMSEタイムアウト（秒） | 60 | 60 |
| MaximumAssociations | 最大同時接続数 | 300 | 300 |
| NetworkTimeout | ネットワークタイムアウト（秒） | 90 | 90 |
| SupportedSOPClassUIDs | サポートするSOP Class UID（カンマ区切り） | "" | 特定のUIDのみ許可する場合に設定 |

### ステップ4: デプロイ実行

1. **パラメータ確認**
   - 全ての必須パラメータが正しく設定されていることを確認

2. **CloudFormationスタック作成**
   - 「Create stack」をクリック
   - スタック作成の進行状況を監視

3. **デプロイ完了確認**
   - スタックステータスが「CREATE_COMPLETE」になることを確認
   - 約10-15分程度で完了

## デプロイ後の設定

### 1. 接続情報の取得

#### CloudFormation Outputsとは
デプロイ完了後に表示される、システムに接続するために必要な情報です。

#### 接続情報取得の詳細手順

**手順1: CloudFormationコンソールにアクセス**
1. AWS Management Consoleにログイン
2. サービス一覧から「CloudFormation」を選択
3. リージョンが正しいことを確認（デプロイしたリージョンと同じ）

**手順2: スタックの確認**
1. スタック一覧で、作成したスタック名を探す
   - スタック名例: "StoreSCP-Stack-20241201"
   - ステータスが「CREATE_COMPLETE」であることを確認
2. スタック名をクリックして詳細画面を開く

**手順3: 接続情報の取得**
1. **「Outputs」タブ**をクリック
2. 以下の重要な情報をメモまたはコピー：

| 項目 | 説明 | 使用目的 |
|------|------|----------|
| NetworkLoadBalancerDNS | 接続先のサーバーアドレス | DICOM機器の接続設定 |
| DICOMPort | 接続ポート番号 | DICOM機器の接続設定 |
| DICOMAETitle | サーバーのAE Title | DICOM機器の接続設定 |

**取得例：**
```
NetworkLoadBalancerDNS: PacsNLB-1234567890.elb.us-east-1.amazonaws.com
DICOMPort: 11112
DICOMAETitle: STORESCP
```

### 2. DICOM機器の接続設定

#### DICOM機器とは
CT、MRI、X線撮影装置、超音波診断装置など、医療画像を生成・送信する機器です。

#### 接続設定の手順

**一般的なDICOM機器での設定項目：**

| 設定項目 | 説明 | 設定値 |
|----------|------|--------|
| Host/Server Address | 接続先サーバーのアドレス | CloudFormation OutputsのNetworkLoadBalancerDNS |
| Port | 接続ポート | CloudFormation OutputsのDICOMPort（通常11112） |
| Called AE Title | 接続先のAE Title | CloudFormation OutputsのDICOMAETitle |
| Calling AE Title | 送信元機器のAE Title | 機器固有の名前（例：CT01、MRI01） |

**設定例：**
```
Host: PacsNLB-1234567890.elb.us-east-1.amazonaws.com
Port: 11112
Called AE Title: STORESCP
Calling AE Title: CT01  # 送信元機器の識別名
```

#### 機器別設定ガイド

**GE製機器の場合：**
1. Service → Network → DICOM Settings
2. 上記パラメータを入力
3. Connection Testで接続確認

**Siemens製機器の場合：**
1. System → Network → DICOM Configuration
2. New Destination を作成
3. 上記パラメータを設定

**Philips製機器の場合：**
1. Setup → System → Network → DICOM
2. Add Destination
3. 接続情報を入力

### 3. 接続テストの実施

#### 接続テストの重要性
実際の医療画像を送信する前に、DICOM接続が正常に動作することを確認します。

#### テスト方法1: DICOM機器からのEchoテスト

**手順：**
1. DICOM機器の管理画面にアクセス
2. Network/DICOM設定画面を開く
3. 「Connection Test」または「Echo Test」を実行
4. 「Success」または「OK」が表示されることを確認

#### テスト方法2: DCMTKツールを使用（技術者向け）

**DCMTKとは**: DICOM通信をテストするための無料ツール

**インストール方法：**
1. [DCMTK公式サイト](https://dicom.offis.de/dcmtk.php.en)からダウンロード
2. インストール後、コマンドラインで実行

**テストコマンド例：**
```bash
# 基本的なEchoテスト
echoscu -aec STORESCP -aet TESTCLIENT PacsNLB-1234567890.elb.us-east-1.amazonaws.com 11112

# 詳細ログ付きテスト
echoscu -v -aec STORESCP -aet TESTCLIENT PacsNLB-1234567890.elb.us-east-1.amazonaws.com 11112
```

**成功時の表示例：**
```
I: Association Request Acknowledged (Max Send PDV: 16372)
I: Echo Response: 0000H (Success)
I: Releasing Association
```

#### テスト方法3: 実際の画像送信テスト

**注意事項：**
- テスト用の匿名化された画像を使用
- 患者情報が含まれる実際の画像は使用しない

**手順：**
1. DICOM機器で小さなテスト画像を選択
2. 送信先を設定したStoreSCPに指定
3. 送信実行
4. AWS HealthImagingで画像が正常に保存されたことを確認

## 監視設定

### 1. CloudWatch ダッシュボード作成

**主要メトリクス**
- ECS CPU使用率
- ECS メモリ使用率
- NLB アクティブ接続数
- Lambda 実行回数・エラー率

### 2. アラーム設定

**推奨アラーム**
```
- ECS CPU使用率 > 80%
- ECS メモリ使用率 > 80%
- Lambda エラー率 > 5%
- HealthImaging インポートエラー
```

## セキュリティ設定

### 1. セキュリティグループ設定

**インバウンドルール例**
```
# VPC内アクセス用
Type: Custom TCP
Port: 11112
Source: 10.0.0.0/16 (VPC CIDR)
Description: VPC internal DICOM SCP access

# インターネットアクセス用
Type: Custom TCP
Port: 11112
Source: 203.0.113.0/24 (病院のグローバルIP CIDR)
Description: Internet DICOM SCP access
```

### 2. TLS設定（オプション）

**ACM証明書の準備**
1. AWS Certificate Managerで証明書を作成
2. ドメイン検証を完了
3. 証明書ARNをパラメータに設定

## トラブルシューティング

### デプロイ時のエラー対処

#### 1. VPC関連エラー

**エラーメッセージ例：**
```
Invalid subnet ID: subnet-xxxxxxxxx does not exist
Subnet subnet-xxxxxxxxx is not in the same VPC as subnet-yyyyyyyyy
```

**原因と対処法：**
- **原因**: 存在しないサブネットIDを指定、または異なるVPCのサブネットを混在
- **確認方法**: 
  1. VPCコンソール → サブネット
  2. 指定したサブネットIDが存在するか確認
  3. 全てのサブネットが同じVPCに属しているか確認
- **対処法**: 正しいサブネットIDを再入力

#### 2. 権限エラー

**エラーメッセージ例：**
```
User: arn:aws:iam::123456789012:user/username is not authorized to perform: cloudformation:CreateStack
Access Denied when calling the CreateRole operation
```

**原因と対処法：**
- **原因**: 必要なIAM権限が不足
- **確認方法**:
  1. IAMコンソール → ユーザー → 該当ユーザー
  2. 「アクセス許可」タブで権限を確認
- **対処法**: 管理者に以下の権限追加を依頼
  - CloudFormationFullAccess
  - ECSFullAccess
  - LambdaFullAccess
  - IAMFullAccess（ロール作成用）

#### 3. リソース制限エラー

**エラーメッセージ例：**
```
The maximum number of VPCs has been reached
Service limit exceeded for resource type 'AWS::ECS::Service'
```

**原因と対処法：**
- **原因**: AWSアカウントのリソース上限に達している
- **確認方法**: Service Quotasコンソールで現在の使用量を確認
- **対処法**: 
  1. 不要なリソースを削除
  2. AWSサポートに上限緩和を申請

### 接続エラーの対処

#### 1. DICOM接続タイムアウト

**症状**: DICOM機器からの接続が「Timeout」エラーで失敗

**確認手順：**

**ステップ1: ネットワーク疎通確認**
DICOM Echoテストまたは直接ECSサービス状態を確認してネットワーク接続を検証します。

**ステップ2: セキュリティグループ確認**
1. EC2コンソール → セキュリティグループ
2. 使用しているセキュリティグループを選択
3. 「インバウンドルール」タブを確認
4. ポート11112が病院のIPアドレスから許可されているか確認

**ステップ3: NLBの状態確認**
1. EC2コンソール → ロードバランサー
2. 該当のNetwork Load Balancerを選択
3. 「ターゲット」タブでヘルスチェック状態を確認
4. 全てのターゲットが「healthy」であることを確認

#### 2. AE Title不一致エラー

**症状**: 接続は成功するが、画像送信時に「Association Rejected」エラー

**原因**: DICOM機器とStoreSCPのAE Title設定が一致していない

**確認方法:**
1. CloudFormation Outputs でDICOMAETitleを確認
2. DICOM機器の「Called AE Title」設定と比較
3. 大文字小文字、スペースも含めて完全一致させる

#### 3. システム負荷エラー

**症状**: 大量の画像送信時にエラーが発生

**確認方法:**
1. CloudWatchコンソール → メトリクス
2. ECS → CPU使用率、メモリ使用率を確認
3. 80%を超えている場合は負荷過多

**対処法:**
1. CloudFormationスタックを更新
2. TaskDesiredCount（サーバー数）を増加
3. AutoscaleMaxCapacity（最大サーバー数）を増加

### 接続エラー

**DICOM接続できない場合**

1. **セキュリティグループ確認**
   - クライアントIPアドレスからのトラフィックを許可しているか確認
   - ポート11112のインバウンドルールをチェック

2. **ECSサービス状態確認**
   - ECS コンソールでサービスが正常に動作しているか確認
   - タスクが「RUNNING」状態か確認

3. **ログ確認**
   ```
   CloudWatch Logs > StackName-PacsServerTaskDefPacsContainerLogGroup*
   ```
   
   *StackNameは作成時に指定したCloudFormationスタック名

## スケーリング設定

### 自動スケーリング

**CPU使用率ベース（ターゲット追跡）**
```
ターゲット値: CPU使用率 50%
最小容量: 1
最大容量: AutoscaleMaxCapacity パラメータで指定（デフォルト3、推奨5）
スケールイン/アウトクールダウン: 60秒
```

**確認方法**
```
AWS Management Console → ECS → クラスター → [クラスター名] → サービス → [サービス名] → Auto Scaling タブ
```

## データ保護機能

### 実装済みの保護機能

**S3バケット**
- 保存時暗号化（S3マネージド暗号化）
- SSL/TLS通信の強制
- パブリックアクセスのブロック

**DynamoDB**
- ポイントインタイムリカバリ有効化
- 保存時暗号化

**AWS HealthImaging**
- AWSマネージドサービスによる自動バックアップ
- 高可用性アーキテクチャ

## 運用・保守ガイド

### 日常的な監視項目

#### 1. システム稼働状況の確認（毎日）

**確認場所**: CloudWatchダッシュボード

**チェック項目:**
- **ECS CPU使用率**: 80%以下が正常
- **ECS メモリ使用率**: 80%以下が正常  
- **NLB アクティブ接続数**: 異常な増減がないか
- **Lambda エラー率**: 5%以下が正常

**異常時の対応:**
- CPU/メモリ使用率が高い → スケーリング設定の見直し
- 接続数の異常 → セキュリティインシデントの可能性を調査
- Lambda エラー → CloudWatch Logsでエラー詳細を確認

#### 2. DICOM画像処理状況の確認（毎日）

**確認場所**: AWS HealthImagingコンソール

**チェック項目:**
- 新しい画像が正常にインポートされているか
- インポートエラーが発生していないか
- ストレージ使用量の増加傾向

#### 3. セキュリティ状況の確認（週次）

**確認場所**: CloudTrailログ（別途設定が必要）

**チェック項目:**
- 不審なアクセスログがないか
- 設定変更の履歴
- 失敗したログイン試行

### 定期メンテナンス

#### 月次メンテナンス

**1. ログの確認と整理**
- CloudWatch Logsで過去1ヶ月のエラーログを確認
- 不要な古いログの削除（コスト削減）
- エラーパターンの分析と対策検討

**2. パフォーマンス分析**
- 月間の画像処理量統計作成
- ピーク時間帯の特定
- 必要に応じてスケーリング設定調整

**3. コスト分析**
- AWS Cost Explorerで月間コスト確認
- 予算超過の有無確認
- コスト最適化の機会検討

#### 四半期メンテナンス

**1. セキュリティ設定見直し**
- セキュリティグループルールの監査
- 不要なアクセス許可の削除
- パスワードポリシーの確認

**2. データ保護状況確認**
- S3バケットの暗号化設定確認
- DynamoDBポイントインタイムリカバリ状況確認
- AWS HealthImagingデータストア状態確認

#### 年次メンテナンス

**1. データ復旧テスト**
- DynamoDBポイントインタイムリカバリのテスト
- データ整合性の確認
- 復旧手順書の更新

**2. システム全体の見直し**
- 新しいAWSサービスの活用検討
- アーキテクチャの最適化検討
- 利用者からのフィードバック収集と改善

### 緊急時対応手順

#### システム停止時の対応

**1. 初期対応（5分以内）**
- CloudFormationスタック状態確認
- ECSサービス状態確認
- Network Load Balancer状態確認

**2. 詳細調査（15分以内）**
- CloudWatch Logsでエラー詳細確認
- AWS Health Dashboardでサービス障害情報確認
- 関係者への状況報告

**3. 復旧作業**
- 必要に応じてECSサービス再起動
- CloudFormationスタック更新
- 復旧後の動作確認

#### セキュリティインシデント時の対応

**1. 即座の対応**
- 不審なアクセス元IPのブロック
- セキュリティグループルールの一時的制限
- 関係者への緊急連絡

**2. 調査と対策**
- CloudTrailログの詳細分析（設定済みの場合）
- 影響範囲の特定
- 必要に応じて外部セキュリティ専門家への相談

### サポート体制

#### AWSサポートの活用
- **Basic**: 無料、ドキュメントとフォーラム
- **Developer**: 月額29USD、技術サポート（営業時間）
- **Business**: 月額100USD、24時間サポート（推奨）

#### 緊急連絡先の整備
- AWS技術サポート連絡先
- 社内IT管理者連絡先
- DICOM機器ベンダー連絡先
- 外部システムインテグレーター連絡先

## よくある質問（FAQ）

### Q1: デプロイにはどのくらいの時間がかかりますか？
**A**: 通常10-15分程度です。初回の場合、AWSリソースの作成に時間がかかることがあります。

### Q2: 月額コストはどのくらいですか？
**A**: 使用量により変動しますが、小規模病院（月間1,000画像程度）で月額200-500USD程度が目安です。詳細は[AWS料金計算ツール](https://calculator.aws)をご利用ください。

### Q3: 既存のPACSシステムと併用できますか？
**A**: はい。StoreSCPは既存システムと並行して動作可能です。段階的な移行も可能です。

### Q4: 患者データのプライバシーは保護されますか？
**A**: はい。AWS HealthImagingはHIPAA準拠で、医療データに適したセキュリティ機能を提供します。

### Q5: 障害時のデータ復旧は可能ですか？
**A**: はい。DynamoDBのポイントインタイムリカバリとAWS HealthImagingの高可用性機能により、データの復旧が可能です。

### Q6: 他のDICOMビューアーで画像を閲覧できますか？
**A**: はい。AWS HealthImaging APIを通じて、標準的なDICOMビューアーで閲覧可能です。

## 追加リソース

### 公式ドキュメント
- [AWS HealthImaging ユーザーガイド](https://docs.aws.amazon.com/healthimaging/)
- [DICOM標準仕様](https://www.dicomstandard.org/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### トレーニングリソース
- [AWS Training and Certification](https://aws.amazon.com/training/)
- [AWS HealthImaging ワークショップ](https://catalog.workshops.aws/)

### コミュニティサポート
- [AWS re:Post](https://repost.aws/) - AWS技術コミュニティ
- [AWS HealthImaging フォーラム](https://forums.aws.amazon.com/)

---

**このガイドについて**

このガイドは、医療機関でのDICOM画像管理システム導入を支援するために作成されました。技術的な質問や導入支援が必要な場合は、AWSパートナーネットワークの認定パートナーにご相談いただくことをお勧めします。

**免責事項**: このソリューションは医療機器ではありません。医療診断や治療の決定には使用しないでください。
