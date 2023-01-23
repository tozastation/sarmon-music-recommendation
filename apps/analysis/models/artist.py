from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Artist:
    id: str
    uri: str
    name: str
