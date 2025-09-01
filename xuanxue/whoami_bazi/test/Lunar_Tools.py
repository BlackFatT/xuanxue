

# # 通过指定年月日初始化阴历
# lunar = Lunar.fromYmd(1986, 4, 21)
#
# # 打印阴历
# print(lunar.toFullString())
#
# # 阴历转阳历并打印
# print(lunar.getSolar().toFullString())

from lunar_python import Lunar
from lunar_python import LunarYear

lunarYear = LunarYear.fromYear(2020)

# // 获取月份
months = lunarYear.getMonths()
for month in months:
  print(month.toString())


print("\n\n----------------------")
# // 获取当年月份
months = lunarYear.getMonthsInYear()
# for(i=0, j=months.length; i<j; i++){
#   print(months[i].toString())
# }
for month in months:
  print(month.toString())


# # 示例：列出2024年所有农历日期
# all_lunar_dates = list_lunar_dates(2024)
# for month, day, leap in all_lunar_dates:
#     leap_str = "闰" if leap else ""
#     print(f"{leap_str}{month}月{day}日")