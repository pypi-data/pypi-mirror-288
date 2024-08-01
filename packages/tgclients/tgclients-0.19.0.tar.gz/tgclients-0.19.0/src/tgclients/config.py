# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

"""Variable config options with defaults to be used with the TextGrid clients library."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT: float = 120.00

PROD_SERVER: str = 'https://textgridlab.org'
DEV_SERVER: str = 'https://dev.textgridlab.org'
TEST_SERVER: str = 'https://test.textgridlab.org'


class TextgridConfig:
    """Provide standard configuration / URLs for TextGrid services.

    Default is to connect to the TextGrid
    production server (https://textgridlab.org).
    Pass the constants tgclients.config.DEV_SERVER or
    tgclients.config.TEST_SERVER to the constructor to change to
    develop or test server or provide an URL for your own instance.
    """

    def __init__(self, host: Optional[str] = 'https://textgridlab.org') -> None:
        """TextGrid Service Endpoint Configuration.

        Overwrite the host string to connect to other servers, e.g.:
        * Test-Server: https://test.textgridlab.org
            (use constant tgclients.config.TEST_SERVER)
        * Development-Server: https://dev.textgridlab.org
            (use constant tgclients.config.DEV_SERVER)

        Args:
            host (Optional[str]):TextGrid server. Defaults to 'https://textgridlab.org'.
        """
        if not isinstance(host, str) or host == '':
            logger.info('host param was None or emtpy, default to: %s', PROD_SERVER)
            host = PROD_SERVER
        if host.endswith('/'):
            logger.info('trailing slash in hostname detected and removed')
            host = host[:-1]
        self._host = host
        self._http_timeout = DEFAULT_TIMEOUT

    @property
    def host(self) -> str:
        """The host URL.

        Returns:
            str: the configured host URL
        """
        return self._host

    @property
    def auth_wsdl(self) -> str:
        """The tgauth WSDL location.

        Returns:
            str: the tgauth WSDL location
        """
        return self._host + '/1.0/tgauth/wsdl/tgextra.wsdl'

    @property
    def auth_address(self) -> str:
        """The tgauth service location.

        Returns:
            str: the tgauth service location
        """
        return self._host + '/1.0/tgauth/tgextra.php'

    @property
    def extra_crud_wsdl(self) -> str:
        """The tgextra WSDL location.

        Returns:
            str: the tgextra WSDL location
        """
        return self._host + '/1.0/tgauth/wsdl/tgextra-crud.wsdl'

    @property
    def extra_crud_address(self) -> str:
        """The tgextra service location.

        Returns:
            str: the tgextra service location
        """
        return self._host + '/1.0/tgauth/tgextra-crud.php'

    @property
    def search(self) -> str:
        """The nonpublic tgsearch service location.

        Returns:
            str: the nonpublic tgsearch service location
        """
        return self._host + '/1.0/tgsearch'

    @property
    def search_public(self) -> str:
        """The public tgsearch service location.

        Returns:
            str: the public tgsearch service location
        """
        return self._host + '/1.0/tgsearch-public'

    @property
    def crud(self) -> str:
        """The nonpublic tgcrud REST service location.

        Returns:
            str: the nonpublic tgcrud REST service location
        """
        return self._host + '/1.0/tgcrud/rest'

    @property
    def crud_public(self) -> str:
        """The public tgcrud REST service location.

        Returns:
            str: the public tgcrud REST service location
        """
        return self._host + '/1.0/tgcrud-public/rest'

    @property
    def aggregator(self) -> str:
        """The aggregator service location.

        Returns:
            str: the aggregator service location
        """
        return self._host + '/1.0/aggregator'

    @property
    def publish(self) -> str:
        """The publish service location.

        Returns:
            str: the publish service location
        """
        return self._host + '/1.0/tgpublish'

    @property
    def http_timeout(self) -> float:
        """HTTP timeout to be used when accessing TextGrid services.

        Returns:
            float: http timeout in seconds
        """
        return self._http_timeout

    @http_timeout.setter
    def http_timeout(self, value: float) -> None:
        """Set HTTP timeout to be used when accessing TextGrid services.

        Args:
            value (float): the timeout
        """
        self._http_timeout = value
