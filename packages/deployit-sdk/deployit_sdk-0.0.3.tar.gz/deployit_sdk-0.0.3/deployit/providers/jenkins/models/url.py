from presentation.rich import RichPresenter
from pydantic import BaseModel, HttpUrl


class JenkinsCrumb(BaseModel):
    crumb: str


class JenkinsURLBuilder(BaseModel):
    base_url: HttpUrl
    crumb: JenkinsCrumb
    presenter = RichPresenter()

    def build_url(self, endpoint_template: str, **kwargs) -> str:
        """
        Build a complete URL for a Jenkins API endpoint.

        Parameters
        ----------
        endpoint_template : str
            The template of the endpoint URL.
        kwargs : dict
            Additional parameters to format the endpoint template.

        Returns
        -------
        str
            The complete URL.
        """
        self.presenter.info(f"Building URL with template: {endpoint_template}")
        self.presenter.info(f"Using base URL: {self.base_url}")
        self.presenter.info(f"Additional parameters: {kwargs}")

        try:
            endpoint = endpoint_template.format(**kwargs)
            complete_url = f"{self.base_url}/{endpoint}"
            self.presenter.info(f"Successfully built URL: {complete_url}")
            return complete_url
        except KeyError as e:
            self.presenter.error(f"Missing parameter for URL template: {e}")
            raise
        except Exception as e:
            self.presenter.error(f"Error building URL: {e}")
            raise
