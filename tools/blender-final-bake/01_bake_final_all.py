# C2 步驟 1 — 正式 bake 全部(Combined + 反光,一次一個)(對話 Q2110,古堡二版打光定案版)
# Blender 文字區塊名:01_正式bake_全部。用法:一直 Alt+P,每次 bake 下一個,到「全部完成!」
# 想全部重 bake:VERSION +1。反光由模組中央眼高 EYE_HEIGHT 的暫時相機(Active Camera)計算,bake 完自動刪除。

import bpy, os
from mathutils import Vector

COLLECTION    = "TINA_HIGH"
UV_NAME       = "BakeUV"
SAMPLES       = 256        # 有雜點就改 512
GLOSSY        = True       # 加入反光(從模組中央的視角計算)
EYE_HEIGHT    = 1.7        # 觀看高度(公尺,從模組最低點算起)
VERSION       = 3          # 想全部重新 bake 時,把這個數字 +1
ONLY_SELECTED = False      # True = 只 bake 選取的模組
PREVIEW       = True       # bake 完自動顯示結果
NODE_NAME     = "__BAKE_TARGET__"

scene, vl = bpy.context.scene, bpy.context.view_layer
folder = bpy.path.abspath("//bake_final")
os.makedirs(folder, exist_ok=True)

def view3d_ctx():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                region = next(r for r in area.regions if r.type == 'WINDOW')
                return dict(window=win, area=area, region=region)
    raise RuntimeError("找不到 3D 視窗")

def eye_point(ob):
    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    cx = sum(p.x for p in pts) / 8
    cy = sum(p.y for p in pts) / 8
    return Vector((cx, cy, min(p.z for p in pts) + EYE_HEIGHT))

selected = set(bpy.context.selected_objects)
ctx = view3d_ctx()
with bpy.context.temp_override(**ctx):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

# ---------- 1. 所有模組先切回同事的材質 ----------
allobjs = sorted([o for o in bpy.data.collections[COLLECTION].all_objects
                  if o.type == 'MESH'], key=lambda o: o.name)
for ob in allobjs:
    for s in ob.material_slots:
        s.link = 'DATA'

objs = []
for ob in allobjs:
    if not ob.visible_get():
        continue
    if UV_NAME not in ob.data.uv_layers or "bake_res" not in ob:
        print(f"⚠ 跳過 {ob.name}:請先執行檢查腳本"); continue
    if not ob.material_slots or any(s.material is None for s in ob.material_slots):
        print(f"⚠ 跳過 {ob.name}:有空的材質欄位"); continue
    objs.append(ob)

todo = [o for o in objs if o in selected] if ONLY_SELECTED \
       else [o for o in objs if o.get("final_ver", 0) < VERSION][:1]

# ---------- 2. Bake ----------
if todo:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = SAMPLES
    scene.cycles.bake_type = 'COMBINED'
    b = scene.render.bake
    b.use_pass_direct = b.use_pass_indirect = True
    b.use_pass_diffuse = b.use_pass_transmission = b.use_pass_emit = True
    b.use_pass_glossy = GLOSSY
    b.view_from = 'ACTIVE_CAMERA'
    b.margin, b.use_clear, b.target = 16, True, 'IMAGE_TEXTURES'
    b.use_selected_to_active = False

    # 暫時相機(bake 完刪除)
    orig_cam = scene.camera
    cam_data = bpy.data.cameras.new("__BAKE_CAM__")
    cam = bpy.data.objects.new("__BAKE_CAM__", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    mats = {s.material for ob in todo for s in ob.material_slots}
    prev_active = {}
    for m in mats:
        m.use_nodes = True
        N = m.node_tree.nodes
        prev_active[m] = N.active
        n = N.get(NODE_NAME) or N.new('ShaderNodeTexImage')
        n.name, n.label, n.location = NODE_NAME, "BAKE(暫時)", (-1400, 0)

    for ob in todo:
        res, name = int(ob["bake_res"]), "FINAL_" + ob.name
        cam.location = eye_point(ob)
        ob.data.uv_layers.active = ob.data.uv_layers[UV_NAME]
        img = bpy.data.images.get(name)
        if img:
            bpy.data.images.remove(img)
        img = bpy.data.images.new(name, res, res, alpha=False, float_buffer=True)
        for s in ob.material_slots:
            N = s.material.node_tree.nodes
            N[NODE_NAME].image = img
            N.active = N[NODE_NAME]
        print(f"\nBake {ob.name}({res}px,反光={'開' if GLOSSY else '關'})...", flush=True)
        try:
            with bpy.context.temp_override(**ctx):
                bpy.ops.object.select_all(action='DESELECT')
                ob.select_set(True); vl.objects.active = ob
                bpy.ops.object.bake(type='COMBINED')
            img.filepath_raw = os.path.join(folder, name + ".exr")
            img.file_format = 'OPEN_EXR'
            img.save()
            ob["final_ver"] = VERSION
            print(f"✔ {ob.name} 完成", flush=True)
        except Exception as e:
            print(f"✘ {ob.name}:{e}", flush=True)

    # 清掉暫時節點與暫時相機
    for m in mats:
        N = m.node_tree.nodes
        n = N.get(NODE_NAME)
        if n:
            N.remove(n)
        if prev_active[m] is not None:
            try: N.active = prev_active[m]
            except Exception: pass
    scene.camera = orig_cam
    bpy.data.objects.remove(cam)
    bpy.data.cameras.remove(cam_data)

# ---------- 3. 預覽:顯示這個版本已完成的 FINAL 圖 ----------
shown = 0
if PREVIEW:
    for ob in objs:
        if ob.get("final_ver", 0) != VERSION:
            continue
        name = "FINAL_" + ob.name
        path = os.path.join(folder, name + ".exr")
        if not os.path.exists(path):
            continue
        img = bpy.data.images.get(name) or bpy.data.images.load(path)
        img.name, img.source, img.filepath = name, 'FILE', path
        img.reload()
        old = bpy.data.materials.get("FINALVIEW_" + ob.name)
        if old:
            bpy.data.materials.remove(old)
        mat = bpy.data.materials.new("FINALVIEW_" + ob.name); mat.use_nodes = True
        N, L = mat.node_tree.nodes, mat.node_tree.links
        N.clear()
        out = N.new('ShaderNodeOutputMaterial'); out.location = (300, 0)
        em  = N.new('ShaderNodeEmission');       em.location  = (100, 0)
        tex = N.new('ShaderNodeTexImage');       tex.location = (-200, 0); tex.image = img
        uv  = N.new('ShaderNodeUVMap');          uv.location  = (-450, 0); uv.uv_map = UV_NAME
        L.new(uv.outputs['UV'], tex.inputs['Vector'])
        L.new(tex.outputs['Color'], em.inputs['Color'])
        L.new(em.outputs[0], out.inputs['Surface'])
        for s in ob.material_slots:
            s.link = 'OBJECT'
            s.material = mat
        shown += 1

bpy.ops.wm.save_mainfile()
left = [o.name for o in objs if o.get("final_ver", 0) < VERSION]
print(f"\n版本 {VERSION}:已完成 {len(objs) - len(left)}/{len(objs)}(畫面顯示 {shown} 個)")
print(f"下一個:{left[0]} → 再按 Alt + P" if left else "全部完成!")
