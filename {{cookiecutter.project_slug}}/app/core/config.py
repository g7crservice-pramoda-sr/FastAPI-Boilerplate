import json
import sys
from pathlib import Path
from typing import List, Optional, Union

from colorama import Fore, Style, init
from pydantic import field_validator, ValidationError
from pydantic_core import PydanticUndefined
from pydantic_settings import BaseSettings, SettingsConfigDict

init(autoreset=True)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Project Metadata
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server Configuration
    BACKEND_URL: str = "http://localhost:8000"
    
    # CORS Origins - list or comma-separated string
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    ALLOWED_HEADERS: List[str] = ["*"]

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # Security
    # In a real project, this MUST be set in .env
    SECRET_KEY: str = "development-secret-key-change-me-locally"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: Optional[str] = None
    
    # Optional individual components if not using a URL
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[str] = "5432"
    DB_USER: Optional[str] = "postgres"
    DB_PASSWORD: Optional[str] = "postgres"
    DB_NAME: Optional[str] = "app_db"


def load_config() -> Config:
    try:
        return Config()
    except ValidationError as e:
        missing_fields = [
            error["loc"][0] for error in e.errors() if error["type"] == "missing"
        ]

        print(
            f"\n{Fore.RED}{Style.BRIGHT}Environment Configuration Error{Style.RESET_ALL}"
        )

        print(f"{Fore.RED}The following required environment variables are missing:\n")

        for field in missing_fields:
            print(f"  {Fore.YELLOW}- {field}")

        print(f"\n{Fore.CYAN}Please check your .env file or environment settings.")
        print(f"{Fore.RED}Application startup aborted.\n")

        sys.exit(1)


config = load_config()


def generate_env_templates():
    env_lines = []
    azure_env = []  # Keeping this as a generic JSON template export

    for field_name, field in Config.model_fields.items():
        default = field.default

        # Handle required fields (PydanticUndefined)
        if default is PydanticUndefined:
            env_value = ""
        else:
            if isinstance(default, list):
                env_value = ",".join(map(str, default))
            else:
                env_value = str(default) if default is not None else ""

        # .env.example entry
        env_lines.append(f"{field_name}={env_value}")

        # JSON template entry
        azure_env.append(
            {
                "name": field_name,
                "value": env_value,
                "slotSetting": False,
            }
        )

    # Write .env.example
    Path(".env.example").write_text("\n".join(env_lines))

    # Write environment JSON for deployment templates
    Path("env_deploy_template.json").write_text(json.dumps(azure_env, indent=2))

    print("Generated .env.example")
    print("Generated env_deploy_template.json")


if __name__ == "__main__":
    generate_env_templates()
