import typer

from ado_clients.board_client import BoardClient


app = typer.Typer()

# Initialize the BoardClient for the organization "microsoft" and project "OS"
organization = "microsoft"
project = "OS"

client = BoardClient(organization, project)


@app.command()
def list_tasks():
    tasks = client.list_tasks()
    for task in tasks:
        typer.echo(f"ID: {task.id}, Title: {task.fields['System.Title']}, State: {task.fields['System.State']}")


@app.command()
def create_task(title: str, description: str):
    task = client.create_task(title, description)
    typer.echo(f"Created task ID: {task.id}, Title: {task.fields['System.Title']}")


@app.command()
def update_task(task_id: int, title: str = None, description: str = None):
    task = client.update_task(task_id, title, description)
    typer.echo(f"Updated task ID: {task.id}, Title: {task.fields['System.Title']}")


@app.command()
def delete_task(task_id: int):
    message = client.delete_task(task_id)
    typer.echo(message)


if __name__ == "__main__":
    app()
