"""
MinIO Migration Management System

This script provides a migration management system for MinIO, enabling:
- Creation of new migrations through an interactive interface
- Application of migrations to MinIO server
- Management of buckets, users, and access policies
- Easy extensibility through custom handlers

1. Requirements
---------------
- Python 3.8+
- Installed MinIO Client (mc)
- Access to MinIO server
- Environment variables for authentication

2. Installation
---------------
2.1 Configure environment variables:
    Create .env file in project root:
    ```ini
    MINIO_HOST=http://localhost:9000
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin
    MINIO_MIGRATION_DIR=migrations_minio
    ```

3. Usage
--------
3.1 Basic commands:
    # Create new migration
    python migrations.py new --name create-user --type create_user

    # Apply all migrations
    python migrations.py apply

3.2 Available actions:
    • create_bucket - Create bucket
    • create_user - Create user with policy

4. Architecture
---------------
4.1 Core components:
    • MigrationManager - Core migration management system
    • CLI - Command line handler
    • Action Handlers - Specific operation handlers

4.2 File structure:
    migrations_minio/      # Migrations directory
    ├── <migration_id>.json  # Migration files
    migrations.py         # Main script

5. Implementation Details
-------------------------
5.1 MigrationManager:
    • Registers and executes actions
    • Handles mc commands
    • Manages migration templates

5.2 Action Handlers:
    • Bucket creation (handle_create_bucket)
    • User creation (handle_create_user)

6. Extending Functionality
--------------------------
6.1 Adding new action:
    @MigrationManager.register_action(
        name="custom_action",
        template={
            "description": "Custom action",
            "fields": [
                {"name": "param1", "type": "str", "prompt": "Parameter 1"}
            ]
        }
    )
    def handle_custom_action(action: Dict[str, Any]):
        # Action implementation

6.2 Template customization:
    • Add new fields to "fields" section
    • Implement custom validation logic

7. Migration Examples
---------------------
7.1 Sample migration file:
    {
        "id": "create-user-1a2b3c4d",
        "created": "2024-03-20T12:34:56.789",
        "actions": [
            {
                "type": "create_user",
                "username": "ml-service",
                "password": "SecurePass123!",
                "policy": "readonly"
            }
        ]
    }

8. Error Handling
-----------------
8.1 Common errors:
    • Missing environment variables
    • Unknown action type
    • Migration command failed

8.2 Diagnostics:
    • Check execution logs
    • Verify MinIO server availability
    • Check access permissions

9. Best Practices
-----------------
9.1 Security:
    • Never store secrets in code
    • Use separate access policies
    • Regularly rotate passwords

9.2 Migration management:
    • Version control migration files
    • Use descriptive names
    • Test migrations before applying
"""

import json
import os
import uuid
import argparse
from datetime import datetime
import subprocess
from typing import Dict, Callable, Any, List

MC_ALIAS = "local"
MIGRATION_DIR = os.getenv("MINIO_MIGRATION_DIR")

if not MIGRATION_DIR:
    raise EnvironmentError(
        f"You need to provide directory '{MIGRATION_DIR}' with migrations.\n"
        "Ensure you created it manually and check MINIO_MIGRATION_DIR environment variable."
    )

# Директория для хранения файлов конфигураций политик
POLICY_CONFIG_DIR = os.path.join(MIGRATION_DIR, "policy_configs")


class MigrationManager:
    """Core migration management system"""
    _actions: Dict[str, Dict[str, Any]] = {}
    _handlers: Dict[str, Callable[[Dict], None]] = {}

    @classmethod
    def get_available_actions(cls) -> List[str]:
        """Get list of registered action names"""
        return list(cls._actions.keys())

    @classmethod
    def get_action_template(cls, name: str) -> Dict[str, Any]:
        """Get action template by action name"""
        template = cls._actions.get(name)
        if template is None:
            raise Exception(f"Action {name} not found")
        return template

    @classmethod
    def register_action(cls, name: str, template: Dict[str, Any]):
        """Decorator to register new migration actions"""
        def decorator(func: Callable[[Dict], None]):
            cls._actions[name] = template
            cls._handlers[name] = func
            return func
        return decorator

    @classmethod
    def execute(cls, action: Dict[str, Any]):
        """Execute registered action"""
        action_type = action["type"]
        if action_type not in cls._handlers:
            raise ValueError(f"Unknown action type: {action_type}")
        cls._handlers[action_type](action)

    @classmethod
    def run_command(cls, command: str):
        """Execute mc command with error handling"""
        full_cmd = f"mc {command}"
        print(f"Executing: {full_cmd}")
        full_cmd = os.path.expandvars(full_cmd)
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(f"Error: {e.stderr}")
            raise RuntimeError("Migration command failed") from e


