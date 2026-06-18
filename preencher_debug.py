# preencher_debug.py
import sys
import time
import pyautogui
import json
from pathlib import Path

sys.path.append('programa_x')
from automator import FormAutomator

def preencher_com_debug():
    """Preenche mostrando onde o mouse está clicando"""
    
    print("=" * 60)
    print("🚀 PREENCHIMENTO COM DEBUG VISUAL")
    print("=" * 60)
    
    # Carrega configuração
    config_path = Path("programa_x/config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    positions = config.get('field_positions', {})
    if not positions:
        print("❌ Calibre os campos primeiro!")
        return
    
    automator = FormAutomator()
    
    if not automator.find_window("Programa Y"):
        print("❌ Programa Y não encontrado!")
        return
    
    # Dados de teste
    dados_teste = {
        'nome': 'João Silva Santos',
        'cpf': '123.456.789-00',
        'data_nasc': '15/03/1985',
        'endereco': 'Rua das Flores, 123',
        'telefone': '(11) 98765-4321',
        'email': 'joao.silva@email.com',
        'observacoes': 'Cliente desde 2020'
    }
    
    print("\n📝 Dados a serem preenchidos:")
    for campo, valor in dados_teste.items():
        print(f"   {campo}: {valor}")
    
    print("\n🚀 Iniciando preenchimento em 3 segundos...")
    print("   Mova o mouse para ver onde ele clica")
    print("   Pressione Ctrl+C para cancelar")
    time.sleep(3)
    
    automator.activate_window()
    time.sleep(0.5)
    
    for campo, valor in dados_teste.items():
        if campo in positions:
            pos = positions[campo]
            print(f"\n✏️ Preenchendo '{campo}' em {pos}")
            
            # Mostra onde o mouse vai clicar
            pyautogui.moveTo(pos[0], pos[1])
            time.sleep(0.5)
            
            # Clica e preenche
            automator.fill_field(campo, valor)
            time.sleep(0.8)
    
    print("\n✅ Preenchimento concluído!")

if __name__ == "__main__":
    try:
        preencher_com_debug()
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário")