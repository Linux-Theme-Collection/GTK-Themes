#!/bin/bash

if (whereis git | grep / >> /dev/null)
then :
else echo "请安装Git"
exit
fi

echo "安装GTK主题..."
sudo cp -rf themes/ /usr/share/

echo "安装KDE主题"
wget -qO- https://raw.githubusercontent.com/PapirusDevelopmentTeam/arc-kde/master/install-arc-kde-root.sh | sh

echo "复制壁纸..."
sudo cp -rf backgrounds/ /usr/share/backgrounds/

echo "安装图标和鼠标主题..."
wget -qO- https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/install-papirus-root.sh | sh
sudo cp -rf icons/ /usr/share/

echo "复制字体..."
sudo cp -rf fonts/ /usr/share/

echo "enjoy! :)"

