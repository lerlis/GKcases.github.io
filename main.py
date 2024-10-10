from pyecharts import options as opts
from pyecharts.charts import Map, Page
from pyecharts.components import Table
from pyecharts.commons.utils import JsCode
import json
#from pyecharts.faker import Faker

# print(pyecharts.__version__)

NAME_MAP_DATA = {
    # "key": "value"
    # "name on the China map": "name in the MAP DATA",
    '北京市':'北京',
    '上海市':'上海',
    '天津市':'天津',
    '重庆市':'重庆',
    '黑龙江省':'黑龙江',
    '吉林省':'吉林',
    '辽宁省':'辽宁',
    '河北省':'河北',
    '内蒙古自治区':'内蒙',
    '河南省':'河南',
    '山东省':'山东',
    '陕西省':'陕西',
    '宁夏回族自治区':'宁夏',
    '湖南省':'湖南',
    '湖北省':'湖北',
    '安徽省':'安徽',
    '江苏省':'江苏',
    '江西省':'江西',
    '浙江省':'浙江',
    '福建省':'福建',
    '广东省':'广东',
    '广西壮族自治区':'广西',
    '海南省':'海南',
    '云南省':'云南',
    '四川省':'四川',
    '贵州省':'贵州',
    '甘肃省':'甘肃',
    '青海省':'青海',
    '新疆维吾尔自治区':'新疆',
    '西藏自治区':'西藏',
    '香港特别行政区':'香港',
    '澳门特别行政区':'澳门',
    '台湾省':'台湾',
}

def table_base(case_list) -> Table:
    table1 = Table()
    headers = ['省份', '类别','报名时间', '考试时间']
    rows = []
    for case in case_list:
        single_row = []
        single_row.append(case.get("Place"))
        single_row.append(case.get("Type"))
        single_row.append(case.get("Date1"))
        single_row.append(case.get("Date2"))
        rows.append(single_row)
    table1.add(headers, rows)
    table1.set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="形式一览表", subtitle="各种类别都可以放进来")
    )
    return table1


def map_base(count_dict) -> Map:
    """
    MAP_DATA = [
        ['北京', 555],
        ['上海', 666],
    ]
    """
    MAP_DATA = []
    num_accu = []
    keys = list(count_dict)
    for key in keys:
        single_row = []
        single_row.append(key)
        value = count_dict.get(key)
        single_row.append(value)
        MAP_DATA.append(single_row)
        num_accu.append(value)
    map_chart = (
        Map()
        .add(
            series_name='数量',
            maptype='china',
            data_pair=MAP_DATA,
            name_map=NAME_MAP_DATA,
            is_map_symbol_show=True,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="参考J数量",
            ),
            visualmap_opts=opts.VisualMapOpts(max_=max(num_accu)),
        )
    )
    return map_chart

def page_base(case_list, count_dict):
    own_page = Page(layout=Page.SimplePageLayout)
    own_page.add(
        map_base(count_dict),
        table_base(case_list)
    )
    own_page.render('./docs/all_in.html')

def read_json(path):
    with open(path, "r", encoding='utf-8') as f:
        db_data = json.load(f)
    case_list = db_data.get("Cases")
    count_dict = dict()
    for case in case_list:
        place = case.get("Place")
        if place in count_dict:
            count_dict[place] += 1
        else:
            count_dict[place] = 1
    return case_list, count_dict


if __name__ == "__main__":
    path = './data.json'
    case_list, count_dict = read_json(path)
    # print(case_list)
    # print(count_dict)
    page_base(case_list, count_dict)