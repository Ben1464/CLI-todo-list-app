import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task
from base import Base

# Set up the database engine and session
engine = create_engine('sqlite:///todo_list.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """CLI for managing tasks."""
    pass

@cli.command()
@click.argument('title')
@click.option('--description', default='', help='Description of the task')
def add_task(title, description):
    """Add a new task."""
    task = Task(title=title, description=description)
    session.add(task)
    session.commit()
    click.echo(f'Task "{title}" added.')

@cli.command()
def list_tasks():
    """List all tasks."""
    tasks = session.query(Task).all()
    for task in tasks:
        click.echo(f'{task.id}: {task.title} - {task.status}')

@cli.command()
@click.argument('task_id', type=int)
@click.argument('status')
def update_task(task_id, status):
    """Update the status of a task."""
    task = session.query(Task).get(task_id)
    if task:
        task.status = status
        session.commit()
        click.echo(f'Task {task_id} status updated to "{status}".')
    else:
        click.echo(f'Task {task_id} not found.')

@cli.command()
@click.argument('task_id', type=int)
def delete_task(task_id):
    """Delete a task."""
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
        click.echo(f'Task {task_id} deleted.')
    else:
        click.echo(f'Task {task_id} not found.')

if __name__ == '__main__':
    cli()
