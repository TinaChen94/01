# B14 步驟 4 — 雙階段法線反面自動修復(對話中的「Q13 第 4 版」)
# 用法:Layout 分頁的透視視窗用 Walk(Shift+`)站到紅色區域前、左鍵停住
#       → 切到 Scripting → Run → 回 Layout 看紅色是否消失;其他區域走過去再跑一次
# 先看 Console 第一行:確認抓到的是「透視視窗」且尺寸是大的那個,不對就先停。
# 第一段(整塊):每個相連零件先統一方向,再用「場景燈 + 視角」投票決定整塊要不要翻
# 第二段(逐面):從眼睛對每個面發 raycast,看得到但背對眼睛的面就翻正
import bpy, bmesh
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

SCREEN = "Layout"
SAMPLES, N_PROBES, MIN_DIST, MAX_DIST, VIEW_DIST = 16, 12, 0.8, 60.0, 80.0

# ---------- 找出正確的視角:透視模式、面積最大的 3D 視窗 ----------
def find_view():
    screens = [bpy.data.screens.get(SCREEN)] + list(bpy.data.screens)
    for scr in [s for s in screens if s]:
        cands = [a for a in scr.areas if a.type == 'VIEW_3D'
                 and a.spaces.active.region_3d.view_perspective in {'PERSP', 'CAMERA'}]
        if cands:
            a = max(cands, key=lambda x: x.width * x.height)
            vm = a.spaces.active.region_3d.view_matrix.inverted()
            return scr.name, a, vm.translation.copy(), -vm.to_3x3().col[2].normalized()
    raise RuntimeError("找不到透視模式的 3D 視窗")

scr_name, area, eye, fwd = find_view()
print(f"使用「{scr_name}」的透視視窗 {area.width}x{area.height},"
      f"位置 {tuple(round(x, 1) for x in eye)}")

vl = bpy.context.view_layer
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
targets = [o for o in vl.objects if o.type == 'MESH' and o.name.endswith("_J")]

probes = [o.matrix_world.translation.copy() for o in vl.objects
          if o.type == 'LIGHT' and o.data.type != 'SUN' and o.visible_get()]
probes.append(eye)
kd = KDTree(len(probes))
for i, p in enumerate(probes):
    kd.insert(p, i)
kd.balance()

def build_bvh():
    verts, polys, off = [], [], []
    for ob in targets:
        mw, base = ob.matrix_world, len(verts)
        off.append(len(polys))
        verts.extend(mw @ v.co for v in ob.data.vertices)
        polys.extend([base + i for i in p.vertices] for p in ob.data.polygons)
    return BVHTree.FromPolygons(verts, polys), off

print("建立遮擋資料...")
bvh, face_off = build_bvh()
orig = {ob.name: [p.normal.copy() for p in ob.data.polygons] for ob in targets}

# ---------- 第一段:整塊零件統一方向 + 燈光/視角投票 ----------
print("第一段:整塊修正...")
for oi, ob in enumerate(targets):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    mw = ob.matrix_world
    nm = mw.to_3x3().inverted_safe().transposed()
    visited = bytearray(len(bm.faces))
    for f0 in bm.faces:
        if visited[f0.index]:
            continue
        island, stack = [f0], [f0]
        visited[f0.index] = 1
        while stack:
            for e in stack.pop().edges:
                for lf in e.link_faces:
                    if not visited[lf.index]:
                        visited[lf.index] = 1
                        island.append(lf); stack.append(lf)
        before = [f.normal.copy() for f in island]
        bmesh.ops.recalc_face_normals(bm, faces=island)
        changed = [f for f, n0 in zip(island, before) if f.normal.dot(n0) < 0]
        good = bad = 0.0
        for f in sorted(island, key=lambda x: x.calc_area(), reverse=True)[:SAMPLES]:
            c, n, a = mw @ f.calc_center_median(), (nm @ f.normal).normalized(), f.calc_area()
            g = face_off[oi] + f.index
            for p, _, d in kd.find_n(c, N_PROBES):
                if MIN_DIST <= d <= MAX_DIST and bvh.ray_cast(p, (c - p) / d, d + 1e-3)[2] == g:
                    if n.dot(p - c) > 0: good += a
                    else:                bad  += a
        if good == 0 and bad == 0:
            if changed:
                bmesh.ops.reverse_faces(bm, faces=changed)
        elif bad > good:
            bmesh.ops.reverse_faces(bm, faces=island)
    bm.to_mesh(ob.data); ob.data.update(); bm.free()

# ---------- 第二段:從視角逐面修正看得到的反面 ----------
print("第二段:逐面修正...")
for oi, ob in enumerate(targets):
    mw = ob.matrix_world
    nm = mw.to_3x3().inverted_safe().transposed()
    flip_idx = []
    for p in ob.data.polygons:
        v = mw @ p.center - eye
        d = v.length
        if d < 0.05 or d > VIEW_DIST or v.dot(fwd) <= 0:
            continue
        if bvh.ray_cast(eye, v / d, d + 1e-3)[2] != face_off[oi] + p.index:
            continue
        if (nm @ p.normal).dot(v) > 0:
            flip_idx.append(p.index)
    if flip_idx:
        bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
        bmesh.ops.reverse_faces(bm, faces=[bm.faces[i] for i in flip_idx])
        bm.to_mesh(ob.data); ob.data.update(); bm.free()

# ---------- 報告 ----------
print("\n=== 結果(和執行前相比)===")
for ob in targets:
    n = sum(1 for p, n0 in zip(ob.data.polygons, orig[ob.name]) if p.normal.dot(n0) < 0)
    if n:
        print(f"{ob.name:<24} 翻轉 {n} 個面")
print("完成")
