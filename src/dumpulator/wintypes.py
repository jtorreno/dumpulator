# Source: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/win32/context_amd64.py

from ctypes import *
import ctypes

LPVOID = ctypes.c_void_p
CHAR = ctypes.c_char
WCHAR = ctypes.c_wchar
BYTE = ctypes.c_ubyte
SBYTE = ctypes.c_byte
WORD = ctypes.c_uint16
SWORD = ctypes.c_int16
DWORD = ctypes.c_uint32
SDWORD = ctypes.c_int32
QWORD = ctypes.c_uint64
SQWORD = ctypes.c_int64
SHORT = ctypes.c_int16
USHORT = ctypes.c_uint16
INT = ctypes.c_int32
UINT = ctypes.c_uint32
LONG = ctypes.c_int32
ULONG = ctypes.c_uint32
LONGLONG = ctypes.c_int64  # c_longlong
ULONGLONG = ctypes.c_uint64  # c_ulonglong
LPSTR = ctypes.c_char_p
LPWSTR = ctypes.c_wchar_p
INT8 = ctypes.c_int8
INT16 = ctypes.c_int16
INT32 = ctypes.c_int32
INT64 = ctypes.c_int64
UINT8 = ctypes.c_uint8
UINT16 = ctypes.c_uint16
UINT32 = ctypes.c_uint32
UINT64 = ctypes.c_uint64
LONG32 = ctypes.c_int32
LONG64 = ctypes.c_int64
ULONG32 = ctypes.c_uint32
ULONG64 = ctypes.c_uint64
DWORD32 = ctypes.c_uint32
DWORD64 = ctypes.c_uint64
BOOL = ctypes.c_int32
FLOAT = ctypes.c_float  # not sure on cygwin
DOUBLE = ctypes.c_double  # not sure on cygwin

EXCEPTION_READ_FAULT = 0  # exception caused by a read
EXCEPTION_WRITE_FAULT = 1  # exception caused by a write
EXCEPTION_EXECUTE_FAULT = 8  # exception caused by an instruction fetch

CONTEXT_AMD64 = 0x00100000

CONTEXT_CONTROL = (CONTEXT_AMD64 | 0x1)
CONTEXT_INTEGER = (CONTEXT_AMD64 | 0x2)
CONTEXT_SEGMENTS = (CONTEXT_AMD64 | 0x4)
CONTEXT_FLOATING_POINT = (CONTEXT_AMD64 | 0x8)
CONTEXT_DEBUG_REGISTERS = (CONTEXT_AMD64 | 0x10)

CONTEXT_MMX_REGISTERS = CONTEXT_FLOATING_POINT

CONTEXT_FULL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_FLOATING_POINT)

CONTEXT_ALL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_SEGMENTS |
               CONTEXT_FLOATING_POINT | CONTEXT_DEBUG_REGISTERS)

CONTEXT_EXCEPTION_ACTIVE = 0x8000000
CONTEXT_SERVICE_ACTIVE = 0x10000000
CONTEXT_EXCEPTION_REQUEST = 0x40000000
CONTEXT_EXCEPTION_REPORTING = 0x80000000

INITIAL_MXCSR = 0x1f80  # initial MXCSR value
INITIAL_FPCSR = 0x027f  # initial FPCSR value

class M128A(Structure):
    _fields_ = [
        ("Low",     ULONGLONG),
        ("High",    LONGLONG),
    ]

class XMM_SAVE_AREA32(Structure):
    _pack_ = 1
    _fields_ = [
        ('ControlWord', WORD),
        ('StatusWord', WORD),
        ('TagWord', BYTE),
        ('Reserved1', BYTE),
        ('ErrorOpcode', WORD),
        ('ErrorOffset', DWORD),
        ('ErrorSelector', WORD),
        ('Reserved2', WORD),
        ('DataOffset', DWORD),
        ('DataSelector', WORD),
        ('Reserved3', WORD),
        ('MxCsr', DWORD),
        ('MxCsr_Mask', DWORD),
        ('FloatRegisters', M128A * 8),
        ('XmmRegisters', M128A * 16),
        ('Reserved4', BYTE * 96),
    ]


LEGACY_SAVE_AREA_LENGTH = sizeof(XMM_SAVE_AREA32)
PXMM_SAVE_AREA32 = ctypes.POINTER(XMM_SAVE_AREA32)
LPXMM_SAVE_AREA32 = PXMM_SAVE_AREA32

