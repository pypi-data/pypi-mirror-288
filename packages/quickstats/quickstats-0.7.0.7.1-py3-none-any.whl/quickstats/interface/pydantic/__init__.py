import quickstats
quickstats.core.methods._require_module_version('python', (3, 8, 0))
quickstats.core.methods._require_module_version('pydantic', (2, 0, 0))

from .default_model import DefaultModel