import os
import unittest
from unittest import mock

from feature_launchpad import env


class RequireTests(unittest.TestCase):
    def test_passes_when_all_vars_present(self):
        with mock.patch.dict(os.environ, {"FOO": "x", "BAR": "y"}, clear=False):
            env.require(("FOO", "BAR"))  # should not raise

    def test_raises_with_missing_var_names(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(env.MissingEnvVarError) as ctx:
                env.require(("FOO", "BAR"))
        self.assertIn("FOO", str(ctx.exception))
        self.assertIn("BAR", str(ctx.exception))

    def test_blank_value_counts_as_missing(self):
        with mock.patch.dict(os.environ, {"FOO": ""}, clear=True):
            with self.assertRaises(env.MissingEnvVarError):
                env.require(("FOO",))


if __name__ == "__main__":
    unittest.main()
