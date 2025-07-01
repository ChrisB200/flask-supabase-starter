import logging.config

dev = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%d-%m-%Y %H:%M"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG"
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG"
    }
}

prod = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%d-%m-%Y %H:%M"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": "app.log",
            "level": "INFO"
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO"
    }
}


def switch_logging_config(config_name):
    if config_name == "dev":
        logging.config.dictConfig(dev)
    elif config_name == "prod" or config_name == "production":
        logging.config.dictConfig(prod)
    else:
        raise ValueError(f"Unknown config: {config_name}")
