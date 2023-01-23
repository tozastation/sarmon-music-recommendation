from dataclasses import dataclass

from dataclasses_json import dataclass_json

from models.artist import Artist


@dataclass_json
@dataclass
class Track:
    id: str
    uri: str
    artists: list[Artist]
