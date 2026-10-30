# C2 步驟 3 — 切換檢查:算圖結果(FINAL) ↔ 同事貼圖(對話 Q2108;Blender 文字區塊名:03_切換檢查)
# 用法:Viewport 切 Rendered → 點選模組 → Alt+P 切換,再按一次切回。存檔/匯出前:MODE="RESTORE"、ONLY_SELECTED=False

import bpy, os

COLLECTION    = "TINA_HIGH"
UV_NAME       = "BakeUV"
MODE          = "TOGGLE"   # "TOGGLE" = 切換 / "FINAL" = 顯示算圖結果 / "RESTORE" = 恢復同事貼圖
ONLY_SELECTED = True       # True = 只切換選取的模組 / False = 全部模組

folder = bpy.path.abspath("//bake_final")

def is_final(ob):
    return any(s.link == 'OBJECT' and s.material and s.material.name.startswith("FINALVIEW_")
               for s in ob.material_slots)

def show_coworker(ob):
    for s in ob.material_slots:
        s.link = 'DATA'

def show_final(ob):
    name = "FINAL_" + ob.name
    path = os.path.join(folder, name + ".exr")
    if not os.path.exists(path):
        return False
    img = bpy.data.images.get(name) or bpy.data.images.load(path)
    img.name, img.source, img.filepath = name, 'FILE', path
    img.reload()
    mat = bpy.data.materials.get("FINALVIEW_" + ob.name)
    if not mat:
        mat = bpy.data.materials.new("FINALVIEW_" + ob.name); mat.use_nodes = True
        N, L = mat.node_tree.nodes, mat.node_tree.links
        N.clear()
        out = N.new('ShaderNodeOutputMaterial'); out.location = (300, 0)
        em  = N.new('ShaderNodeEmission');       em.location  = (100, 0)
        tex = N.new('ShaderNodeTexImage');       tex.location = (-200, 0)
        uv  = N.new('ShaderNodeUVMap');          uv.location  = (-450, 0); uv.uv_map = UV_NAME
        L.new(uv.outputs['UV'], tex.inputs['Vector'])
        L.new(tex.outputs['Color'], em.inputs['Color'])
        L.new(em.outputs[0], out.inputs['Surface'])
    next(n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE').image = img
    for s in ob.material_slots:
        s.link = 'OBJECT'
        s.material = mat
    return True

allobjs = [o for o in bpy.data.collections[COLLECTION].all_objects
           if o.type == 'MESH' and o.material_slots]
targets = [o for o in allobjs if o in set(bpy.context.selected_objects)] if ONLY_SELECTED else allobjs
if not targets:
    raise RuntimeError("沒有選到 TINA_HIGH 裡的模組,請先在 Outliner 或畫面上點選")

print()
for ob in sorted(targets, key=lambda o: o.name):
    want_final = MODE == "FINAL" or (MODE == "TOGGLE" and not is_final(ob))
    if want_final:
        if show_final(ob):
            print(f"{ob.name:<24} → 算圖結果(FINAL)")
        else:
            show_coworker(ob)
            print(f"{ob.name:<24} → ⚠ 沒有 FINAL 圖,維持同事貼圖")
    else:
        show_coworker(ob)
        print(f"{ob.name:<24} → 同事的貼圖")
