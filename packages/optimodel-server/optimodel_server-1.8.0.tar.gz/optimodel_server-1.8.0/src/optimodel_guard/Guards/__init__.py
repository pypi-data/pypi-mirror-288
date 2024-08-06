from .LLamaPromptGuard import LLamaPromptGuard
from .RegexGuard import LytixRegexGuard

GuardMapping = {
    "META_LLAMA_PROMPT_GUARD_86M": LLamaPromptGuard(),
    "LYTIX_REGEX_GUARD": LytixRegexGuard(),
}
