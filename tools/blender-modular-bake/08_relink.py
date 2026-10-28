# B14 救援 — 重新連結 bake 圖(畫面洋紅色 = Blender 找不到貼圖)
# 用法:Run → 看 Console:全部 ✔ 就 Ctrl+S;有 ✘ 的表示當時沒存成功,要重 bake
# 換電腦時也用這支:.blend 旁要一起帶 bake/ 資料夾
import bpy, os

folder = bpy.path.abspath("//bake")
ok, miss = [], []

for img in bpy.data.images:
    if not img.name.startswith("BAKE_"):
        continue
    path = os.path.join(folder, img.name + ".exr")
    if os.path.exists(path):
        img.source = 'FILE'
        img.filepath = bpy.path.relpath(path)
        img.reload()
        ok.append(img.name)
    elif img.has_data and img.filepath and os.path.exists(bpy.path.abspath(img.filepath)):
        ok.append(img.name + "(原路徑)")
    else:
        miss.append(img.name)

print(f"\n✔ 已連結 {len(ok)} 張")
for n in ok: print("  ", n)
print(f"✘ 找不到 {len(miss)} 張")
for n in miss: print("  ", n)
print("bake 資料夾:", folder)
