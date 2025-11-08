"""Init command for setting up new projects."""

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()

init_app = typer.Typer(help="Initialize new project")


@init_app.command()
def project(
    name: str = typer.Option(None, "--name", "-n", help="Project name"),
    template: str = typer.Option("basic", "--template", "-t", help="Project template"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force overwrite existing files"
    ),
) -> None:
    """Initialize a new project."""
    if not name:
        name = Prompt.ask("Enter project name")

    project_path = Path.cwd() / name

    if project_path.exists() and not force:
        if not Confirm.ask(f"Directory '{name}' already exists. Continue?"):
            console.print("❌ Project initialization cancelled", style="red")
            raise typer.Exit(1)

    # Create project structure
    project_path.mkdir(exist_ok=True)

    # Create basic files
    readme_content = f"# {name}\n\nYour new project description here.\n"
    (project_path / "README.md").write_text(readme_content)
    (project_path / ".gitignore").write_text(_get_gitignore_content())

    if template == "python":
        _create_python_project(project_path, name)
    elif template == "web":
        _create_web_project(project_path, name)
    else:
        _create_basic_project(project_path, name)

    console.print(f"✅ Project '{name}' initialized successfully!", style="green")
    console.print(f"📁 Project created at: {project_path.absolute()}", style="cyan")


def _get_gitignore_content() -> str:
    """Get common .gitignore content."""
    return """# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Node modules
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""


def _create_basic_project(project_path: Path, name: str) -> None:
    """Create a basic project structure."""
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "docs").mkdir(exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)

    main_py_content = (
        f'"""Main module for {name}."""\n\n'
        "def main():\n"
        f'    print("Hello from {name}!")\n\n'
        'if __name__ == "__main__":\n'
        "    main()\n"
    )
    (project_path / "src" / "main.py").write_text(main_py_content)


def _create_python_project(project_path: Path, name: str) -> None:
    """Create a Python project structure."""
    _create_basic_project(project_path, name)

    # Create pyproject.toml
    pyproject_content = f"""[project]
name = "{name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
target-version = "py311"
"""
    (project_path / "pyproject.toml").write_text(pyproject_content)


def _create_web_project(project_path: Path, name: str) -> None:
    """Create a web project structure."""
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "public").mkdir(exist_ok=True)
    (project_path / "assets").mkdir(exist_ok=True)

    # Create basic HTML file
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>Welcome to {name}</h1>
    <p>Your web project is ready!</p>
</body>
</html>
"""
    (project_path / "public" / "index.html").write_text(html_content)


@init_app.command()
def docker(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force pull image even if exists"
    ),
    config_path: str = typer.Option(
        "./config.yaml", "--config", "-c", help="Config file path"
    ),
) -> None:
    """Initialize Docker environment with T3 Edge Video."""
    import subprocess

    import yaml

    console.print("🐳 Initializing Docker environment...", style="bold blue")

    # Pull Docker image
    try:
        console.print("📥 Pulling Docker image ghcr.io/t3-labs/edge-video:latest...")
        result = subprocess.run(
            ["docker", "pull", "ghcr.io/t3-labs/edge-video:latest"],
            capture_output=True,
            text=True,
            check=True,
        )
        console.print("✅ Docker image pulled successfully!", style="green")

        # Show image info
        if result.stdout:
            console.print(result.stdout)

    except subprocess.CalledProcessError as e:
        console.print(
            f"⚠️ Warning: Failed to pull Docker image: {e.stderr}", style="yellow"
        )
        console.print("💡 Continuing with configuration setup...", style="blue")
    except FileNotFoundError:
        console.print(
            "⚠️ Warning: Docker not found. Continuing with configuration setup...",
            style="yellow",
        )

    # Create config.yaml
    config_file_path = Path(config_path)

    if config_file_path.exists() and not force:
        if not Confirm.ask(f"Config file '{config_path}' already exists. Overwrite?"):
            console.print("❌ Config creation cancelled", style="yellow")
            return

    # Default configuration
    config_data = {
        "docker": {
            "image": "ghcr.io/t3-labs/edge-video:latest",
            "container_name": "t3-edge-video",
            "ports": {"web": 8080, "api": 3000, "rtmp": 1935},
            "volumes": ["./data:/app/data", "./config:/app/config", "./logs:/app/logs"],
            "environment": {
                "T3_ENV": "production",
                "T3_LOG_LEVEL": "INFO",
                "T3_ENABLE_API": "true",
                "T3_ENABLE_WEB": "true",
            },
        },
        "video": {
            "input": {
                "source": "camera",
                "resolution": "1920x1080",
                "fps": 30,
                "format": "h264",
            },
            "processing": {
                "enable_ai": True,
                "model": "yolo-v8",
                "confidence_threshold": 0.5,
                "batch_size": 4,
            },
            "output": {
                "enable_streaming": True,
                "enable_recording": False,
                "output_path": "./recordings",
                "stream_quality": "high",
            },
        },
        "network": {
            "api_host": "0.0.0.0",
            "api_port": 3000,
            "web_port": 8080,
            "rtmp_port": 1935,
            "enable_cors": True,
        },
        "storage": {
            "data_path": "./data",
            "max_storage_gb": 100,
            "cleanup_older_than_days": 7,
        },
    }

    try:
        with config_file_path.open("w") as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)

        console.print(
            f"✅ Configuration file created: {config_file_path.absolute()}",
            style="green",
        )

        # Create necessary directories
        directories = ["data", "config", "logs", "recordings"]
        for directory in directories:
            dir_path = Path(directory)
            dir_path.mkdir(exist_ok=True)
            console.print(f"📁 Created directory: {dir_path}", style="cyan")

        # Show usage instructions
        console.print(
            "\n🚀 Docker environment initialized successfully!", style="bold green"
        )
        console.print("\nNext steps:", style="bold")
        console.print("1. Review and edit the config.yaml file as needed")
        console.print("2. Run the container:")
        console.print("   docker run -d --name t3-edge-video \\")
        console.print("     -p 8080:8080 -p 3000:3000 -p 1935:1935 \\")
        console.print("     -v $(pwd)/data:/app/data \\")
        console.print("     -v $(pwd)/config:/app/config \\")
        console.print("     -v $(pwd)/logs:/app/logs \\")
        console.print(
            "     --env-file <(grep -v '^#' config.yaml | grep '=' || true) \\"
        )
        console.print("     ghcr.io/t3-labs/edge-video:latest")
        console.print("3. Access the web interface at http://localhost:8080")
        console.print("4. Use API endpoints at http://localhost:3000")

    except ImportError:
        console.print("❌ PyYAML not found. Installing PyYAML...", style="yellow")
        try:
            subprocess.run(["pip", "install", "pyyaml"], check=True)
            console.print("✅ PyYAML installed successfully!", style="green")
            # Retry creating config file
            docker(force, config_path)
        except subprocess.CalledProcessError:
            console.print(
                "❌ Failed to install PyYAML. "
                "Please install manually: pip install pyyaml",
                style="red",
            )
            raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"❌ Failed to create config file: {e}", style="red")
        raise typer.Exit(1) from e
