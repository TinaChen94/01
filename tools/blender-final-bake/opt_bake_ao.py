# C2 選用 — 腳本 C:bake AO(分批)(對話 Q2103;本案最後未採用,留作參考)
# 純幾何遮蔽、與燈光無關,bake 一次即可;圖存 bake_final/AO_<模組>.exr。AO_DIST:0.3~0.5 只壓縫隙 / 1.0 建議 / 2+ 偏暗

import bpy, os

COLLECTION    = "TINA_HIGH"
UV_NAME       = "BakeUV"
SAMPLES       = 128
AO_DIST       = 1.0      # AO 範圍(公尺):0.5 = 只壓縫隙;1~2 = 角落也壓暗
ONLY_SELECTED = False    # True = 只 bake 選取的模組
BATCH         = 3
REDO          = False
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

selected = set(bpy.context.selected_objects)
ctx = view3d_ctx()
with bpy.context.temp_override(**ctx):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

objs = []
for ob in sorted(bpy.data.collections[COLLECTION].all_objects, key=lambda o: o.name):
    if ob.type != 'MESH' or not ob.visible_get():
        continue
    if REDO:
        ob.pop("ao_baked", None)
    if UV_NAME not in ob.data.uv_layers or "bake_res" not in ob:
        print(f"⚠ 跳過 {ob.name}:請先執行檢查腳本"); continue
    for s in ob.material_slots:
        s.link = 'DATA'                       # 若在 VIEW/COMBINED 模式,先切回原材質
    if not ob.material_slots or any(s.material is None for s in ob.material_slots):
        print(f"⚠ 跳過 {ob.name}:有空的材質欄位")
    else:
        objs.append(ob)

todo = [o for o in objs if o in selected] if ONLY_SELECTED \
       else [o for o in objs if not o.get("ao_baked")][:BATCH]
if not todo:
    print("沒有要 bake 的模組")

scene.render.engine = 'CYCLES'
scene.cycles.samples = SAMPLES
scene.cycles.bake_type = 'AO'
if scene.world:
    scene.world.light_settings.distance = AO_DIST
b = scene.render.bake
b.margin, b.use_clear, b.target = 16, True, 'IMAGE_TEXTURES'
b.use_selected_to_active = False

mats = {s.material for ob in todo for s in ob.material_slots}
prev_active = {}
for m in mats:
    m.use_nodes = True
    N = m.node_tree.nodes
    prev_active[m] = N.active
    n = N.get(NODE_NAME) or N.new('ShaderNodeTexImage')
    n.name, n.label, n.location = NODE_NAME, "BAKE(暫時)", (-1400, 0)

for ob in todo:
    res, name = int(ob["bake_res"]), "AO_" + ob.name
    ob.data.uv_layers.active = ob.data.uv_layers[UV_NAME]
    img = bpy.data.images.get(name)
    if img:
        bpy.data.images.remove(img)
    img = bpy.data.images.new(name, res, res, alpha=False, float_buffer=True)
    for s in ob.material_slots:
        N = s.material.node_tree.nodes
        N[NODE_NAME].image = img
        N.active = N[NODE_NAME]
    print(f"AO {ob.name}({res}px)...", flush=True)
    try:
        with bpy.context.temp_override(**ctx):
            bpy.ops.object.select_all(action='DESELECT')
            ob.select_set(True); vl.objects.active = ob
            bpy.ops.object.bake(type='AO')
        img.filepath_raw = os.path.join(folder, name + ".exr")
        img.file_format = 'OPEN_EXR'
        img.save()
        img.buffers_free()
        ob["ao_baked"] = True
        bpy.ops.wm.save_mainfile()
        print(f"✔ {ob.name} 完成", flush=True)
    except Exception as e:
        print(f"✘ {ob.name}:{e}", flush=True)

for m in mats:
    N = m.node_tree.nodes
    n = N.get(NODE_NAME)
    if n: N.remove(n)
    if prev_active[m] is not None:
        try: N.active = prev_active[m]
        except Exception: pass

bpy.ops.wm.save_mainfile()
left = [o.name for o in objs if not o.get("ao_baked")]
print(f"\nAO 已完成 {len(objs) - len(left)}/{len(objs)},還剩 {len(left)} 個")
