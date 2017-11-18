import typing as t


# Re-export some common types
Any = t.Any
Optional = t.Optional

FilePath = t.NewType('FilePath', str)
