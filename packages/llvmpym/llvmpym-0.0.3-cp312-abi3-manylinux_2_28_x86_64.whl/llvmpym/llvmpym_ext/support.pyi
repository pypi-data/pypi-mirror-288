from collections.abc import Sequence


def load_library_permanently(filename: str) -> bool:
    """
    This function permanently loads the dynamic library at the given path.It is safe to call this function multiple times for the same library.
    """

def parse_command_line_options(args: Sequence[str], overview: str) -> None:
    """
    This function parses the given arguments using the LLVM command line parser.Note that the only stable thing about this function is its signature; youcannot rely on any particular set of command line arguments being interpretedthe same way across LLVM versions.
    """
