"""
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