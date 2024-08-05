from enum import Enum
import openai_tiny_function_calling


class Unit(Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


def get_current_weather(location: str, unit: Unit = Unit.CELSIUS):
    """
    Get the current weather in a given location

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: The temperature unit to use
    """
    pass


def test_example():
    function = openai_tiny_function_calling.create_function_dict(get_current_weather)
    print(function)
    assert function["name"] == "get_current_weather"
    assert function["description"] == "Get the current weather in a given location"
    assert function["parameters"]["properties"]["location"]["type"] == "string"
    assert function["parameters"]["properties"]["location"]["description"] == "The city and state, e.g. San Francisco, CA"
    assert function["parameters"]["properties"]["unit"]["type"] == "string"
    assert set(function["parameters"]["properties"]["unit"]["enum"]) == {"celsius", "fahrenheit"}
    assert function["parameters"]["properties"]["unit"]["description"] == "The temperature unit to use (Default: celsius)"
    assert set(function["parameters"]["required"]) == {"location"}
