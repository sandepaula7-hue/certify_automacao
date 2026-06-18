# atualizar_config.py
import json
import win32gui

def encontrar_janela_por_parte(nome_parcial):
    """Encontra janela por parte do nome"""
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if nome_parcial.lower() in title.lower():
                windows.append(title)
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def atualizar_config():
    """Atualiza o título da janela no config.json"""
    
    # Procura janelas com "Programa Y"
    janelas = encontrar_janela_por_parte("Programa Y")
    
    if not janelas:
        print("❌ Programa Y não encontrado!")
        print("Certifique-se de que o Programa Y está aberto.")
        return
    
    # Usa a primeira janela encontrada
    titulo_correto = janelas[0]
    print(f"✅ Janela encontrada: {titulo_correto}")
    
    # Atualiza o config.json
    config_path = "programa_x/config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config["window_title"] = titulo_correto
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Config atualizado para: {titulo_correto}")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar config: {e}")

if __name__ == "__main__":
    atualizar_config()