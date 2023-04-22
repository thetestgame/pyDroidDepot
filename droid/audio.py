"""
"""

from droid.utils import  int_to_hex
from droid.protocol import DroidMultipurposeCommand

class DroidAudioCommand(object):
    """
    """

    RetrieveDroidType = 0x01
    RetrievePersonalityChip = 0x08
    RetrieveAffiliation = 0x0a
    SetVolume = 0x0e
    UnknownCommand1 = 0x0f
    PlayAudioFromGroupByValue = 0x10
    PlayAudioFromGroupByValueWithoutLeds = 0x11
    PlayAudioFromSelectedGroup = 0x18
    CycleAudioFromSelectedGroup = 0x1c
    SetSelectedSoundBank = 0x1f
    SetLoopedAudio = 0x21
    UnknownCommand2 = 0x42
    UnknownCommand3 = 0x44
    FlashHeadLeds = 0x45
    SetLedOn = 0x48
    SetLedOff = 0x49
    DisableHeadLeds = 0x4a
    EnableHeadLeds = 0x4b

class DroidLedIdentifier(object):
    """
    """

    # R and C units
    RUnitLeftHeadLed = "01"
    RUnitMiddleHeadLed = "02"
    RUnitRightHeadLed = "04"
    RUnitLeftAccessoryLed = "08"
    RUnitRightAcessoryLed = "10"

    # BB Units
    BUnitHeadLeds = "01"

    # BD Units
    BDUnitLed0Green = "00"
    BDUnitLED0Green = "01"
    BDUnitLED0Red = "02"
    BDUnitLED1Blue = "03"
    BDUnitLED1Green = "04"
    BDUnitLED1Red = "05"
    BDUnitLED2Blue = "06"
    BDUnitLED2Green = "07"
    BDUnitLED2Red = "08"
    BDUnitLED3Blue = "09"
    BDUnitLED3Green = "0A"
    BDUnitLED3Blue = "0B"
    BDUnitLeftEyeLed = "0C"
    BDUnitRightEyeLed = "0D"

class DroidAudioController(object):
    """
    """

    def __init__(self, droid: object) -> None:
        """
        """

        self.droid = droid
        self.sound_bank = 0
        self.disabled_leds = []
        self.turned_on_leds = []

    async def shutdown(self) -> None:
        """
        """

    async def execute_audio_command(self, command_id: str, data: str = "00") -> None:
        """
        """

        command_id = int_to_hex(command_id)
        command_data = "%s%s"  % (command_id, data)
        await self.droid.send_droid_multi_command(DroidMultipurposeCommand.AudioControllerCommand, command_data)

    async def play_audio(self, sound_id: int = None, bank_id: int = None, cycle: bool = False, volume: int = None) -> None:
        """
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
        """

        bank_id = int_to_hex(bank_id if bank_id != None else 0)
        self.sound_bank = bank_id

        await self.execute_audio_command(DroidAudioCommand.SetSelectedSoundBank, bank_id)

    async def set_volume(self, volume_level: int) -> None:
        """
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