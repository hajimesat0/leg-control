# leg-control

## 脚単体チェッカ(unit_leg_checker)

* モーター2軸を使って脚単体の動作を確認するためのチェッカ
  * リンク機構のデバッグを目的とする
  * そのうちモーター換える

## 4脚制御

* 1脚あたり2軸使って4脚を制御する
* raspi-configコマンドのインストール

```sh
wget -4 https://archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20210604_all.deb -P /tmp
sudo apt-get install libnewt0.52 whiptail parted triggerhappy lua5.1 alsa-utils -y
sudo apt-get install -fy
dpkg -i /tmp/raspi-config_20210604_all.deb
```

* I2C利用設定を有効化
* PCA9685はAdafruit社のライブラリを使用

```sh
pip install setuptools
git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
cd Adafruite_python_PCA9685
sudo python setup.py install
```

* PCA9685のアドレス確認

```sh
sudo apt-get install i2c-tools
sudo i2cdetect -y 1
```

## 参考

* [PICO-STDモーター仕様書](https://gwsus.com/gws_com_tw_www/english/product/servo/sat%20form.htm)
* [SG-90モーター仕様書]https://akizukidenshi.com/download/ds/towerpro/SG90_a.pdf)
* [raspi-configのインストール](https://askubuntu.com/questions/1130052/enable-i2c-on-raspberry-pi-ubuntu)
* [I2C利用設定の有効化](https://qiita.com/fujit33/items/763b09a6e71e65519740)
* [RaspiとPCA9685の接続](https://rb-station.com/blogs/article/pca9685-raspbery-pi-python)
