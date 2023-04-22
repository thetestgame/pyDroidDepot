"""
This module defines classes for controlling audio and LEDs for a droid. It contains three classes:
1. DroidAudioCommand: A collection of audio commands for a droid
2. DroidLedIdentifier: A collection of LED identifiers for a droid
3. DroidAudioController: Represents an audio controller for a Droid and has methods for controlling audio and LEDs

This code is MIT licensed.
"""

from droid.utils import  int_to_hex
from droid.protocol import DroidMultipurposeCommand

class DroidAudioCommand(object):
    """
    A collection of audio commands for a droid.

    Attributes:
        RetrieveDroidType (int): Command to retrieve the droid type.
        RetrievePersonalityChip (int): Command to retrieve the personality chip.
        RetrieveAffiliation (int): Command to retrieve the affiliation.
        SetVolume (int): Command to set the audio volume.
        UnknownCommand1 (int): Unknown audio command.
        PlayAudioFromGroupByValue (int): Command to play audio from a group by value.
        PlayAudioFromGroupByValueWithoutLeds (int): Command to play audio from a group by value without LEDs.
        PlayAudioFromSelectedGroup (int): Command to play audio from the selected group.
        CycleAudioFromSelectedGroup (int): Command to cycle audio from the selected group.
        SetSelectedSoundBank (int): Command to set the selected sound bank.
        SetLoopedAudio (int): Command to set the audio to loop.
        UnknownCommand2 (int): Unknown audio command.
        UnknownCommand3 (int): Unknown audio command.
        FlashHeadLeds (int): Command to flash the head LEDs.
        SetLedOn (int): Command to set a specific LED on.
        SetLedOff (int): Command to set a specific LED off.
        DisableHeadLeds (int): Command to disable the head LEDs.
        EnableHeadLeds (int): Command to enable the head LEDs.
    """

    RetrieveDroidType = 1
    RetrievePersonalityChip = 8
    RetrieveAffiliation = 10
    SetVolume = 14
    UnknownCommand1 = 15
    PlayAudioFromGroupByValue = 16
    PlayAudioFromGroupByValueWithoutLeds = 17
    PlayAudioFromSelectedGroup = 24
    CycleAudioFromSelectedGroup = 28
    SetSelectedSoundBank = 31
    SetLoopedAudio = 33
    UnknownCommand2 = 66
    UnknownCommand3 = 68
    FlashHeadLeds = 69
    SetLedOn = 72
    SetLedOff = 73
    DisableHeadLeds = 74
    EnableHeadLeds = 75

class DroidAudioBankIdentifier(object):
    """
    A collection of identifiers used to represent available audio banks of a droid or its connected personality chip. 
    These are used in audio playback.
    """

    GeneralUseAudioBank = 1
    DroidDepotAudioBank = 2
    ResistenceAudioBank = 3
    UnknownAudioBank = 4
    OgasCantinaAudioBank = 5
    DokOndarsAudioBank = 6
    FirstOrderAudioBank = 7
    InitialActivationAudioBank = 8
    MotorSoundAudioBank = 9
    EmptyAudioBank = 10
    BlasterAcessoryAudioBank = 11
    ThrusterAccessoryAudioBank = 12

