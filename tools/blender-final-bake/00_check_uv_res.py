# C2 步驟 0 — 檢查腳本 v3(分批):建 BakeUV + 重排 UV + 依實際 UV 用量算解析度(對話 Q1905/Q1906)
# 用法:另存副本 → Run → 看「還剩 N 個」→ 一直 Alt+P 到「全部完成!」;當掉就重開再跑(自動降級 CONCAVE→CONVEX→不重排)
# 結果寫入 ob["bake_res"],給 01/02 bake 腳本用。改 DENSITY / MAX_RES 後重跑只重算解析度(幾秒)。

import bpy, math, statistics
import numpy as np

COLLECTION = "TINA_HIGH"
UV_NAME    = "BakeUV"
DENSITY    = 16
MIN_RES, MAX_RES = 512, 8192   # 實戰定案 8192(4096 時 TURN 只有 7.3 px/m);記憶體 32GB 以下可改 6144
BATCH      = 2          # 每次執行處理幾個模組;還是會當就改成 1
MARGIN     = 0.003
REDO       = False      # True = 清掉進度,全部重做

vl = bpy.context.view_layer
SHAPES = ['CONCAVE', 'CONVEX', None]     # 當掉一次就降一級;None = 不重排

def view3d_ctx():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                region = next(r for r in area.regions if r.type == 'WINDOW')
                return dict(window=win, area=area, region=region)
    raise RuntimeError("找不到 3D 視窗")

ctx = view3d_ctx()
with bpy.context.temp_override(**ctx):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

objs = sorted([o for o in bpy.data.collections[COLLECTION].all_objects
               if o.type == 'MESH' and o.visible_get()], key=lambda o: o.name)
if REDO:
    for o in objs:
        o.pop("uv_done", None); o.pop("uv_try", None)

# ---------- 處理這一批 ----------
todo = [o for o in objs if not o.get("uv_done")]
for ob in todo[:BATCH]:
    tries = int(ob.get("uv_try", 0))
    shape = SHAPES[min(tries, 2)]
    ob["uv_try"] = tries + 1
    bpy.ops.wm.save_mainfile()          # 先存檔:萬一當掉,下次會自動降級
    print(f"處理 {ob.name}(排列方式:{shape or '不重排'})...", flush=True)

    me = ob.data
    uv = me.uv_layers.get(UV_NAME) or me.uv_layers.new(name=UV_NAME)
    me.uv_layers.active = uv            # 相機圖示(算圖 UV)不動
    with bpy.context.temp_override(**ctx):
        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True); vl.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=MARGIN)
        if shape:
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.pack_islands(rotate=True, rotate_method='ANY',
                                    margin_method='FRACTION', margin=MARGIN,
                                    shape_method=shape)
        bpy.ops.object.mode_set(mode='OBJECT')

    for o in objs:                      # 共用同一份網格的物件一起標記完成
        if o.data == me:
            o["uv_done"] = True
            o.pop("uv_try", None)
    bpy.ops.wm.save_mainfile()
    print(f"✔ 完成 {ob.name},已存檔", flush=True)

# ---------- 報告(只列已完成的) ----------
def uv_area_of(me, uv):
    n = len(me.loops)
    co = np.empty(n * 2); uv.data.foreach_get("uv", co); co = co.reshape(-1, 2)
    P = len(me.polygons)
    st = np.empty(P, dtype=np.int64); me.polygons.foreach_get("loop_start", st)
    tt = np.empty(P, dtype=np.int64); me.polygons.foreach_get("loop_total", tt)
    nxt = np.arange(1, n + 1); nxt[st + tt - 1] = st
    cross = co[:, 0] * co[nxt, 1] - co[nxt, 0] * co[:, 1]
    return float(np.abs(np.add.reduceat(cross, st)).sum() / 2)

rows = []
for ob in objs:
    if not ob.get("uv_done"):
        continue
    me = ob.data
    s = ob.matrix_world.to_scale()
    pa = np.empty(len(me.polygons)); me.polygons.foreach_get("area", pa)
    wa = float(pa.sum()) * abs(s.x * s.y * s.z) ** (2 / 3)
    ua = uv_area_of(me, me.uv_layers[UV_NAME])
    raw = DENSITY * math.sqrt(wa / ua) if ua else MAX_RES
    res = int(min(MAX_RES, max(MIN_RES, round(raw / 256) * 256)))
    ob["bake_res"] = res
    rows.append((ob.name, wa, ua, res, res * math.sqrt(ua / wa) if wa else 0))

left = [o.name for o in objs if not o.get("uv_done")]
if rows:
    med = statistics.median(r[4] for r in rows)
    print(f"\n已完成 {len(rows)}/{len(objs)},中位數 {med:.1f} px/m")
    print(f"{'模組':<24}{'面積m²':>9}{'UV用量':>8}{'解析度':>8}{'px/m':>8}  備註")
    for name, wa, ua, res, pm in rows:
        notes = []
        if pm < med / 1.3 or pm > med * 1.3: notes.append("⚠ 密度差異大")
        if ua > 1.0:   notes.append("⚠ UV 超出或重疊")
        elif ua < 0.3: notes.append("⚠ UV 用量偏低")
        if res == MAX_RES and pm < DENSITY * 0.8: notes.append(f"⚠ 已達 {MAX_RES} 上限")
        print(f"{name:<24}{wa:>9.0f}{ua*100:>7.0f}%{res:>8}{pm:>8.1f}  {' '.join(notes)}")
bpy.ops.wm.save_mainfile()
print(f"\n還剩 {len(left)} 個 → {'再執行一次' if left else '全部完成!'}")
