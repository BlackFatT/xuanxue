def calculate_tiangan_shishen(day_master, other_gan):
    """
    根据日元天干计算其他天干的十神

    参数:
        day_master: 日元天干，如"甲"
        other_gan: 其他柱的天干，如"乙"

    返回:
        十神名称，如"比肩"、"劫财"等
    """
    # 天干的阴阳属性: 阳为1，阴为0
    yin_yang = {
        '甲': 1, '乙': 0,
        '丙': 1, '丁': 0,
        '戊': 1, '己': 0,
        '庚': 1, '辛': 0,
        '壬': 1, '癸': 0
    }

    # 天干的五行属性
    wuxing = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 五行相生关系: 键生值
    generate = {
        '木': '火',
        '火': '土',
        '土': '金',
        '金': '水',
        '水': '木'
    }

    # 五行相克关系: 键克值
    conquer = {
        '木': '土',
        '土': '水',
        '水': '火',
        '火': '金',
        '金': '木'
    }

    # 检查输入有效性
    if day_master not in yin_yang or other_gan not in yin_yang:
        raise ValueError("输入的天干不正确，必须是甲乙丙丁戊己庚辛壬癸之一")

    # 日元的五行和阴阳
    dm_wuxing = wuxing[day_master]
    dm_yinyang = yin_yang[day_master]

    # 其他天干的五行和阴阳
    og_wuxing = wuxing[other_gan]
    og_yinyang = yin_yang[other_gan]

    # 判断十神关系
    if day_master == other_gan:
        return "比肩"
    elif dm_wuxing == og_wuxing:
        return "劫财"
    elif generate[dm_wuxing] == og_wuxing:  # 日元生其他天干
        if dm_yinyang != og_yinyang:
            return "伤官"
        else:
            return "食神"
    elif conquer[dm_wuxing] == og_wuxing:  # 日元克其他天干
        if dm_yinyang == og_yinyang:
            return "正财"
        else:
            return "偏财"
    elif conquer[og_wuxing] == dm_wuxing:  # 其他天干克日元
        if dm_yinyang != og_yinyang:
            return "正官"
        else:
            return "七杀"
    elif generate[og_wuxing] == dm_wuxing:  # 其他天干生日元
        if dm_yinyang != og_yinyang:
            return "正印"
        else:
            return "枭神"
    else:
        return "FKU！"


