"""
Module for working with SWGE Beacon data and emulating park beacons

This code is MIT licensed.
"""

from droid.utils import *

class OfficialDroidBeaconLocations(object):
    """
    Constants representing every official Walt Disney World and DisneyLand SWGE Droid Beacon
    """

    DL_Marketplace =        '0A040102A601'
    DL_BehindDroidDepot =   '0A040202A601'
    DL_Resistence =         '0A040302A601'
    DL_FirstOrder =         '0A040702A601'
    DL_DroidDepot =         '0A040318BA01'
    DL_InFrontOfOgas =      '0A0405FFA601'

    WDW_OutdoorsArea =      '0A040102A601'
    WDW_BehindDroidDepot =  '0A040202A601'
    WDW_Resistence =        '0A040302A601'
    WDW_DokOndars =         '0A040602A601'
    WDW_FirstOrder =        '0A040702A601'
    WDW_Marketplace =       '0A040618BA01'
    WDW_DroidDetector =     '0A0405FFA601'
    WDW_InFrontOfOgas =     '0A0407FFA601'

def create_location_beacon_payload(script_id: int, reaction_interval: int, signal_strength: int, droid_paired: bool = True) -> str:
    """
    Creates a Location beacon payload for getting an area based reaction out of a SWGE droid
    """

    beacon_payload = "0A04"
    beacon_payload += int_to_hex(script_id)
    beacon_payload += int_to_hex(reaction_interval)
    beacon_payload += dbm_to_hex(signal_strength)
    beacon_payload += "01" if droid_paired else "00"

    return beacon_payload.upper()

def decode_location_beacon_payload(payload: str) -> dict:
    """
    Decodes a SWGE location beacon payload into its various parts
    """

    script_id = hex_to_int(payload[4:6])
    reaction_interval = hex_to_int(payload[6:8])
    signal_strength = hex_to_dbm(payload[8:10])
    droid_paired = bool(hex_to_int(payload[10:12]))

    return { 'script_id': script_id, 'reaction_interval': reaction_interval, 'signal_strength': signal_strength, 'droid_paired': droid_paired }

def create_droid_beacon_payload(droid_paired: bool = True, affiliation_id: int = 1, personality_id: int = 1) -> str:
    """
    Creates a droid beacon payload for a droid given its paired state, affilitation id, and personality id
    """

    droid_paired_byte = 0x80 + int(droid_paired)
    affiliation_byte = (affiliation_id * 2) + 0x80
    personality_byte = personality_id
    hex_string = f"030444{droid_paired_byte:02X}{affiliation_byte:02X}{personality_byte:02X}"
    return hex_string

def decode_droid_beacon_payload(payload: str) -> dict:
    """
    Decodes a SWGE droid beacon payload into its various parts
    """

    data_length = hex_to_int(payload[4:6])  - 0x40
    droid_paired = hex_to_int(payload[6:8]) - 0x80
    affiliation_id = int((hex_to_int(payload[8:10]) - 0x80) / 2)
    personality_id = hex_to_int(payload[10:12])

    return { 'data_length': data_length, 'droid_paired': droid_paired, 'affiliation_id': affiliation_id, 'personality_id': personality_id }
