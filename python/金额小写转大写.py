def money_trans(num: float) -> str:
    num_dict = {
        0: "零", 1: "壹", 2: "贰", 3: "叁", 4: "肆", 5: "伍",
        6: "陆", 7: "柒", 8: "捌", 9: "玖", 10: "拾"
    }
    amount_str = str(num)
    if '.' in amount_str:
        int_part, decimal_part = amount_str.split('.')
        int_digits = [int(i) for i in int_part]
        decimal_digits = [int(i) for i in decimal_part]
    else:
        int_digits = [int(i) for i in amount_str]
        decimal_digits = []

    int_units = ["元", "拾", "佰", "仟", "万", "亿"]
    decimal_units = ["角", "分"]
    res = []
    for i, digit in enumerate(reversed(int_digits)):
        if digit == 0:
            res.append("零")
        else:
            res.append(num_dict[digit] + int_units[i % 6])
    res = res[::-1] + ["整"]

    if decimal_digits:
        res = res[:-1] + [num_dict[decimal_digits[0]] + decimal_units[0]]
        if len(decimal_digits) > 1:
            res.append(num_dict[decimal_digits[1]] + decimal_units[1])
    return "".join(res)


amount = float(input("请输入一个数字金额："))
print(money_trans(amount))
