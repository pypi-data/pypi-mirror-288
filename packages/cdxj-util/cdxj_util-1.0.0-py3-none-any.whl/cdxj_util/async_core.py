import aiofiles
import json
from cdxj_util.core import CDXJRecord
from cdxj_util.exceptions import CDXJLoadError
from cdxj_util.config import Config


class AsyncCDXJCore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = Config()

    async def load(self, batch_size=None):
        if batch_size is None:
            batch_size = self.config.DEFAULT_BATCH_SIZE

        try:
            async with aiofiles.open(self.file_path, mode="r") as file:
                batch = []
                async for line in file:
                    line = line.strip()
                    if line and not line.startswith("!"):
                        try:
                            urlkey, timestamp, metadata = line.split(" ", 2)
                            metadata = json.loads(metadata)
                            batch.append(CDXJRecord(urlkey, timestamp, metadata))

                            if len(batch) >= batch_size:
                                yield batch
                                batch = []
                        except (ValueError, json.JSONDecodeError) as e:
                            print(f"Error processing line: {line}. Error: {e}")

                if batch:
                    yield batch
        except FileNotFoundError:
            raise CDXJLoadError(f"File not found: {self.file_path}")
        except PermissionError:
            raise CDXJLoadError(f"Permission denied: {self.file_path}")

    async def load_all_records(self):
        """Load all records from the file and return them as a list."""
        records = []
        async for batch in self.load():
            records.extend(batch)
        return records