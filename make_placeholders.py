# 임시 자리표시 이미지 생성 (사용자가 나노 바나나 이미지를 같은 이름으로 덮어쓰면 됨)
from PIL import Image, ImageDraw, ImageFont
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img")
SPECS = {
 "hero.jpg": (800, 1000, "홈 메인\n코치+학생 둥글게 앉은 장면"),
 "nest.jpg": (1200, 675, "둥지학습\n원형 배치 교실"),
 "planner.jpg": (800, 600, "플래너\n체크하는 손"),
 "naesin.jpg": (800, 600, "내신 대비\n교과서·프린트 플랫레이"),
 "mugakneon.jpg": (800, 600, "무학년 수업\n다른 학년 두 학생"),
 "coach.jpg": (800, 600, "코치 상담\n학부모 상담 장면"),
 "about.jpg": (900, 600, "센터 공간\n사람 없는 인테리어"),
 "ai-class.jpg": (1200, 675, "AI학습클래스\n태블릿 학습"),
 "math.jpg": (600, 600, "수학"),
 "english.jpg": (600, 600, "영어"),
 "korean.jpg": (600, 600, "국어"),
 "success.jpg": (800, 600, "성적 향상\n하이파이브"),
 "og.jpg": (1200, 630, "SNS 썸네일"),
}
font = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 30)
small = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 18)
for name, (w, h, label) in SPECS.items():
    p = os.path.join(OUT, name)
    if os.path.exists(p) and os.path.getsize(p) > 60000 or os.path.exists(p[:-4]+".jpg"):  # 실제 이미지가 들어오면 건드리지 않음
        continue
    im = Image.new("RGB", (w, h), (255, 236, 224))
    d = ImageDraw.Draw(im)
    for i in range(0, w + h, 40):
        d.line([(i, 0), (i - h, h)], fill=(255, 220, 200), width=12)
    d.rounded_rectangle([w*0.12, h*0.3, w*0.88, h*0.7], radius=24, fill=(255, 250, 246), outline=(241, 89, 33), width=3)
    d.multiline_text((w/2, h/2 - 12), label, fill=(27, 36, 48), font=font, anchor="mm", align="center", spacing=8)
    d.text((w/2, h*0.7 - 26), f"임시 이미지 · {name} 로 교체", fill=(241, 89, 33), font=small, anchor="mm")
    im.save(p, optimize=True)
    print("placeholder", name)
