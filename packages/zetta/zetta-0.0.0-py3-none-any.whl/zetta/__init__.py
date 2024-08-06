from zetta_version import __version__

try:
    from . import secret
    from . import job
except ImportError as e:
    print(f"Error importing module: {e}")
except Exception as e:
    print(f"Error: {e}")

__all__ = ["__version__", "secret", "job"]
