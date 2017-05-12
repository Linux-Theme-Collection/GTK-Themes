#!/bin/bash

if (ls /etc/ | grep yum > /dev/null 2>&1)
then PM=yum
elif (ls /etc/ | grep apt > /dev/null 2>&1)
then PM=apt
else PM=else
fi

DIR=$(pwd)
USER=$(ls /home/)

echo "复制conky主题..."
mkdir /home/$USER/.conky
cp -rf conky-theme/ /home/$USER/.conky/

echo "复制窗口主题..."
sudo cp -rf themes/ /usr/share/

echo "复制壁纸..."
sudo cp -rf backgrounds/ /usr/share/backgrounds/

echo "复制图标和鼠标主题..."
sudo cp -rf icons/ /usr/share/

echo "复制字体..."
sudo cp -rf fonts/ /usr/share/

echo "复制grub主题"
if  (cat /etc/* | grep yum > /dev/null 2>&1)
then sudo mkdir /boot/grub2/themes/&&sudo cp -rf grub-theme/ /boot/grub2/themes/ ##grub2的主题复制
elif (cat /etc/* | grep apt > /dev/null 2>&1)
then mkdir backup&&sudo mkdir /boot/grub/themes/&&sudo cp -rf grub-theme/ /boot/grub/themes/ ##创建备份目录 grub主题目录 复制grub主题
mv /root/.bashrc $DIR/backup/root-bashrc&&mv /home/$USER/.bashrc $DIR/backup/$USER-bashrc ##备份bashrc
cp bashrc /root/.bashrc&&cp bashrc /home/$USER/.bashrc&&chmod 777 /home/$USER/.bashrc ##替换bashrc文件
sudo apt update&&sudo apt install conky -y ##安装conky
echo -e "\033[31m 如果你发现bash不能正常使用,到backup/目录恢复.bashrc文件 \033[0m"
else
sudo mkdir /boot/grub/themes/&&sudo cp -rf grub-theme/ /boot/grub/themes/ ##大部分Linux都是这个目录
fi

echo "enjoy! :)"

