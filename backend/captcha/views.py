import base64
from io import BytesIO
import random
import string
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from comments_spa.settings import CAPTCHA_TTL, CAPTCHA_LENGTH


def generate_random_string_with_digits(length: int) -> str:
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )


def generate_captcha():
    captcha_text = generate_random_string_with_digits(CAPTCHA_LENGTH)

    width, height = 200, 70
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)

    start_x = 10

    for char in captcha_text:
        angle = random.randint(-30, 30)

        char_image = Image.new("RGBA", (50, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((0, 0), char, font=font, fill=(0, 0, 0))

        char_image = char_image.rotate(angle, expand=1)

        char_image = char_image.convert("RGB")

        image.paste(char_image, (start_x, random.randint(0, 20)))

        start_x += 40  

    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0), width=2)

    for _ in range(100):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        draw.point((x1, y1), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    image = image.filter(ImageFilter.GaussianBlur(1))

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return captcha_text, buffer


class CaptchaAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        captcha_text, image_buffer = generate_captcha()
        image_base64 = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

        captcha_key = f"captcha_for_user.{request.user.id}"

        cache.set(captcha_key, captcha_text, timeout=CAPTCHA_TTL)

        return Response({
            "captcha_image": image_base64,
            "captcha_key": captcha_key,
            "captcha_format": "png"
        })
