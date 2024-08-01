# -*- coding: utf-8 -*-
import decimal
from datetime import datetime, date

import XX.List.ListHelper


class DictHelper():
    @staticmethod
    def sorted_dict_key(d):
        return dict(sorted(d.items(), key=lambda k: k[0]))

    @staticmethod
    def sorted_dict_value(d):
        return dict(sorted(d.items(), key=lambda k: k[1], reverse=True))

    # 通过v获取k
    @staticmethod
    def get_key_by_value(d, v):
        for key, val in d.items():
            if str(val).lower() == v.lower():
                return key

    @staticmethod
    def decode_v(d, coding="utf-8"):
        dd = {}
        for k, v in d.items():
            if isinstance(k, bytes):
                k = k.decode(coding)
            if type(v) == dict:
                dd[k] = DictHelper.decode_v(v, coding)
            elif type(v) == bytes:
                dd[k] = str(v.decode(coding))
            elif type(v) == list or type(v) == tuple:
                dd[k] = XX.List.ListHelper.ListHelper.decode_v((list(v), coding))
            elif isinstance(v, decimal.Decimal):
                dd[k] = float(v)
            elif isinstance(v, datetime):
                dd[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, date):
                dd[k] = v.strftime('%Y-%m-%d')
            else:
                dd[k] = v
        return dd

    @staticmethod
    def list_dict_duplicate_removal(data_list, key):
        v_sets = set()
        res = []
        for d in data_list:
            for k, v in d.items():
                if k == key:
                    if v not in v_sets:
                        v_sets.add(v)
                        res.append(d)
        return res


