"""Module provides the solax_ev_charger_plugin_G2 class for SolaX EV Charger integration."""

from dataclasses import dataclass
import logging

from .entity_definitions import POW7, POW11, POW22, S16, X1, X3
from .plugin_base import plugin_base

_LOGGER = logging.getLogger(__name__)


# ============================ plugin declaration =================================================


@dataclass
class solax_ev_charger_plugin_g2(plugin_base):
    """Plugin for SolaX EV Charger integration."""

    serialnumber: str = None
    invertertype: int = None
    hw_version: str = "G2"

    @property
    def inverter_model(self) -> str:
        """Return the inverter model based on the inverter type."""
        if (self.invertertype & X1) != 0:
            phase = "X1"
        elif (self.invertertype & X3) != 0:
            phase = "X3"
        else:
            phase = ""
        if (self.invertertype & POW7) != 0:
            p = "7kW"
        elif (self.invertertype & POW11) != 0:
            p = "11kW"
        elif (self.invertertype & POW22) != 0:
            p = "22kW"
        else:
            p = ""
        return f"{phase}-HAC-{p}"

    def map_payload(self, descr, value):
        """Map the payload to the corresponding register based on the address."""

        address = descr.register
        payload = self._reverse_scale(descr, value)

        match address:
            case 0x60D:  # Mode
                return [{"reg": 52, "val": f"{payload}"}]
            # case 0x60C:
            #     return [{"reg": 1, "val": f"{payload}"}]
            case 0x60E: # Eco Gear
                return [{"reg": 62, "val": f"{payload}"}]
            case 0x60F: # Green Gear
                return [{"reg": 63, "val": f"{payload}"}]
            # case 0x610:
            #     return [{"reg": 5, "val": f"{payload}"}]
            # case 0x613:
            #     return [{"reg": 11, "val": f"{payload}"}]
            # case 0x618:
            #     return [{"reg": 22, "val": f"{payload}"}]
            # case 0x625:
            #     return [{"reg": 70, "val": f"{payload}"}]
            case 0x668: #Max Charge Current
                return [{"reg": 54, "val": f"{payload}"}]
            case 0x669: # Charging Mode
                return [{"reg": 132, "val": f"{payload}"}]
            # case 0x634:
            #     if isinstance(payload, datetime.time):
            #         time_val: datetime.time = payload
            #         hour = time_val.hour
            #         minute = time_val.minute
            #         hm_payload = (hour << 8) + minute
            #         return [{"reg": 12, "val": f"{hm_payload}"}]
            #     return None
            # case 0x636:
            #     if isinstance(payload, datetime.time):
            #         time_val: datetime.time = payload
            #         hour = time_val.hour
            #         minute = time_val.minute
            #         hm_payload = (hour << 8) + minute
            #         return [{"reg": 13, "val": f"{hm_payload}"}]
            #     return None
            # case 0x638:
            #     if isinstance(payload, datetime.time):
            #         time_val: datetime.time = payload
            #         hour = time_val.hour
            #         minute = time_val.minute
            #         hm_payload = (hour << 8) + minute
            #         return [{"reg": 15, "val": f"{hm_payload}"}]
            #     return None
            # case 0x63A:
            #     return [{"reg": 14, "val": f"{payload}"}]
            case _:
                return None

    def map_data(self, descr, data) -> any:
        """Map data from the given dictionary based on the descriptor's register value."""

        Set = data["Set"]
        Data = data["Data"]
        Info = data["Info"]

        return_value = None
        match descr.register:
            # case 0xF001: #Min/Sec Last charge start
            #     # Y-M-D H:m:S
            #     year = Data.get(84) >> 8
            #     month = Data.get(84) & 0x00FF
            #     day = Data.get(83) >> 8
            #     hour = Data.get(83) & 0x00FF
            #     minute = Data.get(82) >> 8
            #     second = Data.get(82) & 0x00FF
            #     if month != 0:
            #         return_value = datetime.datetime(
            #             2000 + year, month, day, hour, minute, second
            #         ).astimezone()
            # case 0x600: #SN
            #     return_value = Info.get(2)
            # case 0x60C: #Grid Data Source
            #     return_value = Set.get(0)
            case 0x60D:  # Mode
                return_value = Set.get(1)
            case 0x60E: #Eco Gear
                 return_value = Set.get(11)
            case 0x60F: #Green Gear
                 return_value = Set.get(12)
            # case 0x610: #StartChargeMode
            #     return_value = Set.get(4)
            # case 0x613: #Smart boost Type
            #     return_value = Set.get(11)
            # case 0x615:
            #     return_value=Data[]
            # case 0x616:
            #     return_value=Data[]
            # case 0x61E: # RTC: Y-M-D H:m:S
            #     return_value=[Data[38]H, Data[38]L, Data[37]H, Data[37]L, Data[36]H, Data[36]L]
            # case 0x625:
            #     return_value = Data.get(65)
            case 0x668:  # Max Charge Current
                return_value = Set.get(3)
            case 0x669: # Charging Mode
                return_value = Set.get(81)
            # case 0x634: #Boost time start
            #     val = Set.get(12)
            #     if val is not None:
            #         hour = val >> 8
            #         minute = val & 0x00FF
            #         if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
            #             return_value = datetime.time(hour, minute)
            # case 0x636:
            #     val = Set.get(13)
            #     if val is not None:
            #         hour = val >> 8
            #         minute = val & 0x00FF
            #         if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
            #             return_value = datetime.time(hour, minute)
            # case 0x638: #Boost time
            #     val = Set.get(15)
            #     if val is not None:
            #         hour = val >> 8
            #         minute = val & 0x00FF
            #         if hour >= 0 and hour < 24 and minute >= 0 and minute < 60:
            #             return_value = datetime.time(hour, minute)
            # case 0x63A: #Boost charge
            #     return_value = Set.get(14)
            case 0x0:
                return_value = Data.get(3)
            case 0x1:
                return_value = Data.get(4)
            case 0x2:
                return_value = Data.get(5)
            case 0x4:
                return_value = Data.get(6)
            case 0x5:
                return_value = Data.get(7)
            case 0x6:
                return_value = Data.get(8)
            case 0x8:
                return_value = Data.get(9)
            case 0x9:
                return_value = Data.get(10)
            case 0xA:
                return_value = Data.get(11)
            case 0xB:
                return_value = Data.get(12)
            case 0xC:
                return_value = Data.get(33)
            case 0xD:
                return_value = Data.get(34)
            case 0xE:
                return_value = Data.get(35)
            case 0xF:  # E Actual Charge
                return_value = Data.get(13)
            case 0x10:
                datH = Data.get(16)
                datL = Data.get(15)
                if datH is not None and datL is not None:
                    return_value = datH * 65536 + datL
            # case 0x12: #EA1
            #     return_value = Data.get(16)
            # case 0x13:
            #     return_value = Data.get(17)
            # case 0x14:
            #     return_value = Data.get(18)
            # case 0x15: # EP1
            #     return_value = Data.get(19)
            # case 0x16:
            #     return_value = Data.get(20)
            # case 0x17:
            #     return_value = Data.get(21)
            # case 0x18: #Exces power
            #     return_value = Data.get(22)
            # case 0x1C: #T PCB
            #     return_value = Data.get(24)
            case 0x1D:
                return_value = Data.get(0)
            # case 0x25: #Firmware/ Factory reset
            #     ver = Set.get(19)
            #     if ver is not None:
            #         ver=str(ver)
            #         return_value = f"{ver[0]}.{ver[1:]}"
            case 0x2B:  # Charge time
                datH = Data.get(50)
                datL = Data.get(49)
                if datH is not None and datL is not None:
                    return_value = datH * 65536 + datL + 1
            case _:
                return_value = None

        if return_value is None:
            return None
        if descr.unit == S16 and return_value >= 32768:
            return_value = return_value - 65536

        return self._apply_scale(descr, return_value)
