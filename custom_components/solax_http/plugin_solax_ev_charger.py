from dataclasses import dataclass
import datetime
import logging

from .entity_definitions import ALL_POW_GROUP, ALL_VER_GROUP, ALL_X_GROUP, S16
from .plugin_base import plugin_base

_LOGGER = logging.getLogger(__name__)


# ============================ plugin declaration =================================================


@dataclass
class solax_ev_charger_plugin(plugin_base):
    """Plugin for SolaX EV Charger integration."""

    serialnumber: str = None
    invertertype: int = None

    def map_payload(self, address, payload):
        """Map the payload to the corresponding register based on the address."""

        match address:
            case 0x60D:
                return [{"reg": 2, "val": f"{payload}"}]
            case 0x60C:
                return [{"reg": 1, "val": f"{payload}"}]
            case 0x60E:
                return [{"reg": 3, "val": f"{payload}"}]
            case 0x60F:
                return [{"reg": 4, "val": f"{payload}"}]
            case 0x610:
                return [{"reg": 5, "val": f"{payload}"}]
            case 0x613:
                return [{"reg": 11, "val": f"{payload}"}]
            case 0x618:
                return [{"reg": 22, "val": f"{payload}"}]
            case 0x625:
                return [{"reg": 70, "val": f"{payload}"}]
            case 0x628:
                return [{"reg": 82, "val": f"{payload}"}]
            case 0x634:
                if isinstance(payload, datetime.time):
                    time_val: datetime.time = payload
                    hour = time_val.hour
                    minute = time_val.minute
                    hm_payload = (hour << 8) + minute
                    return [{"reg": 12, "val": f"{hm_payload}"}]
                return None
            case 0x636:
                if isinstance(payload, datetime.time):
                    time_val: datetime.time = payload
                    hour = time_val.hour
                    minute = time_val.minute
                    hm_payload = (hour << 8) + minute
                    return [{"reg": 13, "val": f"{hm_payload}"}]
                return None
            case 0x638:
                if isinstance(payload, datetime.time):
                    time_val: datetime.time = payload
                    hour = time_val.hour
                    minute = time_val.minute
                    hm_payload = (hour << 8) + minute
                    return [{"reg": 15, "val": f"{hm_payload}"}]
                return None
            case 0x63A:
                return [{"reg": 14, "val": f"{payload}"}]
            case _:
                return None

    def map_data(self, descr, data) -> any:
        Set = data["Set"]
        Data = data["Data"]
        Info = data["Info"]

        return_value = None
        match descr.register:
            case 0xF001:
                # Y-M-D H:m:S
                year = Data.get(84) >> 8
                month = Data.get(84) & 0x00FF
                day = Data.get(83) >> 8
                hour = Data.get(83) & 0x00FF
                minute = Data.get(82) >> 8
                second = Data.get(82) & 0x00FF
                if month != 0:
                    return_value = datetime.datetime(
                        2000 + year, month, day, hour, minute, second
                    ).astimezone()
            case 0x600:
                return_value = Info.get(2)
            case 0x60C:
                return_value = Set.get(0)
            case 0x60D:
                return_value = Set.get(1)
            case 0x60E:
                return_value = Set.get(2)
            case 0x60F:
                return_value = Set.get(3)
            case 0x610:
                return_value = Set.get(4)
            case 0x613:
                return_value = Set.get(11)
            # case 0x615:
            #     return_value=Data[]
            # case 0x616:
            #     return_value=Data[]
            # case 0x61E: # RTC: Y-M-D H:m:S
            #     return_value=[Data[38]H, Data[38]L, Data[37]H, Data[37]L, Data[36]H, Data[36]L]
            case 0x625:
                return_value = Data.get(65)
            case 0x628:
                return_value = Set.get(76)
            case 0x634:
                val = Set.get(12)
                if val is not None:
                    hour = val >> 8
                    minute = val & 0x00FF
                    if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
                        return_value = datetime.time(hour, minute)
            case 0x636:
                val = Set.get(13)
                if val is not None:
                    hour = val >> 8
                    minute = val & 0x00FF
                    if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
                        return_value = datetime.time(hour, minute)
            case 0x638:
                val = Set.get(15)
                if val is not None:
                    hour = val >> 8
                    minute = val & 0x00FF
                    if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
                        return_value = datetime.time(hour, minute)
            case 0x63A:
                return_value = Set.get(14)
            case 0x0:
                return_value = Data.get(2)
            case 0x1:
                return_value = Data.get(3)
            case 0x2:
                return_value = Data.get(4)
            case 0x4:
                return_value = Data.get(5)
            case 0x5:
                return_value = Data.get(6)
            case 0x6:
                return_value = Data.get(7)
            case 0x8:
                return_value = Data.get(8)
            case 0x9:
                return_value = Data.get(9)
            case 0xA:
                return_value = Data.get(10)
            case 0xB:
                return_value = Data.get(11)
            case 0xC:
                return_value = Data.get(33)
            case 0xD:
                return_value = Data.get(34)
            case 0xE:
                return_value = Data.get(35)
            case 0xF:
                return_value = Data.get(12)
            case 0x10:
                datH = Data.get(15)
                datL = Data.get(14)
                if datH is not None and datL is not None:
                    return_value = datH * 65536 + datL
            case 0x12:
                return_value = Data.get(16)
            case 0x13:
                return_value = Data.get(17)
            case 0x14:
                return_value = Data.get(18)
            case 0x15:
                return_value = Data.get(19)
            case 0x16:
                return_value = Data.get(20)
            case 0x17:
                return_value = Data.get(21)
            case 0x18:
                return_value = Data.get(22)
            case 0x1C:
                return_value = Data.get(24)
            case 0x1D:
                return_value = Data.get(0)
            case 0x25:
                ver = str(Set.get(19))
                if ver is not None:
                    return_value = f"{ver[0]}.{ver[1:]}"
            case 0x2B:
                datH = Data.get(81)
                datL = Data.get(80)
                if datH is not None and datL is not None:
                    return_value = datH * 65536 + datL + 1
            case _:
                return_value = None

        if return_value is None:
            return None
        if descr.unit == S16 and return_value >= 32768:
            return_value = return_value - 65536
        if isinstance(descr.scale, dict):  # translate int to string
            return_value = descr.scale.get(return_value, "Unknown")
        elif callable(descr.scale):  # function to call ?
            return_value = descr.scale(return_value, descr)
        else:  # apply simple numeric scaling and rounding if not a list of words
            try:
                return_value = round(return_value * descr.scale, descr.rounding)
            except:
                pass  # probably a WORDS instance

        return return_value

    def matchWithMask(self, entitymask, blacklist=None):
        if self.invertertype is None or self.invertertype == 0:
            return False
        # returns true if the entity needs to be created for an inverter
        powmatch = ((self.invertertype & entitymask & ALL_POW_GROUP) != 0) or (
            entitymask & ALL_POW_GROUP == 0
        )
        xmatch = ((self.invertertype & entitymask & ALL_X_GROUP) != 0) or (
            entitymask & ALL_X_GROUP == 0
        )
        vermatch = ((self.invertertype & entitymask & ALL_VER_GROUP) != 0) or (
            entitymask & ALL_VER_GROUP == 0
        )
        blacklisted = False
        if blacklist:
            for start in blacklist:
                if self._serialnumber.startswith(start):
                    blacklisted = True
        return (powmatch and xmatch and vermatch) and not blacklisted