if __name__ == "__main__":
    l = [
        {
            "word": "四",
            "dis": [
                187,
                187
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                192,
                192
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                194,
                194
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                195,
                195
            ],
            "kind": "色情"
        },
        {
            "word": "宋",
            "dis": [
                1211,
                1211
            ],
            "kind": "色情"
        },
        {
            "word": "全",
            "dis": [
                7259,
                7259
            ],
            "kind": "色情"
        },
        {
            "word": "首",
            "dis": [
                7261,
                7261
            ],
            "kind": "色情"
        },
        {
            "word": "社",
            "dis": [
                7265,
                7265
            ],
            "kind": "色情"
        },
        {
            "word": "区",
            "dis": [
                7266,
                7266
            ],
            "kind": "色情"
        },
        {
            "word": "事",
            "dis": [
                7267,
                7267
            ],
            "kind": "色情"
        },
        {
            "word": "登",
            "dis": [
                7345,
                7345
            ],
            "kind": "色情"
        },
        {
            "word": "动",
            "dis": [
                7449,
                7449
            ],
            "kind": "色情"
        },
        {
            "word": "四",
            "dis": [
                7887,
                7887
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                7892,
                7892
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                7894,
                7894
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                7895,
                7895
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                8079,
                8079
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                8207,
                8207
            ],
            "kind": "色情"
        },
        {
            "word": "设",
            "dis": [
                8209,
                8209
            ],
            "kind": "色情"
        },
        {
            "word": "器",
            "dis": [
                8213,
                8213
            ],
            "kind": "色情"
        },
        {
            "word": "首",
            "dis": [
                8214,
                8214
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                8391,
                8391
            ],
            "kind": "色情"
        },
        {
            "word": "设",
            "dis": [
                8393,
                8393
            ],
            "kind": "色情"
        },
        {
            "word": "器",
            "dis": [
                8397,
                8397
            ],
            "kind": "色情"
        },
        {
            "word": "首",
            "dis": [
                8398,
                8398
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                8493,
                8493
            ],
            "kind": "色情"
        },
        {
            "word": "到",
            "dis": [
                8497,
                8497
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                8498,
                8498
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                8584,
                8584
            ],
            "kind": "色情"
        },
        {
            "word": "到",
            "dis": [
                8588,
                8588
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                8589,
                8589
            ],
            "kind": "色情"
        },
        {
            "word": "搜",
            "dis": [
                8718,
                8718
            ],
            "kind": "色情"
        },
        {
            "word": "索",
            "dis": [
                8719,
                8719
            ],
            "kind": "色情"
        },
        {
            "word": "搜",
            "dis": [
                8828,
                8828
            ],
            "kind": "色情"
        },
        {
            "word": "索",
            "dis": [
                8829,
                8829
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                8945,
                8945
            ],
            "kind": "色情"
        },
        {
            "word": "动",
            "dis": [
                8947,
                8947
            ],
            "kind": "色情"
        },
        {
            "word": "边",
            "dis": [
                8973,
                8973
            ],
            "kind": "色情"
        },
        {
            "word": "边",
            "dis": [
                9000,
                9000
            ],
            "kind": "色情"
        },
        {
            "word": "色",
            "dis": [
                9027,
                9027
            ],
            "kind": "色情"
        },
        {
            "word": "求",
            "dis": [
                9110,
                9110
            ],
            "kind": "色情"
        },
        {
            "word": "趣",
            "dis": [
                9136,
                9136
            ],
            "kind": "色情"
        },
        {
            "word": "视",
            "dis": [
                9161,
                9161
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                10637,
                10637
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                10639,
                10639
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                10640,
                10640
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                10665,
                10665
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                10716,
                10716
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                10717,
                10717
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                10722,
                10722
            ],
            "kind": "色情"
        },
        {
            "word": "地",
            "dis": [
                10728,
                10728
            ],
            "kind": "色情"
        },
        {
            "word": "属",
            "dis": [
                10729,
                10729
            ],
            "kind": "色情"
        },
        {
            "word": "浅",
            "dis": [
                10730,
                10730
            ],
            "kind": "色情"
        },
        {
            "word": "丘",
            "dis": [
                10731,
                10731
            ],
            "kind": "色情"
        },
        {
            "word": "东",
            "dis": [
                10733,
                10733
            ],
            "kind": "色情"
        },
        {
            "word": "大",
            "dis": [
                10735,
                10735
            ],
            "kind": "色情"
        },
        {
            "word": "北",
            "dis": [
                10764,
                10764
            ],
            "kind": "色情"
        },
        {
            "word": "省",
            "dis": [
                10770,
                10770
            ],
            "kind": "色情"
        },
        {
            "word": "道",
            "dis": [
                10771,
                10771
            ],
            "kind": "色情"
        },
        {
            "word": "定",
            "dis": [
                10777,
                10777
            ],
            "kind": "色情"
        },
        {
            "word": "水",
            "dis": [
                10778,
                10778
            ],
            "kind": "色情"
        },
        {
            "word": "渠",
            "dis": [
                10780,
                10780
            ],
            "kind": "色情"
        },
        {
            "word": "其",
            "dis": [
                10783,
                10783
            ],
            "kind": "色情"
        },
        {
            "word": "全",
            "dis": [
                10786,
                10786
            ],
            "kind": "色情"
        },
        {
            "word": "其",
            "dis": [
                10804,
                10804
            ],
            "kind": "色情"
        },
        {
            "word": "拔",
            "dis": [
                10817,
                10817
            ],
            "kind": "色情"
        },
        {
            "word": "度",
            "dis": [
                10819,
                10819
            ],
            "kind": "色情"
        },
        {
            "word": "全",
            "dis": [
                10826,
                10826
            ],
            "kind": "色情"
        },
        {
            "word": "设",
            "dis": [
                10860,
                10860
            ],
            "kind": "色情"
        },
        {
            "word": "其",
            "dis": [
                10880,
                10880
            ],
            "kind": "色情"
        },
        {
            "word": "地",
            "dis": [
                10883,
                10883
            ],
            "kind": "色情"
        },
        {
            "word": "地",
            "dis": [
                10895,
                10895
            ],
            "kind": "色情"
        },
        {
            "word": "食",
            "dis": [
                10903,
                10903
            ],
            "kind": "色情"
        },
        {
            "word": "吨",
            "dis": [
                10910,
                10910
            ],
            "kind": "色情"
        },
        {
            "word": "生",
            "dis": [
                10913,
                10913
            ],
            "kind": "色情"
        },
        {
            "word": "吨",
            "dis": [
                10916,
                10916
            ],
            "kind": "色情"
        },
        {
            "word": "吨",
            "dis": [
                10922,
                10922
            ],
            "kind": "色情"
        },
        {
            "word": "吨",
            "dis": [
                10928,
                10928
            ],
            "kind": "色情"
        },
        {
            "word": "输",
            "dis": [
                10932,
                10932
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                10944,
                10944
            ],
            "kind": "色情"
        },
        {
            "word": "比",
            "dis": [
                10946,
                10946
            ],
            "kind": "色情"
        },
        {
            "word": "上",
            "dis": [
                10947,
                10947
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                11096,
                11096
            ],
            "kind": "色情"
        },
        {
            "word": "动",
            "dis": [
                11098,
                11098
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                11121,
                11121
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                11211,
                11211
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                11212,
                11212
            ],
            "kind": "色情"
        },
        {
            "word": "绍",
            "dis": [
                11215,
                11215
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                11218,
                11218
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                11219,
                11219
            ],
            "kind": "色情"
        },
        {
            "word": "绍",
            "dis": [
                11222,
                11222
            ],
            "kind": "色情"
        },
        {
            "word": "闭",
            "dis": [
                11336,
                11336
            ],
            "kind": "色情"
        },
        {
            "word": "扫",
            "dis": [
                11426,
                11426
            ],
            "kind": "色情"
        },
        {
            "word": "请",
            "dis": [
                13526,
                13526
            ],
            "kind": "色情"
        },
        {
            "word": "升",
            "dis": [
                13527,
                13527
            ],
            "kind": "色情"
        },
        {
            "word": "的",
            "dis": [
                13530,
                13530
            ],
            "kind": "色情"
        },
        {
            "word": "版",
            "dis": [
                13536,
                13536
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                13537,
                13537
            ],
            "kind": "色情"
        },
        {
            "word": "布",
            "dis": [
                14744,
                14744
            ],
            "kind": "色情"
        },
        {
            "word": "动",
            "dis": [
                14835,
                14835
            ],
            "kind": "色情"
        },
        {
            "word": "点",
            "dis": [
                16067,
                16067
            ],
            "kind": "色情"
        },
        {
            "word": "点",
            "dis": [
                16084,
                16084
            ],
            "kind": "色情"
        },
        {
            "word": "上",
            "dis": [
                16391,
                16391
            ],
            "kind": "色情"
        },
        {
            "word": "榜",
            "dis": [
                16392,
                16392
            ],
            "kind": "色情"
        },
        {
            "word": "庆",
            "dis": [
                16406,
                16406
            ],
            "kind": "色情"
        },
        {
            "word": "四",
            "dis": [
                16445,
                16445
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                16721,
                16721
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                16740,
                16740
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                16858,
                16858
            ],
            "kind": "色情"
        },
        {
            "word": "设",
            "dis": [
                16865,
                16865
            ],
            "kind": "色情"
        },
        {
            "word": "全",
            "dis": [
                16866,
                16866
            ],
            "kind": "色情"
        },
        {
            "word": "第",
            "dis": [
                16944,
                16944
            ],
            "kind": "色情"
        },
        {
            "word": "说",
            "dis": [
                17576,
                17576
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                17577,
                17577
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                17605,
                17605
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                17969,
                17969
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                18157,
                18157
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                18345,
                18345
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                18533,
                18533
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                18721,
                18721
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                18910,
                18910
            ],
            "kind": "色情"
        },
        {
            "word": "边",
            "dis": [
                19324,
                19324
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                19355,
                19355
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                19471,
                19471
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                19473,
                19473
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                19474,
                19474
            ],
            "kind": "色情"
        },
        {
            "word": "寺",
            "dis": [
                19478,
                19478
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                19566,
                19566
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                19568,
                19568
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                19569,
                19569
            ],
            "kind": "色情"
        },
        {
            "word": "寺",
            "dis": [
                19573,
                19573
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                19587,
                19587
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                19589,
                19589
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                19590,
                19590
            ],
            "kind": "色情"
        },
        {
            "word": "寺",
            "dis": [
                19594,
                19594
            ],
            "kind": "色情"
        },
        {
            "word": "点",
            "dis": [
                19668,
                19668
            ],
            "kind": "色情"
        },
        {
            "word": "点",
            "dis": [
                19766,
                19766
            ],
            "kind": "色情"
        },
        {
            "word": "点",
            "dis": [
                19790,
                19790
            ],
            "kind": "色情"
        },
        {
            "word": "山",
            "dis": [
                19865,
                19865
            ],
            "kind": "色情"
        },
        {
            "word": "区",
            "dis": [
                19868,
                19868
            ],
            "kind": "色情"
        },
        {
            "word": "山",
            "dis": [
                19957,
                19957
            ],
            "kind": "色情"
        },
        {
            "word": "区",
            "dis": [
                19960,
                19960
            ],
            "kind": "色情"
        },
        {
            "word": "山",
            "dis": [
                19975,
                19975
            ],
            "kind": "色情"
        },
        {
            "word": "区",
            "dis": [
                19978,
                19978
            ],
            "kind": "色情"
        },
        {
            "word": "升",
            "dis": [
                20058,
                20058
            ],
            "kind": "色情"
        },
        {
            "word": "区",
            "dis": [
                20063,
                20063
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                20102,
                20102
            ],
            "kind": "色情"
        },
        {
            "word": "区",
            "dis": [
                20109,
                20109
            ],
            "kind": "色情"
        },
        {
            "word": "边",
            "dis": [
                20219,
                20219
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                20250,
                20250
            ],
            "kind": "色情"
        },
        {
            "word": "酥",
            "dis": [
                20719,
                20719
            ],
            "kind": "色情"
        },
        {
            "word": "酥",
            "dis": [
                20808,
                20808
            ],
            "kind": "色情"
        },
        {
            "word": "酥",
            "dis": [
                20823,
                20823
            ],
            "kind": "色情"
        },
        {
            "word": "色",
            "dis": [
                20971,
                20971
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                21119,
                21119
            ],
            "kind": "色情"
        },
        {
            "word": "卜",
            "dis": [
                21235,
                21235
            ],
            "kind": "色情"
        },
        {
            "word": "色",
            "dis": [
                21240,
                21240
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                21245,
                21245
            ],
            "kind": "色情"
        },
        {
            "word": "卜",
            "dis": [
                21334,
                21334
            ],
            "kind": "色情"
        },
        {
            "word": "色",
            "dis": [
                21339,
                21339
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                21344,
                21344
            ],
            "kind": "色情"
        },
        {
            "word": "卜",
            "dis": [
                21358,
                21358
            ],
            "kind": "色情"
        },
        {
            "word": "色",
            "dis": [
                21363,
                21363
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                21368,
                21368
            ],
            "kind": "色情"
        },
        {
            "word": "求",
            "dis": [
                21627,
                21627
            ],
            "kind": "色情"
        },
        {
            "word": "趣",
            "dis": [
                21737,
                21737
            ],
            "kind": "色情"
        },
        {
            "word": "视",
            "dis": [
                21852,
                21852
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                21884,
                21884
            ],
            "kind": "色情"
        },
        {
            "word": "四",
            "dis": [
                22011,
                22011
            ],
            "kind": "色情"
        },
        {
            "word": "省",
            "dis": [
                22013,
                22013
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                22015,
                22015
            ],
            "kind": "色情"
        },
        {
            "word": "四",
            "dis": [
                22061,
                22061
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                22064,
                22064
            ],
            "kind": "色情"
        },
        {
            "word": "市",
            "dis": [
                22067,
                22067
            ],
            "kind": "色情"
        },
        {
            "word": "生",
            "dis": [
                22082,
                22082
            ],
            "kind": "色情"
        },
        {
            "word": "的",
            "dis": [
                22083,
                22083
            ],
            "kind": "色情"
        },
        {
            "word": "被",
            "dis": [
                22087,
                22087
            ],
            "kind": "色情"
        },
        {
            "word": "盗",
            "dis": [
                22088,
                22088
            ],
            "kind": "色情"
        },
        {
            "word": "谁",
            "dis": [
                22090,
                22090
            ],
            "kind": "色情"
        },
        {
            "word": "的",
            "dis": [
                22092,
                22092
            ],
            "kind": "色情"
        },
        {
            "word": "四",
            "dis": [
                22132,
                22132
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                22135,
                22135
            ],
            "kind": "色情"
        },
        {
            "word": "升",
            "dis": [
                22137,
                22137
            ],
            "kind": "色情"
        },
        {
            "word": "多",
            "dis": [
                22283,
                22283
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                22411,
                22411
            ],
            "kind": "色情"
        },
        {
            "word": "四",
            "dis": [
                22795,
                22795
            ],
            "kind": "色情"
        },
        {
            "word": "部",
            "dis": [
                22800,
                22800
            ],
            "kind": "色情"
        },
        {
            "word": "千",
            "dis": [
                22802,
                22802
            ],
            "kind": "色情"
        },
        {
            "word": "秋",
            "dis": [
                22803,
                22803
            ],
            "kind": "色情"
        },
        {
            "word": "编",
            "dis": [
                22866,
                22866
            ],
            "kind": "色情"
        },
        {
            "word": "标",
            "dis": [
                22893,
                22893
            ],
            "kind": "色情"
        },
        {
            "word": "版",
            "dis": [
                22895,
                22895
            ],
            "kind": "色情"
        },
        {
            "word": "本",
            "dis": [
                22900,
                22900
            ],
            "kind": "色情"
        },
        {
            "word": "切",
            "dis": [
                22962,
                22962
            ],
            "kind": "色情"
        },
        {
            "word": "收",
            "dis": [
                22968,
                22968
            ],
            "kind": "色情"
        },
        {
            "word": "术",
            "dis": [
                22978,
                22978
            ],
            "kind": "色情"
        },
        {
            "word": "事",
            "dis": [
                23547,
                23547
            ],
            "kind": "色情"
        },
        {
            "word": "aaaaaanal",
            "dis": [
                23872,
                23880
            ],
            "kind": "色情"
        },
        {
            "word": "aaaaaanal",
            "dis": [
                23886,
                23894
            ],
            "kind": "色情"
        }
    ]
    _ = DictHelper.list_dict_duplicate_removal(l, "word")
    print(len(l), len(_))
    pass
