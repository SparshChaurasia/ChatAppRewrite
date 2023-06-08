import dataclasses
import pickle
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

MType = Enum("mtype", "CHAT MSG")


@dataclass
class Message:
    msg: str
    author: str = None
    # mtype: MType = MType.CHAT
    mtype: str = "CHAT"
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"[bold][red]\[{self.timestamp.strftime('%H:%M')}][/][green]\[{self.author}][/][/] {self.msg}"

    def encode_msg(self):
        serial_obj = pickle.dumps(self)
        return serial_obj
