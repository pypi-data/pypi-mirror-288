# __init__.py
from .image import * 
from .lotto import *
from .names import *

# __all__ = [
#     "show_image",
#     "get_one_number",
# ]

__all__ = image.__all__ + lotto.__all__ + names.__all__

__version__ = '0.0.6'