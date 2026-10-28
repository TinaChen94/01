# B14 步驟 2 — 強制套用中性灰(對話中的「腳本 2 / Q6」:8 顆材質一次換成 1 顆)
# 用法:Viewport 按 Alt+H 顯示全部 → A 全選 → Run
# 01_join_clean.py 已設 GREY 時,合併後已換好,這支可略過。
# GREY_TEST:Base Color #767676(18% 中性灰)、Roughness 0.5;注意名稱是 GREY(E)不是 GRAY(A)
import bpy

grey = bpy.data.materials["GREY_TEST"]
for ob in bpy.context.selected_objects:
    if ob.type == 'MESH':
        ob.data.materials.clear()
        ob.data.materials.append(grey)
print("完成")
