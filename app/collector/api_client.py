import requests
from typing import Any, Dict, List, Optional


class ApiClient:
    def __init__(self, base_url: str, api_key: str, timeout_s: int = 20) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_s = timeout_s

    def get_departureboard(
        self,
        *,
        asw_ids: List[str],
        limit: int,
        minutes_after: int,
        preferred_timezone: str,
    ) -> Dict[str, Any]:
        """
        Volá Golemio PID departureboards přes aswIds (nejstabilnější varianta).

        Pozn:
        - URL bez koncového lomítka (někdy řeší 404 na některých gateway)
        - aswIds posíláme jako list (requests z toho udělá opakovaný query param)
        """
        url = f"{self.base_url}/v2/pid/departureboards"
        params: Dict[str, Any] = {
            "aswIds": asw_ids,
            "limit": limit,
            "minutesAfter": minutes_after,
            "preferredTimezone": preferred_timezone,
        }

        headers = {
            "X-Access-Token": self.api_key,
            "Accept": "application/json",
        }

        r = requests.get(url, params=params, headers=headers, timeout=self.timeout_s)

        # Debug při chybě (hlavně pro 404/401/403)
        if r.status_code != 200:
            print("---- GOLEMIO ERROR ----")
            print("URL:", r.url)
            print("STATUS:", r.status_code)
            print("BODY (first 500 chars):", r.text[:500])
            print("-----------------------")

        r.raise_for_status()
        return r.json()