import json


def json_to_proto(json_obj, proto_filename):
    def parse_json(json_obj, message_name="Message", level=0):
        result = []
        field_num = 1
        for key, value in json_obj.items():
            if isinstance(value, dict):
                # Nested message for dictionaries
                nested_message_name = f"{key.capitalize()}Message"
                result.append(f"{'  ' * level}message {nested_message_name} {{")
                result.extend(parse_json(value, nested_message_name, level + 1))
                result.append(f"{'  ' * level}}}")
                result.append(f"{'  ' * level}{nested_message_name} {key} = {field_num};")
            elif isinstance(value, list):
                # Handle lists by assuming homogeneous types; take first element to determine type
                if value:
                    first_elem = value[0]
                    if isinstance(first_elem, dict):
                        nested_message_name = f"{key.capitalize()}Item"
                        result.append(f"{'  ' * level}message {nested_message_name} {{")
                        result.extend(parse_json(first_elem, nested_message_name, level + 1))
                        result.append(f"{'  ' * level}}}")
                        result.append(f"{'  ' * level}repeated {nested_message_name} {key} = {field_num};")
                    else:
                        proto_type = type_to_proto(type(first_elem).__name__)
                        result.append(f"{'  ' * level}repeated {proto_type} {key} = {field_num};")
                else:
                    result.append(
                        f"{'  ' * level}repeated string {key} = {field_num};")  # Default repeated type for empty list
            else:
                # Simple field
                proto_type = type_to_proto(type(value).__name__, value)
                result.append(f"{'  ' * level}{proto_type} {key} = {field_num};")
            field_num += 1
        return result

    def type_to_proto(py_type, value=None):
        if py_type == 'int':
            # Determine if the integer fits within int32 range or requires int64
            if -2147483648 <= value <= 2147483647:
                return 'int32'
            else:
                return 'int64'
        return {
            'str': 'string',
            'float': 'float',
            'bool': 'bool'
        }.get(py_type, 'string')

    proto_lines = [
        'syntax = "proto3";',
        f'package {proto_filename.replace(".proto", "")};'
    ]

    # Start with a top-level message that wraps everything
    proto_lines.append('message TopLevelMessage {')
    proto_lines.extend(parse_json(json_obj))
    proto_lines.append('}')

    with open(proto_filename, 'w') as file:
        file.write('\n'.join(proto_lines))
    print(f"Proto file '{proto_filename}' generated successfully.")


# Example JSON data
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

# json_to_proto(quora_data, "quora_data.proto")
