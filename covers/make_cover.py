#!/usr/bin/env python3
"""山海小队讲成语 · 统一封面生成器 v2（3:4 安全区版）
用法: python3 make_cover.py <标题> <集数标签> <关键帧> <输出>
例:   python3 make_cover.py 闻鸡起舞 第一集 ep1_key.jpg cover_ep1.jpg

版式说明（1080x1920）：
- 抖音主页作品网格按 3:4 居中裁剪，即只显示 y=240~1680 区域。
- 所有关键内容（品牌/标题/徽标/主视觉/印章）必须落在安全区内；
  上下两端（0~240，1680~1920）只放装饰（中国结/山水），被裁不心疼。
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1920
INK = (26, 26, 26)
CINNABAR = (176, 58, 46)

CALLI = "/home/hatch/workspace/covers/MaShanZheng-Regular.ttf"
SERIF_TTC = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SEAL_IMG = "/home/hatch/workspace/covers/media-generation-seal-shanhai-xiaodui-0-1f0d7fd5-2959-4236-90db-64cdaa649d0e.jpg"
BG_V5 = "/home/hatch/workspace/covers/cover-template-bg-v5.jpg"

# 安全区（3:4 居中裁剪可见区域）
SAFE_TOP, SAFE_BOTTOM = 240, 1680

def serif(size):
    for idx in range(4):
        try:
            f = ImageFont.truetype(SERIF_TTC, size, index=idx)
            if "SC" in f.getname()[0]:
                return f
        except Exception:
            continue
    return ImageFont.truetype(SERIF_TTC, size)

def draw_tracked(draw, cx, y, text, font, fill, tracking=18):
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + tracking

def rounded_shadow(base, box, radius, blur=18, alpha=90):
    x0, y0, x1, vy1 = box
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    d.rounded_rectangle([x0 - 6, y0 + 10, x1 + 6, vy1 + 16], radius=radius,
                        fill=(40, 30, 20, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh)

def red_mask(img):
    r, g, b = img.split()
    mx = ImageChops.darker(g, b)
    diff = ImageChops.subtract(r, mx)
    alpha = diff.point(lambda v: max(0, min(255, (v - 25) * 3)))
    return alpha.filter(ImageFilter.GaussianBlur(1.2))

def seal_bbox(img, x0, x1, y0, y1):
    px = img.load()
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y][:3]
            if r > 130 and r - b > 55 and r - g > 35:
                xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)

def stamp(base, seal_img, cx, cy, size):
    sx0, sy0, sx1, sy1 = seal_bbox(seal_img, 0, seal_img.width, 0, seal_img.height)
    m = 40
    crop = seal_img.crop((max(0, sx0 - m), max(0, sy0 - m),
                          min(seal_img.width, sx1 + m), min(seal_img.height, sy1 + m)))
    crop = crop.resize((size, size), Image.LANCZOS)
    alpha = red_mask(crop)
    x0, y0 = int(cx - size / 2), int(cy - size / 2)
    region = base.crop((x0, y0, x0 + size, y0 + size)).convert("RGB")
    multiplied = ImageChops.multiply(region, crop)
    stamped = Image.composite(multiplied, region, alpha)
    base.paste(stamped, (x0, y0))

def make_cover(title, ep_label, keyframe_path, out_path):
    bg = Image.open(BG_V5).convert("RGB").resize((W, H), Image.LANCZOS)
    canvas = bg.convert("RGBA")
    d = ImageDraw.Draw(canvas)

    # 顶部品牌（安全区内）
    brand_font = serif(58)
    draw_tracked(d, W / 2, 300, "山海小队讲成语", brand_font, (38, 38, 38), tracking=22)
    d.line([(W / 2 - 120, 382), (W / 2 + 120, 382)], fill=CINNABAR, width=5)

    # 书法大标题
    title_font = ImageFont.truetype(CALLI, 185)
    d.text((W / 2, 600), title, font=title_font, fill=INK, anchor="mm")

    # 集数徽标
    badge_font = serif(52)
    bw, bh = 330, 92
    bx0, by0 = (W - bw) / 2, 730
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=20, fill=CINNABAR)
    d.text((W / 2, by0 + bh / 2), ep_label, font=badge_font,
           fill=(250, 246, 238), anchor="mm")

    # 主视觉：圆角墨框
    vx0, vy0, vx1, vy1 = 90, 900, 990, 1500
    vw, vh = vx1 - vx0, vy1 - vy0
    rounded_shadow(canvas, (vx0, vy0, vx1, vy1), radius=48)
    frame = Image.open(keyframe_path).convert("RGB")
    fw, fh = frame.size
    band = frame.crop((0, int(fh * 0.32), fw, int(fh * 0.685)))
    band = band.resize((vw, vh), Image.LANCZOS)
    mask = Image.new("L", (vw, vh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, vw, vh], radius=48, fill=255)
    canvas.paste(band, (vx0, vy0), mask)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([vx0, vy0, vx1, vy1], radius=48,
                        outline=(46, 42, 38), width=10)

    # 印章：安全区左下
    seal = Image.open(SEAL_IMG).convert("RGB")
    stamp(canvas, seal, 112, 1600, 130)

    rgb = canvas.convert("RGB")
    rgb.save(out_path, quality=92)
    print("saved", out_path)
    # 3:4 上传版（抖音封面规格 1242x1660 即 3:4，上传不再被强制裁剪）
    ch = int(W / 0.75)
    y0 = (H - ch) // 2
    out34 = out_path.rsplit(".", 1)[0] + "_34." + out_path.rsplit(".", 1)[1]
    rgb.crop((0, y0, W, y0 + ch)).save(out34, quality=92)
    print("saved", out34)

if __name__ == "__main__":
    make_cover(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
