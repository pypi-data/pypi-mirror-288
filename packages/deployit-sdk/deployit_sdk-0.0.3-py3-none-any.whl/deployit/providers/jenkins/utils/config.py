import os


class Config:
    """
    Configuration settings for the Jenkins API library.

    Attributes
    ----------
    JENKINS_DOMAIN : str
        The base URL for the Jenkins server.
    USERNAME : str
        The username for authenticating with Jenkins.
    API_TOKEN : str
        The API token for authenticating with Jenkins.
    TIMEOUT : int
        Timeout duration for API requests.
    """

    JENKINS_DOMAIN = os.getenv("JENKINS_DOMAIN", "localhost")
    USERNAME = os.getenv("JENKINS_USERNAME", "your_username")
    API_TOKEN = os.getenv("JENKINS_API_TOKEN", "your_api_token")
    TIMEOUT = int(os.getenv("JENKINS_TIMEOUT", "10"))
