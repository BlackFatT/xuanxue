from datetime import datetime, timedelta


def calculate_time_offset(longitude:float, timezone_center=120):
    """
    根据经度计算真太阳时与标准时区时间的偏差（分钟）

    参数:
        longitude: 当地经度（浮点数，东经为正，西经为负）
        timezone_center: 所在时区的中央经度（默认120，即东八区北京时间）

    返回:
        float: 时间偏差（分钟），正值表示当地时间超前标准时，负值表示滞后
    """
    # 计算经度差（当地经度 - 时区中央经度）
    longitude_diff = longitude - timezone_center

    # 每度经度对应4分钟偏差（经度每向东1度，时间快4分钟）
    time_offset = longitude_diff * 4

    return time_offset


def datetime_add_minutes(datetime_str:str, minutes:float):
    """
    处理包含日期的时间加减（支持跨天），返回24小时制的日期时间字符串

    参数:
        datetime_str: 日期时间字符串，格式 "YYYY-MM-DD HH:MM:SS"
        minutes: 要加减的分钟数（可正可负）

    返回:
        str: 运算后的日期时间字符串 "YYYY-MM-DD HH:MM:SS"（24小时制）
    """
    # 解析字符串为 datetime 对象（包含日期和时间）
    try:
        dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"无效的格式: {datetime_str}，请使用 'YYYY-MM-DD HH:MM:SS'")

    # 加减分钟（timedelta自动处理跨天/跨月）
    adjusted_dt = dt_obj + timedelta(minutes=minutes)

    # 以24小时制格式化输出（确保HH为00-23）
    # return adjusted_dt.strftime("%Y-%m-%d %H:%M:%S")
    return adjusted_dt

# # 使用示例
# if __name__ == "__main__":
#     # 正常时间加法（不跨天）
#     print(datetime_add_minutes("2023-10-01 08:12:33", 45))
#     # 输出：2023-10-01 08:57:33
#
#     # 跨天加法（当天23点+2小时）
#     print(datetime_add_minutes("2023-12-31 23:30:00", 90))  # 加90分钟=1.5小时
#     # 输出：2024-01-01 01:00:00（自动跨天，年份也变了）
#
#     # 跨天减法（当天0点-30分钟）
#     print(datetime_add_minutes("2024-02-29 00:10:00", -30))  # 减30分钟
#     # 输出：2024-02-28 23:40:00（闰年2月29日的前一天是28日）
#
#     # 跨月减法（3月1日-1天）
#     print(datetime_add_minutes("2023-03-01 01:00:00", -1440))  # 减1440分钟=24小时
#     # 输出：2023-02-28 01:00:00（自动处理月份天数差异）
#
#     # 带小数的分钟（加1.5分钟=90秒）
#     print(datetime_add_minutes("2023-05-15 12:30:00", 1.5))
#     # 输出：2023-05-15 12:31:30


# # 使用示例
# if __name__ == "__main__":
#     # 示例1：北京（东经116.4°，东八区中央经度120°）
#     beijing_lon = 116.4
#     offset1 = calculate_time_offset(beijing_lon)
#     print(f"北京（东经{beijing_lon}°）的时间偏差：{offset1:.2f}分钟")
#     # 输出：北京（东经116.4°）的时间偏差：-14.40分钟（比北京时间晚14.4分钟）
#
#     # 示例2：东京（东经139.8°，东八区计算）
#     tokyo_lon = 139.8
#     offset2 = calculate_time_offset(tokyo_lon)
#     print(f"东京（东经{tokyo_lon}°）的时间偏差：{offset2:.2f}分钟")
#     # 输出：东京（东经139.8°）的时间偏差：79.20分钟（比北京时间早79.2分钟）
#
#     # 示例3：自定义时区（如东七区，中央经度105°）
#     paris_lon = 2.35  # 巴黎经度（东经2.35°）
#     offset3 = calculate_time_offset(paris_lon, timezone_center=105)
#     print(f"巴黎（东经{paris_lon}°）相对东七区的时间偏差：{offset3:.2f}分钟")
#     # 输出：巴黎（东经2.35°）相对东七区的时间偏差：-410.60分钟
