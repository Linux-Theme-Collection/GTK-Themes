#!/bin/bash

# 安装一些工具
install_yaourt(){
    if (grep -i archlinuxcn /etc/pacman.conf > /dev/null);then
        :
    else
        $USER echo "[archlinuxcn]
Server = https://mirrors.ustc.edu.cn/archlinuxcn/\$arch" >> /etc/pacman.conf
    fi
    
    $USER pacman -Syu
    $USER pacman -S archlinuxcn-keyring
    $USER pacman -S yaourt
}

install_layman(){
    $USER emerge layman
    $USER layman -L > /dev/null
}

install_kvantum(){
}

# 获取发行版
get_OS(){
    if (grep -i ubuntu /etc/*release > /dev/null);then
        OS=ubuntu
    elif (grep -i debian /etc/*release > /dev/null);then
        OS=debian
    elif (grep -i arch /etc/*release > /dev/null);then
        OS=arch
        if (whereis yaourt | grep / > /dev/null);then
            :
        else
            install_yaourt
        fi
    elif (grep -i manjaro /etc/*release > /dev/null);then
        OS=manjaro
    elif (grep -i fedora /etc/*release > /dev/null);then
        OS=fedora
    elif (grep -i opensuse /etc/*release > /dev/null);then
        OS=opensuse
    elif (grep -i solus /etc/*release > /dev/null);then
        OS=solus
    elif (grep -i gentoo /etc/*release > /dev/null);then
        OS=gentoo
        if (whereis layman | grep / > /dev/null);then
            :
        else
            install_layman
        fi
    else
        OS=linux
    fi
}

# 安装主题
papirus_icon_theme(){
    case $OS in
        ubuntu) 
                $USER add-apt-repository ppa:papirus/papirus
                $USER apt-get update
                $USER apt-get install papirus-icon-theme
        ;;
        debian) 
                $USER echo "deb http://ppa.launchpad.net/papirus/papirus/ubuntu xenial main" >> /etc/apt/sources.list.d/papirus-ppa.list
                $USER apt-key adv --recv-keys --keyserver keyserver.ubuntu.com E58A9D36647CAE7F
                $USER apt-get update
                $USER apt-get install papirus-icon-theme
        ;;
        arch)
                yaourt -S papirus-icon-theme-git
        ;;
        manjaro)
                $USER pacman -S papirus-icon-theme
        ;;
        fedora)
                $USER wget -q https://copr.fedorainfracloud.org/coprs/dirkdavidis/papirus-icon-theme/repo/fedora-26/dirkdavidis-papirus-icon-theme-fedora-26.repo -P /etc/yum.repos.d/
                $USER yum makecache
                $USER yum update
                $USER yum install papirus-icon-theme
        ;;
        solus)
                $USER eopkg install papirus-icon-theme
        ;;
        gentoo)
                $USER layman -a 4nykey
                $USER layman -S
                $USER echo "=papirus-icon-theme-9999 **" >> /etc/portage/package.accept_keywords
                $USER emerge papirus-icon-theme
        ;;
        *)
                wget -O /tmp/papirus-icon-theme.tar.gz https://github.com/PapirusDevelopmentTeam/papirus-icon-theme/archive/master.tar.gz
                tar -xzf /tmp/papirus-icon-theme.tar.gz -C /tmp
                $USER rm -r /usr/share/icons/*Papirus*
                $USER mv /tmp/papirus-icon-theme-master/*Papirus* /usr/share/icons/
                $USER gtk-update-icon-cache -q /usr/share/icons/*Papirus*
                $USER rm -r /tmp/papirus*
        ;;
    esac
}

paper_icon_theme(){
    case $OS in
        ubuntu)
                $USER add-apt-repository ppa:snwh/pulp
                $USER apt-get update
                $USER apt-get install paper-icon-theme
        ;;
        debian)
                wget -O /tmp/paper-icon.deb https://snwh.org/paper/download.php\?owner=snwh\&ppa=pulp\&pkg=paper-icon-theme,16.04
                $USER dpkg -i /tmp/paper-icon.deb
                $USER apt-get -f install
                rm /tmp/paper-icon.deb
        ;;
        arch)
                yaourt -S paper-icon-theme-git
        ;;
        manjaro)
                yaourt -S paper-icon-theme-git
        ;;
        fedora)
                $USER dnf config-manager --add-repo https://download.opensuse.org/repositories/home:snwh:paper/Fedora_25/home:snwh:paper.repo
                $USER dnf install paper-icon-theme
        ;;
        solus)
                $USER eopkg install paper-icon-theme
        ;;
        gentoo)
                $USER layman -a 4nykey
                $USER layman -S
                $USER echo "=paper-icon-theme-9999 **" >> /etc/portage/package.accept_keywords
                $USER emerge papaer-icon-theme
        ;;
        *)
                $USER rm -r /tmp/paper-icon
                git clone -depth 1 https://github.com/snwh/paper-icon-theme /tmp/paper-icon
                $USER mv /tmp/paper-icon/Paper* /usr/share/icons
                $USER gtk-update-icon-cache -q /usr/share/icons/Paper*
                $USER rm -r /tmp/paper-icon
        ;;
    esac
}

adapta_gtk_theme(){
    case $OS in
        ubuntu)
                $USER add-apt-repository ppa:tista/adapta
                $USER apt-get update
                $USER apt-get install adapta-gtk-theme
        ;;
        arch)
                $USER pacman -S adapta-gtk-theme
        ;;
        manjaro)
                $USER pacman -S adapta-gtk-theme
        ;;
        solus)
                $USER eopkg install adapta-gtk-theme
        ;;
        gentoo)
                $USER layman -a jorgicio
                $USER layman -S
                $USER echo "=adapta-gtk-theme-9999 **" >> /etc/portage/package.accept_keywords
                $USER emerge adapta-gtk-theme
        ;;
        *)
                git clone -depth 1 https://github.com/Linux-Theme-Collection/Theme-By-Mame /tmp/adapta-gtk-theme
                $USER mv /tmp/adapta-gtk-theme/themes/Adapta* /usr/share/themes
                $USER rm -r /tmp/adapta-gtk-theme
        ;;
    esac
}

adapta_kde_theme(){
}

arc_kde_theme(){
}

choose_theme(){
    echo "         输入你想安装的主题
    [1] Papirus Icon Theme(推荐)
    [2] Paper Icon Theme
    [3] Adapta Gtk Theme(推荐)
    [4] Adaota KDE Theme(KDE桌面推荐）
    "
}


# Main
if [ `whoami` == root ];then
    USER=''
elif (whereis sudo | grep / > /dev/null);then
    USER='sudo'
else
    echo "请安装sudo(当然也需要把当前用户添加到wheel用户组并修改sudo配置）或在root用户下运行"
    exit
fi

if (whereis git | grep / > /dev/null);then
    :
else
    echo "请安装Git并设置Git代理"
    exit
fi

get_OS

choose_theme
