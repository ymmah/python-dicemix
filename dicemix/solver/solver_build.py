# pylint: disable = invalid-name

"""Build helper for C++ extension module used to solve the equation system"""

import os.path
from cffi import FFI

here = os.path.abspath(os.path.dirname(__file__))
ffibuilder = FFI()
with open(os.path.join(here, 'solver.cpp')) as cpp:
    ffibuilder.set_source(
        'dicemix._solver',
        cpp.read(),
        source_extension='.cpp',
        libraries=['gmp', 'flint'],
        )
ffibuilder.cdef("""
    int solve(char* out_messages[], const char* prime, const char* my_message,
              const char* sums[], size_t n);
""")

if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
