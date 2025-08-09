# DICOM Store SCP for AWS HealthImaging - AWS Marketplace プロダクトドキュメント

## 製品概要

### DICOM Store SCP for AWS HealthImagingとは

DICOM Store SCP for AWS HealthImaging（StoreSCP）は、医療機関が持つCT、MRI、X線などの医療機器から送信されるDICOM画像を、安全かつ効率的にAWSクラウドで管理するためのソリューションです。

### こんな課題を解決します

**既存のPACSシステムの課題:**
- 高額なハードウェア購入と保守費用
- システムの老化と更新コスト
- データ保護と災害対策の負担
- ストレージ容量の制限と拡張コスト
- IT人材不足と運用負担

**StoreSCPが提供する解決策:**
- 初期投資を大幅に削減（ハードウェア不要）
- 使用量に応じた従量課金でコスト最適化
- AWSの高信頼性インフラでデータ保護
- 無制限のストレージ容量と自動スケーリング
- マネージドサービスで運用負担を軽減

### 対象となる医療機関

- **中小規模病院**: 初期投資を抑えてPACSを導入したい
- **大規模病院**: 既存システムのクラウド移行を検討中
- **放射線科クリニック**: コスト効率の高い画像管理を希望
- **遠隔医療提供者**: クラウドベースの柔軟なアクセスが必要
- **医療ITベンダー**: 顧客にクラウドPACSソリューションを提供したい

## 主要機能

### 🏥 DICOM対応
- DICOM SCP（Service Class Provider）サーバー
- 標準的なDICOM通信プロトコルをサポート
- カスタマイズ可能なAE Title設定

### ☁️ AWS HealthImaging統合
- AWS HealthImagingデータストアとの完全統合
- 自動的なDICOMインポート処理
- 高可用性とスケーラビリティ

### 🔧 完全自動化
- Step Functionsによるワークフロー自動化
- Lambda関数による処理の最適化
- DynamoDBによるメタデータ管理

### 🛡️ セキュリティ
- VPC内での安全な通信
- TLS暗号化対応
- きめ細かいアクセス制御

## アーキテクチャ

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   DICOM Client  │───▶│  Network Load    │───▶│   ECS Fargate   │
│                 │    │   Balancer       │    │   PACS Server   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  AWS Health     │◀───│  Step Functions  │◀───│   S3 Bucket     │
│  Imaging        │    │   Workflow       │    │   (DICOM)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       
         ▼                       ▼                       
