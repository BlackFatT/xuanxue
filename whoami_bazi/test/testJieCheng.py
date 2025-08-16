# def factorial_iterative(n):
#     result = 1
#     for i in range(1, n + 1):
#         result *= i
#     return result
#
#
# num = 5
# print(f"{num} 的阶乘是: {factorial_iterative(num)}")

# 定义一个包含 int 和 string 类型键值对的字典
tiangan_dict = {
    1: "甲",
    2: "乙",
    3: "丙",
    4: "丁",
    5: "戊",
    6: "己",
    7: "庚",
    8: "辛",
    9: "壬",
    10: "癸"
}

#天冲地冲
ganzhi_tianchongdichong_dict = {
    "甲子": "庚午", "甲寅": "庚申", "甲辰": "庚戌", "甲午": "庚子", "甲申": "庚寅", "甲戌": "庚辰",
    "乙丑": "辛未", "乙卯": "辛酉", "乙巳": "辛亥", "乙未": "辛丑", "乙酉": "辛卯", "乙亥": "辛巳",
    "丙子": "壬午", "丙寅": "壬申", "丙辰": "壬戌", "丙午": "壬子", "丙申": "壬寅", "丙戌": "壬辰",
    "丁丑": "癸未", "丁卯": "癸酉", "丁巳": "癸亥", "丁未": "癸丑", "丁酉": "癸卯", "丁亥": "癸巳",
    # "戊子": "庚午", "戊寅": "庚申", "戊辰": "庚戌", "戊午": "庚子", "戊申": "庚寅", "戊戌": "庚辰",
    "庚子": "甲午", "庚寅": "甲申", "庚辰": "甲戌", "庚午": "甲子", "庚申": "甲寅", "庚戌": "甲辰",
    "辛丑": "乙未", "辛卯": "乙酉", "辛巳": "乙亥", "辛未": "乙丑", "辛酉": "乙卯", "辛亥": "乙巳",
    "壬子": "丁午", "壬寅": "丁申", "壬辰": "丁戌", "壬午": "丁子", "壬申": "丁寅", "壬戌": "丁辰",
    "癸丑": "戊未", "癸卯": "戊酉", "癸巳": "戊亥", "癸未": "戊丑", "癸酉": "戊卯", "癸亥": "戊巳"
}

ganzhi_tianhedihe_dict = {
    "甲子": "己丑", "甲寅": "己亥", "甲辰": "己酉", "甲午": "己未", "甲申": "己巳", "甲戌": "己卯",
    "乙丑": "庚子", "乙卯": "庚戌", "乙巳": "庚辰", "乙未": "庚午", "乙酉": "庚辰", "乙亥": "庚寅",
    "丙子": "辛丑", "丙寅": "辛亥", "丙辰": "辛酉", "丙午": "辛未", "丙申": "辛巳", "丙戌": "辛卯",
    "丁丑": "壬子", "丁卯": "壬戌", "丁巳": "壬辰", "丁未": "壬午", "丁酉": "壬辰", "丁亥": "壬寅",
    "戊子": "癸丑", "戊寅": "癸亥", "戊辰": "癸酉", "戊午": "癸未", "戊申": "癸巳", "戊戌": "癸卯",
    "己丑": "庚子", "己卯": "庚戌", "己巳": "庚辰", "己未": "庚午", "己酉": "庚辰", "己亥": "庚寅",
    "庚子": "己丑", "庚寅": "己亥", "庚辰": "己酉", "庚午": "己未", "庚申": "己巳", "庚戌": "己卯",
    "辛丑": "丙子", "辛卯": "丙戌", "辛巳": "丙辰", "辛未": "丙午", "辛酉": "丙辰", "辛亥": "丙寅",
    "壬子": "己丑", "壬寅": "己亥", "壬辰": "己酉", "壬午": "己未", "壬申": "己巳", "壬戌": "己卯",
    "癸丑": "戊子", "癸卯": "戊戌", "癸巳": "戊辰", "癸未": "戊午", "癸酉": "戊辰", "癸亥": "戊寅",
}

