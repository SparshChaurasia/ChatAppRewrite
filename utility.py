import dataclasses
from dataclasses import dataclass, field
from datetime import datetime
import pickle

# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""

#     if isinstance(obj, datetime):
#         return obj.isoformat()
#     raise TypeError ("Type %s not serializable" % type(obj))

@dataclass
class Message:
    msg: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"{self.timestamp}: {self.msg}"

    def encode_msg(self):
        serial_obj = pickle.dumps(self)
        return serial_obj
