"""
公務員制度情報収集アプリの設定ファイル
"""
import os
from pathlib import Path

# スケジュール設定（毎日実行する時間）
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "09:00")

# データ保存ディレクトリ
DATA_DIR = Path(__file__).parent / "data"

# 検索対象の国とキーワード
COUNTRIES = {
    "japan": {
        "name": "日本",
        "keywords": ["公務員制度", "国家公務員", "地方公務員", "人事院"],
        "language": "ja"
    },
    "usa": {
        "name": "アメリカ",
        "keywords": ["civil service", "federal employees", "OPM"],
        "language": "en"
    },
    "uk": {
        "name": "イギリス",
        "keywords": ["civil service UK", "public sector employment UK"],
        "language": "en"
    },
    "germany": {
        "name": "ドイツ",
        "keywords": ["Beamte", "öffentlicher Dienst Deutschland"],
        "language": "de"
    },
    "france": {
        "name": "フランス",
        "keywords": ["fonction publique France", "fonctionnaire"],
        "language": "fr"
    },
    "china": {
        "name": "中国",
        "keywords": ["公务员制度 中国", "国家公务员"],
        "language": "zh"
    },
    "korea": {
        "name": "韓国",
        "keywords": ["공무원 제도", "국가공무원"],
        "language": "ko"
    }
}

# 情報ソースURL（主要な政府・ニュースサイト）
SOURCES = {
    "japan": [
        "https://www.jinji.go.jp/",  # 人事院
        "https://www.soumu.go.jp/",   # 総務省
    ],
    "usa": [
        "https://www.opm.gov/",       # Office of Personnel Management
    ],
    "uk": [
        "https://www.gov.uk/government/organisations/civil-service",
    ],
}

# ログ設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "app.log"
