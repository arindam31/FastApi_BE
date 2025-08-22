import json
import typer

# Local imports
from repository.mongo_repository import MongoRepoClient

app = typer.Typer()


@app.command()
def list_envs(
    db_url: str = "mongodb://localhost:27017",
    env: str = typer.Option(None, help="Filter by environment (e.g., dev, staging, prod)")
):
    """List details of all env configs"""
    repo = MongoRepoClient(db_url)
    db = repo.connect_instance("backend_config")
    collection = "configs"

    if env:
        cfg = repo.get_single_json_document(collection, db, env)
        if cfg:
            cfg.pop("_id", None)
            typer.echo(json.dumps(cfg, indent=2))
        else:
            typer.echo(f"No config found for env={env}")
    else:
        configs = repo.get_all_json_documents(collection, db)
        for cfg in configs:
            cfg.pop("_id", None)
            typer.echo(json.dumps(cfg, indent=2))

@app.command()
def create_env(
    db_url: str = "mongodb://localhost:27017",
    env: str = typer.Option(..., help="Environment name (e.g., dev, staging, prod)"),
    server_ip: str = typer.Option(..., help="Server IP address"),
    users_url: str = typer.Option("http://users:5000", help="Users service URL"),
    orders_url: str = typer.Option("http://orders:5001", help="Orders service URL"),
    logging_level: str = typer.Option("INFO", help="Logging level"),
):
    """Create a new environment config (fails if env exists)."""
    repo = MongoRepoClient(db_url)
    db = repo.connect_instance("backend_config")
    collection = "configs"

    doc = {
        "env": env,
        "server_ip": server_ip,
        "users_url": users_url,
        "orders_url": orders_url,
        "logging_level": logging_level,
        "feature_flags": {"enable_api": True},
    }

    inserted = repo.create_json_document(collection, db, doc)
    if inserted:
        typer.echo(f"Created new config for env={env}")
        doc.pop("_id", None)
        typer.echo(json.dumps(doc, indent=2))
    else:
        typer.echo(f"Config for env={env} already exists")

@app.command()
def edit_env(
    db_url: str = "mongodb://localhost:27017",
    env: str = typer.Option(..., help="Environment to edit"),
    field: str = typer.Option(..., help="Field to update (dot notation allowed)"),
    value: str = typer.Option(..., help="New value"),
):
    """Edit a field in an existing environment config."""
    repo = MongoRepoClient(db_url)
    db = repo.connect_instance("backend_config")
    collection = "configs"

    # build partial update
    updates = {field: value}

    updated_doc = repo.update_json_document(collection, db, env, updates)
    if updated_doc:
        typer.echo(f"Updated env={env}")
        updated_doc.pop("_id", None)
        typer.echo(json.dumps(updated_doc, indent=2, default=str))
    else:
        typer.echo(f"No config found for env={env}")


if __name__ == "__main__":
    app()