┌─────────────────┐    ┌──────────────────┐              
│   S3 Bucket     │    │    DynamoDB      │              
│  (Results)      │    │   (Metadata)     │              
└─────────────────┘    └──────────────────┘              
```

## デプロイメント要件

### 前提条件
- AWS アカウント
- 適切なIAM権限
- VPC（既存または新規作成）
- NAT Gateway（プライベートサブネットからECRアクセス用）

### サポートされるリージョン
AWS HealthImagingがサポートしているリージョン:
- us-east-1 (バージニア北部)
- us-west-2 (オレゴン)
- eu-west-1 (アイルランド)
- ap-southeast-2 (シドニー)

## パラメータ設定

### ネットワーク設定
| パラメータ | 説明 | デフォルト値 |
|-----------|------|-------------|
| VpcID | 使用するVPCのID | - |
| PublicSubnetIDs | パブリックサブネットのID（カンマ区切り） | - |
| PrivateSubnetIDs | プライベートサブネットのID（カンマ区切り） | - |
| SecurityGroupID | ECSサービス用セキュリティグループID | - |
| VpcCIDR | VPCのCIDRブロック | - |

### DICOM設定
| パラメータ | 説明 | デフォルト値 |
|-----------|------|-------------|
| SCPAETitle | DICOM SCPのAE Title | STORESCP |
| SCPPort | DICOM通信ポート | 11112 |
| PeerCIDR1-3 | 許可するクライアントのCIDR | - |
| DIMSETimeout | DIMSE操作のタイムアウト（秒） | 60 |
| MaximumAssociations | 最大同時接続数 | 300 |

### スケーリング設定
| パラメータ | 説明 | デフォルト値 |
|-----------|------|-------------|
| TaskCPU | ECSタスクCPUユニット | 1024 |
| TaskMemoryLimit | ECSタスクメモリ制限 | 2048 |
| TaskDesiredCount | 希望するECSタスク数 | 1 |
| AutoscaleMaxCapacity | オートスケーリング最大容量 | 3 |

### セキュリティ設定
| パラメータ | 説明 | デフォルト値 |
|-----------|------|-------------|
| TLSCertificateARN | TLS証明書のARN（オプション） | - |

## デプロイ手順

### 1. AWS Marketplaceからの起動
1. AWS Marketplaceで「DICOM Store SCP」または「StoreSCP」を検索
2. 「Continue to Subscribe」をクリック
3. 「Continue to Configuration」をクリック
4. リージョンを選択し、「Continue to Launch」をクリック

### 2. パラメータ設定
1. 必須パラメータを入力：
   - VPC ID
   - サブネットID
   - セキュリティグループID
   - 許可するクライアントのCIDR
2. オプションパラメータを調整
3. 「Launch」をクリック

### 3. デプロイ完了の確認
- CloudFormationスタックの作成完了を確認
- ECSサービスが正常に起動していることを確認
- Network Load BalancerのDNS名を取得

## 使用方法

### DICOM接続設定

CloudFormation Outputsタブから取得した情報を使用：
```
ホスト: [NetworkLoadBalancerDNSの値]
ポート: [DICOMPortの値]
AE Title: [DICOMAETitleの値]
```

### 画像送信
1. DICOMクライアントから上記設定で接続
2. C-STORE操作でDICOM画像を送信
3. 自動的にAWS HealthImagingにインポート開始

### 処理状況確認
- DynamoDBテーブルでインポート状況を確認
- CloudWatch Logsでデバッグ情報を確認

## 監視とログ

### CloudWatch メトリクス
- ECS CPU/メモリ使用率
- Network Load Balancer接続数
- Lambda関数実行回数・エラー率
- Step Functions実行状況

### ログ出力先
- ECS Fargate: `[stack-name]-PacsServerTaskDefPacsContainerLogGroup*`
- Lambda Functions: `/aws/lambda/[function-name]`

## トラブルシューティング

### よくある問題

#### 1. DICOM接続エラー
**症状**: クライアントから接続できない
**解決策**:
- セキュリティグループの設定を確認
- PeerCIDRの設定を確認
- Network Load Balancerの状態を確認

#### 2. インポート処理の失敗
**症状**: DICOM画像がHealthImagingに取り込まれない
**解決策**:
- CloudWatch LogsでLambda関数のエラーを確認
- DynamoDBテーブルでジョブ状態を確認
- S3バケットの権限設定を確認

#### 3. パフォーマンス問題
**症状**: 処理が遅い
**解決策**:
- ECSタスクのCPU/メモリ設定を増加
- オートスケーリング設定を調整
- 同時接続数の制限を確認

## サポート

### ドキュメント
- [AWS HealthImaging ドキュメント](https://docs.aws.amazon.com/healthimaging/)
- [DICOM標準仕様](https://www.dicomstandard.org/)

### 技術サポート
AWS Marketplaceを通じてサポートリクエストを送信してください。

## 料金

### AWS サービス料金
- ECS Fargate: 実行時間に基づく課金
- AWS HealthImaging: ストレージとAPI使用量に基づく課金
- Lambda: 実行回数と実行時間に基づく課金
- その他のAWSサービス: 標準料金

詳細な料金見積もりは[AWS料金計算ツール](https://calculator.aws)をご利用ください。

## セキュリティ考慮事項

### データ保護
- 保存時暗号化（S3、DynamoDB）
- 転送時暗号化（TLS対応）
- VPC内での通信分離

### アクセス制御
- IAMロールベースのアクセス制御
- セキュリティグループによるネットワーク制御

### コンプライアンス
- HIPAA対応可能な設計
- AWS責任共有モデルに基づくセキュリティ

## バージョン履歴

### v1.0.0
- 初回リリース
- 基本的なDICOM SCP機能
- AWS HealthImaging統合
- 自動インポートワークフロー

---

**注意**: このソリューションは医療機器ではありません。医療診断や治療の決定には使用しないでください。
