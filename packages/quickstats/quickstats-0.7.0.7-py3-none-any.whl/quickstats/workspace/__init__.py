from quickstats.core.methods import _require_module_version
_require_module_version('python', (3, 8, 0))
_require_module_version('pydantic', (2, 0, 0))

from .argument_sets import SystArgSets, CoreArgSets
from .xml_ws_reader import XMLWSReader
from .ws_builder import WSBuilder