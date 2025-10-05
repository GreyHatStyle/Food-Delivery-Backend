from pathlib import Path


class LogSetup:
    def __init__(self, apps_to_log: list[str]) -> None:
        self.PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

        self.LOGS_DIR = self.PROJECT_ROOT / "logs"
        self.LOGS_DIR.mkdir(exist_ok=True)

        self.APPS_TO_LOG = apps_to_log

    def create_file_app_handlers(self, app_name: str):
        """
        ## For Dev Logs
        Creates logging handlers for given app name. (like account, core, products etc..)

        Args:
            app_name (str): App name (created using django-admin startapp)
        """
        app_logs_dir = self.LOGS_DIR / app_name
        app_logs_dir.mkdir(exist_ok=True)

        return {
            f"{app_name}_normal": {
                "class": "logging.FileHandler",
                "filename": str(app_logs_dir / "normal_logs.log"),
                "level": "DEBUG",
                "formatter": "verbose",
                "filters": ["normal_level_filter"],
            },
            f"{app_name}_critical": {
                "class": "logging.FileHandler",
                "filename": str(app_logs_dir / "critical_logs.log"),
                "level": "ERROR",
                "formatter": "verbose",
            },
        }

    def create_logtail_app_handlers(self, app_name: str, source_token: str, host: str):
        """
        ## For Production Logs
        Creates logging handlers for given app name. (like account, core, products etc..)

        Args:
            app_name (str): App name (created using django-admin startapp)
            source_token (str): The source token provided by better stack in logtail.
            host (str): The host address, provided by better stack
        """

        return {
            f"{app_name}_normal": {
                "class": "logtail.LogtailHandler",
                "source_token": source_token,
                "host": host,
                "level": "DEBUG",
                "formatter": "verbose",
                "filters": ["normal_level_filter"],
            },
            f"{app_name}_critical": {
                "class": "logtail.LogtailHandler",
                "source_token": source_token,
                "host": host,
                "level": "ERROR",
                "formatter": "verbose",
            },
        }

    def create_app_logger(self, app_name: str):
        """
        Creates logger configurations for the app name

        """
        return {
            app_name: {
                "level": "INFO",
                "handlers": [f"{app_name}_normal", f"{app_name}_critical"],
                "propagate": False,
            }
        }
