from typing import Any, List

from rich.live import Live
from rich.table import Table

from deployit.providers.jenkins.presentation.config import PresentationConfig
from deployit.providers.jenkins.utils.decorators import make_singleton


@make_singleton
class RichPresenter:
    def __init__(self, presentation_config: PresentationConfig = PresentationConfig()):
        self.config = presentation_config

    def print(self, message: str) -> None:
        """
        Print a message to the console.

        Parameters
        ----------
        message : str
            The message to print.
        """
        if self.config.use_rich_presentation:
            self.config.console.print(message)
        if self.config.logger:
            self.config.log(message)

    def display_table(
        self, title: str, columns: List[str], rows: List[List[Any]]
    ) -> None:
        """
        Display a table with specified columns and rows.

        Parameters
        ----------
        title : str
            The title of the table.
        columns : List[str]
            A list of column names.
        rows : List[List[Any]]
            A list of rows, where each row is a list of values.
        """
        table = Table(title=title, show_header=True)
        for column in columns:
            table.add_column(column, justify="right")
        for row in rows:
            table.add_row(*map(str, row))
        self.print(table)

    def display_error(self, error_message: str) -> None:
        """
        Display an error message.

        Parameters
        ----------
        error_message : str
            The error message to display.
        """
        self.print(f"[bold red]Error:[/bold red] {error_message}")

    def watch_console_log(self, log_output: str) -> None:
        """
        Display console log output in real-time.

        Parameters
        ----------
        log_output : str
            The log output to display.
        """
        with Live(console=self.config.console) as live:
            live.update(log_output)

    def display_dynamic_table(self, title: str, items: List[Any]) -> None:
        """
        Display a dynamic table based on the attributes of the items.

        Parameters
        ----------
        title : str
            The title of the table.
        items : List[Any]
            A list of objects to display in the table. Each object's attributes
            will be used as columns.
        """
        if not items:
            self.display_error("No items to display.")
            return

        table = Table(title=title, show_header=True)
        first_item = items[0]
        columns = [
            attr
            for attr in dir(first_item)
            if not attr.startswith("_") and not callable(getattr(first_item, attr))
        ]

        for column in columns:
            table.add_column(column.capitalize(), justify="right")

        for item in items:
            row = [str(getattr(item, column)) for column in columns]
            table.add_row(*row)

        self.print(table)

    def info(self, message: str) -> None:
        """
        Prints an informational message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.use_rich_presentation:
            self.config.console.print(message)
        if self.config.logger:
            self.config.logger.info(message)

    def error(self, message: str) -> None:
        """
        Prints an error message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.use_rich_presentation:
            self.config.console.print(f"[bold red]{message}[/bold red]")
        if self.config.logger:
            self.config.logger.error(message)

    def warn(self, message: str) -> None:
        """
        Prints a warning message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.use_rich_presentation:
            self.config.console.print(f"[bold yellow]{message}[/bold yellow]")
        if self.config.logger:
            self.config.logger.warning(message)

    def debug(self, message: str) -> None:
        """
        Prints a debug message to the console using rich presentation if enabled.

        Parameters
        ----------
        message : str
            The message to be printed.
        """
        if self.config.use_rich_presentation:
            self.config.console.print(f"[bold blue]{message}[/bold blue]")
        if self.config.logger:
            self.config.logger.debug(message)
