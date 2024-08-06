"""
This module provides a service for interacting with Jenkins jobs.
"""

from typing import Dict

from deployit.providers.jenkins.endpoints.job import JobEndpoints
from deployit.providers.jenkins.parameters.base import DeployParameters
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService


class JenkinsJobApiService(JenkinsApiService):
    """
    A service class for interacting with Jenkins jobs.
    """

    def __init__(self, jenkins_client):
        super().__init__(jenkins_client)
        self.presenter = RichPresenter()

    def get_all_jobs(self, tree: str) -> Dict:
        """
        Retrieve all jobs information with a specific tree structure.

        Parameters
        ----------
        tree : str
            The tree structure for retrieving job information.

        Returns
        -------
        dict
            Information about all jobs.
        """
        self.presenter.info(f"Retrieving all jobs with tree structure: {tree}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.JOBS_QUERY, method="GET", tree=tree
            )
            self.presenter.info("Successfully retrieved all jobs.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving all jobs: {e}")
            raise

    def get_job_info(self, folder_url: str, short_name: str, depth: int = 1) -> Dict:
        """
        Retrieve information about a specific job.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The job information.
        """
        self.presenter.info(
            f"Retrieving job info for {short_name} in {folder_url} with depth {depth}"
        )
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.JOB_INFO,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                depth=depth,
            )
            self.presenter.info("Successfully retrieved job info.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving job info: {e}")
            raise

    def build_job(self, folder_url: str, short_name: str) -> Dict:
        """
        Trigger a build for a specific job.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.

        Returns
        -------
        dict
            The response from triggering the build.
        """
        self.presenter.info(f"Triggering build for job {short_name} in {folder_url}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_JOB,
                method="POST",
                folder_url=folder_url,
                short_name=short_name,
            )
            self.presenter.info("Successfully triggered build.")
            return response
        except Exception as e:
            self.presenter.error(f"Error triggering build: {e}")
            raise

    def build_with_params(self, folder_url: str, short_name: str, params: Dict) -> Dict:
        """
        Trigger a build for a specific job with parameters.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        params : dict
            The parameters to pass to the job.

        Returns
        -------
        dict
            The response from triggering the build with parameters.
        """
        self.presenter.info(
            f"Triggering build with parameters for job {short_name} in {folder_url} with params {params}"
        )
        try:
            request_query = DeployParameters(**params).to_url_query()
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_WITH_PARAMETERS,
                method="POST",
                query=request_query,
                folder_url=folder_url,
                short_name=short_name,
            )
            self.presenter.info("Successfully triggered build with parameters.")
            return response
        except Exception as e:
            self.presenter.error(f"Error triggering build with parameters: {e}")
            raise

    def get_all_builds(self, folder_url: str, short_name: str, tree: str) -> Dict:
        """
        Retrieve all builds information for a specific job with a specific tree structure.

        Parameters
        ----------
        folder_url : str
            The URL of the folder containing the job.
        short_name : str
            The short name of the job.
        tree : str
            The tree structure for retrieving build information.

        Returns
        -------
        dict
            Information about all builds for the job.
        """
        self.presenter.info(
            f"Retrieving all builds for job {short_name} in {folder_url} with tree structure {tree}"
        )
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.ALL_BUILDS,
                method="GET",
                folder_url=folder_url,
                short_name=short_name,
                tree=tree,
            )
            self.presenter.info("Successfully retrieved all builds.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving all builds: {e}")
            raise
