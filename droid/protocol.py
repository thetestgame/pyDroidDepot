"""
"""

class DroidCommand(object):
    """
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
    """

    AudioControllerCommand = 0
    CenterRUnitHead = 1
    RotateRUnitHead = 2
    RotateRUnitHeadWithoutRamp = 3
    RotateBUnitHead = 4
    DriveBUnit = 5

