"""
スケジューラーモジュール
毎日決まった時間に情報収集を実行
"""
import logging
import schedule
import time
from datetime import datetime
from typing import Callable

import config

logger = logging.getLogger(__name__)


class TaskScheduler:
    """タスクスケジューラークラス"""

    def __init__(self):
        self.jobs = []

    def schedule_daily(self, time_str: str, task: Callable, task_name: str = "task"):
        """
        毎日指定時間にタスクを実行するようスケジュール

        Args:
            time_str: 実行時間 (例: "09:00")
            task: 実行する関数
            task_name: タスク名（ログ用）
        """
        job = schedule.every().day.at(time_str).do(self._run_task, task, task_name)
        self.jobs.append(job)
        logger.info(f"Scheduled '{task_name}' to run daily at {time_str}")

    def _run_task(self, task: Callable, task_name: str):
        """タスクを実行してログを記録"""
        logger.info(f"Starting scheduled task: {task_name}")
        start_time = datetime.now()

        try:
            task()
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Task '{task_name}' completed in {duration:.2f} seconds")
        except Exception as e:
            logger.error(f"Task '{task_name}' failed: {e}")
            raise

    def run_pending(self):
        """保留中のタスクを実行"""
        schedule.run_pending()

    def run_forever(self, check_interval: int = 60):
        """
        スケジューラーを永続的に実行

        Args:
            check_interval: タスクチェック間隔（秒）
        """
        logger.info(f"Scheduler started. Checking every {check_interval} seconds.")
        logger.info(f"Next scheduled run at: {config.SCHEDULE_TIME}")

        try:
            while True:
                self.run_pending()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user.")

    def run_now(self, task: Callable, task_name: str = "immediate_task"):
        """タスクを即時実行"""
        logger.info(f"Running task immediately: {task_name}")
        self._run_task(task, task_name)

    def get_next_run(self) -> str:
        """次回実行予定時刻を取得"""
        next_run = schedule.next_run()
        if next_run:
            return next_run.strftime("%Y-%m-%d %H:%M:%S")
        return "No scheduled tasks"

    def clear_all(self):
        """すべてのスケジュールをクリア"""
        schedule.clear()
        self.jobs = []
        logger.info("All scheduled tasks cleared.")


def main():
    """テスト実行"""
    logging.basicConfig(level=logging.INFO)

    def sample_task():
        print(f"Task executed at {datetime.now()}")

    scheduler = TaskScheduler()
    scheduler.schedule_daily("09:00", sample_task, "sample_collection")

    print(f"Next run: {scheduler.get_next_run()}")
    print("Press Ctrl+C to stop...")

    # テスト用：即時実行
    scheduler.run_now(sample_task, "immediate_test")


if __name__ == "__main__":
    main()
