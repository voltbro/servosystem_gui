#!/bin/bash -i

sudo apt install git
apt install python3.12-venv
sudo apt install python3-pyqt5
sudo gpasswd --add ${USER} dialout

# git clone https://github.com/voltbro/servosystem_gui.git
# cd servosystem_gui
python3 -m venv .venv
source .venv/bin/activate

pip install numpy
pip install matplotlib
pip install pyqt5
pip install pyyaml
pip install pyqtgraph
pip install control
pip install QtAwesome
pip install pyserial