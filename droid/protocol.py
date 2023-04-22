"""
This module defines the DroidCommand and DroidMultipurposeCommand classes used to 
define the constant command identifiers to communicate with a SWGE droid.
"""

class DroidCommand(object):
    """
    A class representing the available droid commands.

    Constants:
        RetrieveFirmwareInformation (int): Command to retrieve firmware information.
        SetPairingLedState (int): Command to set the pairing LED state.
        SetRGBLedState (int): Command to set the RGB LED state.
        FlashPairingLed (int): Command to flash the pairing LED.
        SetMotorSpeed (int): Command to set the motor speed.
        UnusedCommand (int): An unused command.
        ScriptCommand (int): Command to execute a script.
        ScriptDelay (int): Command to delay script execution.
        MultipurposeCommand (int): Command to send a multipurpose command.
    """

    RetrieveFirmwareInformation = 1
    SetPairingLedState = 2
    SetRGBLedState = 3
    FlashPairingLed = 4
    SetMotorSpeed = 5
    UnusedCommand = 6
    ScriptCommand = 12
    ScriptDelay = 13
    MultipurposeCommand = 15

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

