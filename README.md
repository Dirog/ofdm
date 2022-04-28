# OFDM приемник и передатчик для Pluto SDR
Для работы необходимо установить библиотеки для работы с Pluto SDR ([источник](https://pysdr.org/content/pluto.html)):
```console
sudo apt-get install build-essential git libxml2-dev bison flex libcdk5-dev cmake python3-pip libusb-1.0-0-dev libavahi-client-dev libavahi-common-dev libaio-dev
cd ~
git clone --branch v0.23 https://github.com/analogdevicesinc/libiio.git
cd libiio
mkdir build
cd build
cmake -DPYTHON_BINDINGS=ON ..
make -j
sudo make install
sudo ldconfig

cd ~
git clone https://github.com/analogdevicesinc/libad9361-iio.git
cd libad9361-iio
mkdir build
cd build
cmake ..
make -j
sudo make install

cd ~
git clone https://github.com/analogdevicesinc/pyadi-iio.git
cd pyadi-iio
pip3 install --upgrade pip
pip3 install -r requirements.txt
sudo python3 setup.py install
```

Для приема сигнала необходимо запустить скрипт приемника:
```console
python3 rx.py ./config.json
```
При этом будут построены графики. Если отображение графиков не требуется можно запусить скрипт с флагом '-O':
```console
python3 -O rx.py ./config.json
```

Для передачи сигнала необходимо запусить следующий скрипт:
```console
python3 tx.py ./config.json
```
Скрипты будут работать, пока их не оставновит пользователь. Для отстановки скрипта необходимо нажать 'ctrl + c' в консоле.

Конфигурация приемника и передатчика производится черех файл *config.json*.