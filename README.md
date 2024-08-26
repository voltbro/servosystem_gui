Программа тестировалась только на Ubuntu 24.04

## Установка: <br>
```
sudo apt install git
cd ~
git clone https://github.com/voltbro/servosystem_gui.git
cd servosystem_gui
./install.sh
sudo reboot
```
## Запуск <br>
### Первый способ:
```
cd servosystem_gui
source .venv/bin/activate
python3 main.py
```
### Второй способ: <br>
На рабочем столе кликните правой кнопкой мыши по иконке DCMotorControl и выберите Allow Launching. Затем дважды кликните по иконке, чтобы запустить программу. Также приложение доступно в меню приложений Ubuntu.