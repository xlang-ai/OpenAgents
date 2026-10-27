"""Operator-controlled policy for model-generated Python, not a sandbox."""

import os


DEFAULT_CODE_EXECUTION_MODE = "disabled"
LOCAL_EXECUTION_WARNING = (
    "UNSAFE local Python execution is enabled: generated code runs inside the "
    "backend process with access to its credentials, files and network. "
    "Use only for trusted, single-user development, including trusted input data. "
    "See backend/README.md#python-execution-trust-boundary."
)
DISABLED_EXECUTION_MESSAGE = (
    "Python execution is disabled by the server operator. Python analysis and "
    "Python-generated charts require an explicitly configured execution mode. "
    "See backend/README.md#python-execution-trust-boundary."
)


def validate_code_execution_mode(mode: str) -> str:
    """Reject unknown modes and require a separate acknowledgement for local use."""
    if mode not in {"disabled", "local", "docker"}:
        raise ValueError("CODE_EXECUTION_MODE must be disabled, local, or docker")
    if mode == "local" and os.getenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION") != "true":
        raise ValueError(
            "CODE_EXECUTION_MODE=local requires ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=true. "
            + LOCAL_EXECUTION_WARNING
        )
    return mode


def configured_code_execution_mode() -> str:
    """Read server environment only; request data must not select this policy."""
    return validate_code_execution_mode(os.getenv("CODE_EXECUTION_MODE", DEFAULT_CODE_EXECUTION_MODE))
