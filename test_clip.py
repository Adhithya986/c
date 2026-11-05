import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = wintypes.HGLOBAL

kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalLock.restype = wintypes.LPVOID

kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalUnlock.restype = wintypes.BOOL

user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.OpenClipboard.restype = wintypes.BOOL

user32.EmptyClipboard.argtypes = []
user32.EmptyClipboard.restype = wintypes.BOOL

user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
user32.SetClipboardData.restype = wintypes.HANDLE

user32.CloseClipboard.argtypes = []
user32.CloseClipboard.restype = wintypes.BOOL

user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.GetClipboardData.restype = wintypes.HANDLE

CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002

def set_clipboard(text: str):
    data = (text + '\0').encode('utf-16le')
    h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
    if not h_mem:
        return False
    ptr = kernel32.GlobalLock(h_mem)
    if not ptr:
        return False
    ctypes.memmove(ptr, data, len(data))
    kernel32.GlobalUnlock(h_mem)

    if not user32.OpenClipboard(None):
        return False
    user32.EmptyClipboard()
    user32.SetClipboardData(CF_UNICODETEXT, h_mem)
    user32.CloseClipboard()
    return True

def get_clipboard() -> str:
    if not user32.OpenClipboard(None):
        return ""
    h_mem = user32.GetClipboardData(CF_UNICODETEXT)
    if not h_mem:
        user32.CloseClipboard()
        return ""
    ptr = kernel32.GlobalLock(h_mem)
    text = ctypes.wstring_at(ptr)
    kernel32.GlobalUnlock(h_mem)
    user32.CloseClipboard()
    return text

if __name__ == "__main__":
    msg = "Test Ctypes Clipboard Success!"
    set_clipboard(msg)
    read_back = get_clipboard()
    print("Read back:", read_back)

