import importlib
import json
import zlib

from google.protobuf.descriptor import FieldDescriptor


def create_message(proto_module_param, message_type_param):
    """Dynamically create a Protobuf message."""
    return getattr(proto_module_param, message_type_param)()


def load_proto_module(proto_module_name_arg):
    """Dynamically load a Protobuf module."""
    return importlib.import_module(proto_module_name_arg)


def set_message_fields(message, data: dict):
    """Recursively set fields in a Protobuf message from a dictionary with error handling, including parsing nested JSON strings."""
    for key, value in data.items():
        if not hasattr(message, key):
            print(f"Warning: {key} is not a valid field of {message.DESCRIPTOR.name}")
            continue

        field_descriptor = message.DESCRIPTOR.fields_by_name[key]

        if field_descriptor.label == FieldDescriptor.LABEL_REPEATED:
            field = getattr(message, key)
            if not isinstance(value, list):
                print(f"Error: Field {key} is a repeated field, but a non-list value was provided")
                continue
            for item in value:
                if field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
                    if isinstance(item, str):
                        item = json.loads(item)
                    sub_message = field.add()
                    set_message_fields(sub_message, item)
                else:
                    field.append(item)
        elif field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
            field = getattr(message, key)
            if isinstance(value, str):
                value = json.loads(value)
            if isinstance(value, dict):
                set_message_fields(field, value)
            else:
                print(f"Error: Field {key} is a message type, but a non-dict value was provided")
        else:
            if value is None:
                setattr(message, key, "")
                continue
            setattr(message, key, value)

    return message


def serialize_message(message):
    """Serialize a Protobuf message to a compressed binary string."""
    return zlib.compress(message.SerializeToString())


if __name__ == "__main__":
    proto_module_name = 'grpc.generated.quora_data_pb2'
    message_type = 'TopLevelMessage'
    quora_data = {
        "RawData": json.loads(
            "{\"ObjectId\": 1623297786281202642, \"SocialID\": \"de9aeaed48ff63a3fe30cc5099dbec6b\", \"OrderID\": 220, \"CreatedDate\": \"2023-11-26 13:30:55\", \"NumCommentsCount\": 0, \"NumShareCount\": 0, \"NumVideoViews\": 1287, \"Description\": \"How long does it take you to become an expert at crypto trading?\", \"LanguageName\": \"english\", \"FilterKeywords\": \" (finance)\", \"UserInfo\": {\"AuthorSocialID\": \"dsdsdasdsa\"}, \"URL\": \"https://www.quora.com/unanswered/How-long-does-it-take-you-to-become-an-expert-at-crypto-trading\", \"AnswerCounts\": 11, \"SimplifiedText\": \"Question: How long does it take you to become an expert at crypto trading?\"}"),
        "ChannelGroup": 36,
        "ChannelType": 75,
        "BrandInfo": {
            "BrandID": 12168,
            "BrandName": "Titktok",
            "CategoryID": 1808,
            "CategoryName": "LocobuzzTestDB",
            "BrandSettings": {},
            "OperationEnum": None
        },
        "MentionTrackingDetails": {
            "FetchingServiceInTime": "2024-06-27T05:24:20.967412",
            "FetchingServiceOutTime": "2024-06-27T05:24:22.670233"
        },
        "ServiceName": "QuoraDataCollectionService"
    }
    # Load the module dynamically
    proto_module = load_proto_module(proto_module_name)
    message = create_message(proto_module, message_type)
    set_message_fields(message, quora_data)
    # Serialize the message to a compressed binary string
    binary_data = serialize_message(message)
    print(binary_data)
    from deserialize_protobuf import deserialize_message
    from protocol_to_json import protobuf_to_dict
    msg = deserialize_message(proto_module, message_type, binary_data)
    print(msg)
    print(type(msg))
    dict_msg = protobuf_to_dict(msg)
    print(dict_msg)
    print(type(dict_msg))