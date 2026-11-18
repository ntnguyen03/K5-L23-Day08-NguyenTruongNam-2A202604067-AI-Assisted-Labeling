$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot/..
python scripts/sam2_points.py --image img_004.jpg --pos "380,385" --pos "350,260" --neg "480,320" --sam sam2.1_b.pt --device cpu --out submission/masks --name tuk_green_img004
if ($LASTEXITCODE -ne 0) { throw "SAM failed" }
python scripts/sam2_points.py --image img_013.jpg --pos "700,290" --pos "760,440" --neg "820,400" --sam sam2.1_b.pt --device cpu --out submission/masks --name driver_img013
if ($LASTEXITCODE -ne 0) { throw "SAM failed" }
python scripts/sam2_points.py --image img_004.jpg --pos "890,320" --pos "900,450" --neg "810,390" --sam sam2.1_b.pt --device cpu --out submission/masks --name person_img004
if ($LASTEXITCODE -ne 0) { throw "SAM failed" }
Get-ChildItem submission/masks/*.jpg