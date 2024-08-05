import os
import pickle
from traceback import print_exc
import json

# import csv
# from datetime import datetime, timedelta
# # 获取当前模块的路径
# import pymysql
# from evaluator import get_df_from_db
# from multiprocessing import Pool
# import pandas as pd
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
path = MODULE_PATH + "\pjtTransferDictionary.pkl"
file = open(path, 'rb')  # 以二进制读模式（rb）打开pkl文件
pjtTransferDictionary = pickle.load(file)  # 读取存储的pickle文件


df_pjt_damage_standards = pjtTransferDictionary["df_pjt_damage_standards"]
model_productId_dic = pjtTransferDictionary["model_productId_dic"]
id_model_dic = pjtTransferDictionary["id_model_dic"]
id_model_dic2 = pjtTransferDictionary["id_model_dic2"]
model_id_dic = pjtTransferDictionary["model_id_dic"]
model_id_dic2 = pjtTransferDictionary["model_id_dic2"]

dic_transfer = pjtTransferDictionary["dic_transfer"]
standardsCode_chxStandards_dic = pjtTransferDictionary["standardsCode_chxStandards_dic"]
# print(standardsCode_chxStandards_dic)
# print(len(standardsCode_chxStandards_dic))
dic_productId_allJson = pjtTransferDictionary["dic_productId_allJson"]
# print(len(dic_productId_allJson))

