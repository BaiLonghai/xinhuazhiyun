import calendar
import datetime
import os

from docx import Document

# 设置年份
year = 2020

# 设置日期格式
date_format = "%Y%m%d"

# 遍历每一周
for week in range(1, 53):
    # 获取当前周的第一天
    first_day = datetime.datetime.strptime("%s-W%s-1" % (year, week), "%Y-W%W-%w")
    # 获取当前周的最后一天
    last_day = first_day + datetime.timedelta(days=5)
    # 转换为字符串
    first_day_str = first_day.strftime(date_format)
    last_day_str = last_day.strftime(date_format)

    # 创建文件名
    filename = "项目周报_%s-%s第%s周.docx" % (
        first_day_str,
        last_day_str,
        week
    )

    # 创建一个文档对象
    document = Document()

    # 在文档中添加文本
    document.add_paragraph(filename)

    # 保存文档
    document.save(filename)