def calculate_dizhi_shishen(day_master, earthly_branch):
    """
        不考虑藏干，仅根据地支本气五行和日元天干计算十神

        参数:
            day_master: 日元天干（如"甲"）
            earthly_branch: 地支（如"寅"）

        返回:
            该地支对应的十神名称
        """
    # 1. 天干的阴阳属性（阳=1，阴=0）
    yin_yang = {
        '甲': 1, '乙': 0, '丙': 1, '丁': 0,
        '戊': 1, '己': 0, '庚': 1, '辛': 0,
        '壬': 1, '癸': 0
    }

    # 2. 天干对应的五行
    gan_wuxing = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火',
        '戊': '土', '己': '土', '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 3. 地支本气五行（地支最主要的五行属性，不考虑藏干）
    dizhi_wuxing = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }

    dizhi_yinyang = {
        '子': 1, '亥': 0, '寅': 1, '卯': 0,
        '辰': 1, '丑': 0, '午': 1, '巳': 0,
        '申': 1, '酉': 0, '戌': 1, '未': 0,
    }

    # 4. 五行相生相克关系
    generate = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}  # 相生：键生值
    conquer = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}  # 相克：键克值

    # 检查输入有效性
    if day_master not in yin_yang:
        raise ValueError("日元天干必须是：甲乙丙丁戊己庚辛壬癸")
    if earthly_branch not in dizhi_wuxing:
        raise ValueError("地支必须是：子丑寅卯辰巳午未申酉戌亥")

    # 获取日元的五行和阴阳
    dm_wuxing = gan_wuxing[day_master]
    dm_yin_yang = yin_yang[day_master]

    # 获取地支的本气五行
    branch_wuxing = dizhi_wuxing[earthly_branch]
    branch_yinyang = dizhi_yinyang[earthly_branch]

    # # 关键规则：根据地支本气五行与日元的关系，结合日元阴阳判断十神
    # # （注：此处简化为用地支本气五行模拟一个"虚拟天干"，其阴阳与本气五行的"阳干"一致）
    # # 例如：地支本气为"木"，虚拟天干取阳干"甲"的阴阳（1）；本气为"火"，取阳干"丙"的阴阳（1），以此类推
    # virtual_gan_yin_yang = {
    #     '木': yin_yang['甲'],  # 木的阳干为甲（阳=1）
    #     '火': yin_yang['丙'],  # 火的阳干为丙（阳=1）
    #     '土': yin_yang['戊'],  # 土的阳干为戊（阳=1）
    #     '金': yin_yang['庚'],  # 金的阳干为庚（阳=1）
    #     '水': yin_yang['壬']  # 水的阳干为壬（阳=1）
    # }[branch_wu]

    # 计算十神
    if dm_wuxing == branch_wuxing:
        # 同五行：比肩（与日元同阴阳）或劫财（与日元异阴阳）
        return "比肩" if dm_yin_yang == branch_yinyang else "劫财"
    elif generate[dm_wuxing] == branch_wuxing:
        # 日元生地支：食神（异阴阳）或伤官（同阴阳）
        return "食神" if dm_yin_yang != branch_yinyang else "伤官"
    elif conquer[dm_wuxing] == branch_wuxing:
        # 日元克地支：正财（异阴阳）或偏财（同阴阳）
        return "正财" if dm_yin_yang == branch_yinyang else "偏财"
    elif conquer[branch_wuxing] == dm_wuxing:
        # 地支克日元：正官（异阴阳）或七杀（同阴阳）
        return "正官" if dm_yin_yang != branch_yinyang else "七杀"
    elif generate[branch_wuxing] == dm_wuxing:
        # 地支生日元：正印（异阴阳）或偏印（同阴阳）
        return "正印" if dm_yin_yang == branch_yinyang else "枭神"
    else:
        return "未知"


# 获取简化的十神名称
def shortening_shishen_name(original_name):
    shishen = {'正印': '印', '枭神': '枭', '正官': '官', '七杀': '杀',
               '食神': '食', '伤官': '伤', '正财': '财', '偏财': '才', '比肩': '比',
               '劫财': '劫'}

    # 检查输入有效性
    if original_name not in shishen:
        raise ValueError("what is the fuck!!!")

    return shishen[original_name]


# 同时计算天干地支的十神
def calculate_ganzhi_shishen(day_master, ganzhi):
    tiangan_ret = calculate_tiangan_shishen(day_master, ganzhi[0])
    dizhi_ret = calculate_dizhi_shishen(day_master, ganzhi[1])
    return shortening_shishen_name(tiangan_ret)+shortening_shishen_name(dizhi_ret)


def calculate_empty_death(day_gan_zhi):
    """
    根据日柱天干地支计算空亡地支

    参数:
        day_gan_zhi: 日柱干支，如"甲子"、"丙寅"等

    返回:
        空亡的地支列表，如['戌', '亥']
    """
    # 六十甲子顺序表（每10个为一旬，共6旬）
    sixty_jiazi = [
        # 甲子旬（空亡：戌、亥）
        '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
        # 甲戌旬（空亡：申、酉）
        '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
        # 甲申旬（空亡：午、未）
        '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
        # 甲午旬（空亡：辰、巳）
        '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
        # 甲辰旬（空亡：寅、卯）
        '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
        # 甲寅旬（空亡：子、丑）
        '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
    ]

    # 各旬对应的空亡地支（索引与上述六十甲子的旬对应）
    xun_empty = [
        ['戌', '亥'],  # 甲子旬
        ['申', '酉'],  # 甲戌旬
        ['午', '未'],  # 甲申旬
        ['辰', '巳'],  # 甲午旬
        ['寅', '卯'],  # 甲辰旬
        ['子', '丑']  # 甲寅旬
    ]

    # 检查输入有效性
    if day_gan_zhi not in sixty_jiazi:
        raise ValueError("无效的日柱干支，请输入正确的六十甲子组合（如'甲子'、'丙寅'）")

    # 确定日柱所在的旬（每10个为一旬）
    index = sixty_jiazi.index(day_gan_zhi)
    xun_index = index // 10  # 0-5，对应6个旬

    # 将列表转换为无分隔符的字符串
    return ''.join(xun_empty[xun_index])


