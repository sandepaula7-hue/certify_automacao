# verificar_janela.py
import win32gui
import win32con

def get_window_info():
    """Mostra informações da janela do Programa Y"""
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Programa Y" in title or "Formulário" in title:
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        hwnd, title = windows[0]
        rect = win32gui.GetWindowRect(hwnd)
        x, y, x2, y2 = rect
        
        print("=" * 60)
        print("INFORMAÇÕES DA JANELA")
        print("=" * 60)
        print(f"Título: {title}")
        print(f"Posição: ({x}, {y})")
        print(f"Tamanho: {x2-x} x {y2-y}")
        print(f"Largura: {x2-x}")
        print(f"Altura: {y2-y}")
        print(f"Centro: ({x + (x2-x)//2}, {y + (y2-y)//2})")
        print("=" * 60)
        
        # Sugere posições baseadas no centro
        center_x = x + (x2-x)//2
        center_y = y + (y2-y)//2
        
        print("\n💡 Posições sugeridas (baseado no centro):")
        print(f"   nome: [{center_x - 150}, {center_y - 100}]")
        print(f"   cpf: [{center_x - 150}, {center_y - 50}]")
        print(f"   data_nasc: [{center_x - 150}, {center_y}]")
        print(f"   endereco: [{center_x - 150}, {center_y + 50}]")
        
    else:
        print("❌ Programa Y não encontrado!")

if __name__ == "__main__":
    get_window_info()