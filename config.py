from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        "configs/settings.toml",          # a file for main settings
        "configs/.secrets.toml"           # a file for sensitive data must be (gitignored)
    ],
    environments=True,
    load_dotenv=True,               # Load envvars from a file named `.env`
                                    # TIP: probably you don't want to load dotenv on production environments
                                    #      pass `load_dotenv={"when": {"env": {"is_in": ["development"]}}}
    envvar_prefix="PW",             # variables exported as `PW_FOO=bar` becomes `settings.FOO == "bar"`
    env_switcher="ENV_FOR_PW",      # to switch environments `export ENV_FOR_PW=production`

    dotenv_path="configs/.env"      # custom path for .env file to be loaded
)

