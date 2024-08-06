class CDXJRetrieval:
    def __init__(self, cdxj_core):
        self.cdxj_core = cdxj_core

    def get_all_urls(self):
        return {record.metadata.get('url', '') for record in self.cdxj_core}

    def get_all_timestamps(self):
        return {record.timestamp for record in self.cdxj_core}