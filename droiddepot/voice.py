"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.

This module provides a voice controller for SWGE droids that attempts to match the droid's configured affiliation
to a tone of voice based on the available audio banks in the droid's memory. 

It contains a `DroidVoiceController` class that has methods to get voice bank IDs for different tones of 
voice based on the droid's affiliation. 

The `DroidVoiceTone` class defines identifiers for the possible tones of voice to use when speaking. 
The `talk_with_animation` method of the `DroidVoiceController` class sends a command to the droid to speak with a random animation and audio file
based around the tone supplied when invoked.
"""

from droiddepot.hardware import DroidAffiliation, DroidAudioBankIdentifier
import random

class DroidVoiceTone(object):
    """
    Identifer for the possible tones of voice to use when speaking
    """

    Friendly = 1
    Indifferent = 2
    Upset = 3

class DroidVoiceController(object):
    """
    Experimental voice controller for SWGE droids that attempts to match the droid's configured affiliation
    to a tone of voice based on the available audio banks in the droid's memory.
    """

    def __init__(self, droid: object) -> None:
        self.droid = droid

    def get_friendly_voice_bank_id(self) -> int:
        """
        Returns a voice bank id for the droid's configuration that can be viewed as "happy" or "excited"
        """

        if self.droid.affiliation_id == DroidAffiliation.Resistenace:
            return DroidAudioBankIdentifier.ResistenceAudioBank
        elif self.droid.affiliation_id == DroidAffiliation.FirstOrder:
            return DroidAudioBankIdentifier.FirstOrderAudioBank
        else:
            return self.get_random_indifferent_voice_bank_id()

    def get_upset_voice_bank_id(self) -> int:
        """
        Returns a voice bank id for the droids configuration that can be viewed as "upset" or "scared"
        """

        if self.droid.affiliation_id == DroidAffiliation.Resistenace:
            return DroidAudioBankIdentifier.FirstOrderAudioBank
        elif self.droid.affiliation_id == DroidAffiliation.FirstOrder:
            return DroidAudioBankIdentifier.ResistenceAudioBank
        else:
            return self.get_random_indifferent_voice_bank_id()
        
    def get_random_indifferent_voice_bank_id(self) -> int:
        """
        Returns a random voice bank that can be viewed as "neutral" or indifferent
        """

        options = list(DroidAudioBankIdentifier.TalkingBanks)
        if self.droid.affiliation_id != DroidAffiliation.Scoundrel:
            options.remove(self.get_upset_voice_bank_id())
        return random.choice(options)

    async def talk_with_animation(self, tone: int) -> None:
        """
        Sends a command to the droid to speak with a random animation and audio file
        based around the tone supplied when invoked.
        """

        voice_script = 0
        if tone == DroidVoiceTone.Friendly:
            voice_script = self.get_friendly_voice_bank_id()
        elif tone == DroidVoiceTone.Upset:
            voice_script = self.get_upset_voice_bank_id()
        else:
            voice_script = self.get_random_indifferent_voice_bank_id()

        await self.droid.script_engine.execute_script(voice_script)