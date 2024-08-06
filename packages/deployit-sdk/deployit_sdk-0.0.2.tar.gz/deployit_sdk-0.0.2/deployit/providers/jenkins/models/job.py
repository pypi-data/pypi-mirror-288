from typing import List, Optional

from pydantic import BaseModel

from deployit.providers.jenkins.models.build import Build


class Job(BaseModel):
    """
    Model representing a Jenkins job.

    Attributes
    ----------
    name : str
        The name of the job.
    url : str
        The URL of the job.
    build_history : Optional[List[Build]]
        The build history of the job.
    subjobs : Optional[List[Job]]
        The subjobs of the job.
    color : Optional[str]
        The color of the job.
    requires_parameters : Optional[bool]
        Whether the job requires parameters.
    required_parameters : Optional[List[str]]
        The list of required parameters
    """

    name: str
    url: str
    build_history: Optional[List[Build]] = []
    subjobs: Optional[List["Job"]] = []
    color: Optional[str] = None
    requires_parameters: Optional[bool] = False
    required_parameters: Optional[List[str]] = []
