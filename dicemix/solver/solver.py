from _solver import ffi, lib

def _int2hexbytes(n):
    return bytes(hex(n), 'ascii')[2:]

# 2**160 - 47
P = 1461501637330902918203684832716283019655932542929
_HEX_P = _int2hexbytes(P)

_C_RET_INVALID = 1
_C_RET_INTERNAL_ERROR = 100
_C_RET_INPUT_ERROR = 101

def solve(dc_sums, my_message):
    """Solve function from protocol specification.

    Solves the equation system
      forall 0 <= i < size(dc_sums). sum_{j=0}^{size(dc_sums)-1)} messages[j]^{i+1} = dc_sums[i]
    in the finite prime field F_P for messages, and checks if my_message is in the solution.
    Assumes that size(dc_sums) >= 2.

    Returns a list of messages as solution (sorted in ascending numerial order) in case of success.
    Returns None if dc_sums is not a proper list of power sums, or if my_message is not a solution.
    """
    ffi_sums = [ffi.new('char[]', _int2hexbytes(s)) for s in dc_sums]
    # Allocate result buffers (size of P in hex + 1 null char)
    ffi_messages = [ffi.new('char[]', len(_HEX_P) + 1) for _ in dc_sums]

    res = lib.solve(ffi_messages, _HEX_P, _int2hexbytes(my_message), ffi_sums, len(dc_sums))

    if res == 0:
        return [int(ffi.string(m), 16) for m in ffi_messages]
    elif res == _C_RET_INVALID:
        return None
    elif res == _C_RET_INPUT_ERROR:
        raise ValueError
    else:
        raise RuntimeError