ganzhi_tianshengdihe_dict = {
    "甲子": "己丑", "甲寅": "己亥", "甲辰": "己酉", "甲午": "己未", "甲申": "己巳", "甲戌": "己卯",
    "乙丑": "庚子", "乙卯": "庚戌", "乙巳": "庚辰", "乙未": "庚午", "乙酉": "庚辰", "乙亥": "庚寅",
    "丙子": "辛丑", "丙寅": "辛亥", "丙辰": "辛酉", "丙午": "辛未", "丙申": "辛巳", "丙戌": "辛卯",
    "丁丑": "壬子", "丁卯": "壬戌", "丁巳": "壬辰", "丁未": "壬午", "丁酉": "壬辰", "丁亥": "壬寅",
    "戊子": "癸丑", "戊寅": "癸亥", "戊辰": "癸酉", "戊午": "癸未", "戊申": "癸巳", "戊戌": "癸卯",
    "己丑": "庚子", "己卯": "庚戌", "己巳": "庚辰", "己未": "庚午", "己酉": "庚辰", "己亥": "庚寅",
    "庚子": "己丑", "庚寅": "己亥", "庚辰": "己酉", "庚午": "己未", "庚申": "己巳", "庚戌": "己卯",
    "辛丑": "丙子", "辛卯": "丙戌", "辛巳": "丙辰", "辛未": "丙午", "辛酉": "丙辰", "辛亥": "丙寅",
    "壬子": "己丑", "壬寅": "己亥", "壬辰": "己酉", "壬午": "己未", "壬申": "己巳", "壬戌": "己卯",
    "癸丑": "戊子", "癸卯": "戊戌", "癸巳": "戊辰", "癸未": "戊午", "癸酉": "戊辰", "癸亥": "戊寅",
}

ganzhi_tiankedichong_dict = {
    "甲子": "己丑", "甲寅": "己亥", "甲辰": "己酉", "甲午": "己未", "甲申": "己巳", "甲戌": "己卯",
    "乙丑": "庚子", "乙卯": "庚戌", "乙巳": "庚辰", "乙未": "庚午", "乙酉": "庚辰", "乙亥": "庚寅",
    "丙子": "辛丑", "丙寅": "辛亥", "丙辰": "辛酉", "丙午": "辛未", "丙申": "辛巳", "丙戌": "辛卯",
    "丁丑": "壬子", "丁卯": "壬戌", "丁巳": "壬辰", "丁未": "壬午", "丁酉": "壬辰", "丁亥": "壬寅",
    "戊子": "癸丑", "戊寅": "癸亥", "戊辰": "癸酉", "戊午": "癸未", "戊申": "癸巳", "戊戌": "癸卯",
    "己丑": "庚子", "己卯": "庚戌", "己巳": "庚辰", "己未": "庚午", "己酉": "庚辰", "己亥": "庚寅",
    "庚子": "己丑", "庚寅": "己亥", "庚辰": "己酉", "庚午": "己未", "庚申": "己巳", "庚戌": "己卯",
    "辛丑": "丙子", "辛卯": "丙戌", "辛巳": "丙辰", "辛未": "丙午", "辛酉": "丙辰", "辛亥": "丙寅",
    "壬子": "己丑", "壬寅": "己亥", "壬辰": "己酉", "壬午": "己未", "壬申": "己巳", "壬戌": "己卯",
    "癸丑": "戊子", "癸卯": "戊戌", "癸巳": "戊辰", "癸未": "戊午", "癸酉": "戊辰", "癸亥": "戊寅",
}

dizhi_dict = {
    1: "子",
    2: "丑",
    3: "寅",
    4: "卯",
    5: "辰",
    6: "巳",
    7: "午",
    8: "未",
    9: "申",
    10: "酉",
    11: "戌",
    12: "亥"
}

