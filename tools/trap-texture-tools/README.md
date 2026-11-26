# trap-texture-tools — A13 陷阱道具的程式修圖 / 烘貼圖工具

> 對應案例:[`docs/asset-cases/A13-trap-props-saw-spike.md`](../../docs/asset-cases/A13-trap-props-saw-spike.md)
> 核心分工:**AI 出材質,程式修幾何**(齒數、正圓、對稱、無縫、正交、UV 對位)。

⚠️ 這些是**實戰當下直接用的腳本**,不是通用套件:部分常數(半徑、交界列、畫布邊界、OBJ 路徑)
是針對 A13 那幾張圖量出來的。換新圖時,先照下表「要改的常數」調整,或直接請 Claude 照新圖重量。
依賴:`numpy`、`Pillow`、`scipy`;`bronze_to_silver.py` 另需 `scikit-image`。

| 腳本 | 用途 | 用法 | 要改的常數 |
|---|---|---|---|
| `radial_teeth.py` | 圓鋸齒數重排:挑一顆齒、縮放到 360/N 度、環形複製 N 份(只換外圈齒帶) | `python3 radial_teeth.py src.png 24 <齒編號> out.png [齒帶內半徑]` | 取樣半徑範圍(預設針對 1024 圖) |
| `disc_seam_circle.py` | 去掉盤面水平接縫(用同心紋旋轉樣本覆蓋)+ 把溝線拉成正圓 | `python3 disc_seam_circle.py src.png out.png` | 盤面半徑 190/408、拉圓範圍 200/440 |
| `hub_symmetry.py` | 中心軸 N 重旋轉對稱重建(例:6 螺栓 = 60°) | `python3 hub_symmetry.py src.png out.png 6 <起始角> <半徑>` | — |
| `hub_round_rgba.py` | 中心鐵圈修正圓(擬合圓心 + 徑向平均輪廓重建同心環),保留透明通道 | `python3 hub_round_rgba.py src.png out.png 0.55 <取樣角> <螺栓起始角>` | — |
| `strip_tile_variants.py` | 橫向 tile 變化型:每顆螺栓切成單元、重新排列/翻轉,所有變化型共用接縫可任意互拼 | 直接執行(來源圖與列範圍寫在檔內) | 來源列範圍、螺栓中心座標、單元寬 212.5 |
| `ortho_guide_from_obj.py` | 從 OBJ 算出「真正正交」的形狀底稿(可轉 22.5° 讓一面正對鏡頭) | 直接執行(讀 `in/TrapB.obj`) | OBJ 路徑、旋轉角、畫布上下界 60/1500 |
| `unroll_faces.py` | 八角柱 4 面展開底稿(每面正對鏡頭並排)+ 對應的烘焙 | `python3 unroll_faces.py guide` / `bake painted.png out.png` | OBJ 路徑、橫向放寬倍率 SXK |
| `bake_front_to_uv.py` | 把「角朝前的正交正面圖」烘進模型自己的 UV:每面取自最近的中間面(無拉扯)、側面跳過 V 字、側面壓暗 | `python3 bake_front_to_uv.py model.obj front.jpg hw.npy out.png 4096` | 交界高度對照表 HM、交界列 J、側面壓暗比例 |
| `obj_preview_render.py` | 軟體算圖:把貼圖套到 OBJ 上出正面/斜角預覽(自動鏡射後半) | `python3 obj_preview_render.py model.obj tex.png out.png <yaw> <pitch>` | — |
| `bronze_to_silver.py` | 古銅 → 銀色:Lab 空間只拿掉古銅色軸,保留環境帶入的藍紫/暖光,並加強暗部藍紫 | `python3 bronze_to_silver.py src.png out.png` | 保留暖光比例 keep、藍紫加強 S |
