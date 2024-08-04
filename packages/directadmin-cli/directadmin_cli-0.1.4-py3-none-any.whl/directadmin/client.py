"""
DirectAdmin API Client Module
"""

from typing import Dict, Any
import json
from urllib.parse import parse_qs, urljoin, urlencode, urlparse, urlunparse
from abc import ABC

import requests
from requests.auth import HTTPBasicAuth

# Admin Endpoints
GET_ALL_USERS = "CMD_API_SHOW_ALL_USERS"
GET_ALL_ADMINS = "CMD_API_SHOW_ADMINS"
GET_ALL_RESELLERS = "CMD_API_SHOW_RESELLERS"
GET_ADMIN_STATS = "CMD_API_ADMIN_STATS"
CREATE_ADMIN_ACCOUNT = "CMD_ACCOUNT_ADMIN"

# Reseller Endpoint
GET_RESELLER_PACKAGES = "CMD_API_PACKAGES_RESELLER"
GET_RESELLER_IP_LIST = "CMD_API_SHOW_RESELLER_IPS"
CREATE_RESELLER_ACCOUNT = "CMD_ACCOUNT_RESELLER"

# User Endpoints
GET_USER_PACKAGES = "CMD_API_PACKAGES_USER"
GET_USER_CONFIG = "CMD_API_SHOW_USER_CONFIG"
GET_USER_USAGE = "CMD_API_SHOW_USER_USAGE"
GET_USER_DOMAIN = "CMD_API_SHOW_USER_DOMAINS"
CREATE_USER_ACCOUNT = "CMD_API_ACCOUNT_USER"


class BaseDirectAdminAPIClient(ABC):
    """
    A base class for interacting with the DirectAdmin API.

    This class provides methods for making HTTP requests to the DirectAdmin API, handling authentication,
    and processing responses.

    Attributes:
        server (str): The base URL of the DirectAdmin server.
        ssl (bool): Whether to verify SSL certificates. Defaults to False.
        __auth (HTTPBasicAuth): HTTP basic authentication credentials.
        user_agent (str): The User-Agent header to be sent with requests. Defaults to "DirectAdmin Client/0.1.0".

    Methods:
        _make_request(endpoint, params=None, method="GET", data=None):
            Makes an HTTP request to the DirectAdmin API with the specified parameters.

        _build_url(endpoint, params=None):
            Constructs a full URL by combining the server base URL with the endpoint and optional query parameters.

        _parse_response(response):
            Parses the response from the DirectAdmin API, handling both JSON and query string formats.

    Args:
        server (str): The base URL of the DirectAdmin server.
        username (str): The username for HTTP basic authentication.
        password (str): The password for HTTP basic authentication.
        ssl (bool, optional): Whether to use SSL verification for requests. Defaults to False.
        user_agent (str, optional): The User-Agent string to be used in requests. Defaults to "DirectAdmin Client/0.1.0".
    """

    def __init__(self, server, username, password, ssl=False, user_agent=None):
        """
        Initializes the BaseDirectAdminAPIClient with the provided parameters.

        Args:
            server (str): The base URL of the DirectAdmin server.
            username (str): The username for HTTP basic authentication.
            password (str): The password for HTTP basic authentication.
            ssl (bool, optional): Whether to use SSL verification for requests. Defaults to False.
            user_agent (str, optional): The User-Agent string to be used in requests. Defaults to "DirectAdmin Client/0.1.0".
        """
        self.server = server
        self.ssl = ssl
        self.__auth = HTTPBasicAuth(username, password)
        self.user_agent = user_agent or "DirectAdmin Client/0.1.0"

    def _make_request(self, endpoint, params=None, method="GET", data=None):
        """
        Makes an HTTP request to the DirectAdmin API with the specified parameters.

        Args:
            endpoint (str): The API endpoint to request.
            params (dict, optional): A dictionary of query parameters to include in the request URL.
            method (str, optional): The HTTP method to use for the request. Defaults to "GET". Can be "GET" or "POST".
            data (dict, optional): Data to be sent in the body of a POST request. Ignored for GET requests.

        Returns:
            dict: The parsed response from the DirectAdmin API, as a dictionary.

        Raises:
            ValueError: If the provided method is not "GET" or "POST".
        """
        url = self._build_url(endpoint, params)
        headers = {"User-Agent": self.user_agent}
        if method == "GET":
            response = requests.get(
                url, auth=self.__auth, verify=self.ssl, headers=headers, timeout=60
            )
        elif method == "POST":
            response = requests.post(
                url,
                auth=self.__auth,
                verify=self.ssl,
                headers=headers,
                data=data,
                timeout=60,
            )
        else:
            raise ValueError("Method must be GET or POST")
        return self._parse_response(response)

    def _build_url(self, endpoint, params=None):
        """
        Constructs a full URL by combining the server base URL with the endpoint and optional query parameters.

        Args:
            endpoint (str): The API endpoint to append to the base URL.
            params (dict, optional): A dictionary of query parameters to include in the URL.

        Returns:
            str: The full URL constructed from the base URL, endpoint, and query parameters.
        """
        base_url = self.server.rstrip("/")
        url = urljoin(base_url, endpoint.lstrip("/"))

        if params:
            query_string = urlencode(params)
            url_parts = list(urlparse(url))
            url_parts[4] = query_string
            url = urlunparse(url_parts)
        return url

    @staticmethod
    def _parse_response(response):
        """
        Parses the response from the DirectAdmin API, handling both JSON and query string formats.

        Args:
            response (requests.Response): The HTTP response object to parse.

        Returns:
            dict: The parsed response data, either from JSON or query string format. Returns an empty dictionary if parsing fails.
        """
        response_text = response.text.strip()

        try:
            parsed_data = json.loads(response_text)
        except json.JSONDecodeError:
            parsed_data = parse_qs(response_text)

        if isinstance(parsed_data, dict):
            if "list[]" in parsed_data:
                return parsed_data["list[]"]
            return parsed_data
        print("Unexpected response format")
        return {}


