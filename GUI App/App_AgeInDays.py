#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import ui_ageindays # designerで作ったUIを変換してソースとして読み込み
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
import calendar as cal
from datetime import date, timedelta, datetime


class MainWindow(QMainWindow, ui_ageindays.Ui_AgeInDays):

    # 初期設定
    def __init__(self):
        super(MainWindow, self).__init__()
        # setupUi というメソッドが定義されているので実行する
        # これで設置したウィジェットなどがインスタンス化される
        self.setupUi(self)
        # 継承したので self.名前 でアクセスできる
        self.setWindowTitle("AgeInDays") # ウィンドウタイトル
        # 操作と関数のひも付け
        self.pushButton_Go.clicked.connect(self.calculate)
        self.pushButton_Clear.clicked.connect(self.textBrowser.clear)
        self.change_mode.activated.connect(self.target_mode_change)
        self.switch_target_age.activated.connect(self.target_mode_change)
        self.switch_target_range.activated.connect(self.target_mode_change)

        # 日付入力に今日の日付を挿入
        self.input_research_date.setDate(QDate.currentDate())
        self.input_birthday.setDate(QDate.currentDate())

        # ラジオボタンの初期設定とカレンダーにひも付け
        self.switch_birthday.toggled.connect(self.connect_calendar) # ボタングループで判定されるので１つだけ
        self.switch_research_date.setChecked(True)
        self.switch_birthday.setChecked(False)

        # カレンダーのひも付けとUIのデフォルト状態を設定しておく
        self.connect_calendar()
        self.target_mode_change()

    # エラーチェック：誕生日が調査日よりも未来にならないように
    def input_check_future(self, research_date, birthday):
        if research_date <= birthday:
            QMessageBox.warning(self, "Error", "誕生日を調査日以前に設定し直してください。")
            return False
        else:
            return True

    # エラーチェック：対象年齢入力に半角数字以外が入力されないように
    def input_check_hankaku(self):
        try: # 整数型にできない　≒　半角数字以外の入力の可能性
            Age1_years = int(self.input_target1_years.text())
            Age1_months = int(self.input_target1_months.text())
            Age1_days = int(self.input_target1_days.text())

            Age2_years = int(self.input_target2_years.text())
            Age2_months = int(self.input_target2_months.text())
            Age2_days = int(self.input_target2_days.text())
            return True

        except:
            QMessageBox.warning(self, "Error", "対象年齢は半角数字で入力してください。")
            return False

    # エラーチェック：対象年齢入力に月日の範囲を超える入力（1歳16ヶ月35日とか）、または対象2 < 対象1になる入力がされないように
    def input_check_range(self):
        Age1_years = int(self.input_target1_years.text())
        Age1_months = int(self.input_target1_months.text())
        Age1_days = int(self.input_target1_days.text())

        Age2_years = int(self.input_target2_years.text())
        Age2_months = int(self.input_target2_months.text())
        Age2_days = int(self.input_target2_days.text())

        target_mode = self.switch_target_age.currentText()
        target_range = self.switch_target_range.currentText()

        if target_range == "範囲":
            if target_mode == "月齢":
                if 0 <= Age1_months and 0 <= Age1_days <= 31 and \
                   0 <= Age2_months and 0 <= Age2_days <= 31:

                    if Age1_months <= Age2_months: # 対象2 < 対象1チェック
                        return True
                    else:
                        QMessageBox.warning(self, "Error", "対象2は対象1より大きな値を設定してください。")
                        return False
                else:
                    QMessageBox.warning(self, "Error", "対象年齢の月は0以上、日は0~31の間で入力してください。")
                    return False

            else: # target_mode == "年齢"
                if 0 <= Age1_months <= 11 and 0 <= Age1_days <= 31 and \
                   0 <= Age2_months <= 11 and 0 <= Age2_days <= 31:

                    if Age1_years <= Age2_years or Age1_months <= Age2_months: # 対象2 < 対象1チェック
                        return True
                    else:
                        QMessageBox.warning(self, "Error", "対象2は対象1より大きな値を設定してください。")
                        return False
                else:
                    QMessageBox.warning(self, "Error", "対象年齢の月は0~11、日は0~31の間で入力してください。")
                    return False
        else: #  target_range == "固定"
            if target_mode == "月齢":
                if 0 <= Age1_months and 0 <= Age1_days <= 31:
                    return True
                else:
                    QMessageBox.warning(self, "Error", "対象年齢の月は0以上、日は0~31の間で入力してください。")
                    return False
            else: # target_mode == "年齢"
                if 0 <= Age1_months <= 11 and 0 <= Age1_days <= 31:
                    return True
                else:
                    QMessageBox.warning(self, "Error", "対象年齢の月は0~11、日は0~31の間で入力してください。")
                    return False

    # 調査日と誕生日から年齢・月齢・日齢を判定
    def age_in_days(self):
        research_date_set = self.input_research_date.date().toString("yyyy/MM/dd")
        research_date = datetime.strptime(research_date_set, "%Y/%m/%d")
        research_date = date(research_date.year, research_date.month, research_date.day)

        birthday_set = self.input_birthday.date().toString("yyyy/MM/dd")
        birthday = datetime.strptime(birthday_set, "%Y/%m/%d")
        birthday = date(birthday.year, birthday.month, birthday.day)

        # エラーチェック：誕生日 ＞ 調査日にならないように
        if self.input_check_future(research_date, birthday):

            ###  メイン関数  ###

            # 年齢の計算（閏日補正含む）：今何歳なのか？:age
            try:
                t_year = birthday.replace(year=research_date.year)
            except ValueError:
                b += timedelta(days=1)
                t_year = birthday.replace(year=research_date.year)

            age = research_date.year - birthday.year
            if research_date < t_year:
                age -= 1

            # 月齢および何歳”何ヶ月”を計算:months, year_months
            if (research_date.day - birthday.day) >= 0:
                months = (research_date.year - birthday.year) * 12 \
                + (research_date.month - birthday.month)

                year_months = (research_date.year - birthday.year) * 12 - age * 12 \
                + (research_date.month - birthday.month)

            else: # 誕生日が来るまでは月齢も-1
                months = (research_date.year - birthday.year) * 12 \
                + (research_date.month - birthday.month) - 1

                year_months = (research_date.year - birthday.year) * 12 - age * 12 \
                + (research_date.month - birthday.month) - 1


            # 日齢および何歳何ヶ月の余り日数（何歳何ヶ月”何日”）:year_days
            if (research_date.day - birthday.day) >= 0:
                year_days = research_date.day - birthday.day
            else:
                try:
                    if research_date.month == 1:
                        before = research_date.replace(year=research_date.year - 1,
                                                       month=12, day=birthday.day)
                        year_days = (research_date - before).days
                    else:
                        before = research_date.replace(month=research_date.month - 1,
                                                       day=birthday.day)
                        year_days = (research_date - before).days
                except ValueError:
                    year_days = research_date.day
                    # 2月は1ヶ月バックするとエラーになる時がある(誕生日が29-31日の時)
                    # なのでそうなった場合は、すでに前月の誕生日を迎えたことにする（setされた日が日数とイコールになる）

            # 年齢を表示
            age             = str(age)
            age_year_months = str(year_months)
            age_year_days   = str(year_days)
            age_months      = str(months)
            age_days        = str((research_date - birthday).days)

            age_details = age + "歳 " +age_year_months + "ヶ月 " + age_year_days + "日"

            results = ["モード1：年齢計算モード",
                       " ",
                       "調査日  " + research_date_set,
                       "誕生日  " + birthday_set,
                       " ",
                       "年齢  " + age + " 歳",
                       "月齢  " + age_months + " ヶ月",
                       "日齢  " + age_days + " 日",
                       " ",
                       "詳細な年齢  " + age_details]

        else:
            results = ["Error!"]


        return results

    # 対象年齢の入力を日付処理ができる形に変換
    def get_target_age(self):
        target_mode = self.switch_target_age.currentText()
        target_range = self.switch_target_range.currentText()

        if target_range == "範囲":
            if target_mode == "月齢":
                Age1_months = int(self.input_target1_months.text())
                Age1_days = int(self.input_target1_days.text())
                Age1 = [Age1_months//12, Age1_months%12, Age1_days]
                # 月齢入力になっているので月齢を年（12で割る数）と月（12で割った余り）に分解

                Age2_months = int(self.input_target2_months.text())
                Age2_days = int(self.input_target2_days.text())
                Age2 = [Age2_months//12, Age2_months%12, Age2_days]
                # 月齢入力になっているので月齢を年（12で割る数）と月（12で割った余り）に分解

            else: # target_mode == "年齢"
                Age1_years = int(self.input_target1_years.text())
                Age1_months = int(self.input_target1_months.text())
                Age1_days = int(self.input_target1_days.text())
                Age1 = [Age1_years, Age1_months, Age1_days]

                Age2_years = int(self.input_target2_years.text())
                Age2_months = int(self.input_target2_months.text())
                Age2_days = int(self.input_target2_days.text())
                Age2 = [Age2_years, Age2_months, Age2_days]

            return [Age1, Age2]

        else: # target_range == "固定"
            if target_mode == "月齢":
                Age3_months = int(self.input_target1_months.text())
                Age3_days = int(self.input_target1_days.text())
                Age3 = [Age3_months//12, Age3_months%12, Age3_days]
                # 月齢入力になっているので月齢を年（12で割る数）と月（12で割った余り）に分解

            else: # target_mode == "年齢"
                Age3_years = int(self.input_target1_years.text())
                Age3_months = int(self.input_target1_months.text())
                Age3_days = int(self.input_target1_days.text())
                Age3 = [Age3_years, Age3_months, Age3_days]

            return [Age3]

    # 対象年齢と調査予定日から誕生日を推定
    def age_to_birthday(self):
        research_date_set = self.input_research_date.date().toString("yyyy/MM/dd")
        research_date = datetime.strptime(research_date_set, "%Y/%m/%d")
        research_date = date(research_date.year, research_date.month, research_date.day)

        # エラーチェック：半角入力と対象年齢の範囲確認
        if self.input_check_hankaku() and self.input_check_range():

            ###  メイン関数  ###

            age_list = self.get_target_age() # 対象年齢の取得
            cal_result = [] # 結果リスト

            for age in age_list:
                set_days = int(age[2])  # 年齢（日）
                set_months = research_date.month - int(age[1])  # 調査予定日の月から年齢（月）を引く

                # 引いた月の数がマイナスになる時は、年齢からもう1年引いて、月に12ヶ月足す → 再計算
                if set_months <= 0:
                    set_years = research_date.year - int(age[0]) - 1
                    set_months = 12 + set_months
                else:
                    set_years = research_date.year - int(age[0])  # 調査予定日の年から年齢（年）を引く

                # 調査予定日を基準に年齢の年・月を引いてから日を引き算
                try:
                    bd = research_date.replace(year=set_years, month=set_months)
                    # 調査予定日から年と月を計算後に変更
                    bd -= timedelta(days=set_days)  # 変更後から日数を変更

                # 調査予定日が29-31日で、変更後の月が2月（29-31日）、4・6・9・11月（31日）だとエラー（存在しないため）
                except ValueError:
                    # 調査予定日から年と月を計算後に変更、日は変更後の月末にとりあえず指定
                    bd = research_date.replace(year=set_years, month=set_months,
                                      day=cal.monthrange(set_years, set_months)[1])
                    bd += timedelta(days=research_date.day - bd.day)
                    # とりあえず変更した日数（減らした日数分）を追加
                    bd -= timedelta(days=set_days)  # 変更後から日数を変更

                bd = date(bd.year, bd.month, bd.day)
                cal_result.append(bd)

            # 結果リストの長さでモード"固定"と"範囲"を判定して出力を変える
            if len(cal_result) > 1:
                result = ["モード2：アポ取りモード",
                          " ",
                          "対象になる誕生日の範囲",
                          str(cal_result[1]) + " ～ " + str(cal_result[0])]
            else:
                result = ["モード2：アポ取りモード",
                          " ",
                          "対象になる誕生日",
                          str(cal_result[0])]

        else:
            result = ["Error!"]

        return result

    # 対象年齢と誕生日から調査予定日を推定
    def age_to_date(self):
        birthday_set = self.input_birthday.date().toString("yyyy/MM/dd")
        birthday = datetime.strptime(birthday_set, "%Y/%m/%d")
        birthday = date(birthday.year, birthday.month, birthday.day)

        # エラーチェック：半角入力と対象年齢の範囲確認
        if self.input_check_hankaku() and self.input_check_range():

            ###  メイン関数  ###

            age_list = self.get_target_age() # 対象年齢の取得
            cal_result = [] # 結果リスト

            for age in age_list:
                set_days = int(age[2])  # 年齢（日）
                set_months = birthday.month + int(age[1])  # 調査予定日の月から年齢（月）を引く

                # 引いた月の数がマイナスになる時は、年齢からもう1年引いて、月に12ヶ月足す → 再計算
                if set_months > 12:
                    set_years = birthday.year + int(age[0]) + 1
                    set_months = set_months - 12
                else:
                    set_years = birthday.year + int(age[0])  # 調査予定日の年から年齢（年）を引く

                # 誕生日を基準に年齢の年・月を足してから日を足し算
                try:
                    d = birthday.replace(year=set_years, month=set_months)  # 誕生日から年と月を計算後に変更
                    d += timedelta(days=set_days)  # 変更後から日数を変更

                # 誕生日が29-31日で、変更後の月が2月（29-31日）、4・6・9・11月（31日）だとエラー（存在しないため）
                except ValueError:
                    # 誕生日から年と月を計算後に変更、日は変更後の月末にとりあえず指定
                    d = birthday.replace(year=set_years, month=set_months,
                                   day=cal.monthrange(set_years, set_months)[1])
                    d += timedelta(days=birthday.day - d.day)  # とりあえず変更した日数（減らした日数分）を追加
                    d += timedelta(days=set_days)  # 変更後から日数を変更

                d = date(d.year, d.month, d.day)
                cal_result.append(d)

            # 結果リストの長さでモード"固定"と"範囲"を判定して出力を変える
            if len(cal_result) > 1:
                result = ["モード3：調査日決定モード",
                          " ",
                          "調査日候補の範囲",
                          str(cal_result[0]) + " ～ " + str(cal_result[1])]
            else:
                result = ["モード3：調査日決定モード",
                          " ",
                          "調査日候補",
                          str(cal_result[0])]

        else:
            result = ["Error!"]

        return result

    # モードによって計算関数をスイッチ、最終的な出力
    def calculate(self):
        # モードの先頭の数字で場合分け
        mode = int(self.change_mode.currentText()[0])
        if mode == 1:
            text = self.age_in_days()
        elif mode == 2:
            text = self.age_to_birthday()
        elif mode == 3:
            text = self.age_to_date()
        else:
            pass

        # 出力の見た目改善
        text.insert(0, "------------------------------------")
        text.append("------------------------------------")

        # リストの要素を1行ずつテキストブラウザに出力
        for i in text:
            self.textBrowser.append(i) #

    # カレンダーとのひも付けをラジオボタンで操作
    def connect_calendar(self):
        # ラジオボタンの状態をチェック
        if self.switch_research_date.isChecked():
            # なんのひも付けもない状態ではひも付けの解除ができずエラーになるのでtry & exceptでひも付けの処理だけを通す
            try:
                # 調査日入力とカレンダーをひも付け
                self.calendarWidget.clicked[QDate].connect(self.input_research_date.setDate)
                # 誕生日入力とカレンダーのひも付けを解除
                self.calendarWidget.clicked[QDate].disconnect(self.input_birthday.setDate)
            except:
                pass
        if self.switch_birthday.isChecked():
            try:
                # 調査日入力とカレンダーのひも付けを解除
                self.calendarWidget.clicked[QDate].disconnect(self.input_research_date.setDate)
                # 誕生日入力とカレンダーをひも付け
                self.calendarWidget.clicked[QDate].connect(self.input_birthday.setDate)
            except:
                pass

    # コンボボックスの操作に合わせてUI変更（使わないものをOFFに）
    def target_mode_change(self):
        mode = int(self.change_mode.currentText()[0])
        target_mode = self.switch_target_age.currentText()
        target_range = self.switch_target_range.currentText()

        # モード1：年齢計算モード（調査日・誕生日→年齢）
        if mode == 1:
            self.input_target1_years.setEnabled(False)
            self.input_target1_months.setEnabled(False)
            self.input_target1_days.setEnabled(False)
            self.input_target2_years.setEnabled(False)
            self.input_target2_months.setEnabled(False)
            self.input_target2_days.setEnabled(False)
            self.input_birthday.setEnabled(True)
            self.input_research_date.setEnabled(True)

        # モード2：アポ取りモード（対象年齢・調査日→誕生日）
        if mode == 2:
            self.input_birthday.setEnabled(False)
            self.input_research_date.setEnabled(True)

            if target_mode == "月齢":
                if target_range == "固定":
                    self.input_target1_years.setEnabled(False)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(False)
                    self.input_target2_months.setEnabled(False)
                    self.input_target2_days.setEnabled(False)
                else: # target_range == "範囲"
                    self.input_target1_years.setEnabled(False)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(False)
                    self.input_target2_months.setEnabled(True)
                    self.input_target2_days.setEnabled(True)
            else: # target_mode == "年齢"
                if target_range == "固定":
                    self.input_target1_years.setEnabled(True)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(False)
                    self.input_target2_months.setEnabled(False)
                    self.input_target2_days.setEnabled(False)
                else: # target_range == "範囲"
                    self.input_target1_years.setEnabled(True)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(True)
                    self.input_target2_months.setEnabled(True)
                    self.input_target2_days.setEnabled(True)

        # モード3：調査日決定モード（対象年齢・誕生日→調査日）
        if mode == 3:
            self.input_birthday.setEnabled(True)
            self.input_research_date.setEnabled(False)

            if target_mode == "月齢":
                if target_range == "固定":
                    self.input_target1_years.setEnabled(False)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(False)
                    self.input_target2_months.setEnabled(False)
                    self.input_target2_days.setEnabled(False)
                else: # target_range == "範囲"
                    self.input_target1_years.setEnabled(False)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(False)
                    self.input_target2_months.setEnabled(True)
                    self.input_target2_days.setEnabled(True)
            else: # target_mode == "年齢"
                if target_range == "固定":
                    self.input_target1_years.setEnabled(True)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(False)
                    self.input_target2_months.setEnabled(False)
                    self.input_target2_days.setEnabled(False)
                else: # target_range == "範囲"
                    self.input_target1_years.setEnabled(True)
                    self.input_target1_months.setEnabled(True)
                    self.input_target1_days.setEnabled(True)
                    self.input_target2_years.setEnabled(True)
                    self.input_target2_months.setEnabled(True)
                    self.input_target2_days.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv) # キー入力やイベント発生などのリソース管理
    main_window = MainWindow()   # ウィンドウインスタンスの作成
    main_window.show()           # ウィンドウの描画
    sys.exit(app.exec_())        # アプリのイベントループが終わったらプログラムを修了