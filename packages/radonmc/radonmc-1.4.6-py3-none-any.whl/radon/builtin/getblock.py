from typing import List

from ..cpl._base import CompileTimeValue
from ..cpl.score import CplScore
from ..error import raise_syntax_error
from ..transpiler import FunctionDeclaration, TranspilerContext, add_lib


def lib_getblock(ctx: TranspilerContext, args: List[CompileTimeValue], token):
    pass


add_lib(FunctionDeclaration(
    type="python-cpl",
    name="getblock",
    function=lib_getblock,
))