class paramTransfer:
    df_pjt_damage_standards = df_pjt_damage_standards
    model_productId_dic = model_productId_dic
    id_model_dic = id_model_dic
    id_model_dic2 = id_model_dic2
    model_id_dic = model_id_dic
    model_id_dic2 = model_id_dic2

    dic_transfer = dic_transfer
    standardsCode_chxStandards_dic = standardsCode_chxStandards_dic
    dic_productId_allJson = dic_productId_allJson
    def __init__(self):
        self.dic_productId_allJson = dic_productId_allJson
        self.model_productId_dic = model_productId_dic
        self.id_model_dic = id_model_dic
        self.model_id_dic = model_id_dic
        self.dic_transfer = dic_transfer
        self.standardsCode_chxStandards_dic = standardsCode_chxStandards_dic
        self.df_pjt_damage_standards = df_pjt_damage_standards
        self.id_model_dic2 = id_model_dic2
        self.model_id_dic2 = model_id_dic2
    def get_properties_info(self,productId,data,zzt_desc_code_dic):
        netWork = data["netWork"]
        purchase_channel = data["purchase_channel"]
        color = data["color"]
        if(purchase_channel == "国行"):
            purchase_channel = "大陆国行"
        post_id_li = []
        post_CN_li = []

        warranty_period = data["warranty_period"]
        if(data["ram"] !="" and data["ram"] != None):
            ram_storage = data["ram"]+"+"+data["storage"]
            item_data = [purchase_channel, color, ram_storage, warranty_period, netWork]

        else:
            ram_storage = data["storage"]
            item_data = [ram_storage, purchase_channel, color, warranty_period, netWork]
        # print(item_data)
        try:
            all_json = json.loads(self.get_jsdataByProductId(productId))
            # print(all_json)
            data = all_json["data"]
        except TypeError as e:
            return [],[]

        try:
            #选择物品信息
            item_infos = data[0]["properties"]
            # print(item_infos)
            # print(len(item_infos))
            for item_info in item_infos:
                name_ = item_info["name"]
                pricePropertyValues = item_info["pricePropertyValues"]
                df_pjt_damage_standards_properties = self.df_pjt_damage_standards[
                    (self.df_pjt_damage_standards["sdandards_Level_1"] == "物品信息") & (
                                self.df_pjt_damage_standards["sdandards_Level_2"] == f"{name_}")]
                dic_pjt_properties = {}
                dic_pjt_properties_reverse = {}
                for i in range(df_pjt_damage_standards_properties.shape[0]):
                    pjt_properties_id = df_pjt_damage_standards_properties["id"].iloc[i]
                    pjt_warranty_period_CN = \
                    df_pjt_damage_standards_properties["sdandards_Level_3"].iloc[i]
                    dic_pjt_properties[pjt_warranty_period_CN] = pjt_properties_id
                    dic_pjt_properties_reverse[pjt_properties_id] = pjt_warranty_period_CN
                # print(dic_pjt_properties)
                flag_ = True
                for pricePropertyValue in pricePropertyValues:
                    # print(damageInfor_CN_li, pricePropertyValue["value"])

                    if(pricePropertyValue["value"] in item_data):
                        # print(damageInfor_CN_li,pricePropertyValue["value"])
                        flag_ = False
                        pricePropertyValue["isPreferred"] = True
                        post_CN_li.append(pricePropertyValue["value"])
                        try:
                            post_id_li.append(dic_pjt_properties[pricePropertyValue["value"]])
                            break
                        except KeyError as e:
                            # with open("./data/pjt_lacked_id.csv", mode='a+', encoding='utf-8', newline='') as info_csv:
                            #     info_csv_obj = csv.writer(info_csv, dialect='excel')
                            #     info_csv_obj.writerow([productId,pricePropertyValue["value"]])
                            #     print(f"已写入{productId},{pricePropertyValue['value']}.........")
                            pass

                    else:
                        pricePropertyValue["isPreferred"] = False
                if(flag_):
                    pricePropertyValues[0]["isPreferred"] = True
                    post_CN_li.append(pricePropertyValues[0]["value"])
                    # print(dic_pjt_properties)
                    post_id_li.append(dic_pjt_properties[pricePropertyValues[0]["value"]])
        except KeyError as e:
            pass


        #选择成色情况
        try:
            damageInfor_CN_li = []
            pjt_damage_id_li = zzt_desc_code_dic.values()
            for i in range(self.df_pjt_damage_standards.shape[0]):
                if(self.df_pjt_damage_standards["id"].iloc[i] in pjt_damage_id_li):
                    damageInfor_CN_li.append(self.df_pjt_damage_standards["sdandards_Level_3"].iloc[i])
            quality_infos = data[1]["properties"]
            # print(quality_infos)
            # print(len(quality_infos))
            for quality_info in quality_infos:
                name_ = quality_info["name"]
                pricePropertyValues = quality_info["pricePropertyValues"]
                df_pjt_damage_standards_properties = self.df_pjt_damage_standards[
                    (self.df_pjt_damage_standards["sdandards_Level_1"] == "成色情况") & (
                                self.df_pjt_damage_standards["sdandards_Level_2"] == f"{name_}")]
                dic_pjt_properties = {}
                dic_pjt_properties_reverse = {}
                for i in range(df_pjt_damage_standards_properties.shape[0]):
                    pjt_properties_id = df_pjt_damage_standards_properties["id"].iloc[i]
                    pjt_warranty_period_CN = \
                    df_pjt_damage_standards_properties["sdandards_Level_3"].iloc[i]
                    dic_pjt_properties[pjt_warranty_period_CN] = pjt_properties_id
                    dic_pjt_properties_reverse[pjt_properties_id] = pjt_warranty_period_CN
                # print(dic_pjt_properties)
                flag_ = True
                for pricePropertyValue in pricePropertyValues:
                    # print(damageInfor_CN_li, pricePropertyValue["value"])
                    if(pricePropertyValue["value"] in damageInfor_CN_li):
                        # print(damageInfor_CN_li,pricePropertyValue["value"])
                        flag_ = False
                        pricePropertyValue["isPreferred"] = True
                        post_CN_li.append(pricePropertyValue["value"])
                        post_id_li.append(dic_pjt_properties[pricePropertyValue["value"]])
                        break
                    else:
                        pricePropertyValue["isPreferred"] = False
                if(flag_):
                    pricePropertyValues[0]["isPreferred"] = True
                    post_CN_li.append(pricePropertyValues[0]["value"])
                    post_id_li.append(dic_pjt_properties[pricePropertyValues[0]["value"]])
                # print(quality_info)
        except KeyError as e:
            pass
        try:
            #选择功能情况
            function_infos = data[2]["properties"]
            # print(function_infos)
            # print(len(function_infos))
            for function_info in function_infos:
                name_ = function_info["name"]
                pricePropertyValues = function_info["pricePropertyValues"]
                df_pjt_damage_standards_properties = self.df_pjt_damage_standards[
                    (self.df_pjt_damage_standards["sdandards_Level_1"] == "功能情况") & (
                                self.df_pjt_damage_standards["sdandards_Level_2"] == f"{name_}")]
                dic_pjt_properties = {}
                dic_pjt_properties_reverse = {}
                for i in range(df_pjt_damage_standards_properties.shape[0]):
                    pjt_properties_id = df_pjt_damage_standards_properties["id"].iloc[i]
                    pjt_warranty_period_CN = \
                    df_pjt_damage_standards_properties["sdandards_Level_3"].iloc[i]
                    dic_pjt_properties[pjt_warranty_period_CN] = pjt_properties_id
                    dic_pjt_properties_reverse[pjt_properties_id] = pjt_warranty_period_CN
                # print(dic_pjt_properties)
                flag_ = True
                for pricePropertyValue in pricePropertyValues:
                    # print(damageInfor_CN_li, pricePropertyValue["value"])
                    if(pricePropertyValue["value"] in damageInfor_CN_li):
                        # print(damageInfor_CN_li,pricePropertyValue["value"])
                        flag_ = False
                        pricePropertyValue["isPreferred"] = True
                        post_CN_li.append(pricePropertyValue["value"])
                        post_id_li.append(dic_pjt_properties[pricePropertyValue["value"]])
                        break
                    else:
                        pricePropertyValue["isPreferred"] = False
                if(flag_):
                    pricePropertyValues[0]["isPreferred"] = True
                    # print(pricePropertyValues[0])
                    post_CN_li.append(pricePropertyValues[0]["value"])
                    try:
                        post_id_li.append(dic_pjt_properties[pricePropertyValues[0]["value"]])
                    except KeyError as e:
                        post_id_li.append(pricePropertyValues[0]["id"])
                    # print(dic_pjt_properties)
                # print(function_info)
        except KeyError as e:
            pass

        # all_json["data"][0] = item_infos
        # all_json["data"][1] = quality_infos
        # all_json["data"][2] = function_infos
        # print(post_CN_li)
        # print(post_id_li)
        # print(all_json)
        for i in range(len(post_id_li)):
            if(post_id_li[i] == 10203):
                post_id_li[i] = 9625
                post_CN_li[i] = "已激活，可还原"
            elif(post_id_li[i] == 20267):
                post_id_li[i] = 20268
                post_CN_li[i] = "90%＜电池健康度≤99%"
            elif(post_id_li[i] == 2124):
                post_id_li[i] = 2125
                post_CN_li[i] = "外壳完美"
        return post_id_li,post_CN_li
    def get_jsdataByProductId(self,ProductId):
        try:
            dic_productId_allJson = self.dic_productId_allJson
            return dic_productId_allJson[str(ProductId)]
        except KeyError as e:
            pass
            # print(f"paramTransfer.py 196行 pjt_inspection不存在product_id:{ProductId}")
            # print_exc()
            # if (ProductId != None):
            #     with open("cralwer/data/lacked_productId.csv", mode="a+", encoding="utf-8") as info_csv:
            #         info_csv_obj = csv.writer(info_csv, dialect='excel')
            #         info_csv_obj.writerow([ProductId])

    def verifyCHXdesc(self,desc_CN_dic):
        standardsCode_li = []
        for q_level_1,q_level_2 in desc_CN_dic.items():
            main_desc_li = q_level_2.split("|")
            for desc in main_desc_li:
                try:
                    standardsCode = self.standardsCode_chxStandards_dic[desc]
                    if(type(standardsCode) == list):
                        standardsCode_li.extend(standardsCode)
                    else:
                        standardsCode_li.append(standardsCode)
                except KeyError as e:
                    continue
                    # if (desc != None):
                    #     with open("cralwer/data/lacked_desc.csv", mode="a+", encoding="utf-8") as info_csv:
                    #         info_csv_obj = csv.writer(info_csv, dialect='excel')
                    #         info_csv_obj.writerow([desc])
                    #         continue

        # print(desc_CN_dic)
        # print(standardsCode_li)
        return standardsCode_li

    def returnSearchPriceParam(self, data):
        try:
            data["damageInfor"] = json.loads(data["damageInfor"])
        except Exception as e:
            pass
        # 全角转成半角
        def full2half(s):
            n = ''
            for char in s:
                num = ord(char)
                if num == 0x3000:  # 将全角空格转成半角空格
                    num = 32
                elif 0xFF01 <= num <= 0xFF5E:  # 将其余全角字符转成半角字符
                    num -= 0xFEE0
                num = chr(num)
                n += num
            return n
        temp_model = data["model"]
        # print("temp_model",temp_model)

        data["model"] = str(data["model"].replace("红米","Redmi")).replace(" ","").lower().replace("vivo iqoo","iqoo")
        if(type(data["model"]) != int):
            try:
                data["model"] = self.model_id_dic[data["model"]]
            except KeyError as e:
                try:
                    data["model"] = self.model_id_dic2[data["model"]]
                except KeyError as e:
                    return {"msg":"不存在对应机型product_id","model":temp_model}
                # with open("./data/pjt_model_lacked.csv", mode='a+', encoding='utf-8', newline='') as info_csv:
                #     info_csv_obj = csv.writer(info_csv, dialect='excel')
                #     info_csv_obj.writerow([full2half(data["model"]).replace('\n', '').replace('\r', '')])
                #     print(f"已写入{data['model']}.........")

        try:
            data["damageInfor"] = self.createDamageInfor(data["damageInfor"])
        except Exception as e:
            pass
        try:
            damageInfor_li = data["damageInfor"]
            model = data["model"]

            zzt_desc_code_dic = {}
            try:
                for code in damageInfor_li:
                    zzt_desc_code_dic[code] = self.dic_transfer[code]
            except Exception as e:
            # except TypeError as e:
                pass
            post_id_li, post_CN_li = self.get_properties_info(model, data, zzt_desc_code_dic)
            if(post_CN_li == [] and post_id_li == []):
                return {"msg":"pjt_inspection不存在对应product_id AllJson数据","product_id":model,"model_CN":temp_model}
            else:
                return {
                    "productId": model,
                    "pjt_post_data": {"post_id_li": post_id_li, "post_CN_li": post_CN_li}}
        except Exception as e:
            print_exc()

    def createDamageInfor(self,damage):
        damage_info = self.verifyCHXdesc(damage)
        return damage_info
