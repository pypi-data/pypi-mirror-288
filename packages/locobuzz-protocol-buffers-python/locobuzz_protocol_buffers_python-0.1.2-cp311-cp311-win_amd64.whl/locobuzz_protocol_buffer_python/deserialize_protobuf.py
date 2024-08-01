# proto_module_name = 'app.grpc.generated.user_pb2'
import importlib
import zlib


def load_proto_module(proto_module_name_arg):
    """Dynamically load a Protobuf module."""
    return importlib.import_module(proto_module_name_arg)


def create_message(proto_module_param, message_type_param):
    """Dynamically create a Protobuf message."""
    return getattr(proto_module_param, message_type_param)()


def deserialize_message(proto_module, message_type, binary_data):
    """Deserialize a compressed binary string to a Protobuf message."""
    message = create_message(proto_module, message_type)
    message.ParseFromString(zlib.decompress(binary_data))
    return message
