// EnvCube 自動匯入設定(Unity Editor 腳本)
// 放到專案的 Assets/Editor/ 資料夾即可生效。
// 規則:檔名含 "envcube" 的貼圖,匯入時自動設成 Cubemap:
//   - 檔名含 "_ball"    → Mirrored Ball (Spheremap)
//   - 其他(含 "_latlong")→ Latitude-Longitude (Cylindrical)
// 同時開 sRGB、勾 Fixup Edge Seams、Max Size 1024。
// 已匯入的舊檔:在 Project 視窗對檔案按右鍵 → Reimport。
using UnityEditor;

public class EnvCubeImporter : AssetPostprocessor
{
    void OnPreprocessTexture()
    {
        string name = System.IO.Path.GetFileNameWithoutExtension(assetPath).ToLowerInvariant();
        if (!name.Contains("envcube")) return;

        var importer = (TextureImporter)assetImporter;
        var s = new TextureImporterSettings();
        importer.ReadTextureSettings(s);

        s.textureShape = TextureImporterShape.TextureCube;
        s.generateCubemap = name.Contains("_ball")
            ? TextureImporterGenerateCubemap.Spheremap
            : TextureImporterGenerateCubemap.Cylindrical;
        s.seamlessCubemap = true;   // Fixup Edge Seams
        s.sRGBTexture = true;

        importer.SetTextureSettings(s);
        importer.maxTextureSize = 1024;
    }
}
