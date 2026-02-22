import json
import os
from datetime import datetime, timezone
from typing import Any, Dict


class RawStore:
    def __init__(self, raw_dir: str) -> None:
        self.raw_dir = raw_dir

    def save(self, payload: Dict[str, Any], *, tag: str) -> str:
        now = datetime.now(timezone.utc)
        day_dir = os.path.join(self.raw_dir, now.strftime("%Y-%m-%d"))
        os.makedirs(day_dir, exist_ok=True)

        path = os.path.join(day_dir, f"{now.strftime('%H%M%S')}_{tag}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        return path
