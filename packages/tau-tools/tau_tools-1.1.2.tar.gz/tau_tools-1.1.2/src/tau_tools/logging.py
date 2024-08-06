from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn
from rich.table import Column
from rich.traceback import install

console = Console()
progress = Progress(
    TextColumn(
        "[progress.description]{task.description}",
        table_column=Column(width=50),
    ),
    BarColumn(bar_width=None),
    MofNCompleteColumn(table_column=Column(width=10, justify="right")),
    console=console,
    expand=True,
    transient=True,
)


def setup_logging():
    install()