count = 0
def do(data):
    trans = paramTransfer()
    global count
    try:
        result = trans.returnSearchPriceParam(data)
        # print(result)
        post_id_li = result["pjt_post_data"]["post_id_li"]
        count = count + 1
        print("已出查价编码个数:", count)
    except KeyError as e:
        if(result["msg"] == "不存在对应机型product_id"):
            result["model"]
        # print_exc()
if __name__ == '__main__':

    # #安卓手机数据传入 例
    # data =   {
    #     "model": "华为 Mate 10",
    #     "netWork":"全网通",
    #     "purchase_channel":"国行",
    #     "color": "香槟金",
    #     "ram": "6G",
    #     "storage": "128GB",
    #     "warranty_period":"",
    #     "damageInfor":
    #     {"屏幕外观": "屏有硬划痕（≥10毫米）", "屏幕显示": "轻微亮度问题(亮点/亮斑/背光不均/黑角/进灰)", "边框背板": "外壳明显磕碰/掉漆（≥3毫米），或镜片破损"}
    # }
    # trans = paramTransfer()
    # result = trans.returnSearchPriceParam(data)
    # print(result)


    #苹果手机数据传入 例
    data =   {
        "model": "苹果 iPhone XS",
        "netWork":"全网通",
        "purchase_channel":"国行",
        "color": "黑色钛金属",
        "ram": "6G",
        "storage": "512G",
        "warranty_period":"",
        "damageInfor":
        {"屏幕外观": "屏有硬划痕（≥10毫米）", "边框背板": "外壳明显磕碰/掉漆（≥3毫米），或镜片破损"}
    }
    trans = paramTransfer()
    result = trans.returnSearchPriceParam(data)
    print(result)

    # today_ = datetime.today()-timedelta(1)
    # # print(today_)
    # # print(today_.year)
    # if (int(today_.month) < 10):
    #     month_ = "0" + str(today_.month)
    # else:
    #     month_ = today_.month
    # if (int(today_.day) < 10):
    #     day_ = "0" + str(today_.day)
    # else:
    #     day_ = today_.day
    #
    # today_patch = str(today_.year) + str(month_) + str(day_) + "_2"
    # ware_price_table = pymysql.connect(
    #     host='47.109.68.137'  # 连接名称，默认127.0.0.1
    #     , user='spider'  # 用户名
    #     , passwd='zzwl@2024'  # 密码
    #     , port=33306  # 端口，默认为3306
    #     , db='spider'  # 数据库名称
    #     , charset='utf8'  # 字符编码
    # )
    # sql_word = f"select model,brand,ram,storage,color,purchase_channel,network,quality_desc,stick_code,grade,warranty_period,patch from ware_price where patch = '{today_patch}'"
    # # sql_word = f"select model,id,brand,ram,storage,color,purchase_channel,network,quality_desc,stick_code,grade,warranty_period,patch from ware_price"
    # # sql_word = f"select distinct(model) from ware_price"
    # df_chx_ware_price = get_df_from_db(sql_word, ware_price_table)
    # print(df_chx_ware_price.shape)
    # # print(df_chx_ware_price.head())
    # trans = paramTransfer()
    # count = 0
    # data_li = []
    # lacked_model_li = []
    # pjt_inspection_lacked_dic = {"product_id":[],"model_CN":[]}
    # for i in range(df_chx_ware_price.shape[0]):#int(df_chx_ware_price.shape[0]/20)
    #     # data = {
    #     #     "model": df_chx_ware_price["model"].iloc[i],
    #     #     "netWork": "",
    #     #     "purchase_channel": "",
    #     #     "color": "",
    #     #     "ram": "",
    #     #     "storage": "",
    #     #     "warranty_period": "",
    #     #     "damageInfor":
    #     #         {}
    #     # }
    #     data = {
    #         "model": df_chx_ware_price["model"].iloc[i],
    #         "netWork": df_chx_ware_price["network"].iloc[i],
    #         "purchase_channel": df_chx_ware_price["purchase_channel"].iloc[i],
    #         "color": df_chx_ware_price["color"].iloc[i],
    #         "ram": df_chx_ware_price["ram"].iloc[i],
    #         "storage": df_chx_ware_price["storage"].iloc[i],
    #         "warranty_period": df_chx_ware_price["warranty_period"].iloc[i],
    #         "damageInfor":
    #             df_chx_ware_price["quality_desc"].iloc[i]
    #     }
    #
    #     # print(data)
    #     # result = trans.returnSearchPriceParam(data)
    #     # data_li.append(data)
    #     try:
    #         result = trans.returnSearchPriceParam(data)
    #         # print(result)
    #         post_id_li = result["pjt_post_data"]["post_id_li"]
    #         count = count + 1
    #         print("已出查价编码个数:", count)
    #     except KeyError as e:
    #         if (result["msg"] == "不存在对应机型product_id"):
    #             lacked_model_li.append(result["model"])
    #         if (result["msg"] == "pjt_inspection不存在对应product_id AllJson数据"):
    #             pjt_inspection_lacked_dic["product_id"].append(result["product_id"])
    #             pjt_inspection_lacked_dic["model_CN"].append(result["model_CN"])
    # print(lacked_model_li)
    # print(len(lacked_model_li))

    # df_lacked_model = pd.DataFrame({"lacked_models":lacked_model_li})
    # df_lacked_model = df_lacked_model.drop_duplicates()
    # print(df_lacked_model.shape)
    # df_lacked_model.to_excel("./2024年7月31日lacked_models.xlsx",index=False)
    #
    # df_pjt_inspection_lacked = pd.DataFrame(pjt_inspection_lacked_dic)
    # df_pjt_inspection_lacked = df_pjt_inspection_lacked.drop_duplicates()
    # print(df_pjt_inspection_lacked.shape)
    # df_pjt_inspection_lacked.to_excel("./2024年7月31日pjt_inspection_lacked.xlsx",index=False)
    # pool = Pool(1)
    # pool.map(do,data_li)
    # pool.close()
    # pool.join()


