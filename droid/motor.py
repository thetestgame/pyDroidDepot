"""
This module provides classes for controlling the motor functions of a SWGE DroidDepot droid.

The classes contained in this module are licensed under the MIT License.
"""

from droid.utils import int_to_hex
from droid.protocol import DroidCommand, DroidMultipurposeCommand

class DroidMotorDirection(object):
    """
    Enumeration of motor directions.
    """

    Forward = 0
    Backwards = 8

    Left = 0
    Right = 8

class DroidMotorIdentifier(object):
    """
    Enumeration of motor identifiers.
    """

    LeftMotor = 0
    RightMotor = 1
    HeadMotor = 2

class DroidMotorController(object):
    """
    Class for controlling the motor functions of a SWGE DroidDepot droid.
    """

    def __init__(self, droid: object) -> None:
        """
        Initializes a new instance of the DroidMotorController class.

        Args:
            droid: A DroidConnection object representing the connection to the droid.
        """

        self.droid = droid

    async def send_motor_speed_command(self, direction: int, motor_id: int, speed: int = 160, ramp_speed: int = 300, delay = 0) -> None:
        """
        Sends a motor speed command to the droid.

        Args:
            direction (int): An integer representing the motor direction. Should be one of the values defined in the DroidMotorDirection class.
            motor_id (int): An integer representing the motor identifier. Should be one of the values defined in the DroidMotorIdentifier class.
            speed (int): An integer representing the motor speed. Defaults to 160.
            ramp_speed (int): An integer representing the motor ramp speed. Defaults to 300.
        """

        delay_hex = int_to_hex(delay)
        if len(delay_hex) < 4:
            missing = 4 - len(delay_hex)
            for x in range(missing):
                delay_hex = '0' + delay_hex

        motor_select = "%s%s" % (direction, motor_id)
        motor_command = "%s%s%s%s" % (motor_select, int_to_hex(speed), int_to_hex(ramp_speed), delay_hex)
        await self.droid.send_droid_command(DroidCommand.SetMotorSpeed, motor_command)

    async def set_movement_speed(self, direction: int, speed: int = 100, ramp_speed: int = 300) -> None:
        """
        Sends a motor speed command to the droid to both the left and right movement motors.

        Args:
            direction (int): An integer representing the motor direction. Should be one of the values defined in the DroidMotorDirection class.
            speed (int): An integer representing the motor speed. Defaults to 160.
            ramp_speed (int): An integer representing the motor ramp speed. Defaults to 300.
        """

        await self.send_motor_speed_command(direction, DroidMotorIdentifier.LeftMotor, speed, ramp_speed)
        await self.send_motor_speed_command(direction, DroidMotorIdentifier.RightMotor, speed, ramp_speed)

    async def rotate_head(self, direction: int, speed: int = 160, ramp_speed: int = 300) -> None:
        """
        Rotates the head of the droid.

        Args:
            direction (int): An integer representing the direction to rotate the head. Should be one of the values defined in the DroidMotorDirection class.
            speed (int): An integer representing the rotation speed. Defaults to 160.
            ramp_speed (int): An integer representing the rotation ramp speed. Defaults to 300.
        """

        if direction != DroidMotorDirection.Left and direction != DroidMotorDirection.Right:
            raise ValueError("Direction is invalid. Expected values are 0 (Left) and 8 (Right)")
        
        await self.send_motor_speed_command(direction, DroidMotorIdentifier.HeadMotor, speed, ramp_speed)

    async def stop_head(self) -> None:
        """
        Stops the rotation of the head.
        """

        await self.rotate_head(DroidMotorDirection.Left, 0)

    async def center_head(self, speed: int = 255, offset: int  = 0) -> None:
        """
        Centers the head of the droid.

        Args:
            speed (int): An integer representing the speed at which to center the head. Defaults to 255.
            offset (int): An integer representing the offset from center. Defaults to 0.
        """

        command_data = "%s%s" % (int_to_hex(speed), int_to_hex(offset))
        await self.droid.send_droid_multi_command(DroidMultipurposeCommand.CenterRUnitHead, command_data)