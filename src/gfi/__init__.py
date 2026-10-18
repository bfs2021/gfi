"""gfi — Good First Issue finder for GitHub contributors."""
from gfi.gh_extension import main as gh_extension_main
from gfi.search import GitHubSearcher, HotTopics, Issue
from gfi.version import __version__

__all__ = ["GitHubSearcher", "Issue", "HotTopics", "gh_extension_main", "__version__"]
