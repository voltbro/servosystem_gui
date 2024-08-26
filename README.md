Программа тестировалась только на Ubuntu 24.04

Установка: <br>
sudo apt install git <br>
apt install python3.12-venv <br>
sudo apt install python3-pyqt5 <br>
sudo gpasswd --add ${USER} dialout <br>

cd ~ <br>
git clone https://github.com/voltbro/servosystem_gui.git <br>
cd servosystem_gui <br>
python -m venv .venv <br>
source .venv/bin/activate <br>
pip install numpy <br>
pip install matplotlib <br>
pip install pyqt5 <br>
pip install pyyaml <br>
pip install pyqtgraph <br>
pip install control <br>
pip install QtAwesome <br>
pip install pyserial <br>

Перезапустите компьютер

Запуск <br>
cd servosystem_gui <br>
source .venv/bin/activate  <br>
python3 main.py <br>