def get_nayin(ganzhi):
    """
    根据干支组合生成对应的纳音五行字符串

    参数:
        ganzhi: 干支组合，如"甲子"、"乙丑"等

    返回:
        纳音五行字符串，如"海中金"、"炉中火"等
    """
    # 六十甲子纳音表
    nayin_table = {
        # 甲子旬
        '甲子': '海中金', '乙丑': '海中金',
        '丙寅': '炉中火', '丁卯': '炉中火',
        '戊辰': '大林木', '己巳': '大林木',
        '庚午': '路旁土', '辛未': '路旁土',
        '壬申': '剑锋金', '癸酉': '剑锋金',

        # 甲戌旬
        '甲戌': '山头火', '乙亥': '山头火',
        '丙子': '涧下水', '丁丑': '涧下水',
        '戊寅': '城头土', '己卯': '城头土',
        '庚辰': '白蜡金', '辛巳': '白蜡金',
        '壬午': '杨柳木', '癸未': '杨柳木',

        # 甲申旬
        '甲申': '泉中水', '乙酉': '泉中水',
        '丙戌': '屋上土', '丁亥': '屋上土',
        '戊子': '霹雳火', '己丑': '霹雳火',
        '庚寅': '松柏木', '辛卯': '松柏木',
        '壬辰': '长流水', '癸巳': '长流水',

        # 甲午旬
        '甲午': '沙中金', '乙未': '沙中金',
        '丙申': '山下火', '丁酉': '山下火',
        '戊戌': '平地木', '己亥': '平地木',
        '庚子': '壁上土', '辛丑': '壁上土',
        '壬寅': '金箔金', '癸卯': '金箔金',

        # 甲辰旬
        '甲辰': '佛灯火', '乙巳': '佛灯火',
        '丙午': '天河水', '丁未': '天河水',
        '戊申': '大驿土', '己酉': '大驿土',
        '庚戌': '钗钏金', '辛亥': '钗钏金',
        '壬子': '桑柘木', '癸丑': '桑柘木',

        # 甲寅旬
        '甲寅': '大溪水', '乙卯': '大溪水',
        '丙辰': '沙中土', '丁巳': '沙中土',
        '戊午': '天上火', '己未': '天上火',
        '庚申': '石榴木', '辛酉': '石榴木',
        '壬戌': '大海水', '癸亥': '大海水'
    }

    # 检查输入有效性
    if ganzhi not in nayin_table:
        raise ValueError(f"无效的干支组合: {ganzhi}，请输入正确的六十甲子")

    return nayin_table[ganzhi]


