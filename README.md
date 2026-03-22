# Koike-Zone

コンテンツ制作エージェントチーム - Claude Agent SDK を使った記事制作の自動化

## 概要

4つの専門エージェントがチームとして連携し、テーマを入力するだけで高品質な記事を自動生成します。

```
テーマ入力 → 企画 → 執筆 → 編集 → 校正 → 完成記事
              │       │       │       │
           Planner  Writer  Editor  Proofreader
```

## エージェント構成

| エージェント | 役割 | 担当 |
|-------------|------|------|
| **Planner** (企画) | テーマ分析・ターゲット設定・構成案作成 | Sonnet |
| **Writer** (ライター) | 記事本文の執筆 | Opus |
| **Editor** (編集者) | 論理構成・読みやすさ・正確性チェック | Sonnet |
| **Proofreader** (校正者) | 誤字脱字・文法・表記ゆれチェック | Sonnet |

## セットアップ

```bash
# 依存関係のインストール
pip install claude-agent-sdk

# APIキーの設定
export ANTHROPIC_API_KEY="your-api-key"
```

## 使い方

### チーム全体で記事制作

```bash
# 基本
python -m content_team.main "AIエージェントの未来"

# 出力先を指定
python -m content_team.main "Python入門ガイド" --output ./articles

# 予算上限を設定
python -m content_team.main "Rustの魅力" --budget 3.0
```

### 個別エージェントの実行

```bash
# 企画だけ
python -m content_team.main --step planner "AIエージェントの未来"

# 執筆だけ
python -m content_team.main --step writer "企画の内容..."

# 編集だけ
python -m content_team.main --step editor "記事の内容..."

# 校正だけ
python -m content_team.main --step proofreader "記事の内容..."
```

### Pythonから直接利用

```python
import asyncio
from content_team.team import run_content_team

result = asyncio.run(run_content_team(
    topic="AIエージェントの未来",
    output_dir="./output",
    max_budget_usd=5.0,
))
print(f"記事が保存されました: {result}")
```

## プロジェクト構成

```
content_team/
├── __init__.py    # パッケージ初期化
├── agents.py      # エージェント定義（4エージェント）
├── team.py        # チームオーケストレーター
└── main.py        # CLIエントリポイント
```

## 制作フロー詳細

1. **企画 (Planner)**: テーマを受け取り、ターゲット読者・構成案・キーワードを提案
2. **執筆 (Writer)**: 企画をもとにMarkdown形式で記事本文を執筆
3. **編集 (Editor)**: 論理構成・読みやすさ・情報の一貫性をチェックし改善
4. **校正 (Proofreader)**: 誤字脱字・文法・表記ゆれを修正し最終版を出力

## 技術スタック

- **Claude Agent SDK** - エージェント制御
- **Claude Opus** - 高品質な文章生成（ライター）
- **Claude Sonnet** - 高速な分析・チェック（企画・編集・校正）
