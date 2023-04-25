"""
This module contains classes and functions for interacting with droid scripts.

1. DroidScripts: An enumeration containing constants representing available droid scripts.
2. DroidScriptActions: An enumeration containing constants representing available droid script actions.
3. DroidScriptEngine: A class that represents the droid script engine and provides methods for executing droid scripts.

This code is MIT licensed.
"""

import asyncio
import logging
from datetime import datetime
from droiddepot.protocol import DroidCommandId, protocol_action
from droiddepot.beacon import DroidReactionBeaconScanner, decode_location_beacon_payload

class DroidScripts(object):
    """
    An enumeration containing constants representing available droid scripts.
    """

    GeneralParkResponseScript = 1
    DroidDepotParkResponseScript = 2
    ResistenceParkResponseScript = 3
    UnknownParkResponseScript = 4
    OgasCantinaParkResponseScript = 5
    DokOndarsParkResponseScript = 6
    FirstOrderParkResponseScript = 7
    DroidBayActivationSequence = 8
    UnknownBUnitScript9 = 9
    UnknownBUnitScript10 = 10
    DroidPairingSequence1 = 11
    DroidPairingSequence2 = 12
    FullThrottleTestScript = 13

class DroidScriptActions(object):
    """
    An enumeration containing constants representing available droid script actions.
    """

    OpenScript = 0
    CloseScript = 1
    ExecuteScript = 2

class DroidScriptEngine(object):
    """
    A class that represents the droid script engine and provides methods for executing droid scripts.
    """

    def __init__(self, droid: object) -> None:
        """
        Initializes a new instance of the DroidScriptEngine class.

        Args:
            droid (object): The droid instance to use.
        """

        self.droid = droid

        self.__location_reaction_tracker = {}
        self.reaction_scanner = DroidReactionBeaconScanner()
        self.reaction_scanner.add_location_handler(self.__perform_droid_location_reactions)

    async def send_script_command(self, script_id: int, script_action: int) -> None:
        """
            Sends a script command to the droid.

            Args:
                script_id (int): The ID of the script to execute.
                script_action (int): The action to perform with the script.

            Raises:
                ValueError: If the script ID is 13 (FullThrottleTestScript) or
                the script is less then 0.
        """

        if script_id <= 0 and script_action != DroidScriptActions.CloseScript:
            raise ValueError("Invalid script id requested. Script ids must be larger then 0")

        if script_id == 13:
            raise ValueError("Attempted to use a dangerous script. Execution denied")

        command_data = "%s%s" % ("{:02d}".format(script_id), "{:02d}".format(script_action))
        await self.droid.send_droid_command(DroidCommandId.ScriptActionComand, command_data)

    @protocol_action
    async def execute_script(self, script_id: int) -> None:
        """
        Executes a droid script.

        Args:
            script_id (int): The ID of the script to execute.
        """

        await self.send_script_command(script_id, DroidScriptActions.ExecuteScript)

    @protocol_action
    async def execute_location_beacon_payload(self, payload: str) -> None:
        """
        Executes a location beacon on the connected droid emulation what would happen
        if the droid encountered the beacon at a Disney park

        Args:
            payload (str): Payload advertised by a park beacon
        """

        data = decode_location_beacon_payload(payload)
        await self.execute_script(data['script_id'])

    async def open_script(self, script_id: int) -> None:
        """
        Opens a droid script for writing. All command sent after the script is opened will be
        written into the script id until close_script is called

        Args:
            script_id (int): The ID of the script to open for writing.
        """

        if script_id <= 0:
            raise ValueError('Script ids must be larger then 0')

        if script_id >= 1 and script_id <= 13:
            raise ValueError("Attempted to rewrite Disney programmed scripts. Action prevented for safety")

        await self.send_script_command(script_id, DroidScriptActions.OpenScript)

    async def close_script(self, script_id: int = 0) -> None:
        """
        Closes the currently open script. This will also stop any script currently
        being executed.

        Args:
            script_id (int): The ID of the script to close.
        """

        await self.send_script_command(script_id, DroidScriptActions.CloseScript)

    def __calculate_reaction_time(self, interval: int) -> int:
        """
        Calculates the time in seconds from a park beacon's reaction interval.

        Args:
            interval (int): Reaction interval received from a location beacon
        """

        interval = interval * 5
        if interval < 60:
            interval = 60

        return interval

    async def __perform_droid_location_reactions(self, locations: list) -> None:
        """
        Executes a script associated with each park location beacon that the droid enters.

        Args:
            locations (list): A list of location beacon addresses to react to

        Returns:
            int: The calculated reaction time in seconds.
        """

        # Verify we have at least one location to react to first.
        if len(locations) == 0:
            return
        
        can_execute = True
        already_executed = False
        for location_beacon_address in locations:
            try:
                location_data = locations[location_beacon_address]

                # Check if we already reacted and if we have check if we are in a new reaction window
                if location_beacon_address in self.__location_reaction_tracker:
                    last_execution = self.__location_reaction_tracker[location_beacon_address]
                    time_since_last = (datetime.now() - last_execution).total_seconds()
                    can_execute = time_since_last >= self.__calculate_reaction_time(location_data['reaction_interval'])

                # Attempt to execute the reaction
                if can_execute and already_executed == False:
                    await self.execute_script(location_data['script_id'])
                    self.__location_reaction_tracker[location_beacon_address] = datetime.now()
                    already_executed = True
            except ValueError:
                logging.error('Failed to handle location beacon execution. Likely attempted to execute a dangerous script')
            except Exception as e:
                logging.error('An unexpected error occured processing a park location beacon: %s' % location_beacon_address)
                logging.error(e, exc_info=True) 

        if already_executed:
            await asyncio.sleep(5)

    def start_beacon_reactions(self) -> None:
        """
        Enables SWGE park beacon reactions similar to the internal firmware.
        """

        self.reaction_scanner.start()

    def stop_beacon_reactions(self) -> None:
        """
        Disables park beacon reactions.
        """

        self.reaction_scanner.stop()