# 天干五行映射（甲木、乙木...）
tiangan_wuxing = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 地支五行映射（含主气和余气）
dizhi_wuxing = {
    '子': ['水'],
    '丑': ['土'],
    '寅': ['木'],
    '卯': ['木'],
    '辰': ['土'],
    '巳': ['火'],
    '午': ['火'],
    '未': ['土'],
    '申': ['金'],
    '酉': ['金'],
    '戌': ['土'],
    '亥': ['水']
}

#天干相冲
tiangan_xiangchong_dict = {
    '甲':'庚','乙':'辛','丙':'壬','丁':'癸'
}

#天干相合
tiangan_xianghe_dict = {
    '甲':'己','乙':'庚','丙':'辛','丁':'壬','戊':'癸'
}

#地支相冲
dizhi_xiangchong_dict = {
    '子':'午','丑':'未','寅':'申','卯':'酉','辰':'戌','巳':'亥'
}

#地支相合
dizhi_xianghe_dict = {
    '子':'丑','寅':'亥','卯':'戌','辰':'酉','巳':'申','午':'未'
}

class ganzhi:
    def __init__(self,tiangan,dizhi):
        self.tiangan = tiangan
        self.dizhi = dizhi
        self.ganzhi=tiangan+dizhi

    def __str__(self):
        #return f"ganzhi(tiangan={self.tiangan},dizhi={self.dizhi})"
        return f"{self.ganzhi}"

    def get_wuxing(self):
        ltiangan_wuxing = tiangan_wuxing[self.tiangan]
        ldizhi_wuxing = dizhi_wuxing[self.dizhi]
        return [ltiangan_wuxing]+ldizhi_wuxing


class bazi:
    def __init__(self,nianzhu:ganzhi,yuezhu:ganzhi,rizhu:ganzhi,shizhu:ganzhi):
        self.年柱 = nianzhu
        self.月柱 = yuezhu
        self.日柱 = rizhu
        self.时柱 = shizhu

    def __str__(self):
        return f"八字:{self.年柱} {self.月柱} {self.日柱} {self.时柱}"


def count_wuxing(bazi_instance: bazi):
    """统计八字中五行元素的个数"""
    wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    pillars = [bazi_instance.年柱, bazi_instance.月柱,
               bazi_instance.日柱, bazi_instance.时柱]

    for pillar in pillars:
        wuxing_list = pillar.get_wuxing()
        for wuxing in wuxing_list:
            wuxing_count[wuxing] += 1

    #按照从多到少进行排序
    sorted_wuxing = sorted(wuxing_count.items(), key=lambda item: item[1], reverse=True)
    print(sorted_wuxing)
    return sorted_wuxing

# def count_wuxing_ganzhi(bazi_instance: bazi,isTianganNotDozjo):
#     """统计八字中五行元素的个数"""
#     wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
#     pillars = [bazi_instance.年柱, bazi_instance.月柱,
#                bazi_instance.日柱, bazi_instance.时柱]
#
#     for pillar in pillars:
#         wuxing_list = pillar.get_wuxing()
#         for wuxing in wuxing_list:
#             wuxing_count[wuxing] += 1
#
#     #按照从多到少进行排序
#     sorted_wuxing = sorted(wuxing_count.items(), key=lambda item: item[1], reverse=True)
#     print(sorted_wuxing)
#     return sorted_wuxing

def count_tiangan_dizhi(bazi_instance: bazi):
    """分别统计八字中天干和地支元素的个数"""
    tiangan_count = {}
    dizhi_count = {}
    pillars = [bazi_instance.年柱, bazi_instance.月柱,
               bazi_instance.日柱, bazi_instance.时柱]

    for pillar in pillars:
        # 统计天干
        if pillar.tiangan in tiangan_count:
            tiangan_count[pillar.tiangan] += 1
        else:
            tiangan_count[pillar.tiangan] = 1

        # 统计地支
        if pillar.dizhi in dizhi_count:
            dizhi_count[pillar.dizhi] += 1
        else:
            dizhi_count[pillar.dizhi] = 1

    print(tiangan_count)
    print(dizhi_count)
    return tiangan_count, dizhi_count


