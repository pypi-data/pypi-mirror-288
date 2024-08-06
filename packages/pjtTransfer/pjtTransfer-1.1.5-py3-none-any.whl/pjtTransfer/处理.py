# -*- coding:utf-8 -*-
import pymysql
import pandas as pd
#显示所有的列
pd.set_option('display.max_columns', None)
#显示所有的行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)


# 定义获取函数
def get_df_from_db(sql, db):
    cursor = db.cursor()  # 使用cursor()方法获取用于执行SQL语句的游标
    cursor.execute(sql)  # 执行SQL语句
    """
    使用fetchall函数以元组形式返回所有查询结果并打印出来
    fetchone()返回第一行，fetchmany(n)返回前n行
    游标执行一次后则定位在当前操作行，下一次操作从当前操作行开始
    """
    data = cursor.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = cursor.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in data], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df

    """
    使用完成之后需关闭游标和数据库连接，减少资源占用,cursor.close(),db.close()
    db.commit()若对数据库进行了修改，需进行提交之后再关闭
    """
    cursor.close()
    db.close()

    # print("cursor.description中的内容：", columnDes)
    return df



ware_price_table = pymysql.connect(
    host='47.109.68.137'  # 连接名称，默认127.0.0.1
    , user='spider'  # 用户名
    , passwd='zzwl@2024'  # 密码
    , port=33306  # 端口，默认为3306
    , db='spider'  # 数据库名称
    , charset='utf8'  # 字符编码
)

path = "./2024年7月31日lacked_models.xlsx"
df_model_lacked = pd.read_excel(path)
print(df_model_lacked.shape)
sql_word = "select distinct(model) from ware_price"
df_history_auction = get_df_from_db(sql_word, ware_price_table)
print(df_history_auction.head())
print(df_history_auction.shape)
lacked_org_model_li = []
for i in range(df_model_lacked.shape[0]):
    flag = True
    #.replace("vivo iqoo", "iqoo").replace("红米", "Redmi")
    lacked_model = df_model_lacked["lacked_models"].iloc[i]
    for v in range(df_history_auction.shape[0]):
        org_model = df_history_auction["model"].iloc[v]
        org_model_lower = str(org_model).lower()
        if(lacked_model == org_model_lower):
            if(flag):
                lacked_org_model_li.append(org_model)
                flag = False
                break

print(lacked_org_model_li)
print(len(lacked_org_model_li))

df_lacked_org_model = pd.DataFrame({"lacked_org_model":lacked_org_model_li})
print(df_lacked_org_model.shape)
df_lacked_org_model.to_excel("./3722024年7月31日lacked_org_models.xlsx",index=False)