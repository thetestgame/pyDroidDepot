"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.

This module defines the DroidCommandId and DroidMultipurposeCommand classes used to 
define the constant command identifiers to communicate with a SWGE droid.
"""

from enum import IntEnum

class DisneyBLEManufacturerId(object):
    """
    Constants representing the types of BLE beacons found in Disney parks.
    """

    DisneyiBeacon = 76
    DroidManufacturerId = 387

class DroidBluetoothCharacteristics(object):
    """
    a constants class representing the characteristics available on droid depot droids
    """

    DroidCommandCharacteristic = '09b600b1-3e42-41fc-b474-e9c0c8f0c801'
    DroidNotifyCharacteristic = '09b600b0-3e42-41fc-b474-e9c0c8f0c801'

class DroidCommandId(IntEnum):
    """
    A enum representing the available droid commands.

    Constants:
        RetrieveFirmwareInformation (int): Command to retrieve firmware information.
        SetPairingLedState (int): Command to set the pairing LED state.
        SetRGBLedState (int): Command to set the RGB LED state.
        FlashPairingLed (int): Command to flash the pairing LED.
        SetMotorSpeed (int): Command to set the motor speed.
        UnusedCommand (int): An unused command.
        ScriptActionComand (int): Command to execute a script.
        ScriptDelay (int): Command to delay script execution.
        MultipurposeCommand (int): Command to send a multipurpose command.
    """

    RetrieveFirmwareInformation = 1
    SetPairingLedState = 2
    SetRGBLedState = 3
    FlashPairingLed = 4
    SetMotorSpeed = 5
    ScriptWriteCommand = 6
    ScriptActionComand = 12
    ScriptDelay = 13
    ConnectionHeartbeat = 14
    MultipurposeCommand = 15

    RUnitHeadEvent = 128
    RetrieveFirmwareInformationResponse = 129

    @classmethod
    def valid_command(cls, value: int) -> bool:
        """
        Checks if the command id is valid
        """

        return value in cls._value2member_map_ 

class DroidMultipurposeCommand(object):
    """
    A class representing the available multipurpose commands.

    Constants:
        AudioControllerCommand (int): Command to send an audio control command.
        CenterRUnitHead (int): Command to center the R-unit head.
        RotateRUnitHead (int): Command to rotate the R-unit head.
        RotateRUnitHeadWithoutRamp (int): Command to rotate the R-unit head without ramp.
        RotateBUnitHead (int): Command to rotate the B-unit head.
        DriveBUnit (int): Command to drive the B-unit.
    """

    AudioControllerCommand = 0
    CenterRUnitHead = 1
    RotateRUnitHead = 2
    RotateRUnitHeadWithoutRamp = 3
    RotateBUnitHead = 4
    DriveBUnit = 5

class DroidAffiliation(object):
    """
    Represents a droid's affiliation for BLE interactions and audio playback.
    """

    Scoundrel = 1
    Resistenace = 5
    FirstOrder = 9