# 天干阴阳五行属性
tiangan_yinyang_wuxing = {
    '甲': ('阳', '木'), '乙': ('阴', '木'),
    '丙': ('阳', '火'), '丁': ('阴', '火'),
    '戊': ('阳', '土'), '己': ('阴', '土'),
    '庚': ('阳', '金'), '辛': ('阴', '金'),
    '壬': ('阳', '水'), '癸': ('阴', '水')
}

# 地支阴阳五行属性
dizhi_yinyang_wuxing = {
    '子': ('阳', '水'), '丑': ('阴', '土'),
    '寅': ('阳', '木'), '卯': ('阴', '木'),
    '辰': ('阳', '土'), '巳': ('阴', '火'),
    '午': ('阳', '火'), '未': ('阴', '土'),
    '申': ('阳', '金'), '酉': ('阴', '金'),
    '戌': ('阳', '土'), '亥': ('阴', '水')
}

tiangan_shishen_dict = {
    '甲': {'甲': '比肩', '乙': '劫财', '丙': '食神', '丁': '伤官', '戊': '偏财', '己': '正财', '庚': '七杀', '辛': '正官', '壬': '偏印', '癸': '正印'},
    '乙': {'甲': '劫财', '乙': '比肩', '丙': '伤官', '丁': '食神', '戊': '正财', '己': '偏财', '庚': '正官', '辛': '七杀', '壬': '正印', '癸': '偏印'},
    '丙': {'甲': '偏印', '乙': '正印', '丙': '比肩', '丁': '劫财', '戊': '食神', '己': '伤官', '庚': '偏财', '辛': '正财', '壬': '七杀', '癸': '正官'},
    '丁': {'甲': '正印', '乙': '偏印', '丙': '劫财', '丁': '比肩', '戊': '伤官', '己': '食神', '庚': '正财', '辛': '偏财', '壬': '正官', '癸': '七杀'},
    '戊': {'甲': '七杀', '乙': '正官', '丙': '偏印', '丁': '正印', '戊': '比肩', '己': '劫财', '庚': '食神', '辛': '伤官', '壬': '偏财', '癸': '正财'},
    '己': {'甲': '正官', '乙': '七杀', '丙': '正印', '丁': '偏印', '戊': '劫财', '己': '比肩', '庚': '伤官', '辛': '食神', '壬': '正财', '癸': '偏财'},
    '庚': {'甲': '偏财', '乙': '正财', '丙': '七杀', '丁': '正官', '戊': '偏印', '己': '正印', '庚': '比肩', '辛': '劫财', '壬': '食神', '癸': '伤官'},
    '辛': {'甲': '正财', '乙': '偏财', '丙': '正官', '丁': '七杀', '戊': '正印', '己': '偏印', '庚': '劫财', '辛': '比肩', '壬': '伤官', '癸': '食神'},
    '壬': {'甲': '食神', '乙': '伤官', '丙': '偏财', '丁': '正财', '戊': '七杀', '己': '正官', '庚': '偏印', '辛': '正印', '壬': '比肩', '癸': '劫财'},
    '癸': {'甲': '伤官', '乙': '食神', '丙': '正财', '丁': '偏财', '戊': '正官', '己': '七杀', '庚': '正印', '辛': '偏印', '壬': '劫财', '癸': '比肩'}
}

