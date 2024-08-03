import os
from typing import Optional
from ally_ai_core import Settings
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

class Langsmith():
    """
    New Instance activates langsmith if the settings are correct
    """
    ally_settings: Settings = None

    def __init__(self, settings: Optional[Settings] = None) -> None:

        if settings is None:
            settings = Settings(section='langsmith')

        self.ally_settings = settings
        
        self.activate()


    def activate(self):
        """
        Put settings into the environment variables
        """
        for key, value in self.ally_settings.items():
            os.environ[key.upper()] = str(value)

        logger.info(
            f"Langsmith keys are set to environment variables: {self.ally_settings.keys()}")
