# C2 步驟 2 — 指定模組快速試算 / 正式算(對話 Q2113;Blender 文字區塊名:02_指定bake_試算)
# QUICK=True:最多 2048px / 64 samples(TURN 約 2~4 分鐘),final_ver 設 0(之後仍會正式重算)
# 滿意後 QUICK=False 正式算(TURN 8192 約 15 分鐘以上)。舊圖自動備份 *_old.exr。

import bpy, os, shutil
from mathutils import Vector

COLLECTION = "TINA_HIGH"
TARGETS    = ["SM_TURN_A_HIGH2"]   # 只算 TURN
QUICK      = True                  # True = 快速試算 / False = 正式算
QUICK_RES, QUICK_SAMPLES = 2048, 64
FULL_SAMPLES = 256
UV_NAME    = "BakeUV"
GLOSSY     = True
EYE_HEIGHT = 1.7
NODE_NAME  = "__BAKE_TARGET__"

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
    return Vector((sum(p.x for p in pts) / 8, sum(p.y for p in pts) / 8,
                   min(p.z for p in pts) + EYE_HEIGHT))

def is_final(ob):
    return any(s.link == 'OBJECT' and s.material and s.material.name.startswith("FINALVIEW_")
               for s in ob.material_slots)

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

# ---------- 找出要 bake 的模組 ----------
allobjs = sorted([o for o in bpy.data.collections[COLLECTION].all_objects
                  if o.type == 'MESH' and o.material_slots], key=lambda o: o.name)
todo = [o for o in allobjs if o.name in TARGETS]
if not todo:
    raise RuntimeError(f"在 {COLLECTION} 裡找不到:{TARGETS}")
bad = [o.name for o in todo if UV_NAME not in o.data.uv_layers or "bake_res" not in o]
if bad:
    raise RuntimeError(f"這些模組還沒跑過檢查腳本:{bad}")

ctx = view3d_ctx()
with bpy.context.temp_override(**ctx):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

was_final = {o for o in allobjs if is_final(o)}
for ob in allobjs:
    for s in ob.material_slots:
        s.link = 'DATA'

# ---------- Bake 設定 ----------
scene.render.engine = 'CYCLES'
scene.cycles.samples = QUICK_SAMPLES if QUICK else FULL_SAMPLES
scene.cycles.bake_type = 'COMBINED'
b = scene.render.bake
b.use_pass_direct = b.use_pass_indirect = True
b.use_pass_diffuse = b.use_pass_transmission = b.use_pass_emit = True
b.use_pass_glossy = GLOSSY
b.view_from = 'ACTIVE_CAMERA'
b.margin, b.use_clear, b.target = (4 if QUICK else 16), True, 'IMAGE_TEXTURES'
b.use_selected_to_active = False

orig_cam = scene.camera
cam_data = bpy.data.cameras.new("__BAKE_CAM__")
cam = bpy.data.objects.new("__BAKE_CAM__", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

mats = {s.material for ob in todo for s in ob.material_slots if s.material}
prev_active = {}
for m in mats:
    m.use_nodes = True
    N = m.node_tree.nodes
    prev_active[m] = N.active
    n = N.get(NODE_NAME) or N.new('ShaderNodeTexImage')
    n.name, n.label, n.location = NODE_NAME, "BAKE(暫時)", (-1400, 0)

done = []
for ob in todo:
    full_res = int(ob["bake_res"])
    res = min(full_res, QUICK_RES) if QUICK else full_res
    name = "FINAL_" + ob.name
    path = os.path.join(folder, name + ".exr")

    # 備份舊圖(只備份一次,不會被之後的試算蓋掉)
    backup = os.path.join(folder, name + "_old.exr")
    if os.path.exists(path) and not os.path.exists(backup):
        shutil.copy2(path, backup)
        print(f"已備份舊圖 → {os.path.basename(backup)}")

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
    print(f"\n{'試算' if QUICK else '正式'} Bake {ob.name}"
          f"({res}px / {scene.cycles.samples} samples,正式版為 {full_res}px)...", flush=True)
    try:
        with bpy.context.temp_override(**ctx):
            bpy.ops.object.select_all(action='DESELECT')
            ob.select_set(True); vl.objects.active = ob
            bpy.ops.object.bake(type='COMBINED')
        img.filepath_raw = path
        img.file_format = 'OPEN_EXR'
        img.save()
        if QUICK:
            ob["final_ver"] = 0      # 試算不算完成,之後仍會重算正式版
        done.append(ob)
        print(f"✔ {ob.name} 完成", flush=True)
    except Exception as e:
        print(f"✘ {ob.name}:{e}", flush=True)

# ---------- 清理 ----------
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

for ob in was_final | set(done):
    show_final(ob)
for o in vl.objects:
    o.select_set(o in done)
if done:
    vl.objects.active = done[0]

bpy.ops.wm.save_mainfile()
print(f"\n完成({'試算' if QUICK else '正式'}),已存檔")
