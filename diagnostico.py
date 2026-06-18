# diagnostico.py
import sys
import os
import json
import win32gui
import win32con

def verificar_programa_y():
    """Verifica se o Programa Y está rodando"""
    
    print("=" * 60)
    print("DIAGNÓSTICO DO SISTEMA")
    print("=" * 60)
    
    # 1. Verifica se o Programa Y está rodando
    print("\n[1] Verificando Programa Y...")
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Programa Y" in title or "Formulário" in title:
                windows.append(title)
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        print(f"✅ Programa Y encontrado!")
        for i, win in enumerate(windows, 1):
            print(f"   {i}. {win}")
    else:
        print("❌ Programa Y NÃO encontrado!")
        print("\n   Solução:")
        print("   1. Abra um novo terminal")
        print("   2. Execute: cd programa_y")
        print("   3. Execute: python form_app.py")
        return False
    
    # 2. Verifica o config.json
    print("\n[2] Verificando config.json...")
    config_path = "programa_x/config.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        titulo_config = config.get("window_title", "")
        print(f"📄 Título no config: {titulo_config}")
        
        # Verifica se o título bate
        titulo_correto = windows[0]
        if titulo_config != titulo_correto:
            print(f"⚠️ Título diferente!")
            print(f"   Config: {titulo_config}")
            print(f"   Real:   {titulo_correto}")
            
            # Sugere correção
            print("\n   Para corrigir:")
            print(f"   Atualize o config.json com: {titulo_correto}")
    else:
        print("❌ config.json não encontrado!")
    
    # 3. Verifica dependências
    print("\n[3] Verificando dependências...")
    try:
        import pyautogui
        import win32gui
        print("✅ pywin32 e pyautogui OK")
    except ImportError as e:
        print(f"❌ Erro: {e}")
    
    # 4. Lista todas as janelas
    print("\n[4] Todas as janelas abertas:")
    
    def list_all(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                print(f"   - {title}")
        return True
    
    win32gui.EnumWindows(list_all, None)
    
    print("\n" + "=" * 60)
    return True

if __name__ == "__main__":
    verificar_programa_y()