# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""API for the TextGrid aggregator service."""

import logging
from typing import List, Optional, Union, overload

import requests
from requests.models import Response

from tgclients.config import TextgridConfig

logger = logging.getLogger(__name__)


class Aggregator:
    """Provide access to the Textgrid Aggregator Service.

    API docs: https://textgridlab.org/doc/services/submodules/aggregator/docs/api.html
    """

    def __init__(self, config: TextgridConfig = TextgridConfig()) -> None:
        self._url = config.aggregator
        self._config = config
        self._requests = requests.Session()

    @overload
    def zip(self, textgrid_uris: str, sid: Optional[str] = None) -> Response: ...

    @overload
    def zip(self, textgrid_uris: List[str], sid: Optional[str] = None) -> Response: ...

    def zip(self, textgrid_uris: Union[str, List[str]], sid: Optional[str] = None) -> Response:
        """Download aggregated TextGrid objects as ZIP file.

        https://textgridlab.org/doc/services/submodules/aggregator/docs/zip.html

        Args:
            textgrid_uris (Union[str, List[str]]): a single or a list of TextGrid URIs
            sid (Optional[str], optional): Session ID. Defaults to None.

        Returns:
            Response: the response with zip file in body.content
        """
        if isinstance(textgrid_uris, list):
            textgrid_uris = ','.join(textgrid_uris)
        url = self._url + '/zip/'
        response = self._requests.get(
            url + textgrid_uris, params={'sid': sid}, timeout=self._config.http_timeout
        )
        return response

    @overload
    def text(self, textgrid_uris: str, sid: Optional[str] = None) -> Response: ...

    @overload
    def text(self, textgrid_uris: List[str], sid: Optional[str] = None) -> Response: ...

    # python 3.10 allows writing Union as |
    # https://www.blog.pythonlibrary.org/2021/09/11/python-3-10-simplifies-unions-in-type-annotations/
    def text(self, textgrid_uris: Union[str, List[str]], sid: Optional[str] = None) -> Response:
        """Download aggregated TextGrid objects as plain text file.

        Args:
            textgrid_uris (Union[str, List[str]]): a single or a list of TextGrid URIs
            sid (Optional[str], optional): Session ID. Defaults to None.

        Returns:
            Response: the respone with the text in the body
        """
        if isinstance(textgrid_uris, list):
            textgrid_uris = ','.join(textgrid_uris)
        url = self._url + '/text/'
        response = self._requests.get(
            url + textgrid_uris, params={'sid': sid}, timeout=self._config.http_timeout
        )
        return response

    @overload
    def teicorpus(self, textgrid_uris: str, sid: Optional[str] = None) -> Response: ...

    @overload
    def teicorpus(self, textgrid_uris: List[str], sid: Optional[str] = None) -> Response: ...

    def teicorpus(
        self, textgrid_uris: Union[str, List[str]], sid: Optional[str] = None
    ) -> Response:
        """Download aggregated TextGrid objects as TEI corpus.

        Args:
            textgrid_uris (Union[str, List[str]]): a single or a list of TextGrid URIs
            sid (Optional[str], optional): Session ID. Defaults to None.

        Returns:
            Response: the respone with the TEI corpus in the body
        """
        if isinstance(textgrid_uris, list):
            textgrid_uris = ','.join(textgrid_uris)
        url = self._url + '/teicorpus/'
        response = self._requests.get(
            url + textgrid_uris, params={'sid': sid}, timeout=self._config.http_timeout
        )
        return response

    @overload
    def render(
        self,
        textgrid_uris: str,
        sid: Optional[str] = None,
        stylesheet_uri: Optional[str] = None,
        mediatype: Optional[str] = None,
        link_pattern: Optional[str] = None,
        sandbox: Optional[bool] = None,
    ) -> Response: ...

    @overload
    def render(
        self,
        textgrid_uris: List[str],
        sid: Optional[str] = None,
        stylesheet_uri: Optional[str] = None,
        mediatype: Optional[str] = None,
        link_pattern: Optional[str] = None,
        sandbox: Optional[bool] = None,
    ) -> Response: ...

    def render(  # noqa: PLR0913
        self,
        textgrid_uris: Union[str, List[str]],
        sid: Optional[str] = None,
        stylesheet_uri: Optional[str] = None,
        mediatype: Optional[str] = None,
        link_pattern: Optional[str] = None,
        sandbox: Optional[bool] = None,
    ) -> Response:
        """Apply an XSLT stylesheet to one or more TextGrid URIs.

        Will render (X)HTML by default with XSLT stylesheets from tei-c.org
        see https://textgridlab.org/doc/services/submodules/aggregator/docs/html.html

        Args:
            textgrid_uris (Union[str, List[str]]): a single or a list of TextGrid URIs
            sid (Optional[str], optional): Session ID. Defaults to None.
            stylesheet_uri (Optional[str], optional): alternative XSLT stylesheet to use.
                                                      Must be a TextGrid URI.
            mediatype (Optional[str], optional): The requested content type.
                                                 E.g., text/html or text/xml. Default is text/html
            link_pattern (Optional[str], optional): URL pattern for links.
                                                    @URI@ will be replaced with the textgrid: URI.
            sandbox (Optional[bool], optional): access sandboxed data. Defaults to false

        Returns:
            Response: the respone with the TEI corpus in the body
        """
        if isinstance(textgrid_uris, list):
            textgrid_uris = ','.join(textgrid_uris)
        url = self._url + '/html/'
        response = self._requests.get(
            url + textgrid_uris,
            params={
                'sid': sid,
                'stylesheet': stylesheet_uri,
                'mediatype': mediatype,
                'linkPattern': link_pattern,
                'sandbox': sandbox,
            },
            timeout=self._config.http_timeout,
        )
        return response
