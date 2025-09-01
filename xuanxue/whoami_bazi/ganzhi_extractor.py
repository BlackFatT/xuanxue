class GanZhiExtractor:
    def __init__(self, ganzhi_str):
        """
        初始化天干地支提取器

        参数:
            ganzhi_str: 天干地支组合字符串，如"甲寅辛丑壬午辛卯"
        """
        # 验证输入格式是否符合要求（长度应为偶数）
        if len(ganzhi_str) % 2 != 0:
            raise ValueError(f"无效的天干地支字符串: {ganzhi_str}，长度必须为偶数")

        self.ganzhi_str = ganzhi_str
        self._tiangan = []  # 天干列表
        self._dizhi = []  # 地支列表
        self._extract()

    def _extract(self):
        """内部提取方法，分离天干和地支"""
        # 按每两个字符一组处理（每组第一个为天干，第二个为地支）
        for i in range(0, len(self.ganzhi_str), 2):
            # 提取一组中的天干（第1个字符）
            tian_gan = self.ganzhi_str[i]
            # 提取一组中的地支（第2个字符）
            di_zhi = self.ganzhi_str[i + 1]

            self._tiangan.append(tian_gan)
            self._dizhi.append(di_zhi)

    def get_tiangan(self, join=True):
        """
        获取所有天干

        参数:
            join: 是否拼接为字符串，True返回拼接后的字符串，False返回列表

        返回:
            str或list: 天干组合，如"甲辛壬辛"或['甲', '辛', '壬', '辛']
        """
        if join:
            return ''.join(self._tiangan)
        return self._tiangan.copy()

    def get_dizhi(self, join=True):
        """
        获取所有地支

        参数:
            join: 是否拼接为字符串，True返回拼接后的字符串，False返回列表

        返回:
            str或list: 地支组合，如"寅丑午卯"或['寅', '丑', '午', '卯']
        """
        if join:
            return ''.join(self._dizhi)
        return self._dizhi.copy()


# # 使用示例
# if __name__ == "__main__":
#     # 测试示例：甲寅辛丑壬午辛卯
#     ganzhi = "甲寅辛丑壬午辛卯"
#     extractor = GanZhiExtractor(ganzhi)
#
#     # 获取天干
#     print("天干（字符串）:", extractor.get_tiangan())  # 输出：甲辛壬辛
#     print("天干（列表）:", extractor.get_tiangan(join=False))  # 输出：['甲', '辛', '壬', '辛']
#
#     # 获取地支
#     print("地支（字符串）:", extractor.get_dizhi())  # 输出：寅丑午卯
#     print("地支（列表）:", extractor.get_dizhi(join=False))  # 输出：['寅', '丑', '午', '卯']
#
#     # 测试其他案例
#     another_ganzhi = "甲乙丙丁子丑寅卯"
#     extractor2 = GanZhiExtractor(another_ganzhi)
#     print("\n另一个案例的天干:", extractor2.get_tiangan())  # 甲乙丙丁
#     print("另一个案例的地支:", extractor2.get_dizhi())  # 子丑寅卯
