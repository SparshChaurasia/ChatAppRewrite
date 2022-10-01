import dataclasses
import pickle
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    msg: str
    author: str = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"[bold][red]\[{self.timestamp.strftime('%H:%M')}][/][green]\[{self.author}][/][/] {self.msg}"

    def encode_msg(self):
        serial_obj = pickle.dumps(self)
        return serial_obj
