# Auto-generated, do not edit directly. Run `make generate_command_data` to update.

from enum import Enum
from typing import Literal

from pydantic import BaseModel


class CommandRequestType(str, Enum):
    FILE_READ = "file_read"


class CommandRequestData(BaseModel):
    type: Literal[CommandRequestType.FILE_READ,]


class FileReadCommandRequestData(CommandRequestData):
    type: Literal[CommandRequestType.FILE_READ] = CommandRequestType.FILE_READ

    file_path: str
    language: str


CommandRequestDataType = FileReadCommandRequestData
