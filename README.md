Программа тестировалась только на Ubuntu 24.04

Установка:
cd ~
git clone https://github.com/voltbro/servosystem_gui.git
cd servosystem_gui
python -m venv .venv
source .venv/bin/activate
pip install numpy
pip install matplotlib
pip install pyqt5
pip install pyyaml
pip install pyqtgraph
pip install control
pip install QtAwesome
pip install pyserial

Запуск
cd servosystem_gui
source .venv/bin/activate 
python3 main.py