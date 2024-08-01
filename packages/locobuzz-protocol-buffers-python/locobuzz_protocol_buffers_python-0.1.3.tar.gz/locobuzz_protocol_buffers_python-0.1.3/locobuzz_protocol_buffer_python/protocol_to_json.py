import json
import importlib
from google.protobuf.json_format import MessageToDict, ParseDict, ParseError
from google.protobuf.message import Message


def import_protobuf_module(module_name: str):
    """
    Dynamically imports a protobuf module.

    Args:
        module_name (str): The name of the protobuf module to import.

    Returns:
        module: The imported protobuf module.
    """
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError as e:
        raise ImportError(f"Failed to import module '{module_name}': {e}")


def get_protobuf_class(module, class_name: str):
    """
    Retrieves a protobuf class from the imported module.

    Args:
        module: The imported protobuf module.
        class_name (str): The name of the protobuf class to retrieve.

    Returns:
        class: The protobuf class.
    """
    try:
        protobuf_class = getattr(module, class_name)
        return protobuf_class
    except AttributeError as e:
        raise AttributeError(f"Module '{module.__name__}' has no class '{class_name}': {e}")


def populate_protobuf_from_dict(protobuf_cls, data: dict) -> Message:
    """
    Populates a protobuf message from a dictionary.

    Args:
        protobuf_cls (Descriptor): The protobuf message class to populate.
        data (dict): The data to populate the protobuf message with.

    Returns:
        Message: The populated protobuf message.

    Raises:
        ValueError: If there is an error during population.
    """
    try:
        protobuf_message = protobuf_cls()
        ParseDict(data, protobuf_message)
        return protobuf_message
    except ParseError as e:
        raise ValueError(f"Failed to populate protobuf message from dict: {e}")


def protobuf_to_dict(protobuf_message: Message) -> dict:
    """
    Converts a protobuf message to a dictionary.

    Args:
        protobuf_message (Message): The protobuf message to convert.

    Returns:
        dict: The dictionary representation of the protobuf message.

    Raises:
        TypeError: If the input is not a protobuf message.
        ValueError: If there is an error during conversion.
    """
    if not isinstance(protobuf_message, Message):
        raise TypeError("The input must be a protobuf message.")

    try:
        dict_representation = MessageToDict(protobuf_message)
        return dict_representation
    except ParseError as e:
        raise ValueError(f"Failed to convert protobuf message to dict: {e}")


# Example usage
if __name__ == "__main__":
    try:
        module_name = 'quora_data_pb2'  # Replace with the actual module name
        class_name = 'TopLevelMessage'  # Replace with the actual class name
        data = {
            # Populate with dynamic data
            # "field_name": "value",
        }

        # Dynamically import the protobuf module
        protobuf_module = import_protobuf_module(module_name)

        # Get the protobuf class from the module
        protobuf_cls = get_protobuf_class(protobuf_module, class_name)

        # Populate the protobuf message from the dictionary
        protobuf_message = populate_protobuf_from_dict(protobuf_cls, data)

        # Convert the populated protobuf message to a dictionary
        dict_representation = protobuf_to_dict(protobuf_message)
        print(dict_representation)
    except (ImportError, AttributeError, TypeError, ValueError) as e:
        print(f"Error: {e}")