dizhi_shishen_dict = {
    '甲': {'子': '比肩', '丑': '劫财', '寅': '食神', '卯': '伤官', '辰': '偏财', '巳': '正财', '午': '七杀', '未': '正官', '申': '偏印', '酉': '正印', '戌': '偏印', '亥': '正印'},
    '乙': {'甲': '劫财', '乙': '比肩', '丙': '伤官', '丁': '食神', '戊': '正财', '己': '偏财', '庚': '正官', '辛': '七杀', '壬': '正印', '癸': '偏印'},
    '丙': {'甲': '偏印', '乙': '正印', '丙': '比肩', '丁': '劫财', '戊': '食神', '己': '伤官', '庚': '偏财', '辛': '正财', '壬': '七杀', '癸': '正官'},
    '丁': {'甲': '正印', '乙': '偏印', '丙': '劫财', '丁': '比肩', '戊': '伤官', '己': '食神', '庚': '正财', '辛': '偏财', '壬': '正官', '癸': '七杀'},
    '戊': {'甲': '七杀', '乙': '正官', '丙': '偏印', '丁': '正印', '戊': '比肩', '己': '劫财', '庚': '食神', '辛': '伤官', '壬': '偏财', '癸': '正财'},
    '己': {'甲': '正官', '乙': '七杀', '丙': '正印', '丁': '偏印', '戊': '劫财', '己': '比肩', '庚': '伤官', '辛': '食神', '壬': '正财', '癸': '偏财'},
    '庚': {'甲': '偏财', '乙': '正财', '丙': '七杀', '丁': '正官', '戊': '偏印', '己': '正印', '庚': '比肩', '辛': '劫财', '壬': '食神', '癸': '伤官'},
    '辛': {'甲': '正财', '乙': '偏财', '丙': '正官', '丁': '七杀', '戊': '正印', '己': '偏印', '庚': '劫财', '辛': '比肩', '壬': '伤官', '癸': '食神'},
    '壬': {'甲': '食神', '乙': '伤官', '丙': '偏财', '丁': '正财', '戊': '七杀', '己': '正官', '庚': '偏印', '辛': '正印', '壬': '比肩', '癸': '劫财'},
    '癸': {'甲': '伤官', '乙': '食神', '丙': '正财', '丁': '偏财', '戊': '正官', '己': '七杀', '庚': '正印', '辛': '偏印', '壬': '劫财', '癸': '比肩'}
}

# 十神关系
def get_ten_gods_tiangan(rigan, other):

    # 生我者
    if rigan == '甲'
        if other == '甲':
            return '比肩'
        elif other == '乙':
            return '劫财'
        elif other == '丙':
            return '食神'
        elif other == '丁':
            return '伤官'
        elif other == '戊':
            return '正财'
        elif other == '己':
            return '偏财'
        elif other == '庚':
            return '七杀'
        elif other == '辛':
            return '正官'
        elif other == '壬':
            return '枭神'
        elif other == '癸':
            return '正印'
    elif  rigan == '乙'
        if other == '甲':
            return '劫财'
        elif other == '乙':
            return '比肩'
        elif other == '丙':
            return '伤官'
        elif other == '丁':
            return '食神'
        elif other == '戊':
            return '偏财'
        elif other == '己':
            return '正财'
        elif other == '庚':
            return '正官'
        elif other == '辛':
            return '七杀'
        elif other == '壬':
            return '正印'
        elif other == '癸':
            return '枭神'
    elif  rigan == '乙'
        if other == '甲':
            return '劫财'
        elif other == '乙':
            return '比肩'
        elif other == '丙':
            return '伤官'
        elif other == '丁':
            return '食神'
        elif other == '戊':
            return '偏财'
        elif other == '己':
            return '正财'
        elif other == '庚':
            return '正官'
        elif other == '辛':
            return '七杀'
        elif other == '壬':
            return '正印'
        elif other == '癸':
            return '枭神'




