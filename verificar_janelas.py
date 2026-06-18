# verificar_janelas.py
import win32gui
import win32con

def listar_janelas():
    """Lista todas as janelas abertas"""
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # Só mostra janelas com título
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    print("=" * 60)
    print("JANELAS ABERTAS:")
    print("=" * 60)
    
    for i, (hwnd, title) in enumerate(windows, 1):
        print(f"{i}. {title}")
    
    return windows

if __name__ == "__main__":
    listar_janelas()