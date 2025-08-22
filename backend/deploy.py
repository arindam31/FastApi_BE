import typer
import subprocess
import getpass
from pathlib import Path
from config_loader import ConfigLoader

app = typer.Typer()

USERS = {
    "Arindam": {"password": "arc123", "roles": ["developer"], "allowed_envs": ["dev", "demo"]},
    "Alicia": {"password": "alicia123", "roles": ["ops"], "allowed_envs": ["staging", "prod"]},
    "Martha": {"password": "martha123", "roles": ["admin"], "allowed_envs": ["dev", "demo", "staging", "prod"]},
}


@app.command()
def deploy(env: str):
    """Deploy backend to specified environment"""
    allowed_envs = ["dev", "staging", "prod"]

    # Check user credentials
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = USERS.get(username)
    if not user or user["password"] != password:
        typer.echo("Invalid username or password")
        raise typer.Exit()

    if env not in allowed_envs:
        typer.echo(f"Invalid environment: {env}")
        raise typer.Exit()
    
    # ABAC check
    if env not in user["allowed_envs"]:
        typer.echo(f"Permission denied: {username} cannot deploy to {env}")
        raise typer.Exit()

    if env == "prod":
        confirm = typer.confirm("Are you sure you want to deploy to production?")
        if not confirm:
            raise typer.Exit()
        
    typer.echo(f"User {username} authorized to deploy to {env}")

    # Load config from Mongo
    config = ConfigLoader.load(env=env)
    typer.echo(f"Deploying to {env} at {config.server_ip}...")

    # Map environment to Docker Compose override
    # TODO When you add files inside backend.
    # override_file = Path(f"docker-compose.override.{env}.yml")
    # subprocess.run(
    #     ["docker-compose", "-f", "docker-compose.yml", "-f", str(override_file), "up", "-d", "--build"]
    # )
    # typer.echo(f"Deployment to {env} started successfully!")

if __name__ == "__main__":
    app()
