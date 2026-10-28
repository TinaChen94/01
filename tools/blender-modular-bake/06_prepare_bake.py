# C1 步驟 6 — 切回灰材質 + 選取全部 _J(對話中的「Q14 準備腳本」)
# 用法:Run → Console 應顯示「選取 N 個」→ Render 分頁按 Bake
# Bake 設定:Cycles / Render Max Samples 256 / Bake Type Diffuse /
#           Direct ✅ Indirect ✅ Color ❌ / Target Image Textures / Margin 16 px
# 為何要切回灰材質:顯示 bake 結果時材質正在讀那張圖,bake 又要寫同一張 → 報錯
import bpy

vl = bpy.context.view_layer
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

# 切回灰材質(bake 時不能讀取正在寫入的圖)
for mat in bpy.data.materials:
    if not (mat.name.startswith("BAKE_") and mat.use_nodes):
        continue
    N, L = mat.node_tree.nodes, mat.node_tree.links
    em   = N.get("BakeView")
    out  = next((x for x in N if x.type == 'OUTPUT_MATERIAL'), None)
    bsdf = next((x for x in N if x.type == 'BSDF_PRINCIPLED'), None)
    if em:
        for lk in list(em.inputs['Color'].links):
            L.remove(lk)
    if out and bsdf:
        L.new(bsdf.outputs[0], out.inputs['Surface'])
    tex = next((x for x in N if x.type == 'TEX_IMAGE' and x.image
                and x.image.name.startswith("BAKE_")), None)
    if tex:
        N.active = tex

# 選取全部 _J
objs = [o for o in vl.objects if o.type == 'MESH' and o.name.endswith("_J")]
for o in vl.objects:
    o.select_set(o in objs)
vl.objects.active = objs[0]
print(f"已切回灰材質,選取 {len(objs)} 個 → 可以按 Bake 了")
