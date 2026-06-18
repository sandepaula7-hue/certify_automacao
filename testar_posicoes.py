# testar_posicoes.py
import json
import time
import pyautogui
import win32gui
import win32con
from pathlib import Path

def testar_posicoes():
    """Testa as posições calibradas sem preencher"""
    
    print("=" * 60)
    print("🧪 TESTANDO POSIÇÕES CALIBRADAS")
    print("=" * 60)
    
    # Carrega configuração
    config_path = Path("programa_x/config.json")
    if not config_path.exists():
        print("❌ config.json não encontrado!")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    positions = config.get('field_positions', {})
    if not positions:
        print("❌ Nenhuma posição calibrada!")
        print("   Execute a calibração primeiro (opção 2)")
        return
    
    print(f"\n✅ {len(positions)} posições carregadas")
    
    # Encontra a janela
    def find_window(title):
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                if title.lower() in win32gui.GetWindowText(hwnd).lower():
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows[0] if windows else None
    
    hwnd = find_window("Programa Y")
    if not hwnd:
        print("❌ Programa Y não encontrado!")
        return
    
    # Ativa a janela
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    print("\n🔍 Testando cada posição (o mouse vai clicar nos campos)...")
    print("   Observa o Programa Y para ver se os cliques estão certos")
    print()
    
    for campo, pos in positions.items():
        print(f"📍 Campo '{campo}' em {pos}")
        
        # Move o mouse
        pyautogui.moveTo(pos[0], pos[1])
        time.sleep(0.3)
        
        # Clica
        pyautogui.click()
        time.sleep(0.3)
        
        # Limpa e digita um teste
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        
        # Digita o nome do campo para teste
        pyautogui.write(f"TESTE_{campo}")
        time.sleep(0.5)
        
        print(f"   ✅ Teste realizado em '{campo}'")
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("   Verifique se o Programa Y foi preenchido com 'TESTE_'")
    print("=" * 60)

if __name__ == "__main__":
    testar_posicoes()