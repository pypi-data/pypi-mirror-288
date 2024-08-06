import json
from datetime import datetime, timezone
from typing import Dict
import requests

class TrackTestRequest:
    def __init__(self, name: str, trace: str, executed_at: datetime, result: bool):
        self.name = name
        self.trace = trace
        self.executed_at = executed_at.replace(tzinfo=timezone.utc)

        self.result = result

    def to_dict(self) -> Dict:
        """Convert the TrackTestRequest object to a dictionary."""
        return {
            "name": self.name,
            "trace": self.trace,
            "executedAt": self.executed_at.isoformat(),
            "result": self.result,
        }

    def to_json(self) -> str:
        """Convert the TrackTestRequest object to a JSON string."""
        return json.dumps(self.to_dict())

    def send(self, url: str) -> requests.Response:
        """Send the TrackTestRequest data to a specified endpoint."""
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=self.to_json(), headers=headers)
        return response