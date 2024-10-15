from dynaconf import Dynaconf

# Initialize Dynaconf with your configuration
settings = Dynaconf(
    settings_files=[
        "configs/settings.yaml",  # Default settings
        "configs/dev.yaml",       # Development-specific settings
        "configs/prod.yaml",      # Production-specific settings
        "configs/.secrets.yaml",  # Sensitive data
    ],
    environments=True,
    load_dotenv=True,
    envvar_prefix="PW",
    env_switcher="ENV_FOR_PW",
    dotenv_path="configs/.env",
)