#计算两个八字是否冲合？天地相冲、天地相合、逢三、天比地冲等
# def analyze_bazi(a: bazi, b: bazi):
#     print("what is the fuck?")
#     pillars = ['nianzhu', 'yuezhu', 'rizhu', 'shizhu']
#     for pillar_a in pillars:
#         pillar_a_str = str(getattr(a, pillar_a))
#         for pillar_b in pillars:
#             pillar_b_str = str(getattr(b, pillar_b))
#             if ganzhi_tianchongdichong_dict.get(pillar_a_str) == pillar_b_str:
#                 print(f"{pillar_a}与{pillar_b}天地相冲")
#             elif ganzhi_tianhedihe_dict.get(pillar_a_str) == pillar_b_str:
#                 print(f"{pillar_a}与{pillar_b}天地相合")
# 其他字典需根据实际规则修正，此处暂不展开

#分析两个八字，主要是特殊组合
def analyze_bazi(a: bazi, b: bazi):
    pillars = ['年柱', '月柱', '日柱', '时柱']
    for pillar_a in pillars:
        for pillar_b in pillars:
            # 获取两柱的干支字符串
            ganzhi_a = str(getattr(a, pillar_a))
            ganzhi_b = str(getattr(b, pillar_b))

            #检查天地相冲
            if ganzhi_tianchongdichong_dict.get(ganzhi_a) == ganzhi_b:
                print(f"【冲】{pillar_a}（{ganzhi_a}）与{pillar_b}（{ganzhi_b}）天地相冲")

            #检查天地相合（需修正字典后使用）
            if ganzhi_tianhedihe_dict.get(ganzhi_a) == ganzhi_b:
                print(f"【合】{pillar_a}与{pillar_b}天地相合")

#分析单个八字，主要是自身内部是否存在特殊组合？
def analyze_bazi_single(a: bazi):
    # print("\n\n"+a.__str__())
    print("=" * 80+"\n"+a.__str__())
    #计算五行比例
    count_wuxing(a)

    #计算干支元素个数
    count_tiangan_dizhi(a)

    tiangan_count = {'甲': 0, '乙': 0, '丙': 0, '丁': 0, '戊': 0,'己': 0, '庚': 0, '辛': 0, '壬': 0, '癸': 0}
    dizhi_count = {'子': 0, '丑': 0, '寅': 0, '卯': 0, '辰': 0, '巳': 0, '午': 0, '未': 0, '申': 0, '酉': 0, '戌': 0, '亥': 0}

    pillars = ['年柱', '月柱', '日柱', '时柱']
    for i in range(len(pillars)):
        for j in range(i + 1, len(pillars)):
            pillar_a = pillars[i]
            pillar_b = pillars[j]

            ganzhi_a = str(getattr(a, pillar_a))
            ganzhi_b = str(getattr(a, pillar_b))

            # 检查天地相冲
            if ganzhi_tianchongdichong_dict.get(ganzhi_a) == ganzhi_b:
                print(f"【冲】{pillar_a}（{ganzhi_a}）与{pillar_b}（{ganzhi_b}）天地相冲")

            # 检查天地相合（需确保字典数据正确）
            if ganzhi_tianhedihe_dict.get(ganzhi_a) == ganzhi_b:
                print(f"【合】{pillar_a}（{ganzhi_a}）与{pillar_b}（{ganzhi_b}）天地相合")

            #统计元素个数——五行比例

            #统计干支元素个数
            # tiangan_count[ganzhi_a.tiangan] += 1
            # dizhi_count[ganzhi_a.tiangan] += 1

            #是否支克干？




# 示例运行
ganzhi1 = ganzhi("甲", "子")  # 甲子
ganzhi2 = ganzhi("庚", "午")  # 庚午
bazi1 = bazi(ganzhi1, ganzhi1, ganzhi1,ganzhi1)
bazi2 = bazi(ganzhi2, ganzhi2, ganzhi2,  ganzhi("己","丑"))
bazi3 = bazi(ganzhi1, ganzhi2, ganzhi("乙","未"),  ganzhi("己","丑"))
#analyze_bazi(bazi1, bazi2)
analyze_bazi_single(bazi3)


#还差十神组合，大运，小运，流年；五行里面还差正偏类，