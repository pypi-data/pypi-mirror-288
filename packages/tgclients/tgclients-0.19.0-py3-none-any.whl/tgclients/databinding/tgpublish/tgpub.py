# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ErrorType(Enum):
    NOT_SPECIFIED = "NOT_SPECIFIED"
    AUTH = "AUTH"
    WRONG_CONTENT_TYPE = "WRONG_CONTENT_TYPE"
    NO_PUBLISH_RIGHT = "NO_PUBLISH_RIGHT"
    PID_GENERATION_FAILED = "PID_GENERATION_FAILED"
    MISSING_METADATA = "MISSING_METADATA"
    ALREADY_PUBLISHED = "ALREADY_PUBLISHED"
    METADATA_WARNINGS_EXIST = "METADATA_WARNINGS_EXIST"
    SERVER_ERROR = "SERVER_ERROR"


class ProcessStatusType(Enum):
    FINISHED = "FINISHED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    NOT_QUEUED = "NOT_QUEUED"
    ABORTED = "ABORTED"
    QUEUED = "QUEUED"


@dataclass
class ReferencedUris:
    class Meta:
        name = "referencedUris"

    uri: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


class StatusType(Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    NOT_YET_PUBLISHED = "NOT_YET_PUBLISHED"
    ALREADY_PUBLISHED = "ALREADY_PUBLISHED"


class WarningType(Enum):
    NOT_SPECIFIED = "NOT_SPECIFIED"
    CHECK_REFERENCES = "CHECK_REFERENCES"


@dataclass
class WorldReadableMimetypes:
    class Meta:
        name = "worldReadableMimetypes"

    regexp: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Module:
    class Meta:
        name = "module"

    message: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    status: Optional[StatusType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PublishError:
    class Meta:
        name = "publishError"

    message: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: Optional[ErrorType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class PublishWarning:
    class Meta:
        name = "publishWarning"

    message: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: Optional[WarningType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class PublishObject:
    class Meta:
        name = "publishObject"

    error: List[PublishError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    referenced_uris: Optional[ReferencedUris] = field(
        default=None,
        metadata={
            "name": "referencedUris",
            "type": "Element",
            "namespace": "",
        }
    )
    warning: List[PublishWarning] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    uri: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dest_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "destUri",
            "type": "Attribute",
        }
    )
    pid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    status: Optional[StatusType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PublishStatus:
    class Meta:
        name = "publishStatus"

    module: List[Module] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    progress: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    process_status: Optional[ProcessStatusType] = field(
        default=None,
        metadata={
            "name": "processStatus",
            "type": "Attribute",
        }
    )
    active_module: Optional[str] = field(
        default=None,
        metadata={
            "name": "activeModule",
            "type": "Attribute",
        }
    )


@dataclass
class PublishResponse:
    class Meta:
        name = "publishResponse"

    publish_object: List[PublishObject] = field(
        default_factory=list,
        metadata={
            "name": "PublishObject",
            "type": "Element",
            "namespace": "",
        }
    )
    publish_status: Optional[PublishStatus] = field(
        default=None,
        metadata={
            "name": "PublishStatus",
            "type": "Element",
            "namespace": "",
        }
    )
    dry_run: Optional[bool] = field(
        default=None,
        metadata={
            "name": "dryRun",
            "type": "Attribute",
        }
    )
    object_list_complete: Optional[bool] = field(
        default=None,
        metadata={
            "name": "objectListComplete",
            "type": "Attribute",
        }
    )
