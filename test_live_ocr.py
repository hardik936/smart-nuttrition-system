import requests
from PIL import Image, ImageDraw
import io

img = Image.new('RGB', (800, 600), color='white')
d = ImageDraw.Draw(img)
d.text((10,10), "Nutrition Facts\nCalories 250\nProtein 10g\nCarbohydrate 30g\nFat 5g", fill=(0,0,0))
buf = io.BytesIO()
img.save(buf, format='JPEG')
buf.seek(0)

print('sending request to render...')
r = requests.post('https://smart-nutrition-backend.onrender.com/api/v1/ocr/scan', files={'file': ('test.jpg', buf, 'image/jpeg')})
print(r.status_code, r.text)
