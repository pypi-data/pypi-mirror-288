from deployit.providers.jenkins.utils.errors import JenkinsError
from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.services.build import JenkinsBuildApiService
from deployit.providers.jenkins.presentation.rich import RichPresenter

class BuildRepository:
    """
    Repository for interacting with Jenkins build data.
    """
    def __init__(self, api_service: JenkinsBuildApiService):
        """
        Initialize the BuildRepository with a Jenkins API client.

        Parameters
        ----------
        api_service : JenkinsBuildApiService
            The Jenkins build api endpoints instance.
        """
        self.api_service = api_service
        self.presenter = RichPresenter()

    def fetch_build_status(self, build: Build, folder_url: str, short_name: str) -> str:
        """
        Fetch the status of a given build.

        Parameters
        ----------
        build : Build
            The build object.
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.

        Returns
        -------
        str
            The status of the build.
        """
        self.presenter.info(f"Fetching status for build {build.number} of job {short_name} in folder {folder_url}.")
        try:
            build_info = self.api_service.get_build_info(folder_url, short_name, build.number)
            status = build_info.get('result', 'UNKNOWN')
            self.presenter.info(f"Successfully fetched status for build {build.number} of job {short_name}: {status}")
            return status
        except JenkinsError as e:
            self.presenter.error(f"Jenkins error fetching status for build {build.number} of job {short_name}: {e}")
            raise
        except Exception as e:
            self.presenter.error(f"Unexpected error fetching status for build {build.number} of job {short_name}: {e}")
            raise

    def get_build_console_output(self, build: Build, folder_url: str, short_name: str) -> str:
        """
        Retrieve the console output of a given build.

        Parameters
        ----------
        build : Build
            The build object.
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.

        Returns
        -------
        str
            The console output of the build.
        """
        self.presenter.info(f"Retrieving console output for build {build.number} of job {short_name} in folder {folder_url}.")
        try:
            console_output = self.api_service.get_build_console_output(folder_url, short_name, build.number)
            self.presenter.info(f"Successfully retrieved console output for build {build.number} of job {short_name}.")
            return console_output
        except JenkinsError as e:
            self.presenter.error(f"Jenkins error retrieving console output for build {build.number} of job {short_name}: {e}")
            raise
        except Exception as e:
            self.presenter.error(f"Unexpected error retrieving console output for build {build.number} of job {short_name}: {e}")
            raise