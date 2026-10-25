# Irvine include files

The MASM solutions include `Irvine32.inc`, `Macros.inc` and `GraphWin.inc`
from Kip Irvine's 32-bit assembly library. These headers are vendored here so
that the CI build and local builds do not depend on a Visual Studio install.

The files were copied from the publicly available Irvine32 library
(`Lib32/`) and are used only for compiling the solutions in this repository.
See <https://asmirvine.com/> for the library itself and its terms of use.
