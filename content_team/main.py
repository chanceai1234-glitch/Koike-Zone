"""CLI エントリポイント - 占い科学検証プロジェクト"""

import argparse
import asyncio
import sys

from .team import run_full_pipeline, run_single_phase, PHASE_DESCRIPTIONS


def main():
    parser = argparse.ArgumentParser(
        description="占いの科学的検証プロジェクト - エージェントチーム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全フェーズを一括実行（リサーチ→分析→執筆→チェック→アプリ企画）
  python -m content_team.main

  # 出力先を指定
  python -m content_team.main --output ./results

  # 個別フェーズを実行
  python -m content_team.main --phase research     # 世界の占い手法リサーチ
  python -m content_team.main --phase analyze      # 科学的分析
  python -m content_team.main --phase write        # 啓発記事の執筆
  python -m content_team.main --phase factcheck    # ファクトチェック
  python -m content_team.main --phase plan_app     # 占い体験アプリ企画

  # 予算上限を設定
  python -m content_team.main --budget 8.0

フェーズ一覧:
  research   - 世界中の占い手法を網羅的にリサーチ
  analyze    - 科学的根拠・心理学的メカニズムの分析
  write      - 一般向け啓発記事の執筆
  factcheck  - 科学的正確性・公平性のチェック
  plan_app   - 占い体験サイト/アプリの企画設計
        """,
    )
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="出力先ディレクトリ (default: ./output)",
    )
    parser.add_argument(
        "--budget", "-b",
        type=float,
        default=10.0,
        help="最大予算 USD (default: 10.0)",
    )
    parser.add_argument(
        "--phase", "-p",
        choices=list(PHASE_DESCRIPTIONS.keys()),
        help="個別フェーズのみ実行",
    )
    parser.add_argument(
        "--input", "-i",
        default="",
        help="個別フェーズ実行時の入力テキスト（前フェーズの結果など）",
    )

    args = parser.parse_args()

    try:
        if args.phase:
            desc = PHASE_DESCRIPTIONS[args.phase]
            print(f"[{desc}] を単体実行します...")
            asyncio.run(
                run_single_phase(
                    args.phase, args.input, args.output, args.budget
                )
            )
        else:
            print("=" * 60)
            print("  占いの科学的検証プロジェクト")
            print("  全5フェーズを実行します")
            print("=" * 60)
            for key, desc in PHASE_DESCRIPTIONS.items():
                if key != "full":
                    print(f"  {desc}")
            print("=" * 60)

            result = asyncio.run(
                run_full_pipeline(args.output, args.budget)
            )
            print(f"\n全成果物が保存されました: {result}")
    except KeyboardInterrupt:
        print("\n中断されました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
