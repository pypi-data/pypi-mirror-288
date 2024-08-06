import re
from functools import lru_cache
from typing import List, Tuple, Dict
import asyncio
import json
from urllib.parse import urlparse, parse_qs


class CDXJSearch:
    def __init__(self, records):
        self.records = records

    @lru_cache(maxsize=100)
    def search_by_url(
        self, url_pattern: str, exact_match: bool = False
    ) -> List[Tuple[str, str]]:
        if exact_match:
            regex = re.compile(f"^{re.escape(url_pattern)}$")
        else:
            regex = re.compile(url_pattern)
        return [
            (record.metadata.get("url", ""), record.timestamp)
            for record in self.records
            if regex.search(record.metadata.get("url", ""))
        ]

    @lru_cache(maxsize=50)
    def filter_by_timestamp_range(self, start: str, end: str) -> List[Tuple[str, str]]:
        return [
            (record.metadata.get("url", ""), record.timestamp)
            for record in self.records
            if start <= record.timestamp <= end
        ]

    def clear_cache(self):
        self.search_by_url.cache_clear()
        self.filter_by_timestamp_range.cache_clear()

    def search_multiple_urls(self, url_list: List[str]) -> Dict[str, List[Dict]]:
        result_dict = {}

        for url in url_list:
            parsed_url = urlparse(url)
            path_regex = re.escape(parsed_url.path)
            query_params = parse_qs(parsed_url.query)

            regex_parts = [
                f"^{re.escape(parsed_url.scheme)}://{re.escape(parsed_url.netloc)}{path_regex}"
            ]

            if query_params:
                regex_parts.append(r"\?")
                param_patterns = []
                for key, values in query_params.items():
                    if values:
                        param_patterns.extend(
                            [f"{re.escape(key)}={re.escape(v)}" for v in values]
                        )
                    else:
                        param_patterns.append(f"{re.escape(key)}=")
                regex_parts.append("&".join(param_patterns))

            regex_parts.append("$")
            regex = re.compile("".join(regex_parts))

            filtered_results = [
                {"timestamp": record.timestamp, "metadata": record.metadata}
                for record in self.records
                if regex.search(record.metadata.get("url", ""))
            ]

            if filtered_results:
                result_dict[url] = filtered_results

        return result_dict


class AsyncCDXJSearch:
    def __init__(self, records):
        self.records = records

    async def search_by_url(
        self, url_pattern: str, exact_match: bool = False
    ) -> List[Tuple[str, str]]:
        if exact_match:
            regex = re.compile(f"^{re.escape(url_pattern)}$")
        else:
            regex = re.compile(url_pattern)

        async def search_record(record):
            if regex.search(record.metadata.get("url", "")):
                return (record.metadata.get("url", ""), record.timestamp)
            return None

        results = await asyncio.gather(
            *[search_record(record) for record in self.records]
        )
        return [result for result in results if result is not None]

    async def filter_by_timestamp_range(
        self, start: str, end: str
    ) -> List[Tuple[str, str]]:
        async def filter_record(record):
            if start <= record.timestamp <= end:
                return (record.metadata.get("url", ""), record.timestamp)
            return None

        results = await asyncio.gather(
            *[filter_record(record) for record in self.records]
        )
        return [result for result in results if result is not None]

    async def search_multiple_urls(self, url_list: List[str]) -> Dict[str, List[Dict]]:
        result_dict = {}

        async def search_url(url):
            parsed_url = urlparse(url)
            path_regex = re.escape(parsed_url.path)
            query_params = parse_qs(parsed_url.query)

            regex_parts = [
                f"^{re.escape(parsed_url.scheme)}://{re.escape(parsed_url.netloc)}{path_regex}"
            ]

            if query_params:
                regex_parts.append(r"\?")
                param_patterns = []
                for key, values in query_params.items():
                    if values:
                        param_patterns.extend(
                            [f"{re.escape(key)}={re.escape(v)}" for v in values]
                        )
                    else:
                        param_patterns.append(f"{re.escape(key)}=")
                regex_parts.append("&".join(param_patterns))

            regex_parts.append("$")
            regex = re.compile("".join(regex_parts))

            filtered_results = [
                {"timestamp": record.timestamp, "metadata": record.metadata}
                for record in self.records
                if regex.search(record.metadata.get("url", ""))
            ]
            if filtered_results:
                return (url, filtered_results)
            return None

        results = await asyncio.gather(*[search_url(url) for url in url_list])
        result_dict = dict(result for result in results if result is not None)

        return result_dict
