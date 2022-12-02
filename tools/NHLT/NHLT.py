#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright(c) 2022 Intel Corporation. All rights reserved.
#
# Author: Marc Herbert <marc.herbert@intel.com>

import sys

# https://construct.readthedocs.io/en/latest/

# pylint:disable=unused-wildcard-import
from construct import *

# - https://github.com/acpica/acpica/blob/master/source/include/actbl.h
# - `iasl nhlt.dat` can show these
# - Intel® Smart Sound Technology NHLT Specification
ACPI_TABLE_HEADER = Struct(
    "Signature" / PaddedString(4, "ascii"),  # 'NHLT'
    "Length" / Int32ul,
    "Revision" / Byte,
    "Checksum" / Hex(Byte),
    "OemId" / PaddedString(6, "ascii"),
    "OemTableID" / PaddedString(8, "ascii"),
    "OemRevision" / Hex(Int32ul),
    "CreatorID" / PaddedString(4, "ascii"),
    "CreatorRevision" / Hex(Int32ul),
)

NHLT_TABLE_HEADER = Struct(
    "acpi_header" / ACPI_TABLE_HEADER,
    "ACPI_table_signature_not_NHLT" / Check(this.acpi_header.Signature == "NHLT"),
)


def sub_format(name, GUID):
    return Struct(name / Const(lib.unhexlify(GUID), HexDump(Bytes(16))))


# First matching value wins
SUB_FORMATS_MATCH = Select(
    sub_format("PCM", "0100000000001000800000AA00389B71"),
    HexDump(Bytes(16)),  # no match
)

WAVE_FORMAT = Struct(
    "wFormatTag" / Const(0xFFFE, Hex(Int16ul)),
    "nChannels" / Int16ul,
    "nSamplesPerSec" / Int32ul,
    "nAvgBytesPerSec" / Int32ul,
    "BlockAlign" / Int16ul,
    "wBitsPerSample" / Int16ul,
    "cbSize" / Const(22, Int16ul),  # length of the remaining fields
    "ValidBitsPerSample" / Int16ul,
    "dwChannelMask" / Int32ul,
    "gSubFormat" / SUB_FORMATS_MATCH,
)


SPECIFIC_CONFIG = Struct(
    "CapabilitiesSize" / Int32ul, "Capabilities" / HexDump(Bytes(this.CapabilitiesSize))
)

# sof/src/include/sof/drivers/dmic.h
DMIC_CONFIG = Struct(
    "DmicConfigSize" / Int32ul, "DmicConfigTODO" / HexDump(Bytes(this.DmicConfigSize))
)

FORMAT_CONFIG = Struct(
    "Format" / WAVE_FORMAT,
    "FormatConfiguration"
    / Switch(this._.linkType, {"DMIC": DMIC_CONFIG}, default=SPECIFIC_CONFIG),
)

LINK_TYPE = Enum(Byte, HDA=0, DSP=1, DMIC=2, SSP=3)

# - Intel® Smart Sound Technology NHLT Specification
ENDPOINT_DESC = Struct(
    "descLength" / Int32ul,
    "linkType" / LINK_TYPE,
    "InstanceId" / Byte,
    "VendorId" / Hex(Int16ul),
    "DeviceId" / Hex(Int16ul),
    "RevisionId" / Int16ul,
    "SubsystemId" / Int32ul,
    "DeviceType" / Byte,
    "Direction" / Byte,
    "VirtualBusId" / Byte,
    "EndpointConfig" / SPECIFIC_CONFIG,
    "FormatsCount" / Byte,
    "FormatsConfigs" / FORMAT_CONFIG[this.FormatsCount],
)


NHLT_TABLE = Struct(
    "NhltTableHeader" / NHLT_TABLE_HEADER,
    "EndpointCount" / Byte,
    "EndpointDescriptors" / ENDPOINT_DESC[this.EndpointCount],
)


def main(args):
    seq = NHLT_TABLE.parse_file(args[1])
    print(seq)


if __name__ == "__main__":
    main(sys.argv)
