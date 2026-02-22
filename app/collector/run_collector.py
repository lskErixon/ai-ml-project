import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from api_client import ApiClient
from raw_store import RawStore
from dataset_store import DatasetStore
from normalizer import normalize_departureboard


def run(
    duration_seconds: int,
    *,
    config_path: str = "config/config.json",
    names: Optional[List[str]] = None,
) -> None:
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))

    client = ApiClient(cfg["golemio_base_url"], cfg["golemio_api_key"])
    raw = RawStore(cfg["raw_dir"])
    ds = DatasetStore(cfg["dataset_path"])

    poll = int(cfg["poll_seconds"])
    end_ts = time.time() + duration_seconds

    names_effective = names or cfg.get("default_names") or []
    if not names_effective:
        raise RuntimeError("Není nastavený žádný název zastávky. Nastav default_names v configu nebo pošli --names.")

    source_stop = ", ".join(names_effective)

    while time.time() < end_ts:
        payload = client.get_departureboard(
            asw_ids=cfg["asw_ids"],
            limit=int(cfg["limit"]),
            minutes_after=int(cfg["minutes_after"]),
            preferred_timezone=cfg["preferred_timezone"],
        )

        raw.save(payload, tag="departureboards")
        rows = list(normalize_departureboard(payload, source_stop=source_stop))
        inserted = ds.append_many(rows)

        print(f"[{datetime.now(timezone.utc).isoformat()}] stop='{source_stop}' rows={len(rows)} appended={inserted}")
        time.sleep(poll)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("seconds", nargs="?", type=int, default=600)
    parser.add_argument("--names", nargs="*", default=None, help="Např. --names 'Karlovo náměstí'")
    args = parser.parse_args()

    run(args.seconds, names=args.names)
