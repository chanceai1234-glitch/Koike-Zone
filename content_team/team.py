"""チームオーケストレーター - 占い調査・分析プロジェクトの制御"""

from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, AssistantMessage, ResultMessage, query

from .agents import get_all_agents


PHASE_DESCRIPTIONS = {
    "research": "Phase 1: 世界の占い手法リサーチ",
    "analyze": "Phase 2: 科学的分析",
    "write": "Phase 3: 啓発記事の執筆",
    "factcheck": "Phase 4: ファクトチェック",
    "plan_app": "Phase 5: 占い体験アプリの企画",
    "full": "全フェーズ一括実行",
}


async def run_full_pipeline(
    output_dir: str = "./output",
    max_budget_usd: float = 10.0,
) -> str:
    """全フェーズを通して実行する

    Args:
        output_dir: 出力先ディレクトリ
        max_budget_usd: 最大予算（USD）

    Returns:
        出力ディレクトリのパス
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    team_prompt = f"""あなたは「占いの科学的検証プロジェクト」のプロジェクトマネージャーです。
5つのエージェントチームを統括し、以下のフェーズを順番に実行してください。

## プロジェクトの目的
世界中の占い手法を調査し、科学的根拠に基づいて分析し、
人々が占いとの正しい付き合い方を理解できる啓発コンテンツを制作する。
さらに、占いを実際に体験できるサイト/アプリの企画も行う。

## 実行フロー

### Phase 1: リサーチ（researcher エージェント）
researcherエージェントを使い、世界中の占い手法を網羅的に調査してください。
東アジア・南アジア・中東/アフリカ・ヨーロッパ・アメリカ大陸の各地域を網羅すること。
結果を `{output_path}/01_research.md` に保存してください。

### Phase 2: 科学的分析（scientist エージェント）
Phase 1のリサーチ結果を元に、scientistエージェントを使い、
各占い手法の科学的検証と心理学的メカニズムの分析を行ってください。
バーナム効果、確証バイアス、自己成就予言など関連する心理効果も分析すること。
結果を `{output_path}/02_scientific_analysis.md` に保存してください。

### Phase 3: 啓発記事の執筆（writer エージェント）
Phase 1・2の結果を元に、writerエージェントを使い、
一般読者向けの啓発記事を執筆してください。
占いを信じる人を攻撃せず、科学的事実を元に読者自身が気づきを得られる構成にすること。
結果を `{output_path}/03_article.md` に保存してください。

### Phase 4: ファクトチェック（fact_checker エージェント）
Phase 3の記事をfact_checkerエージェントに渡し、
科学的正確性・公平性・論理的一貫性をチェックしてください。
修正済みの最終版記事を `{output_path}/04_final_article.md` に保存してください。

### Phase 5: アプリ企画（ux_planner エージェント）
ux_plannerエージェントを使い、占い体験サイト/アプリの企画設計を行ってください。
ユーザーが占いを体験した後に科学的解説を読み、
「占いの結果ではなく自分の考え方が大事」と気づける体験設計にすること。
結果を `{output_path}/05_app_plan.md` に保存してください。

## 重要な方針
- 各フェーズの結果は前のフェーズの成果物を踏まえる
- 占いの全否定ではなく、科学的事実に基づいたバランスの取れた分析
- 心理的効果（カウンセリング効果など）は正当に評価する
- 本当に科学的根拠がある効果があれば、それも報告する

各フェーズの進捗を簡潔に報告しながら進めてください。
"""

    agents = get_all_agents()

    print(f"\n{'='*60}")
    print("  占いの科学的検証プロジェクト 起動")
    print(f"  出力先: {output_path}/")
    print(f"{'='*60}\n")

    async for message in query(
        prompt=team_prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Grep", "Glob", "Agent"],
            agents=agents,
            max_turns=80,
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
                total_cost = getattr(message, "total_cost_usd", 0.0)
                num_turns = getattr(message, "num_turns", 0)

                print(f"\n{'='*60}")
                print("  プロジェクト完了!")
                print(f"  ターン数: {num_turns}")
                print(f"  コスト: ${total_cost:.4f}")
                print(f"  出力ファイル:")
                print(f"    - {output_path}/01_research.md")
                print(f"    - {output_path}/02_scientific_analysis.md")
                print(f"    - {output_path}/03_article.md")
                print(f"    - {output_path}/04_final_article.md")
                print(f"    - {output_path}/05_app_plan.md")
                print(f"{'='*60}\n")
            else:
                print(f"\n[エラー] {message.subtype}")

    return str(output_path)


async def run_single_phase(
    phase: str,
    input_text: str = "",
    output_dir: str = "./output",
    max_budget_usd: float = 3.0,
) -> str:
    """個別フェーズを単体実行する

    Args:
        phase: "research", "analyze", "write", "factcheck", "plan_app"
        input_text: 前フェーズの出力（必要に応じて）
        output_dir: 出力先ディレクトリ
        max_budget_usd: 最大予算

    Returns:
        エージェントの出力テキスト
    """
    agents = get_all_agents()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    phase_to_agent = {
        "research": "researcher",
        "analyze": "scientist",
        "write": "writer",
        "factcheck": "fact_checker",
        "plan_app": "ux_planner",
    }

    phase_to_file = {
        "research": "01_research.md",
        "analyze": "02_scientific_analysis.md",
        "write": "03_article.md",
        "factcheck": "04_final_article.md",
        "plan_app": "05_app_plan.md",
    }

    if phase not in phase_to_agent:
        raise ValueError(
            f"不明なフェーズ: {phase} (選択肢: {list(phase_to_agent.keys())})"
        )

    agent_name = phase_to_agent[phase]
    output_file = output_path / phase_to_file[phase]

    context = f"\n\n以下は前のフェーズの結果です:\n{input_text}" if input_text else ""
    prompt = (
        f"{agent_name}エージェントを使って作業を実行してください。"
        f"結果は `{output_file}` に保存してください。{context}"
    )

    description = PHASE_DESCRIPTIONS.get(phase, phase)
    print(f"\n[{description}] 開始...")

    result = ""

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Grep", "Glob", "Agent"],
            agents={agent_name: agents[agent_name]},
            max_turns=30,
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
                print(f"\n[{description}] 完了 → {output_file}")

    return result
