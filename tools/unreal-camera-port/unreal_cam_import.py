# unreal_cam_import.py — 在 Unreal Editor 執行(B7 管線第 2 步)
#
# 讀 blender_cam_export.py 匯出的 cam_unreal.json,在關卡裡生成一顆
# CineCameraActor:filmback / focal 完全照抄 Blender 數值 → 視野逐像素相同,
# 位置 / 旋轉套用轉換後的世界位姿。
#
# 執行方式(擇一):
#   A. Output Log 下方 Cmd 切成 Python,貼上整段執行
#   B. Cmd 輸入: py "D:/path/to/unreal_cam_import.py"
# 前置:Edit → Plugins → 啟用 Python Editor Script Plugin

import json
import unreal

JSON_PATH = r"C:/CHANGE/ME/cam_unreal.json"   # ← 改成 Blender 匯出的 json 路徑

with open(JSON_PATH) as fh:
    d = json.load(fh)

loc = unreal.Vector(*d["location_cm"])
r = d["rotator_deg"]
rot = unreal.Rotator(roll=r["roll"], pitch=r["pitch"], yaw=r["yaw"])

try:    # UE5
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cam = actor_sub.spawn_actor_from_class(unreal.CineCameraActor, loc, rot)
except Exception:  # UE4 fallback
    cam = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, loc, rot)

cam.set_actor_label(d.get("name", "CAM1_GAME"))
cc = cam.camera_component

fb = unreal.CameraFilmbackSettings(
    sensor_width=d["sensor_mm"]["width"],
    sensor_height=d["sensor_mm"]["height"])
cc.set_editor_property("filmback", fb)
cc.set_editor_property("current_focal_length", d["focal_mm"])
cc.set_editor_property("current_aperture", 22.0)      # 光圈縮到最小,弱化景深

fs = cc.get_editor_property("focus_settings")
fs.focus_method = unreal.CameraFocusMethod.DISABLE    # 關景深 → 全畫面銳利
cc.set_editor_property("focus_settings", fs)

print(f"OK: {cam.get_actor_label()}  loc={d['location_cm']}  rot={r}")
print(f"filmback {d['sensor_mm']['width']} x {d['sensor_mm']['height']} mm, "
      f"focal {d['focal_mm']} mm")
print(f"驗算:UE 相機細節面板顯示的 Current FOV(水平)應 ≈ "
      f"{d['fov_deg']['horizontal']}°")