class DroidAudioChipIdentifier(object):
    """
    A collection of identifiers used to represent various types of personality chips for audio 
    lookup as well as droids for their built-in programmed audio.

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
        BdUnit (int): Identifier for the BD unit droid.
        RUnit (int): Identifier for the R unit droid.
        BBUnit (int): Identifier for the BB unit droid.

        ChipAudioCount (dict): Dictionary containing a total count of available audio by audio bank id and by droid/personality chip
    """

    # Personality Chips
    Blue = 1
    Gray = 2
    Red = 3
    Orange = 4
    Purple = 5
    Black = 6
    Red2 = 7
    Yellow = 9
    DarkBlue = 10

    # Droids
    CB23 = 7
    C110P = 8
    BdUnit = 11
    RUnit = 12
    BBUnit = 13  

    ChipAudioCount = {
        DroidAudioBankIdentifier.GeneralUseAudioBank:           { Blue: 5, Gray: 4, Red: 5, Orange: 5, Purple: 4, Black: 3, Red2: 5, CB23: 5, C110P: 6,  Yellow: 4, DarkBlue: 4, BdUnit: 5, RUnit: 4, BBUnit: 5 },
        DroidAudioBankIdentifier.DroidDepotAudioBank:           { Blue: 5, Gray: 5, Red: 5, Orange: 5, Purple: 4, Black: 6, Red2: 5, CB23: 5, C110P: 13, Yellow: 5, DarkBlue: 4, BdUnit: 6, RUnit: 4, BBUnit: 3 },
        DroidAudioBankIdentifier.ResistenceAudioBank:           { Blue: 5, Gray: 5, Red: 5, Orange: 5, Purple: 5, Black: 5, Red2: 5, CB23: 5, C110P: 5,  Yellow: 5, DarkBlue: 4, BdUnit: 6, RUnit: 3, BBUnit: 3 },
        DroidAudioBankIdentifier.UnknownAudioBank:              { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BdUnit: 1, RUnit: 1, BBUnit: 1 },
	    DroidAudioBankIdentifier.OgasCantinaAudioBank:          { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BdUnit: 1, RUnit: 1, BBUnit: 1 },
	    DroidAudioBankIdentifier.DokOndarsAudioBank:            { Blue: 5, Gray: 3, Red: 3, Orange: 3, Purple: 4, Black: 5, Red2: 5, CB23: 5, C110P: 6,  Yellow: 5, DarkBlue: 4, BdUnit: 5, RUnit: 4, BBUnit: 5 },
	    DroidAudioBankIdentifier.FirstOrderAudioBank:           { Blue: 3, Gray: 5, Red: 3, Orange: 3, Purple: 5, Black: 3, Red2: 5, CB23: 5, C110P: 6,  Yellow: 5, DarkBlue: 5, BdUnit: 5, RUnit: 5, BBUnit: 5 },
	    DroidAudioBankIdentifier.InitialActivationAudioBank:    { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BdUnit: 1, RUnit: 1, BBUnit: 1 },
	    DroidAudioBankIdentifier.MotorSoundAudioBank:           { Blue: 1, Gray: 1, Red: 1, Orange: 1, Purple: 1, Black: 1, Red2: 1, CB23: 1, C110P: 1,  Yellow: 1, DarkBlue: 1, BdUnit: 0, RUnit: 1, BBUnit: 0 },
	    DroidAudioBankIdentifier.EmptyAudioBank:                { Blue: 0, Gray: 0, Red: 0, Orange: 0, Purple: 0, Black: 0, Red2: 0, CB23: 0, C110P: 0,  Yellow: 0, DarkBlue: 0, BdUnit: 0, RUnit: 0, BBUnit: 0 },
	    DroidAudioBankIdentifier.BlasterAcessoryAudioBank:      { Blue: 2, Gray: 2, Red: 2, Orange: 2, Purple: 2, Black: 2, Red2: 2, CB23: 2, C110P: 2,  Yellow: 2, DarkBlue: 2, BdUnit: 0, RUnit: 2, BBUnit: 0 },
	    DroidAudioBankIdentifier.ThrusterAccessoryAudioBank:    { Blue: 2, Gray: 2, Red: 2, Orange: 2, Purple: 2, Black: 2, Red2: 2, CB23: 2, C110P: 2,  Yellow: 2, DarkBlue: 2, BdUnit: 0, RUnit: 2, BBUnit: 0 }
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
        BDUnitLed0Green (int): Identifier for LED 0 green on a BD unit.
        BDUnitLED0Green (int): Identifier for LED 0 green on a BD unit.
        BDUnitLED0Red (int): Identifier for LED 0 red on a BD unit.
        BDUnitLED1Blue (int): Identifier for LED 1 blue on a BD unit.
        BDUnitLED1Green (int): Identifier for LED 1 green on a BD unit.
        BDUnitLED1Red (int): Identifier for LED 1 red on a BD unit.
        BDUnitLED2Blue (int): Identifier for LED 2 blue on a BD unit.
        BDUnitLED2Green (int): Identifier for LED 2 green on a BD unit.
        BDUnitLED2Red (int): Identifier for LED 2 red on a BD unit.
        BDUnitLED3Blue (int): Identifier for LED 3 blue on a BD unit.
        BDUnitLED3Green (int): Identifier for LED 3 green on a BD unit.
        BDUnitLED3Blue (int): Identifier for LED 3 blue on a BD unit.
        BDUnitLeftEyeLed (int): Identifier for the left eye LED on a BD unit.
        BDUnitRightEyeLed (int): Identifier for the right eye LED on a BD unit.
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
    BDUnitLed0Green = 0
    BDUnitLED0Green = 1
    BDUnitLED0Red = 2
    BDUnitLED1Blue = 3
    BDUnitLED1Green = 4
    BDUnitLED1Red = 5
    BDUnitLED2Blue = 6
    BDUnitLED2Green = 7
    BDUnitLED2Red = 8
    BDUnitLED3Blue = 9
    BDUnitLED3Green = 10
    BDUnitLED3Blue = 11
    BDUnitLeftEyeLed = 12
    BDUnitRightEyeLed = 13

class DroidAudioController(object):
    """
    Represents an audio controller for a Droid.

    Args:
        droid (DroidConnection): The DroidConnection this audio controller is for.
    """

    def __init__(self, droid: object) -> None:
        """
        Initializes a new instance of the DroidAudioController class.

        Args:
            droid (DroidConnection): The DroidConnection this audio controller is for.
        """

        self.droid = droid
        self.sound_bank = 0
        self.disabled_leds = []
        self.turned_on_leds = []

    async def execute_audio_command(self, command_id: int, data: str = "00") -> None:
        """
        Executes an audio command on the Droid.

        Args:
            command_id (int): The ID of the audio command to execute.
            data (str): The data to send with the audio command, if any.

        Returns:
            None
        """

        command_id = int_to_hex(command_id)
        command_data = "%s%s"  % (command_id, data)
        await self.droid.send_droid_multi_command(DroidMultipurposeCommand.AudioControllerCommand, command_data)

    def get_available_audio_in_bank(self, bank_id: int, personality_id: int) -> int:
        """
        Returns the amount of audio clips that are available to play in a given audio bank depending on the droid/personality chip

        Args:

        Returns:
            an integer representing the total number of available audio clips
        """

        if bank_id not in DroidAudioChipIdentifier.ChipAudioCount:
            return 0
        
        bank_info = DroidAudioChipIdentifier.ChipAudioCount[personality_id]
        return 0 if personality_id not in bank_info else bank_info[personality_id]

    async def play_audio(self, sound_id: int = None, bank_id: int = None, cycle: bool = False, volume: int = None) -> None:
        """
        Plays audio on the Droid.

        Args:
            sound_id (int): The ID of the sound to play. Defaults to 0 if not provided.
            bank_id (int): The ID of the audio bank to use. Defaults to 0 if not provided.
            cycle (bool): If True, cycles through the audio files in the selected audio bank. Defaults to False.
            volume (int): The volume to play the audio at, in the range [0, 100]. If not provided, the Droid's current volume is used.

        Returns:
            None
        """

        if volume:
            await self.set_volume(volume)

        if bank_id and (not hasattr(self, "sound_bank") or self.sound_bank != bank_id):
            await self.set_audio_bank(bank_id)

        sound_id = int_to_hex(sound_id if sound_id != None else 0)
        bank_id = int_to_hex(bank_id if bank_id != None else 0)

        audio_command = "00"
        audio_parameter = "00"

        if sound_id:
            audio_command = DroidAudioCommand.PlayAudioFromSelectedGroup
            audio_parameter = sound_id
        elif cycle:
            audio_command = DroidAudioCommand.CycleAudioFromSelectedGroup
        else:
            audio_command = DroidAudioCommand.PlayAudioFromGroupByValue
            audio_parameter = bank_id
        
        await self.execute_audio_command(audio_command, audio_parameter)

    async def set_audio_bank(self, bank_id: int) -> None:
        """
        Sets the selected audio bank on the Droid.

        Args:
            bank_id (int): The ID of the audio bank to select.
        """

        bank_id = int_to_hex(bank_id if bank_id != None else 0)
        self.sound_bank = bank_id

        await self.execute_audio_command(DroidAudioCommand.SetSelectedSoundBank, bank_id)

    async def set_volume(self, volume_level: int) -> None:
        """
        Sets the volume of the audio playback on the Droid.

        Args:
            volume_level (int): The volume level to set.
        """

        volume_level = int_to_hex(volume_level if volume_level != None else 0)
        await self.execute_audio_command(DroidAudioCommand.SetVolume, volume_level)

    async def reset_head_leds(self) -> None:
        """
        """

        await self.enable_head_led(31)

    async def disable_head_led(self, led_identifier: int) -> None:
        """
        """

        await self.execute_audio_command(DroidAudioCommand.DisableHeadLeds, led_identifier)

        if led_identifier not in self.disabled_leds:
            self.disabled_leds.append(led_identifier)

    async def enable_head_led(self, led_identifier: int) -> None:
        """
        """

        led_identifier = int_to_hex(led_identifier)
        await self.execute_audio_command(DroidAudioCommand.EnableHeadLeds, led_identifier)

        if led_identifier in self.disabled_leds:
            self.disabled_leds.remove(led_identifier)

    async def turn_on_led(self, led_identifier: int) -> None:
        """
        """

        led_identifier = int_to_hex(led_identifier)
        await self.execute_audio_command(DroidAudioCommand.SetLedOn, led_identifier)

        if not led_identifier in self.turned_on_leds:
            self.turned_on_leds.append(led_identifier)

    async def turn_off_led(self, led_identifier: int) -> None:
        """
        """

        led_identifier = int_to_hex(led_identifier)
        await self.execute_audio_command(DroidAudioCommand.SetLedOff, led_identifier)

        if led_identifier in self.turned_on_leds:
            self.turned_on_leds.remove(led_identifier)