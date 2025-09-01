class LeapDateTimeParser:
    def __init__(self, datetime_str):
        """
        初始化解析器，传入带闰月（负数月份）的日期时间字符串

        参数:
            datetime_str: 格式如 "1988/-12/13 08:12:33" 的字符串
        """
        self.datetime_str = datetime_str
        # 解析字符串并存储各部分（字符串类型）
        self._parse()

    def _parse(self):
        """内部解析方法，提取各部分并保持字符串类型"""
        try:
            # 分割日期和时间
            date_part, time_part = self.datetime_str.split(' ')

            # 分割年、月、日（保留原始字符串，包括负号）
            year_str, month_str, day_str = date_part.split('/')

            # 分割时、分、秒（保留原始字符串）
            hour_str, minute_str, second_str = time_part.split(':')

            # 存储为实例变量（均为字符串类型）
            self._year = year_str
            self._month = month_str
            self._day = day_str
            self._hour = hour_str
            self._minute = minute_str
            self._second = second_str

        except Exception as e:
            raise ValueError(f"无效的日期时间格式: {self.datetime_str}，错误: {e}")

    def getYear(self):
        """返回年份（字符串类型）"""
        return self._year

    def getYear_int(self):
        """返回年份（字符串类型）"""
        return int(self._year)

    def getMonth(self):
        """返回月份（字符串类型，保留负号）"""
        return self._month

    def getMonth_int(self):
        """返回月份（字符串类型，保留负号）"""
        return str(self._month)

    def getDay(self):
        """返回日期（字符串类型）"""
        return self._day

    def getDay_int(self):
        """返回日期（字符串类型）"""
        return str(self._day)

    def getHour(self):
        """返回小时（字符串类型）"""
        return self._hour

    def getHour_int(self):
        """返回小时（字符串类型）"""
        return int(self._hour)

    def getMinute(self):
        """返回分钟（字符串类型）"""
        return self._minute

    def getMinute_int(self):
        """返回分钟（字符串类型）"""
        return int(self._minute)

    def getSecond(self):
        """返回秒（字符串类型）"""
        return self._second

    def getSecond_int(self):
        """返回秒（字符串类型）"""
        return int(self._second)


# # 使用示例
# if __name__ == "__main__":
#     # 测试输入字符串
#     input_str = "1988/-12/13 08:12:33"
#
#     # 创建解析器实例
#     parser = LeapDateTimeParser(input_str)
#
#     # 调用各方法获取字符串类型的结果
#     print("年份:", parser.getYear(), type(parser.getYear()))  # 1988 <class 'str'>
#     print("月份:", parser.getMonth(), type(parser.getMonth()))  # -12 <class 'str'>
#     print("日期:", parser.getDay(), type(parser.getDay()))  # 13 <class 'str'>
#     print("小时:", parser.getHour(), type(parser.getHour()))  # 08 <class 'str'>
#     print("分钟:", parser.getMinute(), type(parser.getMinute()))  # 12 <class 'str'>
#     print("秒:", parser.getSecond(), type(parser.getSecond()))  # 33 <class 'str'>
#
#     # 测试另一个案例
#     input_str2 = "2000/3/5 9:05:7"
#     parser2 = LeapDateTimeParser(input_str2)
#     print("\n另一个案例的月份:", parser2.getMonth())  # 3
#     print("另一个案例的小时:", parser2.getHour())  # 9
