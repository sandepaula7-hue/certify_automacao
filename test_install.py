# test_install.py
import sys
import easyocr
import cv2
import pyautogui
import numpy as np
from PIL import Image

print("✅ PyAutoGUI:", pyautogui.__version__)
print("✅ OpenCV:", cv2.__version__)
print("✅ Pillow:", Image.__version__)
print("✅ NumPy:", np.__version__)
print("✅ EasyOCR:", easyocr.__version__)

# Teste rápido do EasyOCR
try:
    reader = easyocr.Reader(['pt'], gpu=False)
    print("✅ EasyOCR funcionando!")
except Exception as e:
    print(f"❌ Erro no EasyOCR: {e}")