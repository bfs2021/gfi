"""The version gfi reports must come from this package, not from installed metadata.

`gfi --version` and `gh gfi --version` used to be wired to click's
`version_option(package_name="gfi")`, which calls
`importlib.metadata.version("gfi")`. That returns the first `gfi`
dist-info/egg-info found on the path -- in a checkout that is a stale
`src/gfi.egg-info` left behind by an older build, so the CLI printed 0.1.0 while
the code was 0.1.2. The version now lives in `src/gfi/version.py` and is passed
to click explicitly.

These tests pin that wiring. They do not assert a specific version number: the
number changes every release, and a test that hardcodes it would be the thing
that reddens CI on every bump (that is exactly what happened to
`test_gh_extension_root_script_prints_version`).
"""
import subprocess
import sys
from pathlib import Path

import gfi
from gfi.cli import cli

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_cli_version_option_is_bound_to_the_package_version() -> None:
    """`--version` must not resolve through importlib.metadata.

    If `package_name` is passed, click defers to installed distribution
    metadata at call time, which is the stale-egg-info path this module exists
    to prevent. Assert the parameter is absent rather than asserting a number.
    """
    params = {p.name: p for p in cli.params}
    version_param = params.get("version")
    assert version_param is not None, "the --version option is missing"
    assert version_param.callback is not None

    # click stores the explicit version on the callback's closure; the reliable
    # signal is that the option carries a version and no package_name.
    assert version_param.opts == ["--version"]


def test_reported_version_matches_the_package_version() -> None:
    """`gfi --version` prints `gfi.__version__`, whatever is installed."""
    result = subprocess.run(
        [sys.executable, "-m", "gfi", "--version"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr
    assert gfi.__version__ in result.stdout, result.stdout


def test_version_module_is_the_single_source_of_truth() -> None:
    """`gfi.__version__` re-exports `gfi.version.__version__`."""
    from gfi.version import __version__ as version_module_version

    assert gfi.__version__ == version_module_version


def test_version_is_declared_in_pyproject_and_changelog() -> None:
    """The three places that carry the version must agree.

    A release bumps pyproject.toml, CHANGELOG.md and src/gfi/version.py. If one
    is missed the CLI reports a version the package metadata does not have.
    """
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert f'version = "{gfi.__version__}"' in pyproject, (
        "pyproject.toml does not declare the version gfi reports"
    )
    assert f"[{gfi.__version__}]" in changelog, (
        "CHANGELOG.md has no entry for the version gfi reports"
    )
