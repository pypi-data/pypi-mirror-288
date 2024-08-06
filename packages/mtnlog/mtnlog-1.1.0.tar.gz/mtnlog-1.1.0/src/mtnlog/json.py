"""JSON logger class for logging arguments and results."""

import json
import os


class JSONLogger:
    """Arguments logger class."""

    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir

    def serialize(self, obj):
        """Custom serialization for non-serializable objects."""
        if isinstance(obj, dict):
            return {k: self.serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.serialize(v) for v in obj]
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        # Convert non-serializable objects to their string representation
        return str(obj)

    def log(self, obj, filename="log"):
        """Logs the object."""
        with open(f"{self.log_dir}/{filename}.json", "w", encoding='utf-8') as f:
            json.dump(self.serialize(obj), f, ensure_ascii=False, indent=4)
