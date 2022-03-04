# leg-control

## 脚単体チェッカ(unit_leg_checker)

* モーター2軸を使って脚単体の動作を確認するためのチェッカ
  * リンク機構のデバッグを目的とする
  * そのうちモーター換える

### シリアル通信設定

* 9600bps
* データ8bit
* パリティなし
* ストップビット1bit
* フロー制御なし
* 改行コード＝LFのみ

### コマンド

* stop
* move
* pos <angle>
  * 2軸角度指定動作
  * <angle> : servo1の指定角度[deg]。0～180。servo2は180-<angle>へ動作
    * 平行配置、対象動作を想定している。
* ud <up_angle> <down_angle>
  * 脚部上下動
  * 角度の小さいほうが
  * <up_angle> : 上端角度、0～180
  * <down_angle> : 下端角度、0～180

## 参考

* [PICO-STDモーター仕様書](https://gwsus.com/gws_com_tw_www/english/product/servo/sat%20form.htm)
