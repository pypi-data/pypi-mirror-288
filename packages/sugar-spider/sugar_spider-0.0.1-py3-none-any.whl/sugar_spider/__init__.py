from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sugar_spider")
except PackageNotFoundError:
    # package is not installed
    pass
