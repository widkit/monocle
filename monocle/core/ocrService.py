import pytesseract
from pytesseract import Output
from PIL import Image, ImageEnhance, ImageFilter
from ..utils import imageUtils

def imgToBoxData(image_path, min_confidence=30):
    """
    Enhanced OCR function with multiple detection strategies
    """
    try:
        img_pil = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error reading '{image_path}': File not found")
        return []
    except Exception as e:
        print(f"Error opening image '{image_path}': {e}")
        return []

    # Try multiple OCR strategies
    word_data_list = []
    
    # Strategy 1: Standard OCR with enhanced configuration
    word_data_list.extend(ocrConf(img_pil, min_confidence, "standard"))
    
    # Strategy 2: OCR with image preprocessing (enhance contrast)
    enhanced_img = preprocessImg(img_pil)
    word_data_list.extend(ocrConf(enhanced_img, min_confidence, "enhanced"))
    
    # Strategy 3: OCR with different PSM modes for different text layouts
    word_data_list.extend(ocrPSM(img_pil, min_confidence))
    
    # Remove duplicates and merge overlapping boxes
    return mergeDuplicateBoxes(word_data_list)

def preprocessImg(img):
    """Preprocess image to improve OCR accuracy"""
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    
    # Apply slight blur to reduce noise
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img

def ocrConf(img, min_confidence, strategy_name):
    """Run OCR with specific configuration"""
    try:
        if strategy_name == "standard":
            config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?@#$%&*()_+-=[]{}|;:\\"<>/\\\\ '
        elif strategy_name == "enhanced":
            config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?@#$%&*()_+-=[]{}|;:\\"<>/\\\\ '
        else:
            config = '--oem 3 --psm 6'
            
        data = pytesseract.image_to_data(img, output_type=Output.DICT, config=config)
        return extractWord(data, min_confidence)
        
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        print("Please install Tesseract OCR engine and/or set 'pytesseract.pytesseract.tesseract_cmd'.")
        return []
    except Exception as e:
        print(f"Error during Tesseract OCR ({strategy_name}): {e}")
        return []

def ocrPSM(img, min_confidence):
    """Try different PSM modes for better text detection"""
    word_data_list = []
    psm_modes = [3, 4, 6, 8, 11, 12]  # Different page segmentation modes
    
    for psm in psm_modes:
        try:
            config = f'--oem 3 --psm {psm}'
            data = pytesseract.image_to_data(img, output_type=Output.DICT, config=config)
            word_data_list.extend(extractWord(data, min_confidence))
        except Exception as e:
            print(f"Error with PSM mode {psm}: {e}")
            continue
    
    return word_data_list

def extractWord(data, min_confidence):
    """Extract word data from OCR results"""
    word_data_list = []
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        # Filter for word-level entries (level 5) and check confidence
        if int(data['level'][i]) == 5:
            confidence = float(data['conf'][i])
            word = data['text'][i].strip()

            # Only include words that meet the minimum confidence and are not empty
            if confidence > min_confidence and word and len(word) > 0:
                word_data_list.append({
                    'word': word,
                    'left': int(data['left'][i]),
                    'top': int(data['top'][i]),
                    'width': int(data['width'][i]),
                    'height': int(data['height'][i]),
                    'confidence': confidence
                })
    
    return word_data_list

def mergeDuplicateBoxes(word_data_list):
    """Merge overlapping or duplicate text boxes"""
    if not word_data_list:
        return []
    
    # Sort by confidence (higher first)
    word_data_list.sort(key=lambda x: x['confidence'], reverse=True)
    
    merged_list = []
    used_positions = set()
    
    for item in word_data_list:
        # Create a position key for this box
        pos_key = (item['left'], item['top'], item['width'], item['height'])
        
        # Check if this position overlaps significantly with any existing box
        is_duplicate = False
        for used_pos in used_positions:
            if boxOverlap(pos_key, used_pos):
                is_duplicate = True
                break
        
        if not is_duplicate:
            merged_list.append(item)
            used_positions.add(pos_key)
    
    return merged_list

def boxOverlap(box1, box2, threshold=0.7):
    """Check if two boxes overlap significantly"""
    left1, top1, width1, height1 = box1
    left2, top2, width2, height2 = box2
    
    # Calculate intersection
    x_overlap = max(0, min(left1 + width1, left2 + width2) - max(left1, left2))
    y_overlap = max(0, min(top1 + height1, top2 + height2) - max(top1, top2))
    
    intersection = x_overlap * y_overlap
    
    # Calculate areas
    area1 = width1 * height1
    area2 = width2 * height2
    
    # Check if overlap exceeds threshold
    if area1 > 0 and area2 > 0:
        overlap_ratio = intersection / min(area1, area2)
        return overlap_ratio > threshold
    
    return False