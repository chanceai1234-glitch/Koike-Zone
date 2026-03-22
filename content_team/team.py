"""チームオーケストレーター - エージェントチーム全体の制御"""

import asyncio
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, AssistantMessage, ResultMessage, query

from .agents import get_all_agents


async def run_content_team(
    topic: str,
    output_dir: str = "./output",
    max_budget_usd: float = 5.0,
) -> str:
    """コンテンツ制作チームを実行する

    Args:
        topic: 記事のテーマ・トピック
        output_dir: 出力先ディレクトリ
        max_budget_usd: 最大予算（USD）

    Returns:
        完成した記事のファイルパス
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    team_prompt = f"""あなたはコンテンツ制作チームのプロジェクトマネージャーです。
以下のテーマで高品質な記事を制作してください。

## テーマ
{topic}

## 制作フロー
以下の順番でエージェントチームに作業を指示してください：

### Step 1: 企画（planner エージェント）
plannerエージェントを使って、テーマの分析・ターゲット読者の設定・記事構成案を作成してください。

### Step 2: 執筆（writer エージェント）
Step 1の企画結果を元に、writerエージェントを使って記事本文を執筆してください。
企画の内容を明確にwriterに伝えてください。

### Step 3: 編集（editor エージェント）
Step 2の記事をeditorエージェントに渡して、論理構成・読みやすさ・情報の正確性をチェックし、改善してください。

### Step 4: 校正（proofreader エージェント）
Step 3の編集済み記事をproofreaderエージェントに渡して、最終的な品質チェックを行ってください。

## 最終出力
校正が完了したら、最終版の記事を `{output_path}/article.md` に保存してください。
Writeツールを使ってファイルに書き出してください。

各ステップの結果を簡潔に報告しながら進めてください。
"""

    agents = get_all_agents()
    result_text = ""
    total_cost = 0.0

    print(f"\n{'='*60}")
    print(f"  コンテンツ制作チーム 起動")
    print(f"  テーマ: {topic}")
    print(f"{'='*60}\n")

    async for message in query(
        prompt=team_prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Grep", "Glob", "Agent"],
            agents=agents,
            max_turns=50,
            max_budget_usd=max_budget_usd,
            effort="high",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text") and block.text:
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"\n  [ツール実行] {block.name}")

        elif isinstance(message, ResultMessage):
            if message.subtype == "success":
                result_text = getattr(message, "result", "")
                total_cost = getattr(message, "total_cost_usd", 0.0)
                num_turns = getattr(message, "num_turns", 0)

                print(f"\n{'='*60}")
                print(f"  制作完了!")
                print(f"  ターン数: {num_turns}")
                print(f"  コスト: ${total_cost:.4f}")
                print(f"  出力先: {output_path}/article.md")
                print(f"{'='*60}\n")
            else:
                print(f"\n[エラー] {message.subtype}")

    return str(output_path / "article.md")


async def run_single_step(
    step: str,
    content: str,
    max_budget_usd: float = 2.0,
) -> str:
    """チームの個別ステップを単体実行する（デバッグ用）

    Args:
        step: "planner", "writer", "editor", "proofreader"
        content: 入力テキスト
        max_budget_usd: 最大予算

    Returns:
        エージェントの出力テキスト
    """
    agents = get_all_agents()

    if step not in agents:
        raise ValueError(f"不明なステップ: {step} (選択肢: {list(agents.keys())})")

    prompt = f"{step}エージェントを使って以下の内容を処理してください:\n\n{content}"
    result = ""

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Grep", "Glob", "Agent"],
            agents={step: agents[step]},
            max_turns=20,
            max_budget_usd=max_budget_usd,
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text") and block.text:
                    print(block.text)
                    result += block.text

        elif isinstance(message, ResultMessage):
            if message.subtype == "success":
                result = getattr(message, "result", result)

    return result
