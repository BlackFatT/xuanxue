def parse_leap_datetime(datetime_str):
    """
    方法1：解析带闰月（负数月份）的日期时间字符串
    返回包含年月日时分秒的字典，保留月份的负号

    参数:
        datetime_str: 格式如 "1988/-12/13 08:12:33" 的字符串

    返回:
        dict: 包含 year, month, day, hour, minute, second 的字典
    """
    # 分割日期和时间部分
    date_part, time_part = datetime_str.split(' ')

    # 分割年、月、日（处理负号）
    year_str, month_str, day_str = date_part.split('/')

    # 分割时、分、秒
    hour_str, minute_str, second_str = time_part.split(':')

    # 转换为对应类型并返回
    return {
        'year': int(year_str),
        'month': int(month_str),  # 保留负号
        'day': int(day_str),
        'hour': int(hour_str),
        'minute': int(minute_str),
        'second': int(second_str)
    }


def generate_leap_datetime(year, month, day, hour, minute, second):
    """
    方法2：根据年月日时分秒生成带闰月（支持负数月份）的日期时间字符串
    格式为 "YYYY/MM/DD HH:MM:SS"，其中MM可以是负数（如-12）

    参数:
        year: 年份（整数）
        month: 月份（整数，可负数表示闰月）
        day: 日期（整数）
        hour: 小时（整数）
        minute: 分钟（整数）
        second: 秒（整数）

    返回:
        str: 格式化后的日期时间字符串
    """
    # 格式化日期部分（年/月/日），月份保留原始符号
    date_part = f"{year}/{month}/{day}"

    # 格式化时间部分（时:分:秒），确保两位数显示
    time_part = f"{hour:02d}:{minute:02d}:{second:02d}"

    # 拼接并返回
    return f"{date_part} {time_part}"


# 测试示例
if __name__ == "__main__":
    # 测试解析功能
    test_str = "1988/-12/13 08:12:33"
    parsed = parse_leap_datetime(test_str)
    print("解析结果:")
    print(parsed)
    # 输出: {'year': 1988, 'month': -12, 'day': 13, 'hour': 8, 'minute': 12, 'second': 33}

    # 测试生成功能
    generated = generate_leap_datetime(
        year=2000,
        month=-4,  # 负号表示闰月
        day=5,
        hour=15,
        minute=3,
        second=7
    )
    print("\n生成结果:")
    print(generated)  # 输出: "2000/-4/5 15:03:07"
