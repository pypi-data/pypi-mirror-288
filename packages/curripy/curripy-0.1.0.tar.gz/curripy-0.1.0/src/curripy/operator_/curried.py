from operator import add as add_
from operator import and_ as and__
from operator import concat as concat_
from operator import contains as contains_
from operator import countOf as countOf_
from operator import delitem as delitem_
from operator import eq as eq_
from operator import floordiv as floordiv_
from operator import ge as ge_
from operator import getitem as getitem_
from operator import gt as gt_
from operator import iadd as iadd_
from operator import iand as iand_
from operator import iconcat as iconcat_
from operator import ifloordiv as ifloordiv_
from operator import ilshift as ilshift_
from operator import imatmul as imatmul_
from operator import imod as imod_
from operator import imul as imul_
from operator import index as index_
from operator import indexOf as indexOf_
from operator import inv as inv_
from operator import invert as invert_
from operator import ior as ior_
from operator import ipow as ipow_
from operator import irshift as irshift_
from operator import is_ as is__
from operator import is_not as is_not_
from operator import isub as isub_
from operator import itruediv as itruediv_
from operator import ixor as ixor_
from operator import le as le_
from operator import lshift as lshift_
from operator import lt as lt_
from operator import matmul as matmul_
from operator import mod as mod_
from operator import mul as mul_
from operator import ne as ne_
from operator import or_ as or__
from operator import pos as pos_
from operator import pow as pow__
from operator import rshift as rshift_
from operator import setitem as setitem_
from operator import sub as sub_
from operator import truediv as truediv_
from operator import xor as xor_

from ..functionalize_tools import curry as c

__all__ = [
    "add",
    "and_",
    "concat",
    "contains",
    "countOf",
    "delitem",
    "eq",
    "floordiv",
    "ge",
    "getitem",
    "gt",
    "iadd",
    "iand",
    "iconcat",
    "ifloordiv",
    "ilshift",
    "imatmul",
    "imod",
    "imul",
    "index",
    "indexOf",
    "inv",
    "invert",
    "ior",
    "ipow",
    "irshift",
    "is_",
    "is_not",
    "isub",
    "itruediv",
    "ixor",
    "le",
    "lshift",
    "lt",
    "matmul",
    "mod",
    "mul",
    "ne",
    "or_",
    "pos",
    "pow_",
    "rshift",
    "setitem",
    "sub",
    "truediv",
    "xor",
]

add = c(add_)
and_ = c(and__)
concat = c(concat_)
contains = c(contains_)
countOf = c(countOf_)
delitem = c(delitem_)
eq = c(eq_)
floordiv = c(floordiv_)
ge = c(ge_)
getitem = c(getitem_)
gt = c(gt_)
iadd = c(iadd_)
iand = c(iand_)
iconcat = c(iconcat_)
ifloordiv = c(ifloordiv_)
ilshift = c(ilshift_)
imatmul = c(imatmul_)
imod = c(imod_)
imul = c(imul_)
index = c(index_)
indexOf = c(indexOf_)
inv = c(inv_)
invert = c(invert_)
ior = c(ior_)
ipow = c(ipow_)
irshift = c(irshift_)
is_ = c(is__)
is_not = c(is_not_)
isub = c(isub_)
itruediv = c(itruediv_)
ixor = c(ixor_)
le = c(le_)
lshift = c(lshift_)
lt = c(lt_)
matmul = c(matmul_)
mod = c(mod_)
mul = c(mul_)
ne = c(ne_)
or_ = c(or__)
pos = c(pos_)
pow_ = c(pow__)
rshift = c(rshift_)
setitem = c(setitem_)
sub = c(sub_)
truediv = c(truediv_)
xor = c(xor_)
