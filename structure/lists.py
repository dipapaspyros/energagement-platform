SUPPORTED_CONNECTION_TYPES = (
    ('MODBUS', 'ModBus Connection'),
)

UNIT_TYPES = (
    ('GENERIC_BUILDING', 'Building'),
    ('FACTORY', 'Factory'),
    ('CHARGING_STATION', 'Charging station'),
)


def get_tupple_label(tt, t0):
    return [t[1] for t in tt if t[0] == t0][0]
