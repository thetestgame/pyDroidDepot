"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.

This modules defines classes and helper functions for working with SWGE droid hardware. 
"""

DroidFirmwareVersion = '4b1001444411110100000000'

class DroidAudioBankIdentifier(object):
    """
    A collection of identifiers used to represent available audio banks of a droid or its connected personality chip. 
    These are used in audio playback.
    """

    GeneralUseAudioBank = 1
    DroidDepotAudioBank = 2
    ResistenceAudioBank = 3
    UnknownAudioBank = 4
    DroidDetectorAudioBank = 5
    DokOndarsAudioBank = 6
    FirstOrderAudioBank = 7
    InitialActivationAudioBank = 8
    MotorSoundAudioBank = 9
    EmptyAudioBank = 10
    BlasterAcessoryAudioBank = 11
    ThrusterAccessoryAudioBank = 12

    TalkingBanks = [
        DroidDepotAudioBank,
        ResistenceAudioBank,
        UnknownAudioBank,
        DokOndarsAudioBank,
        FirstOrderAudioBank]

class DroidAffiliation(object):
    """
    Represents a droid's affiliation for BLE interactions and audio playback.
    """

    Scoundrel = 1
    Resistenace = 5
    FirstOrder = 9

class DroidPersonalityIdentifier(object):
    """
    A collection of identifiers used to represent various types of personality chips for audio and
    affiliation lookup.

    Attributes:
        Blue (int): Identifier for the blue personality chip.
        Gray (int): Identifier for the gray personality chip.
        Red (int): Identifier for the red personality chip.
        Orange (int): Identifier for the orange personality chip.
        Purple (int): Identifier for the purple personality chip.
        Black (int): Identifier for the black personality chip.
        Red2 (int): Identifier for the Red 2 personality chip. Same value as CB23.
        Yellow (int): Identifier for the yellow personality chip.
        DarkBlue (int): Identifier for the dark blue personality chip.

        C110P (int): Identifier for the C1-10P droid.
        CB23 (int): Identifier for the CB-23 droid.
        BUnit (int): Identifier for the BD unit droid.
        RUnit (int): Identifier for the R unit droid.
        BBUnit (int): Identifier for the BB unit droid.

        ChipAudioCount (dict): Dictionary containing a total count of available audio by audio bank id and by droid/personality chip
    """

    # Personality Chips
    Blue = 3
    Gray = 4
    Red = 5
    Orange = 6
    Purple = 7
    Black = 8
    Yellow = 10
    Red2 = 11
    DarkBlue = 13

    # Droids
    BUnit = 1
    RUnit = 2
    CB23 = 9
    C110P = 11
    DO = 12
    BBUnit = 14  

    ChipAudioCount = {
        DroidAudioBankIdentifier.GeneralUseAudioBank:           { Blue: 5, Gray: 4, Red: 5, Orange: 5, Purple: 4, Black: 3, Red2: 5, CB23: 5, C110P: 6,  Yellow: 4, DarkBlue: 4, BUnit: 5, RUnit: 4, BBUnit: 5 },
        DroidAudioBankIdentifier.DroidDepotAudioBank:           { Blue: 5, Gray: 5, Red: 5, Orange: 5, Purple: 4, Black: 6, Red2: 5, CB23: 5, C110P: 13, Yellow: 5, DarkBlue: 4, BUnit: 6, RUnit: 4, BBUnit: 3 },
        DroidAudioBankIdentifier.ResistenceAudioBank:           { Blue: 5, Gray: 5, Red: 5, Orange: 5, Purple: 5, Black: 5, Red2: 5, CB23: 5, C110P: 5,  Yellow: 5, DarkBlue: 4, BUnit: 6, RUnit: 3, BBUnit: 3 },
        DroidAudioBankIdentifier.UnknownAudioBank:              { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BUnit: 1, RUnit: 1, BBUnit: 1 },
        DroidAudioBankIdentifier.DroidDetectorAudioBank:        { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BUnit: 1, RUnit: 1, BBUnit: 1 },
        DroidAudioBankIdentifier.DokOndarsAudioBank:            { Blue: 5, Gray: 3, Red: 3, Orange: 3, Purple: 4, Black: 5, Red2: 5, CB23: 5, C110P: 6,  Yellow: 5, DarkBlue: 4, BUnit: 5, RUnit: 4, BBUnit: 5 },
        DroidAudioBankIdentifier.FirstOrderAudioBank:           { Blue: 3, Gray: 5, Red: 3, Orange: 3, Purple: 5, Black: 3, Red2: 5, CB23: 5, C110P: 6,  Yellow: 5, DarkBlue: 5, BUnit: 5, RUnit: 5, BBUnit: 5 },
        DroidAudioBankIdentifier.InitialActivationAudioBank:    { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BUnit: 1, RUnit: 1, BBUnit: 1 },
        DroidAudioBankIdentifier.MotorSoundAudioBank:           { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BUnit: 0, RUnit: 1, BBUnit: 0 },
        DroidAudioBankIdentifier.EmptyAudioBank:                { Blue: 0, Gray: 0, Red: 0, Orange: 0, Purple: 0, Black: 0, Red2: 0, CB23: 0, C110P: 0,  Yellow: 0, DarkBlue: 0, BUnit: 0, RUnit: 0, BBUnit: 0 },
        DroidAudioBankIdentifier.BlasterAcessoryAudioBank:      { Blue: 2, Gray: 2, Red: 2, Orange: 2, Purple: 2, Black: 2, Red2: 2, CB23: 2, C110P: 2,  Yellow: 2, DarkBlue: 2, BUnit: 0, RUnit: 2, BBUnit: 0 },
        DroidAudioBankIdentifier.ThrusterAccessoryAudioBank:    { Blue: 2, Gray: 2, Red: 2, Orange: 2, Purple: 2, Black: 2, Red2: 2, CB23: 2, C110P: 2,  Yellow: 2, DarkBlue: 2, BUnit: 0, RUnit: 2, BBUnit: 0 }
    }

    ChipAffiliation = {
        Blue:   DroidAffiliation.Resistenace,
        Gray:   DroidAffiliation.Scoundrel,
        Red:    DroidAffiliation.FirstOrder,
        Orange: DroidAffiliation.Resistenace,
        Purple: DroidAffiliation.Scoundrel,
        Black:  DroidAffiliation.FirstOrder,
        Red2:   DroidAffiliation.Scoundrel,
        Yellow: DroidAffiliation.Resistenace,

        CB23:   DroidAffiliation.Scoundrel,
        DO:     DroidAffiliation.Resistenace,
        C110P:  DroidAffiliation.Resistenace,
        RUnit:  DroidAffiliation.Scoundrel,
        BUnit:  DroidAffiliation.Resistenace,
        BBUnit: DroidAffiliation.Scoundrel
    }   

    ChipShutdownTrack = {
        Blue:   (DroidAudioBankIdentifier.FirstOrderAudioBank, 2),
        Gray:   (DroidAudioBankIdentifier.FirstOrderAudioBank, 4),
        Red:    (DroidAudioBankIdentifier.FirstOrderAudioBank, 2),
        Orange: (DroidAudioBankIdentifier.FirstOrderAudioBank, 3),
        Purple: (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        Black:  (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        Red2:   (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        Yellow: (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),

        CB23:   (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        DO:     (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        C110P:  (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        RUnit:  (DroidAudioBankIdentifier.FirstOrderAudioBank, 2),
        BUnit:  (DroidAudioBankIdentifier.FirstOrderAudioBank, 1),
        BBUnit: (DroidAudioBankIdentifier.FirstOrderAudioBank, 3),
    }

class DroidLedIdentifier(object):
    """
    A collection of LED identifiers for a droid.

    Attributes:
        RUnitLeftHeadLed (int): Identifier for the left head LED on an R unit.
        RUnitMiddleHeadLed (int): Identifier for the middle head LED on an R unit.
        RUnitRightHeadLed (int): Identifier for the right head LED on an R unit.
        RUnitLeftAccessoryLed (int): Identifier for the left accessory LED on an R unit.
        RUnitRightAcessoryLed (int): Identifier for the right accessory LED on an R unit.
        BUnitHeadLeds (int): Identifier for the head LEDs on a BB unit.
        BUnitLed0Green (int): Identifier for LED 0 green on a BD unit.
        BUnitLED0Green (int): Identifier for LED 0 green on a BD unit.
        BUnitLED0Red (int): Identifier for LED 0 red on a BD unit.
        BUnitLED1Blue (int): Identifier for LED 1 blue on a BD unit.
        BUnitLED1Green (int): Identifier for LED 1 green on a BD unit.
        BUnitLED1Red (int): Identifier for LED 1 red on a BD unit.
        BUnitLED2Blue (int): Identifier for LED 2 blue on a BD unit.
        BUnitLED2Green (int): Identifier for LED 2 green on a BD unit.
        BUnitLED2Red (int): Identifier for LED 2 red on a BD unit.
        BUnitLED3Blue (int): Identifier for LED 3 blue on a BD unit.
        BUnitLED3Green (int): Identifier for LED 3 green on a BD unit.
        BUnitLED3Blue (int): Identifier for LED 3 blue on a BD unit.
        BUnitLeftEyeLed (int): Identifier for the left eye LED on a BD unit.
        BUnitRightEyeLed (int): Identifier for the right eye LED on a BD unit.
    """

    # R and C units
    RUnitLeftHeadLed = 1
    RUnitMiddleHeadLed = 2
    RUnitRightHeadLed = 4
    RUnitLeftAccessoryLed = 8
    RUnitRightAcessoryLed = 16

    # BB Units
    BUnitHeadLeds = 1

    # BD Units
    BUnitLed0Green = 0
    BUnitLED0Green = 1
    BUnitLED0Red = 2
    BUnitLED1Blue = 3
    BUnitLED1Green = 4
    BUnitLED1Red = 5
    BUnitLED2Blue = 6
    BUnitLED2Green = 7
    BUnitLED2Red = 8
    BUnitLED3Blue = 9
    BUnitLED3Green = 10
    BUnitLED3Blue = 11
    BUnitLeftEyeLed = 12
    BUnitRightEyeLed = 13

def get_personality_id(droid_id: int, chip_id: int = None) -> int:
    """
    Returns the proper personality id given a droid's identifier and its current personality chip if any.

    Args:
        droid_id (int): The identifier representing the droid from the DroidPersonalityIdentifier class
        chip_id (int): The optional chip identifier representing the droid's personality chip from the DroidPersonalityIdentifier class.

    Returns:
        an integer representing the droid's personality that can be used for audio queries.
    """

    return droid_id if chip_id == None else chip_id

def get_available_audio_in_bank(bank_id: int, personality_id: int) -> int:
    """
    Returns the amount of audio clips that are available to play in a given audio bank depending on the droid/personality chip

    Args:
        bank_id (int): Identifier representing the audio bank to search
        personality_id (int): Represents the droid's current configured personality.

    Returns:
        an integer representing the total number of available audio clips
    """

    if bank_id not in DroidPersonalityIdentifier.ChipAudioCount:
        return 0
    
    bank_info = DroidPersonalityIdentifier.ChipAudioCount[personality_id]
    return 0 if personality_id not in bank_info else bank_info[personality_id]

def get_shutdown_audio_track(affiliation_id: int) -> tuple:
    """
    Returns a tuple containing the audio bank and sounud id that should be played when the droid goes to sleep
    based on its afilliation.

    Args:
        affiliation_id (int): The identnfier that represents the droid's affiliation

    Returns:
        A tuple(bank_id, sound_id) containing the droid's shutdown audio information. If the information cannot be found the
        default is returned of (7, 1).
    """

    if affiliation_id not in DroidPersonalityIdentifier.ChipShutdownTrack:
        return (DroidAudioBankIdentifier.FirstOrderAudioBank, 1)
    
    return DroidPersonalityIdentifier.ChipShutdownTrack[affiliation_id]

def get_personality_affiliation(personality_id: int) -> int:
    """
    """

    if personality_id not in DroidPersonalityIdentifier.ChipAffiliation:
        return DroidAffiliation.Scoundrel
    
    return DroidPersonalityIdentifier.ChipAffiliation[personality_id]