def money2number(m):

    first_letter = r'[壹贰叁肆伍陆柒捌玖]'
    middle = r'[零壹贰叁肆伍陆柒捌玖拾十佰百仟千万亿元圆角\n]*'
    last_letter = r'[整分角元圆]'
    chinese_money_regex = first_letter + middle + last_letter
    def money_match_clean(match):

        num = cn2num(match.group())
        return str(num)

    def clean_match(m):
        res = m.group().replace(',','').replace('，','')
        unit_map = {'万':1e4,'亿':1e8}
        if res[-1] in unit_map.keys():
            v = float(res[:-1])
            v *= unit_map[res[-1]]
            res = '%.2f' % v
        res = re.sub('\.?0+$','',res)

        return res
    text = re.sub(chinese_money_regex, money_match_clean, m)
    text = re.sub('[0-9][0-9,，]*\.?[0-9]+[万亿]?', clean_match, text)
    return text
    
def t2s(t):
    T2S = {'壹': '一', '贰': '二', '叁': '三', '肆': '四',
           '伍': '五', '陆': '六', '柒': '七', '捌': '八', '玖': '九','圆':'元',
           '拾': '十',  '佰': '百', '仟': '千', '〇': '零'}
    r = ''
    for value in t:
        r += T2S.get(value, value)
    return r
    
def cn2num(uchars_cn):
    numerals = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    units = {'十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000,
             '元': 1.0, '毛': 0.1, '分': 0.01, '两': 2, '角': 0.1, '块': 1.0}
    units_10 = {'十': '元', '百': '十', '千': '百', '万': '千',
                '亿': '千万', '元': '角', '毛': '分', '角': '分', '块': '角'}
    s = t2s(uchars_cn)
    if len(s) == 0:
        return 0
    if len(s) > 2:
        if s[-1] in numerals:
            if s[-2] in units:
                s = s + units_10[s[-2]]
    return float(cn2digit(s))


def cn2digit(uchars_cn):
    common_used_numerals = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
                            '百': 100, '千': 1000, '万': 10000, '亿': 100000000, '元': 1.0, '毛': 0.1, '分': 0.01, '两
': 2, '角': 0.1, '块': 1.0}
    s = t2s(uchars_cn)
    if not s:
        return 0
    for i in ['亿', '万', '千', '百', '十', '元', '块','圆', '毛', '角', '分']:
        if i in s:
            ps = s.split(i)
            lp = cn2digit(ps[0])
            if lp == 0 and i not in ['元', '块','圆', '毛', '角', '分']:
                lp = 1
            rp = cn2digit(ps[1])
            return 1.0 * lp * common_used_numerals.get(i[-1], 0) + rp * 1.0
    return 1.0 * common_used_numerals.get(s[-1], 0)


def main():
    print(cn2num('陆佰柒拾零元零角叁分'))
    print(cn2num('壹仟肆佰零玖元伍角'))
    print(cn2num('陆仟零柒圆壹角肆分'))


if __name__ == '__main__':
    main()
