from typing import Any, List, Optional, Union

from pydantic import Field, BaseModel, ConfigDict, model_validator

from quickstats import check_type, FlexibleDumper, VerbosePrint
from .alias_generators import to_pascal

__all__ = ['DefaultModel']

_dumper : FlexibleDumper = FlexibleDumper(max_depth=2, max_iteration=3, max_line=100, max_len=100)
_stdout : VerbosePrint = VerbosePrint('INFO')

class DefaultModel(BaseModel):
    """Default configurable class"""

    verbosity : Union[int, str] = Field(default='INFO', description='The verbosity level.')
    
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True,
                              validate_default=True, alias_generator=to_pascal,
                              arbitrary_types_allowed=True)

    _stdout : VerbosePrint = VerbosePrint('INFO')
    _parent : "DefaultModel" = None

    def __repr__(self) -> str:
        return _dumper.dump(self.model_dump())

    def __setattr__(self, name: str, value: Any):
        if hasattr(self, f'_validate_{name}'):
            validator_func = getattr(self, validator_name)
            value = validator_func(value=value)
        super().__setattr__(name, value)

    @property
    def parent(self) -> Optional["DefaultModel"]:
        return self._parent

    @property
    def attached(self) -> bool:
        return self.parent is not None

    @property
    def stdout(self) -> VerbosePrint:
        return self._stdout

    def model_post_init(self, __context: Any) -> None:
        for field_name in self.model_fields:
            validator_name = f'_validate_{field_name}'
            if hasattr(self, validator_name):
                field_value = getattr(self, field_name)
                getattr(self, validator_name)(field_value)

    def _validate_verbosity(self, value: Union[int, str]) -> Union[int, str]:
        self._stdout = VerbosePrint(self.verbosity)
        return value

    def configure_dumper(self, **kwargs) -> None:
        _dumper.configure(**kwargs)