from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Build(BaseModel):
    """
    Data model representing a Jenkins build.

    Attributes
    ----------
    id : int
        The ID of the build.
    number : int
        The number of the build.
    url : str
        The URL of the build.
    status : str, optional
        The status of the build (default is 'pending').
    result : str, optional
        The result of the build (default is None).
    console_log : str, optional
        The console log of the build (default is an empty string).
    """
    id: int
    number: int
    url: str
    timestamp: Optional[datetime]
    status: Optional[str] = "pending"
    result: Optional[str] = None
    console_log: Optional[str] = ""

    def update_status(self, status: str) -> None:
        """
        Update the status of the build.

        Parameters
        ----------
        status : str
            The new status of the build.
        """
        self.status = status

    def set_result(self, result: str) -> None:
        """
        Set the result of the build.

        Parameters
        ----------
        result : str
            The result of the build.
        """
        self.result = result