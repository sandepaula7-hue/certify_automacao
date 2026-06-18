from PIL import Image, ImageDraw, ImageFont
import os

def criar_documento_teste():
    """Cria um documento de teste com dados fictícios"""
    
    # Criar imagem branca
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Tentar usar fonte Arial, ou fallback
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # Título
    draw.text((50, 30), "DOCUMENTO DE CADASTRO", fill='black', font=font_title)
    draw.line([(50, 70), (750, 70)], fill='black', width=2)
    
    # Dados fictícios
    dados = [
        ("Nome Completo:", "João Silva Santos"),
        ("CPF:", "123.456.789-00"),
        ("Data Nascimento:", "15/03/1985"),
        ("Endereço:", "Rua das Flores, 123 - São Paulo/SP"),
        ("Telefone:", "(11) 98765-4321"),
        ("E-mail:", "joao.silva@email.com"),
        ("Observações:", "Cliente desde 2020")
    ]
    
    y_pos = 120
    for label, valor in dados:
        draw.text((50, y_pos), f"{label} {valor}", fill='black', font=font_text)
        y_pos += 40
    
    # Rodapé
    draw.line([(50, 550), (750, 550)], fill='gray', width=1)
    draw.text((50, 560), "Documento gerado para teste de OCR", fill='gray', font=font_text)
    
    # Salvar
    output_path = "documento_exemplo.jpg"
    img.save(output_path)
    print(f"✅ Documento de teste criado: {output_path}")
    return output_path

if __name__ == "__main__":
    criar_documento_teste()