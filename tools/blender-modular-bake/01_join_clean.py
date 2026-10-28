# B14 步驟 1 — 模組合併與清理(對話中的「腳本 3 / Q8 v2」)
# 用法:Outliner 選要合併的模組 Root Empty(可 Ctrl 多選)→ Scripting → Run
# 執行前:另存測試檔、Viewport 按 Alt+H 顯示全部(隱藏的零件不會被合併)
import bpy

SUFFIX       = "_J"          # 合併後的名稱後綴
GREY         = "GREY_TEST"   # 合併後順便換成這顆材質;不想換就改成 None
CLEAN_EMPTY  = True          # 刪掉合併後變空的子 Empty(只刪空的,燈光等不會動)

def view3d_ctx():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                region = next(r for r in area.regions if r.type == 'WINDOW')
                return dict(window=win, area=area, region=region)
    raise RuntimeError("找不到 3D Viewport,請確認畫面上有開 3D 視窗")

ctx = view3d_ctx()
vl  = bpy.context.view_layer

with bpy.context.temp_override(**ctx):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

sel   = set(bpy.context.selected_objects)
roots = [o for o in sel if o.parent not in sel]
grey  = bpy.data.materials.get(GREY) if GREY else None

for root in roots:
    family  = [root, *root.children_recursive]
    meshes  = [o for o in family if o.type == 'MESH' and o.visible_get()]
    skipped = [o.name for o in family if o.type == 'MESH' and not o.visible_get()]
    if skipped:
        print(f"⚠ {root.name}:{len(skipped)} 個隱藏網格沒合併:", skipped[:10])
    if not meshes:
        print(f"跳過 {root.name}:底下沒有可見的網格")
        continue

    with bpy.context.temp_override(**ctx):
        bpy.ops.object.select_all(action='DESELECT')
        for o in meshes:
            o.select_set(True)
        vl.objects.active = meshes[0]
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=False, obdata=True)
        bpy.ops.object.convert(target='MESH')      # 套用 modifier,避免合併時遺失
        bpy.ops.object.join()
        joined = vl.objects.active

    # 放回模組 Empty 底下(保持世界位置不變)
    if joined is not root:
        mw = joined.matrix_world.copy()
        joined.parent = root
        joined.matrix_world = mw
        # 放進跟 Empty 同一個 Collection
        for c in list(joined.users_collection):
            c.objects.unlink(joined)
        for c in root.users_collection:
            c.objects.link(joined)

    joined.name = root.name + SUFFIX
    if grey:
        joined.data.materials.clear()
        joined.data.materials.append(grey)

    # 由下往上刪掉已經空掉的子 Empty
    if CLEAN_EMPTY:
        removed = True
        while removed:
            removed = False
            for o in list(root.children_recursive):
                if o.type == 'EMPTY' and not o.children:
                    bpy.data.objects.remove(o)
                    removed = True

    print(f"✔ {joined.name}:合併了 {len(meshes)} 個零件")

print("全部完成")