def get_changsheng12gong(day_gan, earthly_branch):
    """
        根据日干和具体地支，返回该地支对应的十二长生宫名称

        参数:
            day_gan: 日干，如"甲"、"乙"等
            earthly_branch: 地支，如"寅"、"亥"等

        返回:
            字符串，该地支对应的十二长生宫状态（如"长生"、"帝旺"等）
        """
    # 日干对应的五行属性
    gan_wuxing = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 十二长生宫顺序
    longevity_order = [
        '长生', '沐浴', '冠带', '临官', '帝旺',
        '衰', '病', '死', '墓', '绝', '胎', '养'
    ]

    # 不同五行对应的地支长生十二宫起始位置
    wuxing_longevity_base = {
        '木': '亥',  # 木长生在亥
        '火': '寅',  # 火长生在寅
        '土': '寅',  # 土长生在寅（与火同）
        '金': '巳',  # 金长生在巳
        '水': '申'  # 水长生在申
    }

    # 十二地支固定顺序
    earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳',
                        '午', '未', '申', '酉', '戌', '亥']

    # 检查输入有效性
    if day_gan not in gan_wuxing:
        raise ValueError("无效的日干，请输入甲乙丙丁戊己庚辛壬癸之一")
    if earthly_branch not in earthly_branches:
        raise ValueError("无效的地支，请输入子丑寅卯辰巳午未申酉戌亥之一")

    # 获取日干五行
    wuxing = gan_wuxing[day_gan]

    # 找到长生宫对应的地支索引
    base_branch = wuxing_longevity_base[wuxing]
    base_index = earthly_branches.index(base_branch)

    # 计算目标地支的索引
    target_index = earthly_branches.index(earthly_branch)

    # 计算对应的长生宫索引（通过相对位置差）
    palace_index = (target_index - base_index) % 12

    # 返回对应的长生宫名称
    return longevity_order[palace_index]

#获取天干地支的颜色
def get_element_color(name):
    """
    根据天干或地支的名称，返回对应的五行RGB颜色

    参数:
        name: 天干（甲乙丙丁戊己庚辛壬癸）或地支（子丑寅卯辰巳午未申酉戌亥）的名称

    返回:
        tuple: RGB颜色值，如(255, 0, 0)；若输入无效则返回None
    """
    # 五行对应的RGB颜色
    element_colors = {
        '木': (0, 128, 0),  # 绿色
        '火': (255, 0, 0),  # 红色
        '土': (165, 42, 42),  # 棕色
        '金': (255, 215, 0),  # 白色
        '水': (0, 0, 255)  # 蓝色
    }

    # 天干对应的五行
    heavenly_stems = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 地支对应的五行
    earthly_branches = {
        '子': '水', '丑': '土',
        '寅': '木', '卯': '木',
        '辰': '土', '巳': '火',
        '午': '火', '未': '土',
        '申': '金', '酉': '金',
        '戌': '土', '亥': '水'
    }

    # 统一转换为中文大写（防止输入小写）
    name = name.strip()

    # 判断输入类型并获取五行属性
    if name in heavenly_stems:
        element = heavenly_stems[name]
    elif name in earthly_branches:
        element = earthly_branches[name]
    else:
        print(f"无效的输入: {name}，请输入正确的天干或地支")
        return None

    # 返回对应的RGB颜色
    return element_colors[element]


def get_jie_name(index):
    """
    根据索引号获取对应的节气（节）名称

    参数:
        index: 索引号，范围0-11（0对应第一个节“立春”，11对应最后一个节“小寒”）

    返回:
        str: 节气名称；若索引无效则返回None
    """
    # 一年中12个“节”的顺序列表（每月第一个节气）
    solar_terms = [
        "立春",  # 0：正月节（2月4日左右）
        "惊蛰",  # 1：二月节（3月6日左右）
        "清明",  # 2：三月节（4月5日左右）
        "立夏",  # 3：四月节（5月6日左右）
        "芒种",  # 4：五月节（6月6日左右）
        "小暑",  # 5：六月节（7月7日左右）
        "立秋",  # 6：七月节（8月8日左右）
        "白露",  # 7：八月节（9月8日左右）
        "寒露",  # 8：九月节（10月8日左右）
        "立冬",  # 9：十月节（11月7日左右）
        "大雪",  # 10：十一月节（12月7日左右）
        "小寒"  # 11：十二月节（1月6日左右）
    ]

    # 校验索引范围
    if isinstance(index, int) and 0 <= index < len(solar_terms):
        return solar_terms[index]
    else:
        print(f"无效索引：{index}，请输入0-11之间的整数")
        return None

