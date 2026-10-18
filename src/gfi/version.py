"""Single source of truth for gfi's version.

`gfi --version` and `gh gfi --version` must report the version of the code
being run, not whatever distribution metadata happens to be on the path. Click's
`version_option(package_name=...)` calls `importlib.metadata.version()`, which
reads the first `gfi` dist-info/egg-info it finds -- in a checkout that is a
stale `src/gfi.egg-info` left by an older build, so the CLI printed 0.1.0 while
the code was 0.1.2.

This module is imported by `gfi.cli` and by `gfi/__init__.py`, so the version
lives in exactly one place. `gfi/__init__.py` re-exports it rather than defining
it, which keeps the import acyclic: `__init__` imports `gfi.gh_extension`, which
imports `gfi.cli`, which imports this module.
"""

__version__ = "0.1.2"
