# programa_x/main.py
import sys
import os
import json
import time
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scanner import DocumentScanner
from automator import FormAutomator

class ProgramaX:
    def __init__(self):
        print("🚀 Inicializando Programa X...")
        self.scanner = DocumentScanner()
        self.automator = FormAutomator()
        self.config = self.load_config()
        
        print("=" * 60)
        print("🚀 PROGRAMA X - Sistema de Automação")
        print("=" * 60)
        
    def load_config(self):
        """Carrega configurações com tratamento de erro"""
        
        config_path = Path(__file__).parent / "config.json"
        
        # Configuração padrão
        default_config = {
            "window_title": "Programa Y - Formulário de Cadastro",
            "document_folder": "../documentos_teste",
            "auto_calibrate": True,
            "delay_between_actions": 0.5
        }
        
        # Se o arquivo não existe, cria com configuração padrão
        if not config_path.exists():
            print("⚠️ config.json não encontrado. Criando configuração padrão...")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            return default_config
        
        # Tenta carregar o arquivo
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✅ Configuração carregada com sucesso!")
            return config
            
        except json.JSONDecodeError as e:
            print(f"❌ Erro no arquivo config.json: {e}")
            print("📄 Usando configuração padrão...")
            
            # Faz backup do arquivo corrompido
            backup_path = config_path.parent / "config.json.corrompido"
            try:
                with open(config_path, 'r', encoding='utf-8') as f_old:
                    with open(backup_path, 'w', encoding='utf-8') as f_backup:
                        f_backup.write(f_old.read())
                print(f"📄 Backup salvo em: {backup_path}")
            except:
                pass
            
            # Recria o arquivo com configuração padrão
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            print("✅ Novo config.json criado com configuração padrão!")
            
            return default_config
            
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return default_config
    
    def menu_principal(self):
        """Exibe menu principal"""
        while True:
            print("\n" + "=" * 50)
            print("MENU PRINCIPAL")
            print("=" * 50)
            print("1. 📄 Scan e Preencher Documento")
            print("2. 📷 Calibrar Posições dos Campos")
            print("3. 📋 Listar Documentos Disponíveis")
            print("4. ⚙️ Configurações")
            print("5. ❌ Sair")
            print("=" * 50)
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.scan_and_fill()
            elif opcao == "2":
                self.calibrar_campos()
            elif opcao == "3":
                self.listar_documentos()
            elif opcao == "4":
                self.ver_configuracoes()
            elif opcao == "5":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida!")
    
    def scan_and_fill(self):
        """Processo completo de scan e preenchimento"""
        print("\n" + "=" * 50)
        print("📄 SCAN E PREENCHIMENTO AUTOMÁTICO")
        print("=" * 50)
        
        # 1. Verifica se o Programa Y está aberto
        print("\n🔍 Verificando Programa Y...")
        window_title = self.config.get("window_title", "Programa Y - Formulário de Cadastro")
        
        if not self.automator.find_window(window_title):
            print("❌ Programa Y não encontrado!")
            print(f"   Certifique-se de que o Programa Y está aberto")
            print("   Execute em outro terminal: cd programa_y && python form_app.py")
            
            # Pergunta se quer tentar novamente com outro título
            tentar = input("\nDeseja tentar com outro título? (S/N): ").upper()
            if tentar == 'S':
                novo_titulo = input("Digite o título exato da janela: ")
                if self.automator.find_window(novo_titulo):
                    print("✅ Programa Y encontrado!")
                    # Atualiza o config
                    self.config["window_title"] = novo_titulo
                    self.save_config()
                else:
                    return
            else:
                return
        
        print("✅ Programa Y encontrado!")
        
        # 2. Lista documentos disponíveis
        documentos = self.listar_documentos(return_list=True)
        if not documentos:
            print("❌ Nenhum documento encontrado na pasta de documentos!")
            print("   Execute: cd documentos_teste && python criar_documento_teste.py")
            return
        
        print("\n📋 Documentos disponíveis:")
        for i, doc in enumerate(documentos, 1):
            print(f"   {i}. {Path(doc).name}")
        
        # 3. Seleciona documento
        try:
            escolha = int(input("\nSelecione o número do documento: ")) - 1
            if escolha < 0 or escolha >= len(documentos):
                print("❌ Opção inválida!")
                return
            documento_path = documentos[escolha]
        except ValueError:
            print("❌ Digite um número válido!")
            return
        
        # 4. Faz o scan do documento
        print(f"\n📄 Scaneando: {Path(documento_path).name}")
        dados_extraidos = self.scanner.scan_document(documento_path)
        
        if not dados_extraidos:
            print("❌ Não foi possível extrair dados do documento!")
            return
        
        # 5. Mostra dados extraídos
        print("\n📊 Dados extraídos:")
        for campo, valor in dados_extraidos.items():
            print(f"   {campo}: {valor}")
        
        # 6. Confirma preenchimento
        confirmar = input("\nDeseja preencher o formulário? (S/N): ").strip().upper()
        if confirmar != 'S':
            print("⏹️ Operação cancelada")
            return
        
        # 7. Preenche formulário
        print("\n🚀 Iniciando preenchimento automático...")
        time.sleep(1)
        
        if self.automator.fill_form(dados_extraidos):
            print("\n✅ Formulário preenchido com sucesso!")
        else:
            print("\n⚠️ Alguns campos podem não ter sido preenchidos")
        
        # 8. Pergunta se quer salvar
        salvar = input("\nDeseja salvar os dados no Programa Y? (S/N): ").strip().upper()
        if salvar == 'S':
            # Clica no botão Salvar (posição aproximada)
            self.automator.activate_window()
            # Posição do botão Salvar (ajuste conforme necessário)
            pyautogui.click(300, 520)
            print("✅ Dados salvos!")
    
    def calibrar_campos(self):
        """Calibra as posições dos campos do formulário"""
        print("\n" + "=" * 50)
        print("📷 CALIBRAÇÃO DE CAMPOS")
        print("=" * 50)
        print("\nInstruções:")
        print("1. Certifique-se que o Programa Y esteja aberto")
        print("2. Posicione o mouse sobre cada campo")
        print("3. Pressione ENTER para cada campo")
        print("4. Pressione ESC para cancelar\n")
        
        input("Pressione ENTER para iniciar a calibração...")
        
        window_title = self.config.get("window_title", "Programa Y - Formulário de Cadastro")
        if not self.automator.find_window(window_title):
            print("❌ Programa Y não encontrado!")
            return
        
        self.automator.activate_window()
        positions = self.automator.calibrate_positions()
        
        if positions:
            # Salva posições no config
            self.config["field_positions"] = positions
            self.save_config()
            print("✅ Posições salvas no arquivo de configuração!")
    
    def save_config(self):
        """Salva a configuração atual"""
        config_path = Path(__file__).parent / "config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print("✅ Configuração salva!")
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
    
    def listar_documentos(self, return_list=False):
        """Lista documentos disponíveis na pasta de documentos"""
        doc_folder = Path(__file__).parent / self.config.get("document_folder", "../documentos_teste")
        doc_folder = doc_folder.resolve()
        
        if not doc_folder.exists():
            print(f"❌ Pasta não encontrada: {doc_folder}")
            return [] if return_list else None
        
        extensoes = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.pdf']
        documentos = []
        
        for arquivo in doc_folder.iterdir():
            if arquivo.suffix.lower() in extensoes:
                documentos.append(str(arquivo))
        
        if return_list:
            return documentos
        
        if documentos:
            print(f"\n📋 Documentos encontrados ({len(documentos)}):")
            for doc in documentos:
                print(f"   📄 {Path(doc).name}")
        else:
            print("❌ Nenhum documento encontrado!")
        
        return None
    
    def ver_configuracoes(self):
        """Mostra configurações atuais"""
        print("\n⚙️ CONFIGURAÇÕES ATUAIS")
        print("=" * 50)
        for chave, valor in self.config.items():
            print(f"   {chave}: {valor}")
        
        input("\nPressione ENTER para continuar...")

def main():
    try:
        programa = ProgramaX()
        programa.menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("   Verifique o arquivo config.json")
        input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()