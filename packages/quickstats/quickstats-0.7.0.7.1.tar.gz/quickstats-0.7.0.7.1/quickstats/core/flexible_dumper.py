from typing import Any

class FlexibleDumper:
    """
    A flexible dumper that creates a text representation of a python object.
    """

    @property
    def item_indent(self) -> str:
        return self._item_indent

    @property
    def list_indent(self) -> str:
        return self._list_indent

    @property
    def separator(self) -> str:
        return self._separator

    @property
    def skip_str(self) -> str:
        return self._skip_str

    @property
    def indent_sequence_on_key(self) -> bool:
        return self._indent_sequence_on_key

    @property
    def max_depth(self) -> int:
        return self._max_depth

    @property
    def max_iteration(self) -> int:
        return self._max_iteration

    @property
    def max_item(self) -> int:
        return self._max_item

    @property
    def max_line(self) -> int:
        return self._max_line

    @property
    def max_len(self) -> int:
        return self._max_len
    
    def __init__(self, item_indent: str = '  ', list_indent: str = '- ',
                 separator: str = ': ', skip_str: str = '...',
                 indent_sequence_on_key: bool = True, max_depth: int = -1,
                 max_iteration: int = -1, max_item: int = -1, max_line: int = -1, max_len: int = -1):
        if len(item_indent) != len(list_indent):
            raise ValueError('Length of `item_indent` must equal that of `list_indent`.')
        
        self._item_indent = item_indent
        self._list_indent = list_indent
        self._separator = separator
        self._skip_str = skip_str
        self._indent_sequence_on_key = indent_sequence_on_key
        self._max_depth = max_depth
        self._max_iteration = max_iteration
        self._max_item = max_item
        self._max_line = max_line
        self._max_len = max_len
        self.reset()

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, f'_{key}'):
                raise KeyError(f'Invalid property: {key}')
            setattr(self, f'_{key}', value)        
        
    def reset(self):
        """Reset the state of the dumper."""
        self.terminate = False
        self.terminate_depth = False
        self.lines = []

    def get_indent_str(self, depth: int, iteration: int = 0, list_degree: int = 0) -> str:
        """Get the indentation string for the current depth and iteration."""
        if list_degree > 0:
            if iteration == 0:
                return (depth - list_degree) * self.item_indent + list_degree * self.list_indent
            return (depth - 1) * self.item_indent + self.list_indent
        return depth * self.item_indent

    def add_line(self, text:str, depth: int, iteration: int = 0, item: int = 0, list_degree: int = 0):
        """Add a line to the output with proper indentation and length checks."""
        if self.terminate:
            return
        if self.max_line > 0 and len(self.lines) >= self.max_line:
            self.lines.append(self.skip_str)
            self.terminate = True
            return
        if self.terminate_depth and (depth <= self.max_depth):
            self.terminate_depth = False

        if '\n' in text:
            subtexts = text.split('\n')
            # only need to keep the list indicator for the first line
            self.add_line(subtexts[0], depth, iteration=iteration, item=item, list_degree=list_degree)
            for subtext in subtexts[1:]:
                self.add_line(subtext, depth, iteration=iteration, item=item, list_degree=0)
            return
        
        indent = self.get_indent_str(depth, iteration, list_degree)
        line = indent + text
        
        if self.max_len > 0 and len(line) > self.max_len:
            line = line[:max(len(indent), self.max_len)] + self.skip_str
        
        if self.max_depth > 0 and depth > self.max_depth:
            if not self.terminate_depth:
                line = indent + self.skip_str
                self.terminate_depth = True
            else:
                return
        
        if self.max_iteration > 0:
            if iteration == self.max_iteration:
                if list_degree > 0:
                    line = self.get_indent_str(depth, iteration, 0) + self.skip_str
                else:
                    line = indent + self.skip_str
            elif iteration > self.max_iteration:
                return

        if self.max_item > 0:
            if item == self.max_item:
                line = indent + self.skip_str
            elif item > self.max_item:
                return
        
        self.lines.append(line)

    def dump(self, data: Any, depth: int = 0, iteration: int = 0, list_degree: int = 0, root: bool = True) -> str:
        """Dump the provided data structure to a formatted string."""
        if root:
            self.reset()

        if self.terminate_depth and (depth <= self.max_depth):
            self.terminate_depth = False
        
        if self.terminate or self.terminate_depth:
            return
        
        if iteration > 0 and list_degree > 1:
            list_degree = 1
        
        if isinstance(data, dict) and data:
            for item, (key, value) in enumerate(data.items()):
                if self.max_item > 0 and item == self.max_item:
                    self.add_line('', depth, iteration=iteration, item=item, list_degree=list_degree)
                    break     
                if isinstance(value, (dict, list, tuple)) and value:
                    text = f'{key}{self.separator}'
                    self.add_line(text, depth, iteration=iteration, list_degree=list_degree)
                    if isinstance(value, (list, tuple)) and not self.indent_sequence_on_key:
                        self.dump(value, depth, iteration=iteration, list_degree=0, root=False)
                    else:
                        self.dump(value, depth + 1, iteration=iteration, list_degree=0, root=False)
                else:
                    text = f'{key}{self.separator}{value}'
                    self.add_line(text, depth, iteration=iteration, list_degree=list_degree)
                list_degree = 0
        elif isinstance(data, (list, tuple)) and data:
            for subiteration, data_i in enumerate(data):
                if self.max_iteration > 0 and subiteration == self.max_iteration:
                    self.add_line('', depth, iteration=subiteration, list_degree=list_degree)
                    break         
                self.dump(data_i, depth + 1, iteration=subiteration,
                          list_degree=list_degree + 1, root=False)
        else:
            self.add_line(f'{data}', depth, iteration=iteration, list_degree=list_degree)
        
        if root:
            return '\n'.join(self.lines)