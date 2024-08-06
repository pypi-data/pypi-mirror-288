class CommonEndpoints:
    """
    Common endpoints for Jenkins.

    Attributes
    ----------
    CRUMB_ISSUER : str
        URL template to get the crumb issuer for CSRF protection.
    INFO : str
        URL template to get general information about the Jenkins instance.
    WHOAMI_URL : str
        URL template to get information about the current user.
    """

    CRUMB_ISSUER: str = "crumbIssuer/api/json"
    INFO: str = "api/json"
    WHOAMI_URL: str = "me/api/json?depth={depth}"
