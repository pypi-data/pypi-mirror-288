from deployit.providers.jenkins.services.job import JenkinsJobApiService
from deployit.providers.jenkins.utils.errors import JenkinsError
from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.models.job import Job
from deployit.providers.jenkins.utils.presenter import RichPresenter

class JobRepository:
    """
    Repository for interacting with Jenkins job data.
    """
    def __init__(self, api_service: JenkinsJobApiService, presenter: RichPresenter = RichPresenter()):
        """
        Initialize the JobRepository with a Jenkins API client.

        Parameters
        ----------
        api_service : JenkinsJobApiService
            The Jenkins API service
        """
        self.api_service = api_service
        self.presenter = presenter

    def fetch_job_details(self, job: Job) -> Job:
        """
        Fetch details for a given job and update the job instance.

        Parameters
        ----------
        job : Job
            The job for which to fetch details.

        Returns
        -------
        Job
            The updated job instance.
        """
        self.presenter.info(f"Fetching details for job '{job.name}' with URL '{job.url}'")
        try:
            job_info = self.api_service.get_job_info(folder_url=job.url, short_name=job.name)
            self.presenter.debug(f"Job info received: {job_info}")

            job.name = job_info.get('name', job.name)
            job.url = job_info.get('url', job.url)
            job.color = job_info.get('color')
            job.subjobs = [Job(name=subjob['name'], url=subjob['url'])
                            for subjob in job_info.get('jobs', [])]
            job.build_history = self.fetch_all_builds(job)
            job.requires_parameters = bool(job_info.get('actions', [{}])[0].get('parameterDefinitions', []))
            job.required_parameters = [param['name'] for param in job_info['actions'][0]['parameterDefinitions']
                                   if param.get('defaultParameterValue') is None]

            self.presenter.info(f"Successfully fetched details for job '{job.name}'")
        except Exception as e:
            self.presenter.error(f"Error fetching job details for job '{job.name}': {e}")
            RichPresenter.show_error(f"Error fetching job details: {e}")
            raise JenkinsError(f"Error fetching job details: {e}")
        return job

    def fetch_all_builds(self, job: Job) -> list:
        """
        Fetch all builds for a given job.

        Parameters
        ----------
        job : Job
            The job for which to fetch builds.

        Returns
        -------
        list
            A list of builds associated with the job.
        """
        self.presenter.info(f"Fetching all builds for job '{job.name}' with URL '{job.url}'")
        try:
            builds_data = self.api_service.get_all_builds(folder_url=job.url, short_name=job.name)
            self.presenter.debug(f"Builds data received: {builds_data}")

            builds = [Build(id=build['number'], number=build['number'], url=build['url']) for build in builds_data.get('allBuilds', [])]
            self.presenter.info(f"Fetched {len(builds)} builds for job '{job.name}'")
            return builds
        except Exception as e:
            self.presenter.error(f"Error fetching builds for job '{job.name}': {e}")
            RichPresenter.show_error(f"Error fetching builds: {e}")
            raise JenkinsError(f"Error fetching builds for job '{job.name}': {e}")