class DirectAdminAPIClient(BaseDirectAdminAPIClient):
    """
    A client for interacting with the DirectAdmin API.

    This class provides methods to interact with the DirectAdmin API endpoints,
    allowing you to manage resellers, admins, users, and their related configurations
    and statistics.

    Properties:
        get_all_resellers (list): Fetches a list of all resellers.
        get_all_admins (list): Fetches a list of all admins.
        get_all_users (list): Fetches a list of all users.
        get_all_reseller_packages (list): Fetches a list of all reseller packages.
        get_all_user_packages (list): Fetches a list of all user packages.
        get_reseller_ip_list (list): Fetches a list of IP addresses associated with resellers.
        get_admin_stats (Dict[str, Any]): Fetches statistics about the admin.

    Methods:
        get_reseller_package(package_name: str) -> Dict[str, Any]:
            Fetches details about a specific reseller package.

        get_user_package(package_name: str) -> Dict[str, Any]:
            Fetches details about a specific user package.

        get_user_config(username: str) -> Dict[str, Any]:
            Fetches configuration details for a specific user.

        get_user_usage(username: str) -> Dict[str, Any]:
            Fetches usage statistics for a specific user.

        get_user_domain(username: str) -> Dict[str, Any]:
            Fetches domain information for a specific user.

        create_admin_account(username: str, email: str, passwd: str, notify: str) -> Dict[str, Any]:
            Creates a new admin account with the specified details.

        create_reseller_account(username: str, email: str, passwd: str, notify: str,
                                ip: str, package: str, domain: str) -> Dict[str, Any]:
            Creates a new reseller account with the specified details.

        create_user_account(username: str, email: str, passwd: str, notify: str, ip: str,
                            package: str, domain: str) -> Dict[str, Any]:
            Creates a new user account with the specified details.
    """

    @property
    def get_all_resellers(self) -> list:
        """
        Fetches a list of all resellers.

        Returns:
            list: A list of all resellers.
        """
        return self._make_request(GET_ALL_RESELLERS)

    @property
    def get_all_admins(self) -> list:
        """
        Fetches a list of all admins.

        Returns:
            list: A list of all admins.
        """
        return self._make_request(GET_ALL_ADMINS)

    @property
    def get_all_users(self) -> list:
        """
        Fetches a list of all admins.

        Returns:
            list: A list of all admins.
        """
        return self._make_request(GET_ALL_USERS)

    @property
    def get_all_reseller_packages(self) -> list:
        """
        Fetches a list of all reseller packages.

        Returns:
            list: A list of all reseller packages.
        """
        return self._make_request(GET_RESELLER_PACKAGES)

    @property
    def get_all_user_packages(self) -> list:
        """
        Fetches a list of all user packages.

        Returns:
            list: A list of all user packages.
        """
        return self._make_request(GET_USER_PACKAGES)

    @property
    def get_reseller_ip_list(self) -> list:
        """
        Fetches a list of IP addresses associated with resellers.

        Returns:
            list: A list of IP addresses associated with resellers.
        """
        return self._make_request(GET_RESELLER_IP_LIST)

    @property
    def get_admin_stats(self) -> Dict[str, Any]:
        """
        Fetches statistics about the admin.

        Returns:
            Dict[str, Any]: A dictionary containing admin statistics.
        """
        return self._make_request(GET_ADMIN_STATS)

    def get_reseller_package(self, package_name: str) -> Dict[str, Any]:
        """
        Fetches details about a specific reseller package.

        Args:
            package_name (str): The name of the reseller package.

        Returns:
            Dict[str, Any]: A dictionary containing details of the reseller package.
        """
        params = {"package": package_name}
        return self._make_request(endpoint=GET_RESELLER_PACKAGES, params=params)

    def get_user_package(self, package_name: str) -> Dict[str, Any]:
        """
        Fetches details about a specific user package.

        Args:
            package_name (str): The name of the user package.

        Returns:
            Dict[str, Any]: A dictionary containing details of the user package.
        """
        params = {"package": package_name}
        return self._make_request(endpoint=GET_USER_PACKAGES, params=params)

    def get_user_config(self, username: str) -> Dict[str, Any]:
        """
        Fetches configuration details for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            Dict[str, Any]: A dictionary containing configuration details of the user.
        """
        params = {"user": username}
        return self._make_request(endpoint=GET_USER_CONFIG, params=params)

    def get_user_usage(self, username: str) -> Dict[str, Any]:
        """
        Fetches usage statistics for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            Dict[str, Any]: A dictionary containing usage statistics of the user.
        """
        params = {"user": username}
        return self._make_request(endpoint=GET_USER_USAGE, params=params)

    def get_user_domain(self, username: str) -> Dict[str, Any]:
        """
        Fetches domain information for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            Dict[str, Any]: A dictionary containing domain information of the user.
        """

        params = {"user": username}
        return self._make_request(endpoint=GET_USER_DOMAIN, params=params)

    def create_admin_account(
        self, username: str, email: str, passwd: str, notify: str
    ) -> Dict[str, Any]:
        """
        Creates a new admin account with the specified details.

        Args:
            username (str): The username for the new admin account.
            email (str): The email address associated with the new admin account.
            passwd (str): The password for the new admin account.
            notify (str): Notification preferences.

        Returns:
            Dict[str, Any]: A dictionary containing the result of the account creation.
        """
        params = {
            "action": "create",
            "username": username,
            "email": email,
            "passwd": passwd,
            "passwd2": passwd,
            "notify": notify,
        }
        return self._make_request(endpoint=CREATE_ADMIN_ACCOUNT, params=params)

    def create_reseller_account(
        self,
        username: str,
        email: str,
        passwd: str,
        notify: str,
        ip: str,
        package: str,
        domain: str,
    ) -> Dict[str, Any]:
        """
        Creates a new reseller account with the specified details.

        Args:
            username (str): The username for the new reseller account.
            email (str): The email address associated with the new reseller account.
            passwd (str): The password for the new reseller account.
            notify (str): Notification preferences.
            ip (str): IP address assignment options. Must be one of "shared", "sharedreseller", or "assign".
            package (str): The package to assign to the new reseller account.
            domain (str): The domain for the new reseller account.

        Returns:
            Dict[str, Any]: A dictionary containing the result of the account creation.

        Raises:
            ValueError: If the provided IP address option is invalid.
        """
        ip_allowed_options = ["shared", "sharedreseller", "assign"]
        if ip not in ip_allowed_options:
            raise ValueError(
                f"Invalid IP address. IP should be one of {ip_allowed_options}"
            )

        params = {
            "action": "create",
            "add": "submit",
            "username": username,
            "email": email,
            "passwd": passwd,
            "passwd2": passwd,
            "domain": domain,
            "package": package,
            "ip": ip,
            "notify": notify,
        }
        return self._make_request(endpoint=CREATE_RESELLER_ACCOUNT, params=params)

    def create_user_account(
        self,
        username: str,
        email: str,
        passwd: str,
        notify: str,
        ip: str,
        package: str,
        domain: str,
    ) -> Dict[str, Any]:
        """
        Creates a new user account with the specified details.

        Args:
            username (str): The username for the new user account.
            email (str): The email address associated with the new user account.
            passwd (str): The password for the new user account.
            notify (str): Notification preferences.
            ip (str): IP address for the new user account.
            package (str): The package to assign to the new user account.
            domain (str): The domain for the new user account.

        Returns:
            Dict[str, Any]: A dictionary containing the result of the account creation.
        """
        params = {
            "action": "create",
            "add": "submit",
            "username": username,
            "email": email,
            "passwd": passwd,
            "passwd2": passwd,
            "domain": domain,
            "package": package,
            "ip": ip,
            "notify": notify,
        }
        return self._make_request(endpoint=CREATE_USER_ACCOUNT, params=params)