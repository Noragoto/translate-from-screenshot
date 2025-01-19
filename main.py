from PIL import ImageGrab, ImageFont, Image, ImageDraw
import io
import easyocr
import cv2
import numpy as np
from deep_translator import GoogleTranslator

def get_screenshot_from_clipboard():
    try:
        image = ImageGrab.grabclipboard()

        if image:
            byte_io = io.BytesIO()
            image.save(byte_io, 'PNG')
            byte_io.seek(0)
            return image
        else:
            print("The clipboard does not contain an image")
            return None
    except Exception as e:
        print(f"Error when capturing an image: {e}")
        return None

def add_text_to_image(image, text, position, font_path='arial.ttf', font_size=20, color=(255, 255, 255)):
    # Преобразуем изображение OpenCV в PIL
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Создаем объект для рисования
    draw = ImageDraw.Draw(pil_image)

    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)

    # Добавляем текст
    draw.text(position, text, font=font, fill=color)

    # Преобразуем обратно в формат OpenCV
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return image

def recognize_text(image):
    # Преоьразуем PIL изображение в np.array
    image_np = np.array(image)

    reader = easyocr.Reader(['en'])
    translator = GoogleTranslator(source='en', target='ru')

    result = reader.readtext(image_np)

    for bbox, text, prob in result:
        top_left, top_right, bottom_right, bottom_left = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Переводим текст
        translated_text = translator.translate(text)
        # Рисуем прямоугольник вокруг текста
        image_np = cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)

        # # Добавляем текст
        # cv2.putText(image_np, text, (top_left[0], top_left[1] - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (205, 90, 106), 2)
        # Добавляем перевод
        image_np = add_text_to_image(image_np, translated_text, (bottom_left[0], bottom_left[1] + 10), font_path='arial.ttf', font_size=20, color=(205, 90, 106))

    # Отображаем измененное изображение
    cv2.imshow("Image with text", image_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result


image = get_screenshot_from_clipboard()
if image:
    result = recognize_text(image)