# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

"""tgclients provide access to TextGrid services."""

__version__ = '0.19.0'

from tgclients.aggregator import (
    Aggregator,
)
from tgclients.auth import (
    TextgridAuth,
    TextgridAuthException,
)
from tgclients.config import (
    TextgridConfig,
)
from tgclients.crud import (
    TextgridCrud,
    TextgridCrudException,
    TextgridCrudRequest,
)
from tgclients.metadata import (
    TextgridMetadata,
)
from tgclients.publish import (
    TextgridPublish,
)
from tgclients.search import (
    TextgridSearch,
    TextgridSearchException,
    TextgridSearchRequest,
)
from tgclients.utils import (
    Utils,
)

__all__ = [
    'Aggregator',
    'TextgridAuth',
    'TextgridAuthException',
    'TextgridConfig',
    'TextgridCrud',
    'TextgridCrudRequest',
    'TextgridCrudException',
    'TextgridMetadata',
    'TextgridPublish',
    'TextgridSearch',
    'TextgridSearchRequest',
    'TextgridSearchException',
    'Utils',
]
