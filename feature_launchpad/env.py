"""Environment-variable validation.

Per intent.md Section 5: if a required variable is missing, the workflow must stop
with a clear message and make no repo modifications.
"""

import os


class MissingEnvVarError(RuntimeError):
    pass


def require(var_names):
    missing = [name for name in var_names if not os.environ.get(name)]
    if missing:
        raise MissingEnvVarError(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". Set them before running the launchpad. No files were written."
        )
