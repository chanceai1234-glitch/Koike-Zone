"""CLI エントリポイント"""

import argparse
import asyncio
import sys

from .team import run_content_team, run_single_step


def main():
    parser = argparse.ArgumentParser(
        description="コンテンツ制作エージェントチーム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # チーム全体で記事を制作
  content-team "AIエージェントの未来"

  # 出力先を指定
  content-team "Python入門ガイド" --output ./articles

  # 個別ステップを実行
  content-team --step planner "AIエージェントの未来"
  content-team --step writer "企画内容をここに..."

  # 予算上限を設定
  content-team "Rustの魅力" --budget 3.0
        """,
    )
    parser.add_argument(
        "topic",
        help="記事のテーマ・トピック（または個別ステップへの入力）",
    )
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="出力先ディレクトリ (default: ./output)",
    )
    parser.add_argument(
        "--budget", "-b",
        type=float,
        default=5.0,
        help="最大予算 USD (default: 5.0)",
    )
    parser.add_argument(
        "--step", "-s",
        choices=["planner", "writer", "editor", "proofreader"],
        help="個別ステップのみ実行 (チーム全体ではなく特定のエージェントだけ)",
    )

    args = parser.parse_args()

    try:
        if args.step:
            print(f"[{args.step}] エージェントを単体実行...")
            result = asyncio.run(
                run_single_step(args.step, args.topic, args.budget)
            )
        else:
            print("コンテンツ制作チームを起動します...")
            result = asyncio.run(
                run_content_team(args.topic, args.output, args.budget)
            )
            print(f"\n記事が保存されました: {result}")
    except KeyboardInterrupt:
        print("\n中断されました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
