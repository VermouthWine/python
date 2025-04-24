from datetime import datetime, timedelta

# 工期を「日 時間 分」で入力させる
def get_input(prompt):
    user_input = input(prompt).strip()
    if user_input == '':  # 入力が空の場合
        return 0
    return int(user_input)

# 入力を受け取る
days = get_input('工期の日数を入力: ')
hours = get_input('工期の時間を入力: ')
minutes = get_input('工期の分を入力: ')
available_hours = get_input('利用可能までの時間を入力: ')
available_minutes = get_input('利用可能までの分を入力: ')

# 入力された工期を全て時間単位に換算
total_hours = days * 24 + hours + minutes / 60
available_time = available_hours + available_minutes / 60

# 8時間勤務を考慮して、短縮した工期を計算
shorted_period = ((total_hours - available_time) - (total_hours * 8 / 24)) / 24

# 小数点1位で表示
shorted_period = float('{0:.1f}'.format(shorted_period))

# 日数と時間に分ける
shorted_days = int(shorted_period)  # 日数部分（整数）
shorted_hours = round((shorted_period - shorted_days) * 24)  # 時間部分（小数点以下を時間に換算）

# 現在の日付から工事終了日を計算
current_date = datetime.now()
end_date = current_date + timedelta(days=shorted_period)

# 短縮された期間を計算（元の工期と短縮後の工期の差）
reduced_time = total_hours / 24 - shorted_period
reduced_time = float('{0:.1f}'.format(reduced_time))

# 短縮された工期を日数と時間に分ける
reduced_days = int(reduced_time)
reduced_hours = round((reduced_time - reduced_days) * 24)

# 結果を表示
print(f'短縮前: {days}日 {hours}時間 {minutes}分')
print(f'短縮された期間: {reduced_time}日 ({reduced_days}日{reduced_hours}時間)')
print(f'短縮後: {shorted_period}日 ({shorted_days}日{shorted_hours}時間)')
print(f'工事終了予定日: {end_date.strftime("%Y-%m-%d %H:%M:%S")}')
