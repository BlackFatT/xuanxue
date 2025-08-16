class GanZhiYinYang:
    # 天干阴阳属性：甲、丙、戊、庚、壬为阳；乙、丁、己、辛、癸为阴
    _tiangan_yinyang = {
        '甲': '阳', '乙': '阴',
        '丙': '阳', '丁': '阴',
        '戊': '阳', '己': '阴',
        '庚': '阳', '辛': '阴',
        '壬': '阳', '癸': '阴'
    }

    # 地支阴阳属性：子、寅、辰、午、申、戌为阳；丑、卯、巳、未、酉、亥为阴
    _dizhi = {
        '阳': ['子', '寅', '辰', '午', '申', '戌'],
        '阴': ['丑', '卯', '巳', '未', '酉', '亥']
    }

    @staticmethod
    def get_tiangan():
        return ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

    @staticmethod
    def get_dizhi():
        return ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    @staticmethod
    def get_tiangan_yinyang(tian_gan):
        """
        【静态方法】判断单个天干的阴阳属性

        参数:
            tian_gan: 单个天干字符（如'甲'、'乙'）

        返回:
            str: '阳'或'阴'，若天干无效则返回None
        """
        tian_gan = tian_gan.strip()
        if len(tian_gan) != 1 or tian_gan not in GanZhiYinYang._tiangan_yinyang:
            print(f"无效的天干: {tian_gan}")
            return None
        return GanZhiYinYang._tiangan_yinyang[tian_gan]

    @staticmethod
    def get_dizhi_by_yinyang(yin_yang):
        """
        【静态方法】根据阴阳属性返回对应的地支列表

        参数:
            yin_yang: '阳'或'阴'

        返回:
            list: 对应属性的地支列表，若属性无效则返回空列表
        """
        if yin_yang not in ['阳', '阴']:
            print(f"无效的阴阳属性: {yin_yang}")
            return []
        # 返回列表副本，避免外部修改内部数据
        return GanZhiYinYang._dizhi[yin_yang].copy()

    @staticmethod
    def get_matching_dizhi(tian_gan):
        """
        【静态方法】根据输入的天干，返回同阴阳属性的全部地支

        参数:
            tian_gan: 单个天干字符

        返回:
            list: 同阴阳属性的地支列表，若输入无效则返回空列表
        """
        # 获取天干的阴阳属性
        yin_yang = GanZhiYinYang.get_tiangan_yinyang(tian_gan)
        if not yin_yang:
            return []

        # 返回对应阴阳的地支
        return GanZhiYinYang.get_dizhi_by_yinyang(yin_yang)

#
# # 使用示例（无需创建实例，直接用类名调用）
# if __name__ == "__main__":
#     # 测试阳天干（甲）
#     tian_gan1 = '甲'
#     yang_dizhi = GanZhiYinYang.get_matching_dizhi(tian_gan1)
#     print(f"天干'{tian_gan1}'属{GanZhiYinYang.get_tiangan_yinyang(tian_gan1)}，对应的地支: {yang_dizhi}")
#     # 输出：天干'甲'属阳，对应的地支: ['子', '寅', '辰', '午', '申', '戌']
#
#     # 测试阴天干（乙）
#     tian_gan2 = '乙'
#     yin_dizhi = GanZhiYinYang.get_matching_dizhi(tian_gan2)
#     print(f"天干'{tian_gan2}'属{GanZhiYinYang.get_tiangan_yinyang(tian_gan2)}，对应的地支: {yin_dizhi}")
#     # 输出：天干'乙'属阴，对应的地支: ['丑', '卯', '巳', '未', '酉', '亥']
#
#     # 测试其他天干
#     for g in ['丙', '丁', '戊', '己']:
#         print(f"\n天干'{g}'属{GanZhiYinYang.get_tiangan_yinyang(g)}，对应的地支: {GanZhiYinYang.get_matching_dizhi(g)}")
