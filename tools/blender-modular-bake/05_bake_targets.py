# B14 步驟 5 — 依表面積計算解析度 + 建專屬 BAKE_ 材質與空白圖(對話中的「腳本 10」)
# 用法:不用選取,自動處理所有 _J → Run → Window > Toggle System Console 看表
# 判讀:「實際 px/m」各模組差 2 倍以內即可;出現「⚠ 已達上限」就把 DENSITY 調低讓全部一起降
# 可重跑:已建好的材質會沿用,貼圖尺寸不同時自動換新
import bpy, math

GREY      = "GREY_TEST"
DENSITY   = 16      # 每公尺幾個像素;實戰定案 16(32 時大模組全卡 4096 上限,清晰度差 2.75 倍)
PACK      = 0.6     # Smart UV 大約只用掉 60% 空間,預留給空隙
MIN_RES   = 512
MAX_RES   = 4096

grey = bpy.data.materials[GREY]

def to_pow2(n):
    return int(2 ** round(math.log2(max(n, 1))))

rows = []
for ob in [o for o in bpy.context.view_layer.objects
           if o.type == 'MESH' and o.name.endswith("_J")]:

    # 1. 量表面積(平方公尺,含物件縮放)
    s = ob.matrix_world.to_scale()
    k = abs(s.x * s.y * s.z) ** (2 / 3)
    area = sum(p.area for p in ob.data.polygons) * k

    # 2. 換算解析度
    raw = math.sqrt(area / PACK) * DENSITY
    res = min(MAX_RES, max(MIN_RES, to_pow2(raw)))

    # 3. 專屬材質(GREY_TEST 的複本)— 共用一顆會全部 bake 到同一張圖互相覆蓋
    name = "BAKE_" + ob.name
    mat = bpy.data.materials.get(name) or grey.copy()
    mat.name = name
    ob.data.materials.clear()
    ob.data.materials.append(mat)

    # 4. 專屬空白 bake 圖(32-bit float),放進材質並設為選中 = bake 目標
    img = bpy.data.images.get(name)
    if img and img.size[0] != res:
        bpy.data.images.remove(img)
        img = None
    img = img or bpy.data.images.new(name, res, res, alpha=False, float_buffer=True)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    tex = next((n for n in nodes if n.type == 'TEX_IMAGE' and n.image == img), None)
    if not tex:
        tex = nodes.new('ShaderNodeTexImage')
        tex.image = img
        tex.location = (-600, 400)
    for n in nodes:
        n.select = False
    tex.select = True
    nodes.active = tex

    real = math.sqrt(PACK / area) * res if area else 0
    rows.append((ob.name, area, res, real))

print(f"\n{'模組':<28}{'面積 m²':>10}{'解析度':>8}{'實際 px/m':>11}")
for n, a, r, d in sorted(rows, key=lambda x: -x[1]):
    flag = "  ⚠ 已達上限,密度偏低" if r == MAX_RES and d < DENSITY * 0.7 else ""
    print(f"{n:<28}{a:>10.0f}{r:>8}{d:>11.1f}{flag}")
print("完成")
