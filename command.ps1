# > .\commnad.ps1 movie\xxx.mp4

Param($movie) #�����œ���p�X���擾
$moviename = [System.IO.Path]::GetFileNameWithoutExtension($movie) #�f���f�[�^�̃t�@�C�������擾
New-Item output/$moviename -ItemType Directory -Force #�V�[�����o�p�t�H���_�̍쐬

#�V�[�����o�̉摜�ƕ����f�[�^���o��
#default��臒l��0.5�Ƃ��Ă���B0~1�͈̔͂Őݒ肪�\��1�ɋ߂Â��قǏ�ʓ]���̌��o�������Ȃ�
ffmpeg -i $movie -vf "select=gt(scene\,0.5), scale=1280:720,showinfo" -vsync vfr output/$moviename/%04d.jpg -f null - 2>output/ffout.txt 

#������(positive_data�ɋ߂��摜)�̎���
python get_gamestart_img.py output/$moviename

#ffout�̕����R�[�h��UTF-16����UTF8�ɕϊ�
(get-content -Encoding UTF8 output/ffout.txt) | Set-Content -Encoding UTF8 output/$moviename/ffout.txt
Remove-Item output/ffout.txt

#���Ƃ�(./output/$moviename/)�ɂ���ړI�ȊO�̉摜���폜����
Write-Host "�V�[�����o���I�����܂����B ./output/$moviename/ �̒��ɂ���s�v�ȉ摜�͍폜���Ă�������"
Write-Host "�摜�̍폜���I�����A����̐؂蔲��������ꍇ��[y]�������Ă��������B�I������ꍇ��[n]�������Ă�������"
$usercheck = Read-Host "[y/n]"

$cnt = 0 #�������[�v���
while($cnt -le 10){
    if($usercheck -eq "y"){
        python get_scene_movie.py $movie
        exit
    }
    if($usercheck -eq "n"){
        Write-Host "�����I��"
        exit
    }
    $cnt++
    Write-Host "�摜�̍폜���I�����A����̐؂蔲��������ꍇ��[y]�������Ă��������B�I������ꍇ��[n]�������Ă�������"
    $usercheck = Read-Host "[y\n]"
}

#���ʂɎg�p�����摜��ffuot�t�@�C�����폜
Remove-Item -Path output/$moviename -Recurse -Force