import logging
import re
from typing import List, Literal


from optimodel_guard.Guards.GuardBaseClass import GuardBaseClass
from optimodel_server_types import (
    LytixRegexConfig,
    ModelMessage,
)


logger = logging.getLogger(__name__)


class LytixRegexGuard(GuardBaseClass):
    def handlePreQuery(
        self, messages: List[ModelMessage], config: LytixRegexConfig
    ) -> bool:
        logger.info(f"LYTIX_REGEX is checking pre-query....")
        return self._evaluateRegexMessage(messages, config, "user")

    def handlePostQuery(
        self, messages: List[ModelMessage], config: LytixRegexConfig
    ) -> bool:
        logger.info(f"LYTIX_REGEX is checking post-query....")
        return self._evaluateRegexMessage(messages, config, "assistant")

    def _evaluateRegexMessage(
        self,
        messages: List[ModelMessage],
        config: LytixRegexConfig,
        role: Literal["user", "assistant"],
    ) -> bool:
        """
        Extract any instructions from the query that the user has given.
        """
        messages = ",".join(
            [message.content for message in messages if message.role == role]
        )

        try:
            pattern = re.compile(config.regex_pattern)
            match = pattern.search(messages)
        except re.error as e:
            logger.error(f"Error compiling regex pattern: {e}")
            return False

        if match:
            logger.info(f"Regex pattern matched: {match.group()}")
            return True
        else:
            logger.info("No match found for the regex pattern.")

        return False
