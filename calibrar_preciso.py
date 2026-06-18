# calibrar_preciso.py
import sys
import json
import time
import win32gui
import win32con
import win32api
from pathlib import Path

# Adiciona o caminho do programa_x
sys.path.append('programa_x')
from automator import FormAutomator

def calibrar_com_precisao():
    """Calibração com mais precisão e feedback visual"""
    
    print("=" * 60)
    print("📷 CALIBRAÇÃO PRECISA")
    print("=" * 60)
    print()
    print("Instruções:")
    print("1. Certifique-se que o Programa Y esteja aberto e VISÍVEL")
    print("2. Para cada campo, mova o mouse para DENTRO do campo")
    print("3. Clique com o mouse dentro do campo")
    print("4. Depois pressione ENTER no terminal")
    print()
    
    input("Pressione ENTER para começar...")
    
    automator = FormAutomator()
    
    # Encontra a janela
    if not automator.find_window("Programa Y"):
        print("❌ Programa Y não encontrado!")
        return
    
    automator.activate_window()
    time.sleep(0.5)
    
    # Lista de campos
    campos = ['nome', 'cpf', 'data_nasc', 'endereco', 'telefone', 'email', 'observacoes']
    positions = {}
    
    for i, campo in enumerate(campos, 1):
        print(f"\n[{i}/{len(campos)}] Campo: {campo}")
        print("  1. Clique com o mouse dentro do campo")
        print("  2. Pressione ENTER para confirmar a posição")
        print("  3. Pressione 'p' para pular")
        print("  4. Pressione 'r' para refazer")
        
        while True:
            opcao = input("  Posicione o mouse e pressione ENTER (ou comando): ").strip().lower()
            
            if opcao == 'p':
                print(f"  ⏭️ Pulando campo {campo}")
                break
            elif opcao == 'r':
                print("  🔄 Refazendo...")
                continue
            else:
                # Captura posição
                x, y = win32api.GetCursorPos()
                positions[campo] = (x, y)
                print(f"  ✅ Campo '{campo}' calibrado em ({x}, {y})")
                
                # Testa a posição (clica e digita algo para testar)
                print("  🔍 Testando posição...")
                win32api.SetCursorPos((x, y))
                time.sleep(0.2)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                time.sleep(0.2)
                print("  ✅ Posição testada com sucesso!")
                break
    
    # Salva as posições
    if positions:
        config_path = Path("programa_x/config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config['field_positions'] = positions
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("✅ CALIBRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Posições salvas:")
        for campo, pos in positions.items():
            print(f"   {campo}: {pos}")
    else:
        print("\n❌ Nenhuma posição foi salva!")

if __name__ == "__main__":
    calibrar_com_precisao()