"""
"""

from droid.protocol import DroidCommand

class DroidScripts(object):
    """
    """

    GeneralParkResponseScript = 1
    DroidDepotParkResponseScript = 2
    ResistenceParkResponseScript = 3
    UnknownParkResponseScript = 4
    OgasCantinaParkResponseScript = 5
    DokOndarsParkResponseScript = 6
    FirstOrderParkResposneScript = 7
    DroidBayActivationSequence = 8
    UnknownBUnitScript9 = 9
    UnknownBUnitScript10 = 10
    DroidPairingSequence1 = 11
    DroidPairingSequence2 = 12
    FullThrottleTestScript = 13

class DroidScriptActions(object):
    """
    """

    OpenScript = 0
    CloseScript = 1
    ExecuteScript = 2

class DroidScriptEngine(object):
    """
    """

    def __init__(self, droid: object) -> None:
        """
        """

        self.droid = droid

    async def send_script_command(self, script_id: int, script_action: int) -> None:
        """
        """

        if script_id == 13:
            raise Exception("Attempted to execute a dangerous script. Execution denied")

        command_data = "%s%s" % ("{:02d}".format(script_id), "{:02d}".format(script_action))
        await self.droid.send_droid_command(DroidCommand.ScriptCommand, command_data)

    async def execute_script(self, script_id: int) -> None:
        """
        """

        await self.send_script_command(script_id, DroidScriptActions.ExecuteScript)

    async def stop_script_execution(self) -> None:
        """
        """

        await self.send_script_command(0, DroidScriptActions.CloseScript)