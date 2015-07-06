#!/usr/bin/env python
# coding:utf-8
# env: Python3.3
# python2系でも動くように調整済み

import sys
from datetime import date, timedelta, datetime

################################################
#  宣言
################################################

continue_roop = True

################################################
#  処理関数
################################################


def day_input(text=None):
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


def set_day():
    sday = day_input('Please enter base date (e.g. 2015/06/04, None => today)  ')
    return sday


# 誕生日を入力させる
def get_birthday():
    # 入力待ち(関数を別に作ってPython2系にも対応)
    bday = day_input('Please enter ones birthday (e.g. 2015/06/04)  ')
    return bday


# 年齢の計算（閏日補正含む） ：今何歳何ヶ月なのか？
def count_years(b, s):
    try:
        this_year = b.replace(year=s.year)
    except ValueError:
        b += timedelta(days=1)
        this_year = b.replace(year=s.year)

    age = s.year - b.year
    if base_day < this_year:
        age -= 1

# 何歳”何ヶ月”を計算
    if (s.day - b.day) >= 0:
        year_months = (s.year - b.year) * 12 - age * 12 + (s.month - b.month)
    else:
        year_months = (s.year - b.year) * 12 - age * 12 + (s.month - b.month) - 1  # 誕生日が来るまでは月齢も-1

    return age, year_months


# 月齢の計算
def count_months(b, s):
    if (s.day - b.day) >= 0:
        months = (s.year - b.year) * 12 + (s.month - b.month)
    else:
        months = (s.year - b.year) * 12 + (s.month - b.month) - 1  # 誕生日が来るまでは月齢も-1
    return months


# 月齢および何歳何ヶ月の余り日数（何歳何ヶ月”何日”）
def count_days(b, s):
    if (s.day - b.day) >= 0:
        days = s.day - b.day
    else:
        try:
            before = s.replace(month=s.month - 1, day=b.day)
            days = (s - before).days
        except ValueError:
            days = s.day
            # 2月は1ヶ月バックするとエラーになる時がある(誕生日が29-31日の時)
            # なのでそうなった場合は、すでに前月の誕生日を迎えたことにする（setされた日が日数とイコールになる）
    return days


################################################
#  メイン処理
################################################


if __name__ == '__main__':
    while continue_roop:
        # 日付設定(入力なしで今日にセット)
        while True:
            try:
                sd = set_day()
                sd = datetime.strptime(sd, "%Y/%m/%d")
                break
            except ValueError:
                sd = date.today()
                break
        base_date = sd.strftime('%Y/%m/%d')
        base_day = date(sd.year, sd.month, sd.day)
        print (base_day)

        # 誕生日を入力させて、datetime型に変換（例外処理つき）
        while True:
            try:
                bd = get_birthday()
                bd = datetime.strptime(bd, "%Y/%m/%d")
                break
            except ValueError:
                print ("Error: Please one more!!")
        your_birthday = bd.strftime('%Y/%m/%d')
        birthday = date(bd.year, bd.month, bd.day)
        print(birthday)

        # 年齢を表示
        age             = str(count_years(birthday, base_day)[0])
        age_year_months = str(count_years(birthday, base_day)[1])
        age_days        = str(count_days(birthday, base_day))
        age_months      = str(count_months(birthday, base_day))
        age_in_days     = str((base_day - birthday).days)

        age_details = age + "years " + age_year_months + "months " + age_days + "days"

        print ("********************************************")  # python2では()なし
        print ("Base date  " + base_date)
        print ("Birthday  " + your_birthday)
        print ("Age  " + age)
        print ("Age_months  " + age_months)
        print ("Age_in_days  " + age_in_days)
        print ("Age_details  " + age_details)
        print ("********************************************")

    # 処理のポーズ（y/nでループ続行 or プログラム終了）
        exit = day_input("Exit? Please input y/n (yes or no)   ")
        if exit == "n":
            continue
        else:
            break
