from typing import List

from ..cpl._base import CompileTimeValue
from ..transpiler import FunctionDeclaration, TranspilerContext, add_lib


def lib_raycast(ctx: TranspilerContext, args: List[CompileTimeValue], token):
    pass


add_lib(FunctionDeclaration(
    type="python-cpl",
    name="raycast",
    function=lib_raycast
))
