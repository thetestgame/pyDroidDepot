"""
Module for working with SWGE Beacon data and emulating park beacons

This code is MIT licensed.
"""

from droiddepot.utils import *
from droiddepot.protocol import DisneyBLEManufacturerId
from bleak import BleakScanner
from threading import Thread
import logging
import asyncio

class DroidBeaconType(object):
    """
    Consants representing the beacon types that SWGE droids respond to.
    """

    DroidIdentificationBeacon = 3
    ParkLocationBeacon = 10

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

def get_beacon_header(beacon_type: int, data_length: int = 4) -> str:
    """
    Returns the header used by a SWGE Beacon
    """

    return int_to_hex(beacon_type) + int_to_hex(data_length)

def create_location_beacon_payload(script_id: int, reaction_interval: int, signal_strength: int, droid_paired: bool = True) -> str:
    """
    Creates a Location beacon payload for getting an area based reaction out of a SWGE droid
    """

    if script_id < 1 or script_id > 7:
        raise ValueError('Script ids outside of the range of 1-7 are not currently supported.')

    beacon_payload = get_beacon_header(DroidBeaconType.ParkLocationBeacon, 4)
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

    header = get_beacon_header(DroidBeaconType.DroidIdentificationBeacon, 4)
    droid_paired_byte = 0x80 + int(droid_paired)
    affiliation_byte = (affiliation_id * 2) + 0x80
    personality_byte = personality_id
    hex_string = f"{header}44{droid_paired_byte:02X}{affiliation_byte:02X}{personality_byte:02X}"

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

class DroidReactionBeaconScanner(object):
    """
    A class for scanning and decoding Disney BLE droid reaction beacons.
    """
    
    def __init__(self):
        """
        Initializes a new instance of the DroidReactionBeaconScanner class.
        """

        self.__location_handlers = []
        self.__droid_handlers = []

        self.__scan_loop = asyncio.new_event_loop()
        self.__scan_thread = None

    def add_location_handler(self, handler: object) -> None:
        """
        """

        if handler not in self.__location_handlers:
            self.__location_handlers.append(handler)

    def remove_location_handler(self, handler: object) -> None:
        """
        """

        if handler in self.__location_handlers:
            self.__location_handlers.remove(handler)

    def add_droid_handler(self, handler: object) -> None:
        """
        """

        if handler not in self.__droid_handlers:
            self.__droid_handlers.append(handler)

    def remove_droid_handler(self, handler: object) -> None:
        """
        """

        if handler in self.__droid_handlers:
            self.__droid_handlers.remove(handler)

    async def __scan(self) -> None:
        """
        Scans for nearby Disney BLE droid reaction beacons and decodes their data.
        """

        async with BleakScanner() as scanner:
            await scanner.start()

            while True:
                devices = scanner.discovered_devices_and_advertisement_data
                visible_droids = {}
                locations_in_range = {}
                
                for device_address in devices:
                    try:
                        # Check if the device is advertising with the expected manufacturer ID
                        device, data = devices[device_address]
                        if self.__is_droid_beacon(data.manufacturer_data):
                            beacon_payload = data.manufacturer_data[DisneyBLEManufacturerId.DroidManufacturerId]
                            beacon_payload = beacon_payload.hex()

                            # Decode the beacon data based on type
                            beacon_type = hex_to_int(beacon_payload[:2])
                            if beacon_type == DroidBeaconType.DroidIdentificationBeacon:
                                beacon_data = decode_droid_beacon_payload(beacon_payload)
                                visible_droids[device_address] = beacon_data
                            elif beacon_type == DroidBeaconType.ParkLocationBeacon:    
                                beacon_data = decode_location_beacon_payload(beacon_payload)
                                if beacon_data['signal_strength'] >= data.rssi:
                                    locations_in_range[device_address] = beacon_data
                            else:
                                logging.warning('Discovered unknown droid beacon type: %s' % beacon_type)
                    except Exception as e:
                        logging.error('An unexpected error occured processing bluetooth device: %s' % device_address)
                        logging.error(e, exc_info=True) 

                for handler in self.__location_handlers:
                    await handler(locations_in_range)

                for handler in self.__droid_handlers:
                    await handler(visible_droids)

                await asyncio.sleep(2)

    def __start_scan_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        Starts the beacon scanning event loop
        """

        asyncio.set_event_loop(loop)
        loop.run_forever()

    def __is_droid_beacon(self, data: dict) -> bool:
        """
        Checks if the given data contains data can a droid can react to.
        """

        return DisneyBLEManufacturerId.DroidManufacturerId in data

    def start(self) -> None:
        """
        Starts the beacon scanner
        """

        if self.__scan_loop.is_running():
            return

        self.__scan_thread = Thread(target=self.__start_scan_loop, args=(self.__scan_loop,), daemon=True)
        self.__scan_thread.start()
        asyncio.run_coroutine_threadsafe(self.__scan(), self.__scan_loop)

    def stop(self) -> None:
        """
        Stops the beacon scanner
        """

        if self.__scan_loop.is_running():
            self.__scan_loop.stop()
            self.__scan_thread.join()