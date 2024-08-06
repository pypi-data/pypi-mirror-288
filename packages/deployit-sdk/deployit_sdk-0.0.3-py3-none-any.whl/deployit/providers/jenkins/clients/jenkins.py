import logging
from typing import Dict

from deployit.providers.jenkins.clients.http import HTTPClient
from deployit.providers.jenkins.models.url import JenkinsURLBuilder

logger = logging.getLogger(__name__)


class JenkinsAPIClient:
    def __init__(self, url_builder: JenkinsURLBuilder, http_client: HTTPClient):
        """
        Initialize the JenkinsAPIClient with a URL builder and HTTP client.

        Parameters
        ----------
        url_builder : JenkinsURLBuilder
            The URL builder instance.
        http_client : HTTPClient
            The HTTP client instance.
        """
        self.url_builder = url_builder
        self.http_client = http_client

    def make_request(
        self, endpoint_template: str, method: str = "GET", **kwargs
    ) -> Dict:
        """
        Make a request to the Jenkins API.

        Parameters
        ----------
        endpoint_template : str
            The template of the endpoint URL.
        method : str, optional
            The HTTP method to use (default is 'GET').
        kwargs : dict
            Additional parameters to format the endpoint template.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        ValueError
            If an unsupported method is used.
        """
        url = self.url_builder.build_url(endpoint_template, **kwargs)
        if kwargs["query"]:
            url = f"{url}?{kwargs['query']}"
        headers = {"jenkins-crumb": self.url_builder.crumb.crumb}
        if method == "GET":
            return self.http_client.get(url, headers=headers)
        if method == "POST":
            return self.http_client.post(url, headers=headers)
        if method == "PUT":
            return self.http_client.put(url, headers=headers)
        if method == "DELETE":
            return self.http_client.delete(url, headers=headers)
        logger.error(f"Unsupported method: {method}")
        raise ValueError(f"Unsupported method: {method}")
