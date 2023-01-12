def money_trans(num: int) -> str:
    """将输入的数字金额转换为对应的中文大写金额。"""
    # 定义一个字典，存放数字和大写金额的映射
    num_to_chinese = {
        0: "零", 1: "壹", 2: "贰", 3: "叁", 4: "肆", 5: "伍",
        6: "陆", 7: "柒", 8: "捌", 9: "玖", 10: "拾"
    }
    # 将数字转换为字符串
    amount_str = str(num)
    # 定义一个列表，存放转换后的大写金额
    chinese_amount = []
    # 定义一个列表，存放数字字符串的下标
    index = [i for i in range(len(amount_str))]
    # 定义一个列表，存放数字字符串的值
    value = [int(i) for i in amount_str]
    # 将数字字符串的下标和值组合成一个字典
    num_dict = dict(zip(index, value))
    # 将数字字符串转换为大写金额
    for key, value in num_dict.items():
        if key == 0:
            chinese_amount.append(num_to_chinese[value] + "元")
        elif key == 1:
            chinese_amount.append(num_to_chinese[value] + "拾")
        elif key == 2:
            chinese_amount.append(num_to_chinese[value] + "佰")
        elif key == 3:
            chinese_amount.append(num_to_chinese[value] + "仟")
        elif key == 4:
            chinese_amount.append(num_to_chinese[value] + "万")
        elif key == 5:
            chinese_amount.append(num_to_chinese[value] + "拾")
        elif key == 6:
            chinese_amount.append(num_to_chinese[value] + "佰")
        elif key == 7:
            chinese_amount.append(num_to_chinese[value] + "仟")
        elif key == 8:
            chinese_amount.append(num_to_chinese[value] + "亿")
        elif key == 9:
             chinese_amount.append(num_to_chinese[value] + "拾")
        elif key == 10:
             chinese_amount.append(num_to_chinese[value] + "佰")
        elif key == 11:
             chinese_amount.append(num_to_chinese[value] + "仟")
        # 将列表中的字符串拼接起来
    final_result = "".join(chinese_amount)
        # 返回最终转换后的大写金额
    return final_result




# 调用函数
amount = int(input("请输入一个数字金额："))
print(money_trans(amount))