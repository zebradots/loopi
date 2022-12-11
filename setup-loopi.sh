#!/bin/bash
#
# Install and configure loopi
#

VER=1.0
TARGET_HW="Raspberry Pi 3"
TARGET_OS="buster"
SYSTEM_HW=$(tr -d '\0' < /sys/firmware/devicetree/base/model)
SYSTEM_OS=`grep "PRETTY" /etc/os-release`

# Welcome
echo -e "--------------------"
echo -e "loopi v$VER installer"
echo -e "--------------------"

# Must be run as root on supported hardware and Debian OS
echo
if [ "$EUID" -ne 0 ]
	then echo -e "FATAL ERROR: Must be run as root!\n"
	exit
fi
echo -e "Hardware: $SYSTEM_HW"
if [[ "$SYSTEM_HW" != *"$TARGET_HW"* ]]; then
	echo -e "FATAL ERROR: Expected hardware to be $TARGET_HW\n"
	exit
fi
echo -e "Operating system: $SYSTEM_OS"
if [[ "$SYSTEM_OS" != *"$TARGET_OS"* ]]; then
	echo -e "FATAL ERROR: Expected OS to be $TARGET_OS\n"
	exit
fi

echo "* Setting basic system settings..."
echo loopi > /etc/hostname
perl -p -i -e "s/raspberrypi/loopi/g" /etc/hosts
perl -p -i -e 's/^#disable_overscan=1$/disable_overscan=1/g' /boot/config.txt
raspi-config nonint do_wifi_country US
systemctl enable ssh; systemctl start ssh
perl -p -i -e "s/^/loopi: Seamless looping video player\nVersion $VER\n/" /etc/issue
perl -p -i -e 's/^set compatible$/set nocompatible/g' /etc/vim/vimrc.tiny
perl -p -i -e 's/^"syntax on$/syntax on/g' /etc/vim/vimrc

echo "* Changing keyboard map and timezone..."
perl -p -i -e 's/XKBLAYOUT="gb"/XKBLAYOUT="us"/g' /etc/default/keyboard
ln --force --symbolic /usr/share/zoneinfo/America/Chicago /etc/localtime
dpkg-reconfigure --frontend=noninteractive tzdata

echo "* Installing required packages..."
export DEBIAN_FRONTEND=noninteractive
apt update --yes
apt install --yes \
	nodm \
	openbox \
	xinit \
	x11-xserver-utils \
	xterm \
	unclutter \
	python3-tk \
	fonts-roboto \
	omxplayer \
	hostapd \
	dnsmasq \
	pwgen \
	php-cli \
	php-zip \
	screen

echo "* Configuring WLAN device IP address..."
cat >> /etc/dhcpcd.conf << EOF
# Set WiFI access point IP address
interface wlan0
static ip_address=10.0.0.1/24
nohook wpa_supplicant
EOF
systemctl restart dhcpcd

echo "* Configuring DHCP and DNS server..."
cat > /etc/dnsmasq.conf << EOF
no-resolv
interface=wlan0
dhcp-range=10.0.0.2,10.0.0.10,1h
server=10.0.0.1
address=/#/10.0.0.1
EOF

echo "* Configuring WiFi host access point..."
cat > /etc/hostapd/hostapd.conf << EOF
country_code=US
interface=wlan0
ssid=
channel=9
auth_algs=1
wpa=2
wpa_passphrase=
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
EOF
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd

echo "* Preparing web UI components..."
/usr/bin/cp --force --recursive --verbose overlay/* /
tar zxf vendor/pico-css/v1.5.6.tar.gz pico-1.5.6/css/pico.min.css --strip=1
/usr/bin/cp --force --recursive --verbose css /var/www/html/
rm -rf ./css
unzip -q vendor/filegator/filegator_latest.zip
mv filegator /var/www/
ln -s /var/www/filegator/dist /var/www/html/media
CONF=/var/www/filegator/configuration.php
cp /var/www/filegator/configuration_sample.php $CONF
perl -p -i -e "s/'app_name' =.*$/'app_name' => 'loopi | media manager',/g" $CONF
perl -p -i -e "s/'logo' =.*$/'logo' => '\/assets\/loopi.svg',/g" $CONF
perl -p -i -e "s/'upload_max_size' =.*$/'upload_max_size' => 1000 * 1024 * 1024,/g" $CONF
perl -p -i -e "s/'date_format' =.*$/'date_format' => 'MM\/DD\/YY hh:mm:ss',/g" $CONF
CONF=/var/www/filegator/private/users.json
cp $CONF.blank $CONF
perl -p -i -e 's/"permissions":""/"permissions":"read|write|upload|download"/g' $CONF
sync

echo "* Done installing loopi!"
echo
echo "If no errors were reported, your system is ready to reboot."
echo
exit
