# programa_x/scanner.py
import easyocr
import re
from PIL import Image
import numpy as np

class DocumentScanner:
    def __init__(self):
        print("🔄 Inicializando OCR...")
        try:
            # Inicializa EasyOCR para português
            self.reader = easyocr.Reader(['pt'], gpu=False, verbose=False)
            print("✅ OCR inicializado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inicializar OCR: {e}")
            print("   Verifique se o EasyOCR está instalado: pip install easyocr")
            self.reader = None
        
    def scan_document(self, image_path):
        """
        Lê documento e extrai dados estruturados
        """
        if self.reader is None:
            print("❌ OCR não disponível!")
            return {}
            
        print(f"📄 Scaneando documento: {image_path}")
        
        try:
            # Ler texto da imagem
            result = self.reader.readtext(image_path, detail=0)
            full_text = ' '.join(result)
            
            print(f"📝 Texto extraído: {full_text[:100]}...")
            
            # Extrair campos específicos
            extracted_data = self.extract_fields(full_text)
            
            print(f"✅ Dados extraídos: {extracted_data}")
            return extracted_data
            
        except Exception as e:
            print(f"❌ Erro no scan: {e}")
            return {}
    
    def extract_fields(self, text):
        """Extrai campos específicos do texto usando regex"""
        data = {}
        
        # Nome
        nome_patterns = [
            r'Nome Completo:?\s*([A-Za-zÀ-ÖØ-öø-ÿ\s]{3,})',
            r'Nome:?\s*([A-Za-zÀ-ÖØ-öø-ÿ\s]{3,})',
        ]
        for pattern in nome_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['nome'] = match.group(1).strip()
                break
        
        # CPF
        cpf_match = re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', text)
        if cpf_match:
            data['cpf'] = cpf_match.group()
        
        # Data de Nascimento
        data_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
        if data_match:
            data['data_nasc'] = data_match.group()
        
        # Endereço
        endereco_match = re.search(r'Endereço:?\s*([^,\n]+,\s*\d+[^,\n]*)', text, re.IGNORECASE)
        if endereco_match:
            data['endereco'] = endereco_match.group(1).strip()
        
        # Telefone
        telefone_match = re.search(r'\(?\d{2}\)?\s*\d{4,5}-\d{4}', text)
        if telefone_match:
            data['telefone'] = telefone_match.group()
        
        # Email
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            data['email'] = email_match.group()
        
        # Observações
        obs_match = re.search(r'Observações:?\s*([^\n]+)', text, re.IGNORECASE)
        if obs_match:
            data['observacoes'] = obs_match.group(1).strip()
        
        return data