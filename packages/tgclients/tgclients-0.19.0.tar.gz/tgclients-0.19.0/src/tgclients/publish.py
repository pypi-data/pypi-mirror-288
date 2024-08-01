# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""API for the TextGrid publish service."""

import logging
from io import BytesIO
from typing import List

import requests
from requests.models import Response
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from tgclients.config import TextgridConfig
from tgclients.databinding.tgpublish import PublishResponse

logger = logging.getLogger(__name__)


class TextgridPublishRequest:
    """Provide low level access to the Textgrid Publish Service returning HTTP response objects.

    API docs:
    https://textgridlab.org/doc/services/submodules/kolibri/kolibri-tgpublish-service/docs/index.html
    """

    def __init__(self, config: TextgridConfig = TextgridConfig()) -> None:
        self._url = config.publish
        self._config = config
        # reuse tcp connections: https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
        self._requests = requests.Session()

    def copy(self, sid: str, textgrid_uris: List[str], project_id: str) -> Response:
        """Copies the objects belonging to the given URIs to the given project ID.

        Also copies all aggregated objects (from aggregations/editions/collections).

        Args:
            sid (str): Session ID
            textgrid_uris (List[str]): Textgrid URIs of objects to copy
            project_id (str): Project ID of the project to copy the objects to.

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service - UUID of copy job queued
        """
        params = {
            'sid': sid,
            'uri': textgrid_uris,
            'projectId': project_id,
            'newRevision': 'false',
        }
        response = self._requests.get(
            self._url + '/copy', params=params, timeout=self._config.http_timeout
        )
        return self._handle_response(response)

    def copy_to_new_revision(self, sid: str, textgrid_uris: List[str]) -> Response:
        """Copies the objects belonging to the given URIs to new revisions of themselves.

        Also copies all aggregated objects (from aggregations/editions/collections).

        Args:
            sid (str): Session ID
            textgrid_uris (List[str]): Textgrid URIs of objects to copy

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service - UUID of copy job queued
        """
        params = {
            'sid': sid,
            'uri': textgrid_uris,
            'newRevision': 'true',
        }
        response = self._requests.get(
            self._url + '/copy', params=params, timeout=self._config.http_timeout
        )
        return self._handle_response(response)

    def publish(
        self, sid: str, textgrid_uri: str, ignore_warnings: bool = False, dry_run: bool = True
    ):
        """Publish the edition or collection belonging to the given URIs.

        Also publish all aggregated objects (from aggregations/editions/collections)

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI of object to publish
            ignore_warnings (bool): try publishing even if warnings occured
            dry_run (bool): do not really publish, just check

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service
        """
        params = {
            'sid': sid,
            'ignoreWarnings': str(ignore_warnings),
            'dryRun': str(dry_run),
        }
        response = self._requests.get(
            self._url + '/' + textgrid_uri + '/publish',
            params=params,
            timeout=self._config.http_timeout,
        )
        return self._handle_response(response)

    def get_status(self, job_id) -> Response:
        """Get status for job specified by job_id.

        Args:
            job_id (str): ID of job to get the status for

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service - with XML containing the publish status
        """
        response = self._requests.get(
            self._url + '/' + job_id + '/status', timeout=self._config.http_timeout
        )
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: Response) -> Response:
        """Error handling for responses from tgpublish.

        Args:
            response (Response): a response from tgpublish

        Raises:
            TextgridPublishException: if HTTP-Status >= 400

        Returns:
            Response: the response
        """
        if not response.ok:
            message = (
                '[Error] HTTP Code: ' + str(response.status_code) + ' - ' + response.text[0:255]
            )
            logger.warning(message)
            raise TextgridPublishException(message)
        return response


class TextgridPublish(TextgridPublishRequest):
    """Provide access to the Textgrid Publish Service using XML data binding.

    API docs:
    https://textgridlab.org/doc/services/submodules/kolibri/kolibri-tgpublish-service/docs/index.html
    """

    def __init__(self, config: TextgridConfig = TextgridConfig()) -> None:
        super().__init__(config)
        # It’s recommended to either reuse the same parser/serializer instance
        # or reuse the context instance. see https://xsdata.readthedocs.io/en/latest/xml.html
        context = XmlContext()
        self._parser = XmlParser(context=context)

    def copy(self, sid: str, textgrid_uris: List[str], project_id: str) -> str:
        """Copies the objects belonging to the given URIs to the given project ID.

        Also copies all aggregated objects (from aggregations/editions/collections).

        Args:
            sid (str): Session ID
            textgrid_uris (List[str]): Textgrid URIs of objects to copy
            project_id (str): Project ID of the project to copy the objects to.

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            str: UUID of copy job queued
        """
        response = super().copy(sid=sid, textgrid_uris=textgrid_uris, project_id=project_id)
        return response.text

    def copy_to_new_revision(self, sid: str, textgrid_uris: List[str]) -> str:
        """Copies the objects belonging to the given URIs to new revisions of themselves.

        Also copies all aggregated objects (from aggregations/editions/collections).

        Args:
            sid (str): Session ID
            textgrid_uris (List[str]): Textgrid URIs of objects to copy

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            str: UUID of copy job queued
        """
        response = super().copy_to_new_revision(sid=sid, textgrid_uris=textgrid_uris)
        return response.text

    def publish(
        self, sid: str, textgrid_uri: str, ignore_warnings: bool = False, dry_run: bool = True
    ):
        """Publish the edition or collection belonging to the given URIs.

        Also publish all aggregated objects (from aggregations/editions/collections)

        Args:
            sid (str): Session ID
            textgrid_uri (str): Textgrid URI of object to publish
            ignore_warnings (bool): try publishing even if warnings occured
            dry_run (bool): do not really publish, just check

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            str: just an OK if the job started
        """
        response = super().publish(
            sid=sid, textgrid_uri=textgrid_uri, ignore_warnings=ignore_warnings, dry_run=dry_run
        )
        return response.text

    def get_status(self, job_id) -> PublishResponse:  # type: ignore
        """Get status for job specified by job_id.

        Args:
            job_id (str): ID of job to get the status for

        Raises:
            TextgridPublishException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            PublishResponse: publish response object
        """
        response = super().get_status(job_id)
        return self._parser.parse(BytesIO(response.content), PublishResponse)


class TextgridPublishException(Exception):
    """Exception communicating with tgpublish!"""
