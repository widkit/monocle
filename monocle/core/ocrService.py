import pytesseract
from pytesseract import Output
from PIL import Image
from ..utils import imageUtils

def imgToBoxData(image_path, min_confidence=50):

    try:
        imageUtils.grabScreen(image_path)
    except Exception as e:
        print(f"Error reading image: {e}")

    try:
        img_pil = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error reading '{image_path}': {e}")
        return []
    except Exception as e:
        print(f"Error opening image '{image_path}': {e}")
        return []

    try:
        data = pytesseract.image_to_data(img_pil, output_type=Output.DICT)
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        print("Please install Tesseract OCR engine and/or set 'pytesseract.pytesseract.tesseract_cmd'.")
        return []
    except Exception as e:
        print(f"Error during Tesseract OCR: {e}")
        return []

    word_data_list = []
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        # Filter for word-level entries (level 5) and check confidence
        if int(data['level'][i]) == 5:
            confidence = float(data['conf'][i])
            word = data['text'][i].strip() # Clean whitespace

            # Only include words that meet the minimum confidence and are not empty
            if confidence > min_confidence and word:
                word_data_list.append({
                    'word': word,
                    'left': int(data['left'][i]),
                    'top': int(data['top'][i]),
                    'width': int(data['width'][i]),
                    'height': int(data['height'][i]),
                    'confidence': confidence
                })
    return word_data_list