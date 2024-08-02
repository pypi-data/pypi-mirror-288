from typing import Union, Tuple
import re

class Version:
    """
    A class to represent a package version.

    Parameters
    ----------
    version : str or tuple
        The version information. This can be a string in the format "major.minor.micro" or "major.minor",
        or a tuple of the form (major, minor, micro) or (major, minor).

    Attributes
    ----------
    major : int
        Major version number.
    minor : int
        Minor version number.
    micro : int
        Micro version number.

    Raises
    ------
    ValueError
        If the input version string or tuple is in an invalid format.
    """

    def __init__(self, version: Union[str, Tuple[int, int, int], Tuple[int, int]]):
        if isinstance(version, str):
            self._parse_version_string(version)
        elif isinstance(version, tuple):
            self._parse_version_tuple(version)
        elif isinstance(version, Version):
            self.major, self.minor, self.micro = version.major, version.minor, version.micro
        else:
            raise ValueError("Version must be a string or a tuple")
    
    def _parse_version_string(self, version: str):
        """
        Parse the version string and set the major, minor, and micro attributes.

        Parameters
        ----------
        version : str
            The version string to parse.

        Raises
        ------
        ValueError
            If the version string is not in the correct format.
        """
        pattern = r'^\d+(\.\d+){1,2}$'
        if not re.match(pattern, version):
            raise ValueError("Invalid version string format")
        parts = list(map(int, version.split('.')))
        if len(parts) == 2:
            parts.append(0)
        self.major, self.minor, self.micro = parts

    def _parse_version_tuple(self, version: Tuple[int, int, int]):
        """
        Parse the version tuple and set the major, minor, and micro attributes.

        Parameters
        ----------
        version : tuple
            The version tuple to parse.

        Raises
        ------
        ValueError
            If the version tuple is not in the correct format or contains non-integer elements.
        """
        if not all(isinstance(part, int) for part in version):
            raise ValueError("All elements of the version tuple must be integers")
        if len(version) == 2:
            self.major, self.minor = version
            self.micro = 0
        elif len(version) == 3:
            self.major, self.minor, self.micro = version
        else:
            raise ValueError("Version tuple must have 2 or 3 elements")
    
    def __eq__(self, other):
        other = Version(other)
        return (self.major, self.minor, self.micro) == (other.major, other.minor, other.micro)
    
    def __ne__(self, other):
        other = Version(other)
        return not self.__eq__(other)
    
    def __gt__(self, other):
        other = Version(other)
        return (self.major, self.minor, self.micro) > (other.major, other.minor, other.micro)
    
    def __ge__(self, other):
        other = Version(other)
        return (self.major, self.minor, self.micro) >= (other.major, other.minor, other.micro)
    
    def __lt__(self, other):
        other = Version(other)
        return (self.major, self.minor, self.micro) < (other.major, other.minor, other.micro)
    
    def __le__(self, other):
        other = Version(other)
        return (self.major, self.minor, self.micro) <= (other.major, other.minor, other.micro)
    
    def __repr__(self):
        return f"Version(major={self.major}, minor={self.minor}, micro={self.micro})"
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.micro}"