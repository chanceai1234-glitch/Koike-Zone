# Koike-Zone

占いの科学的検証プロジェクト - Claude Agent SDK によるエージェントチーム

## ミッション

世界中の占い手法を調査し、科学的根拠に基づいて分析。占いとの正しい付き合い方を啓発するコンテンツを制作し、さらに占いを実際に体験できるサイト/アプリを企画する。

**占いそのものに意味があるのではなく、それを受け取る側の考え方次第だと気づいてもらう。**

## エージェントチーム構成

```
[PM: プロジェクトマネージャー]
    │
    ├── Phase 1: Researcher（リサーチャー）
    │   世界中の占い手法を網羅的に調査
    │
    ├── Phase 2: Scientist（科学分析官）
    │   科学的根拠・心理学的メカニズムの分析
    │
    ├── Phase 3: Writer（啓発ライター）
    │   一般読者向けの啓発記事を執筆
    │
    ├── Phase 4: Fact Checker（ファクトチェッカー）
    │   科学的正確性・公平性の最終検証
    │
    └── Phase 5: UX Planner（UX企画）
        占い体験サイト/アプリの企画設計
```

| エージェント | 役割 | モデル |
|-------------|------|--------|
| **Researcher** | 世界の占い手法の網羅的調査（歴史・手法・文化背景） | Opus |
| **Scientist** | 科学的検証・心理学的メカニズム分析（論文・実験・統計） | Opus |
| **Writer** | 科学的分析を元にした啓発記事の執筆 | Opus |
| **Fact Checker** | 科学的正確性・公平性・バランスの最終チェック | Sonnet |
| **UX Planner** | 占い体験 → 科学的解説 → 気づきの体験設計 | Opus |

## セットアップ

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY="your-api-key"
```

## 使い方

### 全フェーズ一括実行

```bash
python -m content_team.main
```

### 個別フェーズの実行

```bash
# Phase 1: 世界の占い手法リサーチ
python -m content_team.main --phase research

# Phase 2: 科学的分析
python -m content_team.main --phase analyze

# Phase 3: 啓発記事の執筆
python -m content_team.main --phase write

# Phase 4: ファクトチェック
python -m content_team.main --phase factcheck

# Phase 5: 占い体験アプリ企画
python -m content_team.main --phase plan_app
```

### オプション

```bash
# 出力先を指定
python -m content_team.main --output ./results

# 予算上限を設定（USD）
python -m content_team.main --budget 8.0
```

## 出力ファイル

| ファイル | 内容 |
|---------|------|
| `output/01_research.md` | 世界の占い手法カタログ |
| `output/02_scientific_analysis.md` | 科学的分析レポート |
| `output/03_article.md` | 啓発記事（ドラフト） |
| `output/04_final_article.md` | ファクトチェック済み最終記事 |
| `output/05_app_plan.md` | 占い体験アプリ企画書 |

## 分析対象の占い手法

### 東アジア
おみくじ、手相、四柱推命、九星気学、姓名判断、血液型占い、六曜、易経、風水、紫微斗数

### 南アジア
ジョーティッシュ（ヴェーダ占星術）、ナーディ占星術

### ヨーロッパ
西洋占星術（ホロスコープ）、タロット、ルーン、数秘術、水晶球

### 中東・アフリカ
砂占い（ジオマンシー）、イファ占い、骨投げ占い

### アメリカ大陸
マヤ暦、ネイティブアメリカンのビジョンクエスト

### その他
ダウジング、オーラリーディング、ペンデュラム

## 科学的分析の観点

- **バーナム効果**: 曖昧な記述を自分だけに当てはまると感じる
- **確証バイアス**: 当たった記憶だけ残る
- **自己成就予言**: 占いを信じて行動が変わる
- **コールドリーディング**: 占い師の読み取り技術
- **プラシーボ効果**: 信じること自体の心理的効果
- **カウンセリング効果**: 話を聞いてもらえる安心感

## プロジェクト構成

```
content_team/
├── __init__.py    # パッケージ初期化
├── agents.py      # 5エージェントの定義
├── team.py        # チームオーケストレーター
└── main.py        # CLIエントリポイント
```

## 方針

- 占いを信じる人を攻撃しない
- 科学的事実に基づいたバランスの取れた分析
- 心理的効果（カウンセリング効果など）は正当に評価する
- 本当に科学的根拠がある効果があれば、それも報告する
- 読者自身が「なるほど」と気づける構成を重視
