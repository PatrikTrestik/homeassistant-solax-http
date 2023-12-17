from homeassistant.components.button import ButtonEntityDescription
from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.time import TimeEntityDescription
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntityDescription,
)
from dataclasses import dataclass

DOMAIN = "solax_http"

ATTR_MANUFACTURER = "SolaX Power"

DEFAULT_NAME = "SolaX API"
DEFAULT_SCAN_INTERVAL = 15
REQUEST_REFRESH_DELAY = 0.3
API_TIMEOUT = 10

CONF_SN = "serial_number"

U16 = "_uint16"
U32 = "_uint32"
S16 = "_int16"
S32 = "_int32"


# ==================================== plugin base class ====================================================================

@dataclass
class plugin_base:
    plugin_name: str
    TIME_TYPES: list[TimeEntityDescription]
    SENSOR_TYPES: list[SensorEntityDescription]
    BUTTON_TYPES: list[ButtonEntityDescription]
    NUMBER_TYPES: list[NumberEntityDescription]
    SELECT_TYPES: list[SelectEntityDescription]

    invertertype = None

    async def initialize(self)->None:
        pass

    def map_data(self, descr, data)->any:
        return None

    def map_payload(self, address, payload):
        return None

    def matchWithMask(self, entitymask, blacklist = None):
        return False

# =================================== base class for sensor entity descriptions =========================================

@dataclass
class BaseHttpSensorEntityDescription(SensorEntityDescription):
    """ base class for modbus sensor declarations """
    allowedtypes: int = 0 # overload with ALLDEFAULT from plugin
    scale: float = 1 # can be float, dictionary or callable function(initval, descr, datadict)
    read_scale_exceptions: list = None # additional scaling when reading from modbus
    blacklist: list = None
    unit: int = None # e.g. U16
    register: int = -1 # initialize with invalid register
    rounding: int = 1
    value_function: callable = None #  value = function(initval, descr, datadict)

@dataclass
class BaseHttpButtonEntityDescription(ButtonEntityDescription):
    allowedtypes: int = 0 # overload with ALLDEFAULT from plugin
    register: int = None
    command: int = None
    blacklist: list = None # none or list of serial number prefixes
    value_function: callable = None #  value = function(initval, descr, datadict)

@dataclass
class BaseHttpSwitchEntityDescription(SwitchEntityDescription):
    allowedtypes: int = 0 # overload with ALLDEFAULT from plugin
    register: int = None
    blacklist: list = None # none or list of serial number prefixes

@dataclass
class BaseHttpSelectEntityDescription(SelectEntityDescription):
    allowedtypes: int = 0 # overload with ALLDEFAULT from plugin
    register: int = None
    scale: dict = None
    unit: int = None
    rounding: int = 1
    reverse_option_dict: dict = None # autocomputed
    blacklist: list = None # none or list of serial number prefixes
    initvalue: int = None # initial default value for WRITE_DATA_LOCAL entities

@dataclass
class BaseHttpNumberEntityDescription(NumberEntityDescription):
    allowedtypes: int = 0 # overload with ALLDEFAULT from plugin
    register: int = None
    read_scale_exceptions: list = None
    read_scale: float = 1
    fmt: str = None
    unit: int = None
    scale: float = 1
    rounding: int = 1
    state: str = None
    max_exceptions: list = None   #  None or list with structue [ ('U50EC' , 40,) ]
    min_exceptions_minus: list = None # same structure as max_exceptions, values are applied with a minus
    blacklist: list = None # None or list of serial number prefixes like
    initvalue: int = None # initial default value for WRITE_DATA_LOCAL entities
    prevent_update: bool = False # if set to True, value will not be re-read/updated with each polling cycle; only when read value changes

@dataclass
class BaseHttpTimeEntityDescription(TimeEntityDescription):
    allowedtypes: int = 0 # overload with ALLDEFAULT from plugin
    register: int = None
    blacklist: list = None # None or list of serial number prefixes like


