_UNITS = {
    'KiB': 1024, 
    'MiB': 1024**2,
    'GiB': 1024**3,
    'TiB': 1024**4
}


def convert_to_bytes(size: str) -> int:
    num, unit = size.split()
    return int(float(num) * _UNITS[unit])
