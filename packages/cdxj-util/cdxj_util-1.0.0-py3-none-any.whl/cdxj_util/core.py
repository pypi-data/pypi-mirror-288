import json
from cdxj_util.exceptions import CDXJLoadError
from cdxj_util.config import Config


class CDXJRecord:
    def __init__(self, urlkey, timestamp, metadata):
        self.urlkey = urlkey
        self.timestamp = timestamp
        self.metadata = metadata


class CDXJCore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = Config()

    def load(self, batch_size=None):
        """Load records with buffering to handle large files efficiently."""
        if batch_size is None:
            batch_size = self.config.DEFAULT_BATCH_SIZE

        try:
            with open(self.file_path, "r") as file:
                batch = []
                for line in file:
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
                            # エラーが発生した行をスキップし、次の行の処理に進む
                            continue

                if batch:
                    yield batch
        except FileNotFoundError:
            raise CDXJLoadError(f"File not found: {self.file_path}")
        except PermissionError:
            raise CDXJLoadError(f"Permission denied: {self.file_path}")

    def load_all_records(self):
        """Load all records from the file and return them as a list."""
        records = []
        for batch in self.load():
            records.extend(batch)
        return records

    def __iter__(self):
        """Iterator for memory-efficient record access."""
        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("!"):
                    urlkey, timestamp, metadata = line.split(" ", 2)
                    metadata = json.loads(metadata)
                    yield CDXJRecord(urlkey, timestamp, metadata)