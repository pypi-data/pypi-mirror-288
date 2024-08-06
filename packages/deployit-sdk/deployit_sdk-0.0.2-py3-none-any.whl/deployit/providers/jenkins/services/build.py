from typing import Dict

from deployit.providers.jenkins.endpoints.build import BuildEndpoints
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService
from deployit.providers.jenkins.utils.errors import JenkinsError


class JenkinsBuildApiService(JenkinsApiService):
    def __init__(self, jenkins_client):
        super().__init__(jenkins_client)
        self.presenter = RichPresenter()

    def stop_build(self, folder_url: str, short_name: str, number: int) -> Dict:
        """
        Stop a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to stop.

        Returns
        -------
        dict
            The response from stopping the build.
        """
        self.presenter.info(
            f"Stopping build {number} for job {short_name} in folder {folder_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.STOP_BUILD,
                method="POST",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
            )
            self.presenter.info(
                f"Successfully stopped build {number} for job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error stopping build {number} for job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error stopping build {number} for job {short_name}: {e}"
            )
            raise

    def get_build_info(
        self, folder_url: str, short_name: str, number: int, depth: int = 1
    ) -> Dict:
        """
        Retrieve information about a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve information about.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The build information.
        """
        self.presenter.info(
            f"Retrieving information for build {number} of job {short_name} in folder {folder_url} with depth {depth}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_INFO,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
                depth=depth,
            )
            self.presenter.info(
                f"Successfully retrieved information for build {number} of job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving information for build {number} of job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving information for build {number} of job {short_name}: {e}"
            )
            raise

    def get_build_console_output(
        self, folder_url: str, short_name: str, number: int
    ) -> Dict:
        """
        Retrieve the console output of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve console output for.

        Returns
        -------
        dict
            The build console output.
        """
        self.presenter.info(
            f"Retrieving console output for build {number} of job {short_name} in folder {folder_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_CONSOLE_OUTPUT,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
            )
            self.presenter.info(
                f"Successfully retrieved console output for build {number} of job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving console output for build {number} of job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving console output for build {number} of job {short_name}: {e}"
            )
            raise

    def get_build_env_vars(
        self, folder_url: str, short_name: str, number: int, depth: int = 1
    ) -> Dict:
        """
        Retrieve the environment variables of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve environment variables for.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The environment variables of the build.
        """
        self.presenter.info(
            f"Retrieving environment variables for build {number} of job {short_name} in folder {folder_url} with depth {depth}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_ENV_VARS,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
                depth=depth,
            )
            self.presenter.info(
                f"Successfully retrieved environment variables for build {number} of job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving environment variables for build {number} of job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving environment variables for build {number} of job {short_name}: {e}"
            )
            raise

    def get_build_test_report(
        self, folder_url: str, short_name: str, number: int, depth: int = 1
    ) -> Dict:
        """
        Retrieve the test report of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve the test report for.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The test report of the build.
        """
        self.presenter.info(
            f"Retrieving test report for build {number} of job {short_name} in folder {folder_url} with depth {depth}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_TEST_REPORT,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
                depth=depth,
            )
            self.presenter.info(
                f"Successfully retrieved test report for build {number} of job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving test report for build {number} of job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving test report for build {number} of job {short_name}: {e}"
            )
            raise

    def get_build_artifact(
        self, folder_url: str, short_name: str, number: int, artifact: str
    ) -> Dict:
        """
        Retrieve a specific artifact from a build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve the artifact from.
        artifact : str
            The artifact path.

        Returns
        -------
        dict
            The artifact data.
        """
        self.presenter.info(
            f"Retrieving artifact {artifact} for build {number} of job {short_name} in folder {folder_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_ARTIFACT,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
                artifact=artifact,
            )
            self.presenter.info(
                f"Successfully retrieved artifact {artifact} for build {number} of job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving artifact {artifact} for build {number} of job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving artifact {artifact} for build {number} of job {short_name}: {e}"
            )
            raise

    def get_build_stages(self, folder_url: str, short_name: str, number: int) -> Dict:
        """
        Retrieve the stages of a specific build.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        number : int
            The build number to retrieve stages for.

        Returns
        -------
        dict
            The build stages information.
        """
        self.presenter.info(
            f"Retrieving stages for build {number} of job {short_name} in folder {folder_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                BuildEndpoints.BUILD_STAGES,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                number=number,
            )
            self.presenter.info(
                f"Successfully retrieved stages for build {number} of job {short_name}."
            )
            return response
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error retrieving stages for build {number} of job {short_name}: {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error retrieving stages for build {number} of job {short_name}: {e}"
            )
            raise
