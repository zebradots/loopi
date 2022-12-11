<img src="https://github.com/zebradots/loopi/blob/main/overlay/var/www/html/assets/logo-purple.png"></img>

## Seamless looped video playback 

<strong>Looking for an easy way to loop video on a screen? With <u>loopi</u> you'll be up and running in minutes.</strong>

Other options exist, but aren't always the best solution. [Screenly OSE](https://www.screenly.io/) requires a [network connection](https://support.screenly.io/hc/en-us/articles/213678603-Can-I-use-Screenly-without-an-internet-connection-) at all times, and refuses to play without it. [Raspberry Pi Video Looper](https://videolooper.de/) works well, but requires shuttling [USB sticks](https://videolooper.de/#you_will_also_need) to update media files.

We made <strong>loopi</strong> to be stable, resilient, and much easier to update. You won't need to move USB sticks back and forth. Updating video is as easy as connecting to a wireless network to drag and drop your media files. Playback is seamless: you won't see black screens or spinners between loops.

This solution can be used for digital signage, wayfinding and directional signs, art show exhibits, tradeshow presentations, museum displays, current events calendars, lobbies, waiting rooms, retail and point-of-purchase displays, restaurant menus, and much more.


## Features

- Solid and stable reliability
- Seamless looping; no black screens or spinners
- No need for USB drives
- No internet or network connection required
- No telemetry or "phoning home"
- Simply connect to loopi's WiFi hotspot to update media
- Media changes detected and applied automatically
- User friendly and intuitive interface


## Screenshots

<div>
  <p align="center">
    <img src="https://github.com/zebradots/loopi/blob/main/overlay/var/www/html/images/loopi-countdown.png" width="30%">
    <img src="https://github.com/zebradots/loopi/blob/main/overlay/var/www/html/images/loopi-status.png" width="30%">
    <img src="https://github.com/zebradots/loopi/blob/main/overlay/var/www/html/images/loopi-media.png" width="30%">
  </p>
</div>


## Requirements

- <strong>Raspberry Pi 3B or 3B+</strong> (other models not tested)
- <strong>8GB or greater SD card</strong>, preferably Class A
- Full HD 1080P screen <strong>connected with HDMI cable</strong>


## Getting started

1. Get the latest image
1. Write the image to a quality SD card
	- Windows: Try [Rufus](https://rufus.ie/)
	- Mac: Use [balenaEtcher](https://www.balena.io/etcher/)
	- Linux: `xzcat loopi-1.X.img.xz | sudo dd of=/dev/sdX bs=4M oflag=dsync status=progress`
1. Put the SD card in your Raspberry Pi and reboot
1. Follow the on-screen instructions to connect your notebook, laptop, phone, or tablet to the WiFi hotspot with the randomly generated password on the screen
1. On your wireless device, open [http://loopi](http://loopi) and click "Manage media"
1. Drag and drop a compatible 1080P video file―it will begin to loop automatically!


## Building custom images

1. Install the latest Debian `buster` RaspiOS image, e.g.: `xzcat 2022-09-22-raspios-buster-armhf-lite.img.xz | sudo dd of=/dev/sdc bs=4M oflag=dsync status=progress`
1. Boot into the system and log in as the default user
1. `git clone https://github.com/zebradots/loopi`
1. `cd loopi`
1. `sudo ./setup-loopi.sh`
1. `sudo poweroff`
1. Remove the card and insert it into an SD reader; ensure the partitions are not mounted
1. `dd if=/dev/sdX of=loopi-1.X.img bs=32M`
1. `wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh`
1. `./pishrink.sh loopi-1.X.img`
1. `xz -9e loopi-1.X.img`


## Sponsors

While <strong>loopi</strong> has you covered for digital signage, you may also want traditional [custom signs, lettering and wall graphics](https://rioprinting.com) to finish your project. The <strong>loopi</strong> project is sponsored by:

- <strong>[Rio Creative Signs and Graphics](https://rioprinting.com/)</strong>
