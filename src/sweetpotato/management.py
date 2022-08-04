import json
from typing import Optional

from sweetpotato.core.utils import BaseProps


class Props(BaseProps):
    def __init__(self, values: Optional[dict] = None):
        super().__init__(values)

    def as_json(self):
        """Return dict as json."""
        return json.dumps(self.values)


class State(Props):
    pass
