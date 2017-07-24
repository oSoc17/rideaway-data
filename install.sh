#!/bin/bash
sudo sed 's/# deb/deb/' -i /etc/apt/sources.list

sudo add-apt-repository ppa:alexlarsson/flatpak
sudo apt update
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
sudo apt-get update
sudo apt install flatpak
sudo apt-get install mono-devel
flatpak install --user --from https://download.mono-project.com/repo/monodevelop.flatpakref
