from rich.console import Console


def log_done(filepath: str, msg: str) -> None:
    console = Console()

    console.print(
        f"[bold green]✔[/] [bold]{filepath}[/] [dim]{msg}[/]",
        highlight=False,
    )


def log_error(filepath: str, msg: str) -> None:
    console = Console()

    console.print(f"[bold red]✗[/] {filepath} {msg}")
