"""Domain errors raised by Negrita Brain."""


class BrainError(RuntimeError):
    """Base error for configuration or runtime contract failures."""


class ConfigurationError(BrainError):
    """Raised when a project cannot resolve its canonical configuration."""


class ProfileResolutionError(ConfigurationError):
    """Raised when skill profile inheritance is invalid."""


class SessionError(BrainError):
    """Raised when a runtime session cannot be found or changed."""


class DecisionError(BrainError):
    """Raised when an append-only decision transition is invalid."""
