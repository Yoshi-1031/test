"""
情報収集モジュール
世界各国の公務員制度に関する情報をウェブから収集
"""
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional
from urllib.parse import quote_plus

import config

logger = logging.getLogger(__name__)


class CivilServiceCollector:
    """公務員制度情報を収集するクラス"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "CivilServiceTracker/1.0 (Educational Purpose)"
        })

    def search_news(self, country_code: str) -> list[dict]:
        """
        指定した国の公務員制度に関するニュースを検索

        Args:
            country_code: 国コード (例: "japan", "usa")

        Returns:
            検索結果のリスト
        """
        if country_code not in config.COUNTRIES:
            logger.warning(f"Unknown country code: {country_code}")
            return []

        country = config.COUNTRIES[country_code]
        results = []

        for keyword in country["keywords"]:
            try:
                items = self._search_keyword(keyword, country["language"])
                results.extend(items)
            except Exception as e:
                logger.error(f"Error searching for '{keyword}': {e}")

        return results

    def _search_keyword(self, keyword: str, language: str) -> list[dict]:
        """キーワードで検索を実行"""
        # 注意: 実際の実装では適切なニュースAPIを使用することを推奨
        # ここではデモ用の構造を提供
        logger.info(f"Searching for: {keyword} (lang: {language})")

        return [{
            "keyword": keyword,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "status": "pending_api_integration"
        }]

    def fetch_official_source(self, url: str) -> Optional[dict]:
        """
        公式ソースから情報を取得

        Args:
            url: 取得先URL

        Returns:
            取得した情報の辞書、失敗時はNone
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # ページタイトルを取得
            title = soup.find("title")
            title_text = title.get_text().strip() if title else "No title"

            # メタ情報を取得
            description = ""
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                description = meta_desc["content"]

            return {
                "url": url,
                "title": title_text,
                "description": description,
                "fetched_at": datetime.now().isoformat(),
                "status": "success"
            }

        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "fetched_at": datetime.now().isoformat(),
                "status": "failed"
            }

    def collect_all(self) -> dict:
        """
        すべての国の情報を収集

        Returns:
            収集結果の辞書
        """
        logger.info("Starting full collection...")

        results = {
            "collection_time": datetime.now().isoformat(),
            "countries": {}
        }

        for country_code, country_info in config.COUNTRIES.items():
            logger.info(f"Collecting data for {country_info['name']}...")

            country_results = {
                "name": country_info["name"],
                "news": self.search_news(country_code),
                "official_sources": []
            }

            # 公式ソースがある場合は取得
            if country_code in config.SOURCES:
                for url in config.SOURCES[country_code]:
                    source_data = self.fetch_official_source(url)
                    if source_data:
                        country_results["official_sources"].append(source_data)

            results["countries"][country_code] = country_results

        logger.info("Collection completed.")
        return results


def main():
    """テスト実行"""
    logging.basicConfig(level=logging.INFO)

    collector = CivilServiceCollector()
    results = collector.collect_all()

    import json
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
