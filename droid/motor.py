"""
"""

from droid.utils import int_to_hex
from droid.protocol import DroidCommand, DroidMultipurposeCommand

class DroidMotorDirection(object):
    """
    """

    Forward = 0
    Backwards = 8

    Left = 0
    Right = 8

class DroidMotorIdentifier(object):
    """
    """

    LeftMotor = 0
    RightMotor = 1
    HeadMotor = 2

class DroidMotorController(object):
    """
    """

    def __init__(self, droid: object) -> None:
        """
        """

        self.droid = droid

    async def send_motor_speed_command(self, direction: int, motor_id: int, speed: int = 160, ramp_speed: int = 300) -> None:
        """
        """

        motor_select = "%s%s" % (direction, motor_id)
        motor_command = "%s%s%s0000" % (motor_select, int_to_hex(speed), int_to_hex(ramp_speed))
        await self.droid.send_droid_command(DroidCommand.SetMotorSpeed, motor_command)

    async def rotate_head(self, direction: int, speed: int = 160, ramp_speed: int = 300) -> None:
        """
        """

        if direction != DroidMotorDirection.Left and direction != DroidMotorDirection.Right:
            raise ValueError("Direction is invalid. Expected values are 0 (Left) and 8 (Right)")
        
        await self.send_motor_speed_command(direction, DroidMotorIdentifier.HeadMotor, speed, ramp_speed)

    async def stop_head(self) -> None:
        """
        """

        await self.rotate_head(DroidMotorDirection.Left, 0)

    async def center_unit_head(self, speed: int = 255, offset: int  = 0) -> None:
        """
        """

        command_data = "%s%s" % (int_to_hex(speed), int_to_hex(offset))
        await self.droid.send_droid_multi_command(DroidMultipurposeCommand.CenterRUnitHead, command_data)