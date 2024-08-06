from collections import Counter
from typing import Dict, Callable

class CDXJStats:
    def __init__(self, records):
        self.records = records

    def total_records(self) -> int:
        return len(self.records)

    def unique_urls(self) -> int:
        return len(set(record.metadata.get("url", "") for record in self.records))

    def distribution_by(self, key_func: Callable[[str], str]) -> Dict[str, int]:
        return Counter(key_func(record.timestamp) for record in self.records)

    def subdomain_distribution(self) -> Dict[str, int]:
        subdomains = Counter()
        for record in self.records:
            parts = record.urlkey.split(")/", 1)
            if len(parts) == 2:
                domain_parts = parts[0].split(",")
                if len(domain_parts) > 2:
                    subdomains[",".join(domain_parts[2:])] += 1
                else:
                    subdomains["(root)"] += 1
        return subdomains

    def mime_type_distribution(self) -> Dict[str, int]:
        return Counter(record.metadata.get("mime", "") for record in self.records)


class AsyncCDXJStats:
    def __init__(self, records):
        self.records = records

    async def total_records(self) -> int:
        return len(self.records)

    async def unique_urls(self) -> int:
        unique_urls = set()
        for record in self.records:
            unique_urls.add(record.metadata.get("url", ""))
        return len(unique_urls)

    async def distribution_by(self, key_func: Callable[[str], str]) -> Dict[str, int]:
        distribution = Counter()
        for record in self.records:
            key = key_func(record.timestamp)
            distribution[key] += 1
        return distribution

    async def subdomain_distribution(self) -> Dict[str, int]:
        subdomains = Counter()
        for record in self.records:
            parts = record.urlkey.split(")/", 1)
            if len(parts) == 2:
                domain_parts = parts[0].split(",")
                if len(domain_parts) > 2:
                    subdomains[",".join(domain_parts[2:])] += 1
                else:
                    subdomains["(root)"] += 1
        return subdomains

    async def mime_type_distribution(self) -> Dict[str, int]:
        return Counter(record.metadata.get("mime", "") for record in self.records)
