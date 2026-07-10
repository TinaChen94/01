# blender_cam_export.py — 在 Blender Text Editor 執行(B7 管線第 1 步)
#
# 把場景相機(預設 scene camera,或指定 CAM_NAME)的世界位姿 + 鏡頭參數
# 轉成 Unreal 座標系,寫出 cam_unreal.json(存在 .blend 檔旁邊)並列印。
#
# 踩坑 #4(B6):Unity 匯入相機掛多層父子鏈,N 面板顯示的是局部座標 —
# 本腳本一律讀 matrix_world,rig 幾層都沒差。
#
# 座標轉換:Blender(右手系 Z-up, 公尺) → Unreal(左手系 Z-up, 公分)
#   (x, y, z) → (x, -y, z),位置再 ×100
# 注意:UE 端的模組 mesh 必須走同一條路(Blender 預設 FBX 匯出 → UE 預設匯入,
# 結果正是同一個 Y 鏡像),相機與場景才會對得上。

import bpy
import json
import math

CAM_NAME = ""              # 留空 = 用 scene camera;或填相機物件名稱
OUT_NAME = "cam_unreal.json"

cam = bpy.data.objects.get(CAM_NAME) if CAM_NAME else bpy.context.scene.camera
assert cam and cam.type == 'CAMERA', "找不到相機:填 CAM_NAME 或先設定 scene camera"

scn = bpy.context.scene
rx, ry = scn.render.resolution_x, scn.render.resolution_y
cd = cam.data

# --- sensor 實際生效值(依 Sensor Fit 規則展開成 寬×高,見 B6 相機2 節) ---
if cd.sensor_fit == 'VERTICAL':
    s_h = cd.sensor_height
    s_w = s_h * rx / ry
elif cd.sensor_fit == 'HORIZONTAL':
    s_w = cd.sensor_width
    s_h = s_w * ry / rx
else:  # AUTO:長邊吃 sensor_width
    if rx >= ry:
        s_w = cd.sensor_width
        s_h = s_w * ry / rx
    else:
        s_h = cd.sensor_width
        s_w = s_h * rx / ry

f = cd.lens
hfov = 2 * math.degrees(math.atan(s_w / (2 * f)))
vfov = 2 * math.degrees(math.atan(s_h / (2 * f)))

# --- 世界位姿 → Unreal ---
M = cam.matrix_world
loc = M.translation
fwd = (-M.col[2].xyz).normalized()   # Blender 相機看局部 -Z
up = M.col[1].xyz.normalized()

def to_ue(v):
    return (v.x, -v.y, v.z)

loc_ue = tuple(c * 100.0 for c in to_ue(loc))
f_ue = to_ue(fwd)
u_ue = to_ue(up)

# UE Rotator:yaw/pitch 由 forward 決定;roll = 實際 up 對比「無滾轉 up」的夾角
yaw = math.atan2(f_ue[1], f_ue[0])
pitch = math.atan2(f_ue[2], math.hypot(f_ue[0], f_ue[1]))
u0 = (-math.sin(pitch) * math.cos(yaw),
      -math.sin(pitch) * math.sin(yaw),
      math.cos(pitch))                          # roll=0 時的相機 up
r0 = (u0[1] * f_ue[2] - u0[2] * f_ue[1],
      u0[2] * f_ue[0] - u0[0] * f_ue[2],
      u0[0] * f_ue[1] - u0[1] * f_ue[0])        # cross(u0, fwd) = roll=0 時的 right

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

roll = math.atan2(dot(u_ue, r0), dot(u_ue, u0))

data = {
    "name": cam.name,
    "focal_mm": round(f, 4),
    "sensor_mm": {"width": round(s_w, 4), "height": round(s_h, 4)},
    "fov_deg": {"horizontal": round(hfov, 2), "vertical": round(vfov, 2)},
    "resolution": [rx, ry],
    "location_cm": [round(c, 3) for c in loc_ue],
    "rotator_deg": {"pitch": round(math.degrees(pitch), 4),
                    "yaw": round(math.degrees(yaw), 4),
                    "roll": round(math.degrees(roll), 4)},
    "clip_m": {"near": round(cd.clip_start, 4), "far": round(cd.clip_end, 4)},
}

out = bpy.path.abspath("//" + OUT_NAME)
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)

print(json.dumps(data, indent=2))
print("已寫出:", out)
if abs(data["rotator_deg"]["roll"]) > 0.5:
    print(f"⚠️ 相機帶滾轉 {data['rotator_deg']['roll']:.2f}°(rig 造成),UE 端腳本會照套")
sx, sy, sz = M.to_scale()
if min(sx, sy, sz) < 0:
    print("⚠️ 相機矩陣帶負縮放(鏡像 rig)— forward/up 可能反向,渲出來顛倒就回報")
