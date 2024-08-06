from deployit.providers.jenkins.clients.jenkins import JenkinsAPIClient
from deployit.providers.jenkins.repositories.job import JobRepository
from deployit.providers.jenkins.repositories.build import BuildRepository
from deployit.providers.jenkins.services.common import JenkinsCommonApiService
from deployit.providers.jenkins.services.build import JenkinsBuildApiService
from deployit.providers.jenkins.services.job import JenkinsJobApiService
from deployit.providers.jenkins.presentation.rich import RichPresenter

class JenkinsClient:
    """
    JenkinsClient acts as an entry point to access various functionalities of the Jenkins client.

    Attributes
    ----------
    job_repository : JobRepository
        An instance of JobRepository to manage job-related operations.
    build_repository : BuildRepository
        An instance of BuildRepository to manage build-related operations.
    common_service : JenkinsCommonApiService
        An instance of JenkinsCommonApiService to manage common Jenkins API operations.
    build_service : JenkinsBuildApiService
        An instance of JenkinsBuildApiService to manage build-related Jenkins API operations.
    job_service : JenkinsJobApiService
        An instance of JenkinsJobApiService to manage job-related Jenkins API operations.
    presenter : RichPresenter
        An instance of RichPresenter to handle presentation logic.
    """

    def __init__(self, base_url: str, username: str, password: str):
        """
        Initializes the JenkinsClient with instances of repositories, services, and parameters.

        Parameters
        ----------
        base_url : str
            The base URL of the Jenkins server.
        username : str
            The username for authentication.
        password : str
            The password or API token for authentication.
        """
        self.jenkins_client = JenkinsAPIClient(base_url, username, password)
        self.job_service = JenkinsJobApiService(self.jenkins_client)
        self.build_service = JenkinsBuildApiService(self.jenkins_client)
        self.common_service = JenkinsCommonApiService(self.jenkins_client)
        self.job_repository = JobRepository(self.job_service)
        self.build_repository = BuildRepository(self.build_service)
        self.presenter = RichPresenter()

    def get_job_repository(self) -> JobRepository:
        """
        Get the JobRepository instance.

        Returns
        -------
        JobRepository
            The instance of JobRepository.
        """
        return self.job_repository

    def get_build_repository(self) -> BuildRepository:
        """
        Get the BuildRepository instance.

        Returns
        -------
        BuildRepository
            The instance of BuildRepository.
        """
        return self.build_repository

    def get_common_service(self) -> JenkinsCommonApiService:
        """
        Get the JenkinsCommonApiService instance.

        Returns
        -------
        JenkinsCommonApiService
            The instance of JenkinsCommonApiService.
        """
        return self.common_service

    def get_build_service(self) -> JenkinsBuildApiService:
        """
        Get the JenkinsBuildApiService instance.

        Returns
        -------
        JenkinsBuildApiService
            The instance of JenkinsBuildApiService.
        """
        return self.build_service

    def get_job_service(self) -> JenkinsJobApiService:
        """
        Get the JenkinsJobApiService instance.

        Returns
        -------
        JenkinsJobApiService
            The instance of JenkinsJobApiService.
        """
        return self.job_service

    def get_presenter(self) -> RichPresenter:
        """
        Get the Presenter instance.

        Returns
        -------
        RichPresenter
            The instance of RichPresenter.
        """
        return self.presenter