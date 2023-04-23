"""
This module contains classes and functions for interacting with droid scripts.

1. DroidScripts: An enumeration containing constants representing available droid scripts.
2. DroidScriptActions: An enumeration containing constants representing available droid script actions.
3. DroidScriptEngine: A class that represents the droid script engine and provides methods for executing droid scripts.

This code is MIT licensed.
"""

from droid.protocol import DroidCommand

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

    async def send_script_command(self, script_id: int, script_action: int) -> None:
        """
            Sends a script command to the droid.

            Args:
                script_id (int): The ID of the script to execute.
                script_action (int): The action to perform with the script.

            Raises:
                ValueError: If the script ID is 13 (FullThrottleTestScript).
        """

        if script_id == 13:
            raise ValueError("Attempted to execute a dangerous script. Execution denied")

        command_data = "%s%s" % ("{:02d}".format(script_id), "{:02d}".format(script_action))
        await self.droid.send_droid_command(DroidCommand.ScriptCommand, command_data)

    async def execute_script(self, script_id: int) -> None:
        """
        Executes a droid script.

        Args:
            script_id (int): The ID of the script to execute.

        """

        await self.send_script_command(script_id, DroidScriptActions.ExecuteScript)

    async def stop_script_execution(self) -> None:
        """
        Stops the execution of a running script.
        """

        await self.send_script_command(0, DroidScriptActions.CloseScript)