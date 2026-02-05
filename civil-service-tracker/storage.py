"""
データ保存モジュール
収集した情報をJSON形式で保存・管理
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import config

logger = logging.getLogger(__name__)


class DataStorage:
    """データ保存クラス"""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or config.DATA_DIR
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """データディレクトリが存在することを確認"""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_filename(self, date: Optional[datetime] = None) -> Path:
        """日付ベースのファイル名を生成"""
        date = date or datetime.now()
        filename = f"civil_service_data_{date.strftime('%Y%m%d')}.json"
        return self.data_dir / filename

    def save(self, data: dict, date: Optional[datetime] = None) -> Path:
        """
        データをJSON形式で保存

        Args:
            data: 保存するデータ
            date: 保存日付（省略時は現在日時）

        Returns:
            保存先ファイルパス
        """
        filepath = self._get_filename(date)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"Data saved to {filepath}")
            return filepath

        except IOError as e:
            logger.error(f"Failed to save data: {e}")
            raise

    def load(self, date: Optional[datetime] = None) -> Optional[dict]:
        """
        保存されたデータを読み込み

        Args:
            date: 読み込む日付（省略時は今日）

        Returns:
            読み込んだデータ、ファイルが存在しない場合はNone
        """
        filepath = self._get_filename(date)

        if not filepath.exists():
            logger.warning(f"Data file not found: {filepath}")
            return None

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)

        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load data: {e}")
            return None

    def load_latest(self) -> Optional[dict]:
        """最新のデータファイルを読み込み"""
        files = sorted(self.data_dir.glob("civil_service_data_*.json"), reverse=True)

        if not files:
            logger.warning("No data files found")
            return None

        latest_file = files[0]
        logger.info(f"Loading latest file: {latest_file}")

        try:
            with open(latest_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load latest data: {e}")
            return None

    def list_files(self) -> list[Path]:
        """保存されているデータファイルの一覧を取得"""
        return sorted(self.data_dir.glob("civil_service_data_*.json"))

    def get_summary(self) -> dict:
        """保存データのサマリーを取得"""
        files = self.list_files()

        return {
            "total_files": len(files),
            "data_dir": str(self.data_dir),
            "files": [f.name for f in files[-10:]],  # 最新10件
            "oldest": files[0].name if files else None,
            "newest": files[-1].name if files else None,
        }


def main():
    """テスト実行"""
    logging.basicConfig(level=logging.INFO)

    storage = DataStorage()

    # テストデータの保存
    test_data = {
        "collection_time": datetime.now().isoformat(),
        "test": True,
        "message": "これはテストデータです"
    }

    filepath = storage.save(test_data)
    print(f"Saved to: {filepath}")

    # 読み込みテスト
    loaded = storage.load()
    print(f"Loaded: {loaded}")

    # サマリー表示
    print(f"Summary: {storage.get_summary()}")


if __name__ == "__main__":
    main()