class _CONTEXT_FLTSAVE_STRUCT(Structure):
    _fields_ = [
        ('Header', M128A * 2),
        ('Legacy', M128A * 8),
        ('Xmm0', M128A),
        ('Xmm1', M128A),
        ('Xmm2', M128A),
        ('Xmm3', M128A),
        ('Xmm4', M128A),
        ('Xmm5', M128A),
        ('Xmm6', M128A),
        ('Xmm7', M128A),
        ('Xmm8', M128A),
        ('Xmm9', M128A),
        ('Xmm10', M128A),
        ('Xmm11', M128A),
        ('Xmm12', M128A),
        ('Xmm13', M128A),
        ('Xmm14', M128A),
        ('Xmm15', M128A),
    ]

class _CONTEXT_FLTSAVE_UNION(Union):
    _fields_ = [
        ('flt', XMM_SAVE_AREA32),
        ('xmm', _CONTEXT_FLTSAVE_STRUCT),
    ]

    def from_dict(self):
        raise NotImplementedError()

    def to_dict(self):
        d = dict()
        d['flt'] = self.flt.to_dict()
        d['xmm'] = self.xmm.to_dict()
        return d


class CONTEXT(Structure):
    _pack_ = 16
    _fields_ = [

        # Register parameter home addresses.
        ('P1Home', DWORD64),
        ('P2Home', DWORD64),
        ('P3Home', DWORD64),
        ('P4Home', DWORD64),
        ('P5Home', DWORD64),
        ('P6Home', DWORD64),

        # Control flags.
        ('ContextFlags', DWORD),
        ('MxCsr', DWORD),

        # Segment Registers and processor flags.
        ('SegCs', WORD),
        ('SegDs', WORD),
        ('SegEs', WORD),
        ('SegFs', WORD),
        ('SegGs', WORD),
        ('SegSs', WORD),
        ('EFlags', DWORD),

        # Debug registers.
        ('Dr0', DWORD64),
        ('Dr1', DWORD64),
        ('Dr2', DWORD64),
        ('Dr3', DWORD64),
        ('Dr6', DWORD64),
        ('Dr7', DWORD64),

        # Integer registers.
        ('Rax', DWORD64),
        ('Rcx', DWORD64),
        ('Rdx', DWORD64),
        ('Rbx', DWORD64),
        ('Rsp', DWORD64),
        ('Rbp', DWORD64),
        ('Rsi', DWORD64),
        ('Rdi', DWORD64),
        ('R8', DWORD64),
        ('R9', DWORD64),
        ('R10', DWORD64),
        ('R11', DWORD64),
        ('R12', DWORD64),
        ('R13', DWORD64),
        ('R14', DWORD64),
        ('R15', DWORD64),

        # Program counter.
        ('Rip', DWORD64),

        # Floating point state.
        ('FltSave', _CONTEXT_FLTSAVE_UNION),

        # Vector registers.
        ('VectorRegister', M128A * 26),
        ('VectorControl', DWORD64),

        # Special debug control registers.
        ('DebugControl', DWORD64),
        ('LastBranchToRip', DWORD64),
        ('LastBranchFromRip', DWORD64),
        ('LastExceptionToRip', DWORD64),
        ('LastExceptionFromRip', DWORD64),
    ]

    _others = ('P1Home', 'P2Home', 'P3Home', 'P4Home', 'P5Home', 'P6Home',
               'MxCsr', 'VectorRegister', 'VectorControl')
    _control = ('SegSs', 'Rsp', 'SegCs', 'Rip', 'EFlags')
    _integer = ('Rax', 'Rcx', 'Rdx', 'Rbx', 'Rsp', 'Rbp', 'Rsi', 'Rdi',
                'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15')
    _segments = ('SegDs', 'SegEs', 'SegFs', 'SegGs')
    _debug = ('Dr0', 'Dr1', 'Dr2', 'Dr3', 'Dr6', 'Dr7',
              'DebugControl', 'LastBranchToRip', 'LastBranchFromRip',
              'LastExceptionToRip', 'LastExceptionFromRip')
    _mmx = ('Xmm0', 'Xmm1', 'Xmm2', 'Xmm3', 'Xmm4', 'Xmm5', 'Xmm6', 'Xmm7',
            'Xmm8', 'Xmm9', 'Xmm10', 'Xmm11', 'Xmm12', 'Xmm13', 'Xmm14', 'Xmm15')