# # 测试函数
# if __name__ == "__main__":
#     # 测试不同日干的长生十二宫
#     test_gans = ['甲', '丙', '戊', '庚', '壬']  # 阳干示例
#
#     for gan in test_gans:
#         print(f"日干 {gan} 的十二地支长生十二宫：")
#         palace = get_longevity_palace(gan)
#         # 按地支顺序打印
#         for branch in ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']:
#             print(f"{branch}: {palace[branch]}", end='  ')
#         print("\n" + "-" * 50)

# # 测试函数
# if __name__ == "__main__":
#     # 测试案例
#     test_cases = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳',
#                   '庚午', '癸酉', '甲戌', '壬午', '庚寅', '癸亥']
#
#     for gz in test_cases:
#         print(f"{gz} → {get_nayin(gz)}")

# # 测试函数
# if __name__ == "__main__":
#     # 测试案例：不同日柱对应的空亡
#     test_cases = [
#         '甲子', '癸酉',  # 甲子旬，空亡戌亥
#         '甲戌', '癸未',  # 甲戌旬，空亡申酉
#         '甲申', '癸巳',  # 甲申旬，空亡午未
#         '甲午', '癸卯',  # 甲午旬，空亡辰巳
#         '甲辰', '癸丑',  # 甲辰旬，空亡寅卯
#         '甲寅', '癸亥',  # 甲寅旬，空亡子丑
#         '壬午'
#     ]
#
#     for gan_zhi in test_cases:
#         empty = calculate_empty_death(gan_zhi)
#         print(f"日柱 {gan_zhi} 的空亡地支：{empty}")

#     # 测试：以"甲"为日元，计算所有地支的十神
#     if __name__ == "__main__":
#         day_master = "甲"  # 日元为甲木（阳木）
#         branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
#
#         print(f"以{day_master}为日元，地支（本气）对应的十神：")
#         for branch in branches:
#             print(f"{branch} → {calculate_earthly_branch_ten_gods_simple(day_master, branch)}")
#
#
# # 测试函数
# if __name__ == "__main__":
#     # 以甲木为日元的测试案例
#     day_master = "甲"
#     test_cases = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
#
#     print(f"以{day_master}为日元的十神关系:")
#     for gan in test_cases:
#         print(f"{gan} -> {calculate_tiangan_shishen(day_master, gan)}")

#统计干支的五行个数,按照排序后的结果进行输出字符串
def count_wuxing_fullstring(tiangan_dizhi_list):
    """
    计算天干地支对应的五行数量

    参数:
        tiangan_list: 天干列表，如 ['甲', '乙', '丙']
        dizhi_list: 地支列表，如 ['子', '丑', '寅']

    返回:
        dict: 五行数量统计，格式 {'木': 2, '火': 1, '土': 0, '金': 3, '水': 2}
    """
    # 天干与五行对应关系
    tiangan_wuxing = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }

    # 地支与五行对应关系
    dizhi_wuxing = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }

    # 初始化五行计数
    wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}

    # 统计天干对应的五行
    for tg_dizhi in tiangan_dizhi_list:
        if tg_dizhi in tiangan_wuxing:
            wuxing = tiangan_wuxing[tg_dizhi]
            wuxing_count[wuxing] += 1

        if tg_dizhi in dizhi_wuxing:
            wuxing = dizhi_wuxing[tg_dizhi]
            wuxing_count[wuxing] += 1
    #
    # # 统计地支对应的五行
    # for dz in dizhi_list:
    #     if dz in dizhi_wuxing:
    #         wuxing = dizhi_wuxing[dz]
    #         wuxing_count[wuxing] += 1
    # 将字典转换为列表，再按数量降序排序
    sorted_by_count = sorted(wuxing_count.items(), key=lambda x: x[1], reverse=True)

    fullStr = ""
    for wuxing, count in sorted_by_count:
        # print(f"{wuxing}：{count}个")
        fullStr += f"{count}{wuxing}"

    return fullStr
