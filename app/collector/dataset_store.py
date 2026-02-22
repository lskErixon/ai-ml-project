import json
import os
from typing import Any, Dict, Iterable


class DatasetStore:
    def __init__(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)

    def append_many(self, rows: Iterable[Dict[str, Any]]) -> int:
        rows_list = list(rows)
        if not rows_list:
            return 0

        with open(self.dataset_path, "a", encoding="utf-8") as f:
            for row in rows_list:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

        return len(rows_list)
