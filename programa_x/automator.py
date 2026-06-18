# programa_x/automator.py
import pyautogui
import time
import win32gui
import win32con
import win32api
from PIL import ImageGrab
import numpy as np

class FormAutomator:
    def __init__(self):
        # Configurar segurança do PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        self.window_handle = None
        self.window_title = None
        self.field_positions = {}
        
        # Posições padrão dos campos (ajuste conforme sua tela)
        self.default_positions = {
            'nome': (250, 180),
            'cpf': (250, 230),
            'data_nasc': (250, 280),
            'endereco': (250, 330),
            'telefone': (250, 380),
            'email': (250, 430),
            'observacoes': (250, 480)
        }
        
    def find_window(self, window_title):
        """
        Encontra a janela do Programa Y pelo título
        Retorna True se encontrou, False caso contrário
        """
        print(f"🔍 Procurando janela: {window_title}")
        
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Ignora janelas sem título
                    # Busca por parte do título (case insensitive)
                    if window_title.lower() in title.lower():
                        windows.append((hwnd, title))
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            self.window_handle, self.window_title = windows[0]
            print(f"✅ Janela encontrada: {self.window_title}")
            return True
        else:
            print(f"❌ Nenhuma janela com '{window_title}' encontrada")
            
            # Lista todas as janelas para debug
            print("\n📋 Janelas abertas:")
            def list_callback(hwnd, _):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        print(f"   - {title}")
                return True
            win32gui.EnumWindows(list_callback, None)
            
            return False
    
    def activate_window(self):
        """Ativa a janela do Programa Y"""
        if self.window_handle:
            try:
                # Restaura se minimizada
                win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                # Traz para frente
                win32gui.SetForegroundWindow(self.window_handle)
                time.sleep(0.3)
                return True
            except Exception as e:
                print(f"⚠️ Erro ao ativar janela: {e}")
                return False
        return False
    
    def calibrate_positions(self):
        """
        Calibra as posições dos campos (modo interativo)
        O usuário move o mouse sobre cada campo e pressiona ENTER
        """
        print("\n🔄 Modo de Calibração")
        print("Mova o mouse sobre cada campo e pressione ENTER")
        print("Pressione ESC para cancelar")
        
        positions = {}
        campos = list(self.default_positions.keys())
        
        for i, field in enumerate(campos, 1):
            print(f"\n[{i}/{len(campos)}] Posicione o mouse no campo '{field}' e pressione ENTER...")
            
            # Espera o usuário pressionar ENTER
            input()
            
            # Captura posição atual do mouse
            x, y = win32api.GetCursorPos()
            positions[field] = (x, y)
            print(f"✅ Campo '{field}' calibrado em ({x}, {y})")
        
        self.field_positions = positions
        print("\n✅ Calibração concluída!")
        return positions
    
    def fill_field(self, field_name, value):
        """
        Preenche um campo específico do formulário
        """
        if not value:
            return False
        
        # Usa posição calibrada ou default
        pos = self.field_positions.get(field_name, self.default_positions.get(field_name))
        if not pos:
            print(f"⚠️ Posição não encontrada para {field_name}")
            return False
        
        try:
            # Ativa a janela
            self.activate_window()
            
            # Clica no campo
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.2)
            
            # Limpa campo existente (Ctrl+A + Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # Digita o valor
            pyautogui.write(str(value))
            time.sleep(0.1)
            
            print(f"✏️ Campo '{field_name}': {value}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao preencher {field_name}: {e}")
            return False
    
    def fill_form(self, data):
        """
        Preenche múltiplos campos do formulário
        """
        print("\n📝 Preenchendo formulário...")
        
        success_count = 0
        total_fields = 0
        
        for field_name, value in data.items():
            if value and field_name in self.default_positions:
                total_fields += 1
                if self.fill_field(field_name, value):
                    success_count += 1
                time.sleep(0.3)  # Pausa entre campos
        
        print(f"\n✅ {success_count}/{total_fields} campos preenchidos")
        return success_count > 0
    
    def capture_screenshot(self, region=None):
        """
        Captura screenshot da janela do Programa Y
        """
        if self.window_handle:
            try:
                # Obtém dimensões da janela
                rect = win32gui.GetWindowRect(self.window_handle)
                x, y, x2, y2 = rect
                
                # Captura a região
                screenshot = ImageGrab.grab(bbox=(x, y, x2, y2))
                return screenshot
            except Exception as e:
                print(f"⚠️ Erro ao capturar screenshot: {e}")
                return None
        return None
    
    def get_window_position(self):
        """
        Retorna a posição da janela na tela
        """
        if self.window_handle:
            try:
                rect = win32gui.GetWindowRect(self.window_handle)
                return rect
            except:
                return None
        return None