from dbnomics_data_model.json_utils.errors import JsonBytesParseError, JsonParseTypeError
from dbnomics_data_model.json_utils.parsing import JsonParser


def parse_json_line_code(line: bytes) -> str:
    parser = JsonParser.create()
    data = parser.parse_bytes(line)
    if not parser.is_object(data):
        raise JsonParseTypeError(data=data, expected_type=dict)

    try:
        code = data["code"]
    except KeyError as exc:
        raise JsonBytesParseError(value=line) from exc

    if not isinstance(code, str):
        raise JsonBytesParseError(value=line)

    return code
