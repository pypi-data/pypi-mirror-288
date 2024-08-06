class Config:
    DEFAULT_BATCH_SIZE = 10000
    MAX_CACHE_SIZE = 1000
    LOG_LEVEL = "INFO"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)