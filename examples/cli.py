"""
"""

import sys
sys.path.insert(0, '../')

from droiddepot.connection import discover_droid, DroidCommandId
from droiddepot.audio import DroidLedIdentifier
from time import sleep
from bleak import BleakError
import asyncio
import inspect
import ast

def cast_argument(argument, arg_type):
    try:
        return ast.literal_eval(argument)
    except ValueError:
        return arg_type(argument)

async def execute_service_command(service_component: object, func_name: str, arguments: list) -> None:
    if not hasattr(service_component, func_name):
        raise ValueError("Function name (%s) not found on object %s" % (func_name, service_component.__class__.__name__))

    func_inst = getattr(service_component, func_name)
    argspec = inspect.getfullargspec(func_inst)
    params = argspec.args[1:]  # Ignore "self" parameter
    
    if len(arguments) < len(params):
        raise ValueError("Incorrect number of arguments supplied. Expected %s, got %s" % (len(params), len(arguments)))

    args = []
    for param, arg in zip(params, arguments):
        arg_type = argspec.annotations.get(param, str)
        cast_arg = cast_argument(arg, arg_type)
        args.append(cast_arg)

    result = None
    if inspect.iscoroutinefunction(func_inst):
        result = await func_inst(*args)
    else:
        result = func_inst(*args)

    if result != None:
        print(result)

def get_service_command_args(input_list: list) -> list:
    if len(input_list) > 2:
        return input_list[2:]
    else:
        return []

async def main() -> None:
    droid = await discover_droid(retry=True)

    async with droid as d:
        try:
            await d.motor_controller.center_head()

            while d.droid.is_connected:            
                command = input("Command:")
                command_parts = command.split(',')
                if len(command_parts) < 2:
                    print('Invalid arguments supplied. <service_component>,<method_name>,<..args>')
                    continue

                service_component_name = command_parts[0]
                service_component_method = command_parts[1]
                service_command_parts = get_service_command_args(command_parts)

                try:
                    if service_component_name == "connection":
                        await execute_service_command(d, service_component_method, service_command_parts)
                    elif service_component_name == "audio":
                        await execute_service_command(d.audio_controller, service_component_method, service_command_parts)
                    elif service_component_name == "script":
                        await execute_service_command(d.script_engine, service_component_method, service_command_parts)
                    elif service_component_name == "motor":
                        await execute_service_command(d.motor_controller, service_component_method, service_command_parts)
                    elif service_component_name == "voice":
                        await execute_service_command(d.voice_controller, service_component_method, service_command_parts)
                    else:
                        print('Unknown service component: %s' % service_component_name)
                except ValueError as err:
                    print(err)
                except SyntaxError as err:
                    print('Invalid arguments. Check your inputs')
        
        except OSError as err:
            print(f"Discovery failed due to operating system: {err}")
        except BleakError as err:
            print(f"Discovery failed due to Bleak: {err}")
        except KeyboardInterrupt as err:
            pass
        finally:
            print("\nShutting down.")

if __name__ == "__main__":
    asyncio.run(main())
