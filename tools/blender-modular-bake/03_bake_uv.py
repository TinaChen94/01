# B14 步驟 3 — 新增 Bake 專用 UV2(BakeUV)並展開(對話中的「Q9 腳本 UV2」)
# 用法:不用選取,自動處理所有名稱結尾 _J 的物件 → Run
# 面數高時 Blender 看起來會卡住,是正常的。UV1(相機圖示 = 算圖用)不動。
import bpy, math

UV_NAME = "BakeUV"
MARGIN  = 0.005      # UV 島之間的間距

def view3d_ctx():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                region = next(r for r in area.regions if r.type == 'WINDOW')
                return dict(window=win, area=area, region=region)
    raise RuntimeError("找不到 3D Viewport")

ctx = view3d_ctx()
vl  = bpy.context.view_layer
targets = [o for o in vl.objects if o.type == 'MESH' and o.name.endswith("_J")]

for ob in targets:
    uvs = ob.data.uv_layers
    uv  = uvs.get(UV_NAME) or uvs.new(name=UV_NAME)   # 已有就沿用,不重複新增
    uvs.active = uv                                   # 反白 = bake 用這套
    # 相機圖示(算圖用的 UV)保持在原本第一套,不動

    with bpy.context.temp_override(**ctx):
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True)
        vl.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=MARGIN)
        bpy.ops.object.mode_set(mode='OBJECT')
    print("✔ UV 展開:", ob.name)

print(f"全部完成,共 {len(targets)} 個")
