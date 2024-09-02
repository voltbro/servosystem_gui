#!/bin/bash -i

DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "Script location: ${DIR}"

sudo apt install python3.12-venv
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
# pip install PyOpenGL


FILE="DCMotorControl.desktop"
echo $FILE
if [ -f "$FILE" ] ; then
    rm "$FILE"
fi
echo -e "[Desktop Entry]" >> $FILE
echo -e "Version=1.0" >> $FILE
echo -e "Encoding=UTF-8" >> $FILE
echo -e "Type=Application" >> $FILE
echo -e "Terminal=false" >> $FILE
echo -e "Name=DCMotorControl" >> $FILE
echo -e "Exec=$DIR/startup.sh" >> $FILE
echo -e "Comment=Yo-ho-ho" >> $FILE
echo -e "Icon=$DIR/icons/icon.png" >> $FILE
echo -e "Name[en]=DCMotorControl" >> $FILE
cp $FILE ~/Desktop/
sudo cp $FILE /usr/share/applications

echo "Installation complete successfully!"