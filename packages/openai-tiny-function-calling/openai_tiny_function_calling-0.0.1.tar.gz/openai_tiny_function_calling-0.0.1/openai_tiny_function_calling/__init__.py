import inspect
from enum import Enum
import re


def create_function_dict(func):
    sig = inspect.signature(func)
    doc = inspect.getdoc(func)

    param_descriptions = {}
    if doc:
        param_section = re.search(r"Args:(.*?)(?:\n\n|\Z)", doc, re.DOTALL)
        if param_section:
            param_lines = param_section.group(1).strip().split('\n')
            for line in param_lines:
                match = re.match(r'\s*(\w+)(?:\s*\((.*?)\))?:\s*(.*)', line)
                if match:
                    param_name, _, param_desc = match.groups()
                    param_descriptions[param_name] = param_desc.strip()

    properties = {}
    required = []
    for name, param in sig.parameters.items():
        prop = {}

        if param.annotation != inspect.Parameter.empty:
            if issubclass(param.annotation, Enum):
                prop["type"] = "string"
                prop["enum"] = [e.value for e in param.annotation]
                assert isinstance(prop["enum"][0], str)
            elif param.annotation == str:
                prop["type"] = "string"

        description = param_descriptions.get(name, "")

        if param.default != inspect.Parameter.empty:
            default_value = param.default.value if isinstance(param.default, Enum) else param.default
            description += f" (Default: {default_value})"

        if description:
            prop["description"] = description

        if param.default == inspect.Parameter.empty:
            required.append(name)

        assert "type" in prop
        properties[name] = prop

    return {
        "name": func.__name__,
        "description": doc.split('\n\n')[0] if doc else "",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }
