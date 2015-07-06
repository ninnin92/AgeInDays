#!/usr/bin/env python
# coding:utf-8
# env: Python3.3
# python2系でも動くように調整済み

import sys
import calendar as cal
from datetime import date, timedelta, datetime

################################################
#  宣言
################################################

continue_roop = True

################################################
#  処理関数
################################################


# 標準入力（python2 or 3で対応切り替え）
def key_input(text=None):
    if text is None:
        if sys.version_info.major > 2:  # 3系かどうかの判定
            return input()
        else:
            return raw_input()  # python2ではraw_input
    else:
        if sys.version_info.major > 2:  # 3系かどうかの判定
            return input(text)
        else:
            return raw_input(text)  # python2ではraw_input


# モードの切替 [1] 年齢と調査日から対象の子の誕生日を推定 [2] 年齢と誕生日から調査予定日を推定
def mode_change():
    mode = key_input("Please enter mode number: [1] age to birthday  [2] age to date  ")
    print("----------------------------------------------")
    print("# Set mode [ " + mode + " ]")
    print("----------------------------------------------")
    return int(mode)


# 年齢を入力させる（範囲入力ができるように）
def get_age():
    # 年齢入力 その１（１個のみの入力の場合はこちらのみを入力）
    while True:
        try:
            age1 = key_input('Please enter age1 (e.g. 1-1-1 = 1years 1months 1days)  ')
            age1 = age1.split("-")  # "-"で文字列を分割（月齢入力にもいつか対応したいところ）
            age1_str = age1[0] + "y " + age1[1] + "m " + age1[2] + "d"
            break
        except (ValueError, IndexError):  # ここは何がなんでも入力させる
            print("Error Age1: Please one more!!")

    # 年齢入力 その２（入力なしでもOK：その場合はスルー）
    while True:
        try:
            age2 = key_input('Please enter age2 (e.g. 1-1-1 = 1years 1months 1days)  ')
            age2 = age2.split("-")
            age2_str = age2[0] + "y " + age2[1] + "m " + age2[2] + "d"
            op_period = True  # 範囲指定からどうかのオプション
            break

        except (IndexError):  # 入力がないとエラー（もしくはリストが３つないとエラー）
            age2 = [0, 0, 0]  # 適当に指定
            op_period = False  # 範囲指定からどうかのオプション
            break

        except (ValueError):  # おかしな入力をするとエラー？
            print("Error Age2: Please one more!!")

    print("# Set age period  :" + age1_str + "  ~  " + age2_str)
    print("----------------------------------------------")
    return age1, age2, op_period


# 誕生日を入力させる
def get_birthday():
    while True:
        try:
            bd = key_input('Please enter ones birthday (e.g. 2015/06/04)  ')
            bd = datetime.strptime(bd, "%Y/%m/%d")  # datetime型に変換
            birthday = date(bd.year, bd.month, bd.day)
            break
        except ValueError:
            print("Error: Please one more!!")

    print("# Birthday:  " + str(birthday))
    print("----------------------------------------------")
    return birthday


# 調査予定日を入力させる
def set_date():
    while True:
        try:
            bdate = key_input('Please enter research date(e.g. 2015/07/04)  ')
            bdate = datetime.strptime(bdate, "%Y/%m/%d")  # datetime型に変換
            base_date = date(bdate.year, bdate.month, bdate.day)
            break
        except ValueError:
            base_date = date.today()  # 入力がなければ「今日」を指定
            break

    print("# Reserch date:  " + str(base_date))
    print("----------------------------------------------")
    return base_date


# 年齢と調査予定日から誕生日を推定
def calc_birthday(age, base):
    set_years = base.year - int(age[0])  # 調査予定日の年から年齢（年）を引く
    set_months = base.month - int(age[1])  # 調査予定日の月から年齢（月）を引く
    set_days = int(age[2])  # 年齢（日）

    # 調査予定日を基準に年齢の年・月を引いてから日を引き算
    try:
        bd = base.replace(year=set_years, month=set_months)  # 調査予定日から年と月を計算後に変更
        bd -= timedelta(days=set_days)  # 変更後から日数を変更

    # 調査予定日が29-31日で、変更後の月が2月（29-31日）、4・6・9・11月（31日）だとエラー（存在しないため）
    except ValueError:
        # 調査予定日から年と月を計算後に変更、日は変更後の月末にとりあえず指定
        bd = base.replace(year=set_years, month=set_months,
                          day=cal.monthrange(set_years, set_months)[1])
        bd += timedelta(days=base.day - bd.day)  # とりあえず変更した日数（減らした日数分）を追加
        bd -= timedelta(days=set_days)  # 変更後から日数を変更
    bd = date(bd.year, bd.month, bd.day)
    return bd


# 年齢と誕生日から調査予定日を推定
def calc_date(age, bd):
    set_years = bd.year + int(age[0])  # 誕生日の年から年齢（年）を足す
    set_months = bd.month + int(age[1])  # 誕生日の月から年齢（月）を足す
    set_days = int(age[2])  # 年齢（日）

    # 誕生日を基準に年齢の年・月を足してから日を足し算
    try:
        d = bd.replace(year=set_years, month=set_months)  # 誕生日から年と月を計算後に変更
        d += timedelta(days=set_days)  # 変更後から日数を変更

    # 誕生日が29-31日で、変更後の月が2月（29-31日）、4・6・9・11月（31日）だとエラー（存在しないため）
    except ValueError:
        # 誕生日から年と月を計算後に変更、日は変更後の月末にとりあえず指定
        d = bd.replace(year=set_years, month=set_months,
                       day=cal.monthrange(set_years, set_months)[1])
        d += timedelta(days=bd.day - d.day)  # とりあえず変更した日数（減らした日数分）を追加
        d += timedelta(days=set_days)  # 変更後から日数を変更
    d = date(d.year, d.month, d.day)
    return d


################################################
#  メイン処理
################################################


if __name__ == '__main__':
    while continue_roop:
        mode = mode_change()  # モード設定
        # [1] 年齢と調査日から対象の子の誕生日を推定
        if mode == 1:
            age1, age2, op_period = get_age()  # 年齢をセット
            base_date = set_date()  # 調査予定日をセット
            # 範囲入力の場合
            if op_period:
                bd1 = calc_birthday(age1, base_date)
                bd2 = calc_birthday(age2, base_date)
                print("********************************************")
                print("# Birthday period: " + str(bd2) + "  ~  " + str(bd1))
                print("********************************************")
            # 範囲入力じゃない場合
            else:
                bd = calc_birthday(age1, base_date)
                print("********************************************")
                print("# Birthday:  " + str(bd))
                print("********************************************")

        # [2] 年齢と誕生日から調査予定日を推定
        elif mode == 2:
            age1, age2, op_period = get_age()  # 年齢をセット
            bd = get_birthday()  # 誕生日をセット

            # 範囲入力の場合
            if op_period:
                d1 = calc_date(age1, bd)
                d2 = calc_date(age2, bd)
                print("********************************************")
                print("# Reserch period: " + str(d1) + "  ~  " + str(d2))
                print("********************************************")
            # 範囲入力じゃない場合
            else:
                d = calc_birthday(age1, base_date)
                print("********************************************")
                print("# Reserch date:  " + str(d))
                print("********************************************")

        # モード入力が1-2以外ならエラーで終了
        else:
            print("mode error: Please restart!")
            break

        # 処理のポーズ（y/nでループ続行 or プログラム終了
        exit = key_input("Continue? Please input y/n (yes or no)   ")
        if exit == "y":
            continue
        else:
            break
