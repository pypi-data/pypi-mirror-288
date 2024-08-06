# cdxj_util

cdxj_util is a Python library for efficiently processing CDXJ (Compressed DeduplicateD Web Archive Index JSON) files. This library provides functionality for loading, searching, and analyzing large CDXJ files.

## Features

- Asynchronous and synchronous loading of CDXJ files
- URL-based searching (exact and partial matching)
- Filtering by timestamp range
- Bulk searching of multiple URLs
- Generation of CDXJ file statistics (total records, unique URLs, subdomain distribution, MIME type distribution, etc.)

## Installation

```bash
pip install cdxj_util
```

## Usage

### Loading a CDXJ file

```python
from cdxj_util.core import CDXJCore

core = CDXJCore("path/to/your.cdxj")
records = core.load_all_records()
```

### Searching URLs

```python
from cdxj_util.search import CDXJSearch

search = CDXJSearch(records)
results = search.search_by_url("http://example.com/", exact_match=True)
```

### Generating statistics

```python
from cdxj_util.stats import CDXJStats

stats = CDXJStats(records)
total_records = stats.total_records()
unique_urls = stats.unique_urls()
mime_distribution = stats.mime_type_distribution()
```

## Asynchronous Support

cdxj_util also supports asynchronous processing, which is particularly useful for handling large CDXJ files:

```python
import asyncio
from cdxj_util.async_core import AsyncCDXJCore

async def process_cdxj():
    async_core = AsyncCDXJCore("path/to/your.cdxj")
    records = await async_core.load_all_records()
    # Further processing...

asyncio.run(process_cdxj())
```

## Examples

For more detailed usage examples, please refer to the demo scripts in the `examples/` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
