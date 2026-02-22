from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional


def _get(d: Dict[str, Any], path: str) -> Optional[Any]:
    cur: Any = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def normalize_departureboard(payload: Dict[str, Any], *, source_stop: str) -> Iterable[Dict[str, Any]]:
    ts = datetime.now(timezone.utc).isoformat()
    departures = payload.get("departures") or payload.get("data") or []

    for dep in departures:
        route_name = _get(dep, "route.short_name") or _get(dep, "route.shortName") or dep.get("route_name")
        stop_id = _get(dep, "stop.id") or dep.get("stop_id")
        platform = _get(dep, "stop.platform_code") or _get(dep, "stop.platformCode")

        scheduled = _get(dep, "departure_timestamp.scheduled") or _get(dep, "departureTimestamp.scheduled")
        predicted = _get(dep, "departure_timestamp.predicted") or _get(dep, "departureTimestamp.predicted")

        delay_min = _get(dep, "delay.minutes") or _get(dep, "delayMinutes")

        trip_id = _get(dep, "trip.id") or dep.get("trip_id")
        headsign = _get(dep, "trip.headsign")

        yield {
            "ts_utc": ts,
            "source_stop": source_stop,
            "stop_id": stop_id,
            "platform": platform,

            "route_name": route_name,
            "trip_id": trip_id,
            "headsign": headsign,

            "scheduled_ts": scheduled,
            "predicted_ts": predicted,
            "delay_min": delay_min,
        }
