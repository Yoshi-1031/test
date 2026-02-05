#!/usr/bin/env python3
"""
公務員制度情報収集アプリ
世界各国の公務員制度に関する情報を毎日収集

使い方:
    python main.py              # スケジューラーを起動
    python main.py --run-now    # 即時実行
    python main.py --status     # ステータス確認
    python main.py --view       # 最新データを表示
"""
import argparse
import logging
import sys
from datetime import datetime

import config
from collector import CivilServiceCollector
from scheduler import TaskScheduler
from storage import DataStorage


def setup_logging():
    """ロギング設定"""
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
        ],
    )


def collection_task():
    """情報収集タスク（スケジューラーから呼び出される）"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("Starting scheduled collection task")
    logger.info("=" * 50)

    collector = CivilServiceCollector()
    storage = DataStorage()

    # データ収集
    data = collector.collect_all()

    # 保存
    filepath = storage.save(data)
    logger.info(f"Collection completed. Data saved to: {filepath}")

    # サマリー表示
    countries_count = len(data.get("countries", {}))
    logger.info(f"Collected data from {countries_count} countries")

    return data


def run_scheduler():
    """スケジューラーを起動"""
    logger = logging.getLogger(__name__)
    logger.info("Starting Civil Service Tracker Scheduler")
    logger.info(f"Scheduled time: {config.SCHEDULE_TIME}")

    scheduler = TaskScheduler()
    scheduler.schedule_daily(
        config.SCHEDULE_TIME,
        collection_task,
        "civil_service_collection"
    )

    print(f"\n公務員制度情報収集アプリを起動しました")
    print(f"毎日 {config.SCHEDULE_TIME} に情報を収集します")
    print(f"次回実行予定: {scheduler.get_next_run()}")
    print(f"終了するには Ctrl+C を押してください\n")

    scheduler.run_forever()


def run_now():
    """即時実行"""
    print("情報収集を即時実行します...")
    data = collection_task()

    print(f"\n収集完了:")
    print(f"  収集時刻: {data['collection_time']}")
    print(f"  対象国数: {len(data['countries'])}")

    for code, info in data["countries"].items():
        print(f"  - {info['name']}: ニュース {len(info['news'])}件, "
              f"公式ソース {len(info['official_sources'])}件")


def show_status():
    """ステータス表示"""
    storage = DataStorage()
    summary = storage.get_summary()

    print("\n=== 公務員制度情報収集アプリ ステータス ===\n")
    print(f"データ保存先: {summary['data_dir']}")
    print(f"保存ファイル数: {summary['total_files']}")

    if summary["oldest"]:
        print(f"最古のデータ: {summary['oldest']}")
        print(f"最新のデータ: {summary['newest']}")

    print(f"\n設定:")
    print(f"  実行時刻: {config.SCHEDULE_TIME}")
    print(f"  対象国数: {len(config.COUNTRIES)}")

    print(f"\n対象国:")
    for code, info in config.COUNTRIES.items():
        print(f"  - {info['name']} ({code})")


def view_latest():
    """最新データを表示"""
    storage = DataStorage()
    data = storage.load_latest()

    if not data:
        print("保存されているデータがありません")
        return

    print(f"\n=== 最新の収集データ ===")
    print(f"収集時刻: {data['collection_time']}\n")

    for code, info in data.get("countries", {}).items():
        print(f"【{info['name']}】")

        if info.get("official_sources"):
            print("  公式ソース:")
            for source in info["official_sources"]:
                status = "✓" if source.get("status") == "success" else "✗"
                print(f"    {status} {source.get('title', 'N/A')}")
                print(f"      URL: {source.get('url', 'N/A')}")

        if info.get("news"):
            print(f"  検索キーワード: {len(info['news'])}件")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="公務員制度情報収集アプリ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python main.py              スケジューラーを起動（毎日定時に実行）
  python main.py --run-now    情報収集を即時実行
  python main.py --status     アプリのステータスを表示
  python main.py --view       最新の収集データを表示

環境変数:
  SCHEDULE_TIME   実行時刻（デフォルト: 09:00）
  LOG_LEVEL       ログレベル（デフォルト: INFO）
        """
    )

    parser.add_argument(
        "--run-now", "-r",
        action="store_true",
        help="情報収集を即時実行"
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="ステータスを表示"
    )
    parser.add_argument(
        "--view", "-v",
        action="store_true",
        help="最新データを表示"
    )

    args = parser.parse_args()

    setup_logging()

    if args.status:
        show_status()
    elif args.view:
        view_latest()
    elif args.run_now:
        run_now()
    else:
        run_scheduler()


if __name__ == "__main__":
    main()
