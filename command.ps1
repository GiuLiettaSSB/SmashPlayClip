# > .\commnad.ps1 movie\xxx.mp4

Param($movie) #引数で動画パスを取得
$moviename = [System.IO.Path]::GetFileNameWithoutExtension($movie) #映像データのファイル名を取得
New-Item output/$moviename -ItemType Directory -Force #シーン検出用フォルダの作成

#シーン検出の画像と文字データを出力
#defaultの閾値は0.5としている。0~1の範囲で設定が可能で1に近づくほど場面転換の検出が多くなる
ffmpeg -i $movie -vf "select=gt(scene\,0.5), scale=1280:720,showinfo" -vsync vfr output/$moviename/%04d.jpg -f null - 2>output/ffout.txt 

#特定場面(positive_dataに近い画像)の識別
python get_gamestart_img.py output/$moviename

#ffoutの文字コードをUTF-16からUTF8に変換
(get-content -Encoding UTF8 output/ffout.txt) | Set-Content -Encoding UTF8 output/$moviename/ffout.txt
Remove-Item output/ffout.txt

#手作業で(./output/$moviename/)にある目的以外の画像を削除する
Write-Host "シーン検出が終了しました。 ./output/$moviename/ の中にある不要な画像は削除してください"
Write-Host "画像の削除が終了し、動画の切り抜きをする場合は[y]を押してください。終了する場合は[n]を押してください"
$usercheck = Read-Host "[y/n]"

$cnt = 0 #無限ループ回避
while($cnt -le 10){
    if($usercheck -eq "y"){
        python get_scene_movie.py $movie
        exit
    }
    if($usercheck -eq "n"){
        Write-Host "処理終了"
        exit
    }
    $cnt++
    Write-Host "画像の削除が終了し、動画の切り抜きをする場合は[y]を押してください。終了する場合は[n]を押してください"
    $usercheck = Read-Host "[y\n]"
}