@MigrationManager.register_action(
    name="create_bucket",
    template={
        "description": "Create new bucket",
        "fields": [
            {"name": "bucket", "type": "str", "prompt": "Bucket name"},
            {"name": "private", "type": "bool", "prompt": "Private (true/false)"}
        ]
    }
)
def handle_create_bucket(action: Dict[str, Any]):
    MigrationManager.run_command(f"mb --ignore-existing {MC_ALIAS}/{action['bucket']}")
    if action.get("private") in [True, "true", "True"]:
        MigrationManager.run_command(f"anonymous set private {MC_ALIAS}/{action['bucket']}")


@MigrationManager.register_action(
    name="create_user",
    template={
        "description": "Create new user and attach policy",
        "fields": [
            {"name": "username", "type": "str", "prompt": "Username"},
            {"name": "password", "type": "str", "prompt": "Password"},
            {"name": "policy", "type": "str", "prompt": "Policy name"}
        ]
    }
)
def handle_create_user(action: Dict[str, Any]):
    # Создаем пользователя
    MigrationManager.run_command(
        f"admin user add {MC_ALIAS} {action['username']} {action['password']}"
    )
    # Прикрепляем политику
    # Ожидается, что политика дефолтная или уже добавлена на сервер через apply_policy_config
    MigrationManager.run_command(
        f"admin policy attach {MC_ALIAS} {action['policy']} --user={action['username']}"
    )


@MigrationManager.register_action(
    name="generate_policy_config",
    template={
        "description": "Generate a new policy configuration template with the policy content",
        "fields": [
            {"name": "config_name", "type": "str", "prompt": "Policy config name"},
            {"name": "policy", "type": "str", "prompt": "Policy JSON/str configuration"}
        ]
    }
)
def handle_generate_policy_config(action: Dict[str, Any]):
    config_name = action["config_name"]
    policy_content = action["policy"]
    # Если policy задан как строка, пытаемся парсить как JSON
    if isinstance(policy_content, str):
        try:
            policy_data = json.loads(policy_content)
        except Exception as e:
            print(f"Warning: Provided policy is not valid JSON. Saving as raw string. Error: {e}")
            policy_data = policy_content
    else:
        policy_data = policy_content

    os.makedirs(POLICY_CONFIG_DIR, exist_ok=True)
    filename = os.path.join(POLICY_CONFIG_DIR, f"{config_name}.json")
    with open(filename, "w") as f:
        json.dump(policy_data, f, indent=2)
    print(f"Policy config template generated: {filename}")
    print("Please review and edit the file if necessary before action {apply_policy_config}.")


@MigrationManager.register_action(
    name="apply_policy_config",
    template={
        "description": "Apply a policy configuration on the server",
        "fields": [
            {"name": "config_name", "type": "str", "prompt": "Policy config name"}
        ]
    }
)
def handle_apply_policy_config(action: Dict[str, Any]):
    config_name = action["config_name"]
    filename = os.path.join(POLICY_CONFIG_DIR, f"{config_name}.json")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Policy config file not found: {filename}")
    MigrationManager.run_command(
        f"admin policy create {MC_ALIAS} {config_name} {filename}"
    )
    print(f"Policy config '{config_name}' applied on the server.")


