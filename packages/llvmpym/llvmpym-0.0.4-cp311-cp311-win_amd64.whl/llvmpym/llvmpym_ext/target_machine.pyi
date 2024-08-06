import enum
from typing import overload

import llvmpym_ext


class CodeGenOptLevel(enum.Enum):
    """CodeGenOptLevel"""

    Null = 0

    Less = 1

    Default = 2

    Aggressive = 3

class CodeModel(enum.Enum):
    """CodeModel"""

    Default = 0

    JITDefault = 1

    Tiny = 2

    Small = 3

    Kernel = 4

    Medium = 5

    Large = 6

class RelocMode(enum.Enum):
    """RelocMode"""

    Default = 0

    Static = 1

    PIC = 2

    DynamicNoPic = 3

    ROPI = 4

    RWPI = 5

    ROPI_RWPI = 6

class Target(llvmpym_ext.PymTargetObject):
    """Target"""

    def __iter__(self) -> TargetIterator: ...

    @staticmethod
    def get_first() -> Target:
        """Returns the first llvm::Target in the registered targets list."""

    @staticmethod
    def get_from_name(name: str) -> Target:
        """Finds the target corresponding to the given name"""

    @staticmethod
    def get_from_triple(triple: str) -> Target:
        """
        Finds the target corresponding to the given triple.Raises:
        	RuntimeError
        """

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def has_jit(self) -> bool: ...

    @property
    def has_target_machine(self) -> bool: ...

    @property
    def has_asm_backend(self) -> bool: ...

    @property
    def next(self) -> Target | None:
        """
        Returns the next llvm::Target given a previous one (or null if there's none)
        """

class TargetIterator:
    """TargetIterator"""

    def __iter__(self) -> TargetIterator: ...

    def __next__(self) -> Target: ...

class TargetMachine(llvmpym_ext.PymTargetMachineObject):
    """TargetMachine"""

    @overload
    def __init__(self, target: Target, triple: str, options: TargetMachineOptions) -> None: ...

    @overload
    def __init__(self, arg0: Target, arg1: str, arg2: str, arg3: str, arg4: CodeGenOptLevel, arg5: RelocMode, arg6: CodeModel, /) -> None: ...

    @property
    def target(self) -> Target: ...

    @property
    def triple(self) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

    @property
    def cpu(self) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

    @property
    def feature_string(self) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

class TargetMachineOptions(llvmpym_ext.PymTargetMachineOptionsObject):
    """TargetMachineOptions"""

    def __init__(self) -> None: ...

    def set_cpu(self, cpu: str) -> None: ...

    def set_features(self, features: str) -> None: ...

    def set_abi(self, abi: str) -> None: ...

    def set_code_gen_opt_level(self, level: CodeGenOptLevel) -> None: ...

    def set_reloc_mode(self, reloc: RelocMode) -> None: ...

    def set_code_model(self, code_model: CodeModel) -> None: ...
