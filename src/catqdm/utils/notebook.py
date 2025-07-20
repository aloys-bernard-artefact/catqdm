from IPython import get_ipython

def _in_notebook() -> bool:
    """Rudimentary notebook detection (IPython kernel / Jupyter / Colab)."""
    try:
        ip = get_ipython()
        if ip is None:
            return False
        cls = ip.__class__.__name__
        if cls.startswith("ZMQ"):
            return True
        if "IPKernelApp" in getattr(ip, "config", {}):
            return True
        return False
    except Exception:
        return False
