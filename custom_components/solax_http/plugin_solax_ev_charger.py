from ctypes import cast
import datetime
import logging
from dataclasses import dataclass
from .const import S16, U16, U32, BaseHttpSwitchEntityDescription, plugin_base
from homeassistant.components.number.const import NumberDeviceClass
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory, UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfEnergy, UnitOfFrequency, UnitOfPower, UnitOfTemperature, UnitOfTime
from .const import BaseHttpButtonEntityDescription, BaseHttpNumberEntityDescription, BaseHttpSelectEntityDescription, BaseHttpSensorEntityDescription, BaseHttpTimeEntityDescription


_LOGGER = logging.getLogger(__name__)

""" ============================================================================================
bitmasks  definitions to characterize inverters, ogranized by group
these bitmasks are used in entitydeclarations to determine to which inverters the entity applies
within a group, the bits in an entitydeclaration will be interpreted as OR
between groups, an AND condition is applied, so all gruoups must match.
An empty group (group without active flags) evaluates to True.
example: GEN3 | GEN4 | X1 | X3 | EPS
means:  any inverter of tyoe (GEN3 or GEN4) and (X1 or X3) and (EPS)
An entity can be declared multiple times (with different bitmasks) if the parameters are different for each inverter type
"""

POW7           = 0x0001
POW11          = 0x0002
POW22          = 0x0004
ALL_POW_GROUP  = POW7 | POW11 | POW22

X1             = 0x0100
X3             = 0x0200
ALL_X_GROUP    = X1 | X3

ALLDEFAULT = 0 # should be equivalent to HYBRID | AC | GEN2 | GEN3 | GEN4 | X1 | X3

# ======================= end of bitmask handling code =============================================

SENSOR_TYPES = []
# =================================================================================================

