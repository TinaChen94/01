# C1 步驟 7 — 一鍵存 EXR + 切換發光預覽 + 存 .blend(對話中的「Q14 存檔與預覽腳本」)
# 用法:Bake 完成後 Run → Viewport 切 Material Preview(第 3 顆球)巡接縫
# 關鍵:用 filepath_raw + save(),Blender 才會記住路徑;
#       舊版用 img.save(filepath=...) 存得到檔但沒記路徑 → 重開變洋紅色(見 08_relink.py)
import bpy, os

folder = bpy.path.abspath("//bake")
os.makedirs(folder, exist_ok=True)
saved = 0
for img in bpy.data.images:
    if img.name.startswith("BAKE_") and img.has_data:
        img.filepath_raw = os.path.join(folder, img.name + ".exr")
        img.file_format = 'OPEN_EXR'
        img.save()
        saved += 1

for mat in bpy.data.materials:
    if not (mat.name.startswith("BAKE_") and mat.use_nodes):
        continue
    N, L = mat.node_tree.nodes, mat.node_tree.links
    out = next((x for x in N if x.type == 'OUTPUT_MATERIAL'), None)
    tex = next((x for x in N if x.type == 'TEX_IMAGE' and x.image
                and x.image.name.startswith("BAKE_")), None)
    if not (out and tex):
        continue
    # 貼圖要讀 BakeUV,不是原本的 UV1
    uv = N.get("BakeUV_node") or N.new('ShaderNodeUVMap')
    uv.name, uv.uv_map, uv.location = "BakeUV_node", "BakeUV", (-850, 400)
    if not tex.inputs['Vector'].links:
        L.new(uv.outputs['UV'], tex.inputs['Vector'])
    em = N.get("BakeView") or N.new('ShaderNodeEmission')
    em.name, em.location = "BakeView", (-250, 550)
    if not em.inputs['Color'].links:
        L.new(tex.outputs['Color'], em.inputs['Color'])
    L.new(em.outputs[0], out.inputs['Surface'])
    N.active = tex   # 保持 bake 目標不變

bpy.ops.wm.save_mainfile()
print(f"已儲存 {saved} 張 bake 圖,切換為顯示 bake 結果,.blend 已存檔")