class CLI:
    """Command Line Interface handler"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="MinIO Migration Management System",
            formatter_class=argparse.RawTextHelpFormatter
        )
        self.subparsers = self.parser.add_subparsers(
            title="commands",
            dest="command",
            required=True
        )
        self._setup_new_parser()
        self._setup_apply_parser()

    def _setup_new_parser(self):
        """Configure new migration command parser (non-interactive generation)"""
        parser = self.subparsers.add_parser(
            "new",
            help="Generate new migration file with a JSON template to be filled manually"
        )
        parser.add_argument(
            "-n", "--name",
            required=True,
            help="Unique migration name (will be part of the file name)"
        )
        parser.add_argument(
            "-t", "--type",
            required=True,
            choices=MigrationManager.get_available_actions(),
            help=f"Migration type\nAvailable types: {', '.join(MigrationManager.get_available_actions())}"
        )
        parser.add_argument(
            "-o", "--order",
            type=int,
            default=0,
            help="Execution order number for this migration (lower numbers execute first)"
        )
        parser.set_defaults(func=self.handle_new)

    def _setup_apply_parser(self):
        """Configure apply migrations command parser"""
        parser = self.subparsers.add_parser(
            "apply",
            help="Apply all pending migrations"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force apply all migrations"
        )
        parser.set_defaults(func=self.handle_apply)

    @staticmethod
    def handle_new(args: argparse.Namespace):
        """Handle new migration creation by generating a JSON template file"""
        generate_migration(args.name, args.type, args.order)

    @staticmethod
    def handle_apply(args: argparse.Namespace):
        """Handle migrations applying"""
        apply_migrations(args.force)

    def run(self):
        """Execute CLI command"""
        args = self.parser.parse_args()
        args.func(args)


def generate_migration(name: str, migration_type: str, order: int):
    """Generate new migration file with a JSON template to be filled by the user"""
    template = MigrationManager.get_action_template(migration_type)
    migration_id = f"{name}-{uuid.uuid4().hex[:8]}"
    filename = os.path.join(MIGRATION_DIR, f"{migration_id}.json")
    os.makedirs(MIGRATION_DIR, exist_ok=True)

    action = {"type": migration_type}
    for field in template["fields"]:
        # В качестве значения по умолчанию выводим подсказку
        action[field["name"]] = field["prompt"]

    migration = {
        "id": migration_id,
        "created": datetime.now().isoformat(),
        "order": order,
        "actions": [action]
    }

    with open(filename, "w") as f:
        json.dump(migration, f, indent=2)

    print(f"\nMigration template generated: {filename}")
    print("Please fill in the required fields in the generated file before applying migrations.")


def apply_migrations(force: bool = False):
    """Apply all pending migrations sorted by 'order' and then creation time"""
    required_vars = (
        ("MINIO_HOST", os.getenv("MINIO_HOST")),
        ("MINIO_ROOT_USER", os.getenv("MINIO_ROOT_USER")),
        ("MINIO_ROOT_PASSWORD", os.getenv("MINIO_ROOT_PASSWORD")),
    )
    missing = [name for name, value in required_vars if not value]
    if missing:
        raise EnvironmentError(
            "Missing required environment variables:\n" +
            "\n".join(f"• {var}" for var in missing) +
            "\n\nPlease configure your MinIO credentials first."
        )
    try:
        # Configure MinIO alias
        MigrationManager.run_command(
            f"alias set {MC_ALIAS} "
            f"{os.getenv('MINIO_HOST')} "
            f"{os.getenv('MINIO_ROOT_USER')} "
            f"{os.getenv('MINIO_ROOT_PASSWORD')}"
        )
        migrations = []
        for filename in sorted(os.listdir(MIGRATION_DIR)):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(MIGRATION_DIR, filename)
            with open(filepath) as f:
                migration = json.load(f)
                migrations.append(migration)
        migrations.sort(key=lambda m: (m.get("order", 0), m.get("created", "")))
        for migration in migrations:
            print(f"\nApplying migration: {migration['id']}")
            for action in migration["actions"]:
                MigrationManager.execute(action)
    except Exception as e:
        print(f"\nMigration failed: {str(e)}")
        raise


def main():
    """Entry point"""
    try:
        cli = CLI()
        cli.run()
    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)
    print("\nOperation completed successfully")


if __name__ == "__main__":
    main()