@dataclass
class SolaXEVChargerHttpButtonEntityDescription(BaseHttpButtonEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolaXEVChargerHttpSwitchEntityDescription(BaseHttpSwitchEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolaXEVChargerHttpNumberEntityDescription(BaseHttpNumberEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolaXEVChargerHttpTimeEntityDescription(BaseHttpNumberEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolaXEVChargerHttpSelectEntityDescription(BaseHttpSelectEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolaXEVChargerHttpSensorEntityDescription(BaseHttpSensorEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

# ====================================== Computed value functions  =================================================

# ================================= Button Declarations ============================================================

BUTTON_TYPES = [
    # SolaXEVChargerHttpButtonEntityDescription(
    #     name = "Sync RTC",
    #     key = "sync_rtc",
    #     register = 0x61E,
    #     icon = "mdi:home-clock",
    #     value_function = value_function_sync_rtc,
    # ),
]

# ================================= Switch Declarations ============================================================

SWITCH_TYPES = [
    # SolaXEVChargerHttpSwitchEntityDescription(
    #     name = "Boost set",
    #     key = "boost_set",
    #     register = 0x61E,
    #     icon = "mdi:home-clock",
    #     value_function = value_function_sync_rtc,
    # ),
]
# ================================= Time Declarations ============================================================

TIME_TYPES = [
    ###
    #
    #  Normal time types
    #
    ###
    SolaXEVChargerHttpTimeEntityDescription(
        name = "Timed boost start",
        key = "timed_boost_start",
        register = 0x634,
    ),
    SolaXEVChargerHttpTimeEntityDescription(
        name = "Timed boost end",
        key = "timed_boost_end",
        register = 0x636,
    ),
    SolaXEVChargerHttpTimeEntityDescription(
        name = "Smart boost end",
        key = "smart_boost_end",
        register = 0x638,
    ),
]

# ================================= Number Declarations ============================================================

NUMBER_TYPES = [
    ###
    #
    # Data only number types
    #
    ###

    ###
    #
    #  Normal number types
    #
    ###
    # SolaXEVChargerHttpNumberEntityDescription(
    #     name = "Datahub Charge Current",
    #     key = "datahub_charge_current",
    #     register = 0x624,
    #     fmt = "f",
    #     native_min_value = 6,
    #     native_max_value = 32,
    #     native_step = 0.1,
    #     scale = 0.01,
    #     native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
    #     device_class = NumberDeviceClass.CURRENT,
    # ),
    SolaXEVChargerHttpNumberEntityDescription(
        name = "Max Charge Current Setting",
        key = "max_charge_current_setting",
        register = 0x628,
        fmt = "f",
        native_min_value = 6,
        native_max_value = 16,
        native_step = 1,
        scale = 1,
        allowedtypes = POW11,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = NumberDeviceClass.CURRENT,
    ),
    SolaXEVChargerHttpNumberEntityDescription(
        name = "Max Charge Current Setting",
        key = "max_charge_current_setting",
        register = 0x628,
        fmt = "f",
        native_min_value = 6,
        native_max_value = 32,
        native_step = 1,
        scale = 1,
        allowedtypes = POW7 | POW22,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = NumberDeviceClass.CURRENT,
    ),
    SolaXEVChargerHttpNumberEntityDescription(
        name = "Smart boost energy",
        key = "smart_boost_energy",
        register = 0x63A,
        fmt = "f",
        native_min_value = 0,
        native_max_value = 100,
        native_step = 1,
        scale = 1,
        native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR,
        device_class = NumberDeviceClass.ENERGY,
    ),
]

# ================================= Select Declarations ============================================================

SELECT_TYPES = [
    ###
    #
    #  Normal select types
    #
    ###
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Meter Setting",
        key = "meter_setting",
        register = 0x60C,
        scale = {
            0: "External CT",
            1: "External Meter",
            2: "Inverter", },
        entity_registry_enabled_default = False,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:meter-electric",
    ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Charger Use Mode",
        key = "charger_use_mode",
        register = 0x60D,
        scale = {
            0: "Stop",
            1: "Fast",
            2: "ECO",
            3: "Green", },
        icon = "mdi:dip-switch",
    ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Charger Green Mode Level",
        key = "charger_green_mode",
        register = 0x60F,
        scale = {
            3: "3A",
            6: "6A",
            },
        icon = "mdi:dip-switch",
    ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Charger Eco Mode Level",
        key = "charger_eco_mode",
        register = 0x60E,
        scale = {
            6: "6A",
            10: "10A",
            16: "16A",
            20: "20A",
            25: "25A",
            },
        icon = "mdi:dip-switch",
        allowedtypes = POW7 | POW22,
    ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Charger Eco Mode Level",
        key = "charger_eco_mode",
        register = 0x60E,
        scale = {
            6: "6A",
            10: "10A"
            },
        icon = "mdi:dip-switch",
        allowedtypes = POW11,
    ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Start Charge Mode",
        key = "start_charge_mode",
        register = 0x610,
        scale =  {
            0: "Plug & Charge",
            1: "RFID to Charge", },
        icon = "mdi:lock",
    ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Boost Mode",
        key = "boost_mode",
        register = 0x613,
        scale =  {
            0: "Normal",
            1: "Timer Boost",
            2: "Smart Boost", },
        icon = "mdi:dip-switch",
    ),
    # SolaXEVChargerHttpSelectEntityDescription(
    #     name = "Device Lock",
    #     key = "device_lock",
    #     register = 0x615,
    #     option_dict =  {
    #         0: "Unlock",
    #         1: "Lock", },
    #     icon = "mdi:lock",
    # ),
    # SolaXEVChargerHttpSelectEntityDescription(
    #     name = "RFID Program",
    #     key = "rfid_program",
    #     register = 0x616,
    #     option_dict =  {
    #         0: "Program New",
    #         1: "Program Off", },
    #     icon = "mdi:dip-switch",
    # ),
    SolaXEVChargerHttpSelectEntityDescription(
        name = "Charge Phase",
        key = "charge_phase",
        register = 0x625,
        scale =  {
            0: "Three Phase",
            1: "L1 Phase",
            2: "L2 Phase",
            3: "L3 Phase", },
        icon = "mdi:dip-switch",
    ),
    # SolaXEVChargerHttpSelectEntityDescription(
    #     name = "Control Command",
    #     key = "control_command",
    #     register = 0x627,
    #     option_dict =  {
    #         1: "Available",
    #         2: "Unavailable",
    #         3: "Stop charging",
    #         4: "Start Charging",
    #         5: "Reserve",
    #         6: "Cancel the Reservation", },
    #     icon = "mdi:dip-switch",
    # ),
]

# ================================= Sennsor Declarations ============================================================

SENSOR_TYPES_MAIN: list[SolaXEVChargerHttpSensorEntityDescription] = [
    ###
    #
    # Holding
    #
    ###
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge start time",
        key = "charge_start_time",
        register = 0xF001,
        device_class = SensorDeviceClass.TIMESTAMP,
        entity_registry_enabled_default = True,
        icon = "mdi:clock",
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "CT Meter Setting",
        key = "ct_meter_setting",
        register = 0x60C,
        scale = {
            0: "External CT",
            1: "External Meter",
            2: "Inverter", },
        entity_registry_enabled_default = False,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:meter-electric",
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charger Use Mode",
        key = "charger_use_mode",
        register = 0x60D,
        scale = {
            0: "Stop",
            1: "Fast",
            2: "ECO",
            3: "Green", },
        entity_registry_enabled_default = False,
        icon = "mdi:dip-switch",
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Start Charge Mode",
        key = "start_charge_mode",
        register = 0x610,
        scale = {
            0: "Plug & Charge",
            1: "RFID to Charge", },
        entity_registry_enabled_default = False,
        icon = "mdi:lock",
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Boost Mode",
        key = "boost_mode",
        register = 0x613,
        scale = {
            0: "Normal",
            1: "Timer Boost",
            2: "Smart Boost", },
        entity_registry_enabled_default = False,
        icon = "mdi:dip-switch",
    ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "Device Lock",
    #     key = "device_lock",
    #     register = 0x615,
    #     scale = {
    #         0: "Unlock",
    #         1: "Lock", },
    #     entity_registry_enabled_default = False,
    #     icon = "mdi:lock",
    # ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "RFID Program",
    #     key = "rfid_program",
    #     register = 0x616,
    #     scale = {
    #         0: "Program New",
    #         1: "Program Off", },
    #     entity_registry_enabled_default = False,
    #     icon = "mdi:dip-switch",
    # ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "RTC",
    #     key = "rtc",
    #     register = 0x61E,
    #     unit = WORDS,
    #     wordcount = 6,
    #     scale = value_function_rtc,
    #     entity_registry_enabled_default = False,
    #     entity_category = EntityCategory.DIAGNOSTIC,
    #     icon = "mdi:clock",
    # ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "Datahub Charge Current",
    #     key = "datahub_charge_current",
    #     register = 0x624,
    #     scale = 0.01,
    #     rounding = 1,
    #     native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
    #     device_class = SensorDeviceClass.CURRENT,
    #     allowedtypes = HYBRID,
    #     entity_registry_enabled_default = False,
    # ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "Charge Phase",
    #     key = "charge_phase",
    #     register = 0x625,
    #     scale = {
    #         0: "Three Phase",
    #         1: "L1 Phase",
    #         2: "L2 Phase",
    #         3: "L3 Phase", },
    #     allowedtypes = X3,
    #     entity_registry_enabled_default = False,
    #     icon = "mdi:dip-switch",
    # ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Max Charge Current",
        key = "max_charge_current",
        register = 0x628,
        scale = 1,
        rounding = 0,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        entity_registry_enabled_default = False,
    ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "Control Command",
    #     key = "control_command",
    #     register = 0x627,
    #     scale = {
    #         1: "Available",
    #         2: "Unavailable",
    #         3: "Stop charging",
    #         4: "Start Charging",
    #         5: "Reserve",
    #         6: "Cancel the Reservation", },
    #     entity_registry_enabled_default = False,
    #     icon = "mdi:dip-switch",
    # ),
    ###
    #
    # Input
    #
    ###
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Voltage",
        key = "charge_voltage",
        register = 0x0,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        allowedtypes = X1,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Voltage L1",
        key = "charge_voltage_l1",
        register = 0x0,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Voltage L2",
        key = "charge_voltage_l2",
        register = 0x1,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Voltage L3",
        key = "charge_voltage_l3",
        register = 0x2,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "Charge PE Voltage",
    #     key = "charge_pe_voltage",
    #     register = 0x3,
    #     scale = 0.01,
    #     native_unit_of_measurement = UnitOfElectricPotential.VOLT,
    #     device_class = SensorDeviceClass.VOLTAGE,
    #     entity_registry_enabled_default = False,
    # ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Current",
        key = "charge_current",
        register = 0x4,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X1,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Current L1",
        key = "charge_current_l1",
        register = 0x4,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X3,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Current L2",
        key = "charge_current_l2",
        register = 0x5,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X3,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Current L3",
        key = "charge_current_l3",
        register = 0x6,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X3,
    ),
    # SolaXEVChargerHttpSensorEntityDescription(
    #     name = "Charge PE Current",
    #     key = "charge_pe_current",
    #     register = 0x7,
    #     register_type = REG_INPUT,
    #     native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE,
    #     device_class = SensorDeviceClass.CURRENT,
    #     entity_registry_enabled_default = False,
    # ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Power",
        key = "charge_power",
        register = 0x8,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X1,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Power L1",
        key = "charge_power_l1",
        register = 0x8,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Power L2",
        key = "charge_power_l2",
        register = 0x9,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Power L3",
        key = "charge_power_l3",
        register = 0xA,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Power Total",
        key = "charge_power_total",
        register = 0xB,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Time",
        key = "charge_time",
        register = 0x2B,
        native_unit_of_measurement = UnitOfTime.SECONDS,
        device_class = SensorDeviceClass.DURATION,
        state_class = SensorStateClass.TOTAL,
        entity_registry_enabled_default = True,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Frequency",
        key = "charge_frequency",
        register = 0xC,
        scale = 0.01,
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        allowedtypes = X1,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Frequency L1",
        key = "charge_frequency_l1",
        register = 0xC,
        scale = 0.01,
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Frequency L2",
        key = "charge_frequency_l2",
        register = 0xD,
        scale = 0.01,
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Frequency L3",
        key = "charge_frequency_l3",
        register = 0xE,
        scale = 0.01,
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Added",
        key = "charge_added",
        register = 0xF,
        scale = 0.1,
        native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR,
        device_class = SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charge Added Total",
        key = "charge_added_total",
        register = 0x10,
        unit = U32,
        scale = 0.1,
        native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR,
        device_class = SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Current",
        key = "grid_current",
        register = 0x12,
        unit = S16,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X1,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Current L1",
        key = "grid_current_l1",
        register = 0x12,
        unit = S16,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Current L2",
        key = "grid_current_l2",
        register = 0x13,
        unit = S16,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Current L3",
        key = "grid_current_l3",
        register = 0x14,
        unit = S16,
        scale = 0.01,
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Power",
        key = "grid_power",
        register = 0x15,
        unit = S16,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X1,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Power L1",
        key = "grid_power_l1",
        register = 0x15,
        unit = S16,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Power L2",
        key = "grid_power_l2",
        register = 0x16,
        unit = S16,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Grid Power L3",
        key = "grid_power_l3",
        register = 0x17,
        unit = S16,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = X3,
        entity_registry_enabled_default = False,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Available PV Power",
        key = "available_pv_power",
        register = 0x18,
        unit = S16,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default = True,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Charger Temperature",
        key = "charger_temperature",
        register = 0x1C,
        native_unit_of_measurement = UnitOfTemperature.CELSIUS,
        device_class = SensorDeviceClass.TEMPERATURE,
        state_class = SensorStateClass.MEASUREMENT,
        entity_category = EntityCategory.DIAGNOSTIC,
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Run Mode",
        key = "run_mode",
        unit = U16,
        register = 0x1D,
        scale = { 0: "Available",
                  1: "Preparing",
                  2: "Charging",
                  3: "Finishing",
                  4: "Fault Mode",
                  5: "Unavailable",
                  6: "Reserved",
                  7: "Suspended EV",
                  8: "Suspended EVSE",
                  9: "Update",
                 10: "RFID Activation", },
        icon = "mdi:run",
    ),
    SolaXEVChargerHttpSensorEntityDescription(
        name = "Firmware Version",
        key = "firmwareversion",
        register = 0x25,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:information",
    ),
]

# ============================ plugin declaration =================================================

@dataclass
class solax_ev_charger_plugin(plugin_base):
    _serialnumber:str=None
    invertertype=None

    async def initialize(self, data):
        self._serialnumber=await self._read_serialnr(data)
        self.invertertype=await self._determine_type()

    def map_payload(self, address, payload):
        match address:
            case 0x60D:
                return [{"reg":2,"val":f"{payload}"}]
            case 0x60C:
                return [{"reg":1,"val":f"{payload}"}]
            case 0x60E:
                return [{"reg":3,"val":f"{payload}"}]
            case 0x60F:
                return [{"reg":4,"val":f"{payload}"}]
            case 0x610:
                return [{"reg":5,"val":f"{payload}"}]
            case 0x613:
                return [{"reg":11,"val":f"{payload}"}]
            case 0x625:
                return [{"reg":70,"val":f"{payload}"}]
            case 0x628:
                return [{"reg":82,"val":f"{payload}"}]
            case 0x634:
                if isinstance(payload, datetime.time):
                    time_val:datetime.time=payload
                    hour=time_val.hour
                    minute=time_val.minute
                    hm_payload=(hour << 8) + minute
                    return [{"reg":12,"val":f"{hm_payload}"}]
                return None
            case 0x636:
                if isinstance(payload, datetime.time):
                    time_val:datetime.time=payload
                    hour=time_val.hour
                    minute=time_val.minute
                    hm_payload=(hour << 8) + minute
                    return [{"reg":13,"val":f"{hm_payload}"}]
                return None
            case 0x638:
                if isinstance(payload, datetime.time):
                    time_val:datetime.time=payload
                    hour=time_val.hour
                    minute=time_val.minute
                    hm_payload=(hour << 8) + minute
                    return [{"reg":15,"val":f"{hm_payload}"}]
                return None
            case 0x63A:
                return [{"reg":14,"val":f"{payload}"}]
            case _:
                return None

    def map_data(self, descr, data)->any:
        Set=data['Set']
        Data=data['Data']
        Info=data['Info']

        return_value=None
        match descr.register:
            case 0xF001:
                #Y-M-D H:m:S
                year=Data.get(84) >> 8
                month=Data.get(84) & 0x00FF
                day=Data.get(83) >> 8
                hour=Data.get(83) & 0x00FF
                minute=Data.get(82) >> 8
                second=Data.get(82) & 0x00FF
                if month!=0:
                    return_value=datetime.datetime(2000+year,month,day,hour,minute,second).astimezone()
            case 0x600:
                return_value=Info.get(2)
            case 0x60C:
                return_value=Set.get(0)
            case 0x60D:
                return_value=Set.get(1)
            case 0x60E:
                return_value=Set.get(2)
            case 0x60F:
                return_value=Set.get(3)
            case 0x610:
                return_value=Set.get(4)
            case 0x613:
                return_value=Set.get(11)
            # case 0x615:
            #     return_value=Data[]
            # case 0x616:
            #     return_value=Data[]
            # case 0x61E: # RTC: Y-M-D H:m:S
            #     return_value=[Data[38]H, Data[38]L, Data[37]H, Data[37]L, Data[36]H, Data[36]L]
            case 0x625:
                return_value=Data.get(65)
            case 0x628:
                return_value=Set.get(76)
            case 0x634:
                val=Set.get(12)
                if val is not None:
                    hour=val >> 8
                    minute=val & 0x00FF
                    if hour>=0 and hour<24 and minute>=0 and minute<60:
                        return_value=datetime.time(hour, minute)
            case 0x636:
                val=Set.get(13)
                if val is not None:
                    hour=val >> 8
                    minute=val & 0x00FF
                    if hour>=0 and hour<24 and minute>=0 and minute<60:
                        return_value=datetime.time(hour, minute)
            case 0x638:
                val=Set.get(15)
                if val is not None:
                    hour=val >> 8
                    minute=val & 0x00FF
                    if hour>=0 and hour<24 and minute>=0 and minute<60:
                        return_value=datetime.time(hour, minute)
            case 0x63A:
                return_value=Set.get(14)
            case 0x0:
                return_value=Data.get(2)
            case 0x1:
                return_value=Data.get(3)
            case 0x2:
                return_value=Data.get(4)
            case 0x4:
                return_value=Data.get(5)
            case 0x5:
                return_value=Data.get(6)
            case 0x6:
                return_value=Data.get(7)
            case 0x8:
                return_value=Data.get(8)
            case 0x9:
                return_value=Data.get(9)
            case 0xA:
                return_value=Data.get(10)
            case 0xB:
                return_value=Data.get(11)
            case 0xC:
                return_value=Data.get(33)
            case 0xD:
                return_value=Data.get(34)
            case 0xE:
                return_value=Data.get(35)
            case 0xF:
                return_value=Data.get(12)
            case 0x10:
                datH=Data.get(15)
                datL=Data.get(14)
                if datH is not None and datL is not None:
                    return_value=datH*65536+datL
            case 0x12:
                return_value=Data.get(16)
            case 0x13:
                return_value=Data.get(17)
            case 0x14:
                return_value=Data.get(18)
            case 0x15:
                return_value=Data.get(19)
            case 0x16:
                return_value=Data.get(20)
            case 0x17:
                return_value=Data.get(21)
            case 0x18:
                return_value=Data.get(22)
            case 0x1C:
                return_value=Data.get(24)
            case 0x1D:
                return_value=Data.get(0)
            case 0x25:
                ver=str(Set.get(19))
                if ver is not None:
                    return_value=f'{ver[0]}.{ver[1:]}'
            case 0x2B:
                datH=Data.get(81)
                datL=Data.get(80)
                if datH is not None and datL is not None:
                    return_value=datH*65536+datL+1
            case _:
                return_value=None

        if return_value is None:
            return None
        if descr.unit == S16 and return_value >= 32768:
            return_value=return_value - 65536
        if isinstance(descr.scale, dict): # translate int to string
            return_value = descr.scale.get(return_value, "Unknown")
        elif callable(descr.scale):  # function to call ?
            return_value = descr.scale(return_value, descr)
        else: # apply simple numeric scaling and rounding if not a list of words
            try:
                return_value = round(return_value*descr.scale, descr.rounding)
            except:
                pass # probably a WORDS instance

        return return_value

    async def _read_serialnr(self, data):
        res=data['Info'].get(2)
        if res is None:
            _LOGGER.warning(f"Attempt to read serialnumber failed")
            return "unknown"
        _LOGGER.info(f"Read serial number: {res}")
        return res


    async def _determine_type(self):
        _LOGGER.info(f"Trying to determine inverter type")

        # derive invertertupe from seriiesnumber
        # Adding support for G1.1 (C1071). If required add new flag to distinguish G1.0 (C1070) and G1.1
        if   self._serialnumber.startswith('C107'):  
            invertertype = X1 | POW7 # 7kW EV Single Phase
        elif self._serialnumber.startswith('C3110'):  
            invertertype = X3 | POW11 # 11kW EV Three Phase
        elif self._serialnumber.startswith('C3220'):  
            invertertype = X3 | POW22 # 22kW EV Three Phase
        # add cases here
        else:
            invertertype = 0
            _LOGGER.error(f"unrecognized inverter type - serial number : {self._serialnumber}")
        return invertertype

    def matchWithMask(self, entitymask, blacklist = None):
        if self.invertertype is None or self.invertertype==0:
            return False
        # returns true if the entity needs to be created for an inverter
        powmatch = ((self.invertertype & entitymask & ALL_POW_GROUP)  != 0) or (entitymask & ALL_POW_GROUP  == 0)
        xmatch   = ((self.invertertype & entitymask & ALL_X_GROUP)    != 0) or (entitymask & ALL_X_GROUP    == 0)
        blacklisted = False
        if blacklist:
            for start in blacklist:
                if self._serialnumber.startswith(start) : blacklisted = True
        return (powmatch and xmatch) and not blacklisted

def get_plugin_instance():
    return solax_ev_charger_plugin(
        plugin_name = 'solax_ev_charger',
        TIME_TYPES=TIME_TYPES,
        SENSOR_TYPES = SENSOR_TYPES_MAIN,
        NUMBER_TYPES = NUMBER_TYPES,
        BUTTON_TYPES = BUTTON_TYPES,
        SELECT_TYPES = SELECT_TYPES,
        )
