import logging

log = logging.getLogger(__name__)


def get_layer_from_serial_number(serial_number):
    """
    Get the layer from the serial number.
    """
    if len(serial_number) != 14 or not serial_number.startswith("20U"):
        log.exception("Error: Please enter a valid ATLAS SN.")
        raise ValueError()

    if "PIMS" in serial_number or "PIR6" in serial_number:
        return "L0"

    if "PIM0" in serial_number or "PIR7" in serial_number:
        return "R0"

    if "PIM5" in serial_number or "PIR8" in serial_number:
        return "R0.5"

    if "PIM1" in serial_number or "PIRB" in serial_number:
        return "L1"

    if "PG" in serial_number:
        return "L2"

    log.exception("Invalid module SN: %s", serial_number)
    raise ValueError()


def chip_serial_number_to_uid(serial_number):
    """
    Convert chip serial number to hexadecimal UID.
    """
    assert serial_number.startswith(
        "20UPGFC"
    ), "Serial number must be for a valid RD53 chip"
    return hex(int(serial_number[-7:]))


def chip_uid_to_serial_number(uid):
    """
    Convert chip hexadecimal UID to serial number.
    """
    return f"20UPGFC{int(uid, 16):07}"


def get_chip_type_from_serial_number(serial_number):
    """
    Convert module SN or chip SN to chip type
    """
    if "FC" in serial_number.upper():
        serial_number = str(chip_serial_number_to_uid(serial_number))
        if int(serial_number[-5]) == 1:
            return "RD53B"
        if int(serial_number[-5]) >= 2:
            return "ITKPIXV2"
        log.exception("Invalid serial number: %s", serial_number)
        raise ValueError()

    if serial_number[7] in ["1", "2"]:
        return "RD53B"
    if serial_number[7] == "3":
        return "ITKPIXV2"
    log.exception("Invalid serial number: %s", serial_number)
    raise ValueError()


def get_chip_type_from_config(config):
    """
    Get chip type from keyword in chip config
    """
    chiptype = ""
    try:
        chiptype = next(iter(config.keys()))
    except IndexError:
        log.error("One of your chip configuration files is empty")

    if chiptype not in {"RD53B", "ITKPIXV2"}:
        log.warning(
            "Chip name in configuration not one of expected chip names (RD53B or ITKPIXV2)"
        )
    return chiptype
