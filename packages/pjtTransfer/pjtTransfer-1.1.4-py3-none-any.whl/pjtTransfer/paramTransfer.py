import os
import pickle
from traceback import print_exc
import json

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
dic_productId_allJson = pjtTransferDictionary["dic_productId_allJson"]

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

    def get_properties_info(self, productId, data, zzt_desc_code_dic):
        netWork = data["netWork"]
        purchase_channel = data["purchase_channel"]
        color = data["color"]
        if (purchase_channel == "国行"):
            purchase_channel = "大陆国行"
        post_id_li = []
        post_CN_li = []

        warranty_period = data["warranty_period"]
        if (data["ram"] != "" and data["ram"] != None):
            ram_storage = data["ram"] + "+" + data["storage"]
            item_data = [purchase_channel, color, ram_storage, warranty_period, netWork]

        else:
            ram_storage = data["storage"]
            item_data = [ram_storage, purchase_channel, color, warranty_period, netWork]
        try:
            all_json = json.loads(self.get_jsdataByProductId(productId))
            js_data = all_json["data"]
        except TypeError as e:
            return [], []

        try:
            # 选择物品信息
            try:
                item_infos = js_data[0]["properties"]
            except KeyError as e:
                item_infos = js_data["productInfos"]
                for ite in item_infos:
                    ite["pricePropertyValues"] = ite["pricePropertyValueVos"]
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
                flag_ = True
                for pricePropertyValue in pricePropertyValues:
                    if (pricePropertyValue["value"] in item_data):
                        flag_ = False
                        pricePropertyValue["isPreferred"] = True
                        post_CN_li.append(pricePropertyValue["value"])
                        try:
                            post_id_li.append(dic_pjt_properties[pricePropertyValue["value"]])
                            break
                        except KeyError as e:
                            pass

                    else:
                        pricePropertyValue["isPreferred"] = False
                if (flag_):
                    pricePropertyValues[0]["isPreferred"] = True
                    post_CN_li.append(pricePropertyValues[0]["value"])
                    post_id_li.append(dic_pjt_properties[pricePropertyValues[0]["value"]])
        except KeyError as e:
            print(productId, " A*100")
            print_exc()

        # 选择成色情况
        try:
            damageInfor_CN_li = []
            pjt_damage_id_li = zzt_desc_code_dic.values()
            for i in range(self.df_pjt_damage_standards.shape[0]):
                if (self.df_pjt_damage_standards["id"].iloc[i] in pjt_damage_id_li):
                    damageInfor_CN_li.append(self.df_pjt_damage_standards["sdandards_Level_3"].iloc[i])
            try:
                quality_infos = js_data[1]["properties"]
            except KeyError as e:
                quality_infos = js_data["qualityInfos"]
                for ite in quality_infos:
                    ite["pricePropertyValues"] = ite["pricePropertyValueVos"]
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
                flag_ = True
                for pricePropertyValue in pricePropertyValues:
                    if (pricePropertyValue["value"] in damageInfor_CN_li):
                        flag_ = False
                        pricePropertyValue["isPreferred"] = True
                        post_CN_li.append(pricePropertyValue["value"])
                        post_id_li.append(dic_pjt_properties[pricePropertyValue["value"]])
                        break
                    else:
                        pricePropertyValue["isPreferred"] = False
                if (flag_):
                    if (len(dic_pjt_properties) == 0):
                        for pricePropertyValue in pricePropertyValues:
                            pjt_properties_key = pricePropertyValue["value"]
                            pjt_properties_value = pricePropertyValue["id"]
                            dic_pjt_properties[pjt_properties_key] = pjt_properties_value
                    pricePropertyValues[0]["isPreferred"] = True
                    post_CN_li.append(pricePropertyValues[0]["value"])
                    try:
                        post_id_li.append(dic_pjt_properties[pricePropertyValues[0]["value"]])
                    except KeyError as e:
                        print(pricePropertyValues)
                        print(dic_pjt_properties)
        except KeyError as e:
            print_exc()
        try:
            # 选择功能情况
            try:
                function_infos = js_data[2]["properties"]
            except KeyError as e:
                function_infos = js_data["functionInfos"]
                for ite in function_infos:
                    ite["pricePropertyValues"] = ite["pricePropertyValueVos"]
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
                flag_ = True
                for pricePropertyValue in pricePropertyValues:
                    if (pricePropertyValue["value"] in damageInfor_CN_li):
                        flag_ = False
                        pricePropertyValue["isPreferred"] = True
                        post_CN_li.append(pricePropertyValue["value"])
                        post_id_li.append(dic_pjt_properties[pricePropertyValue["value"]])
                        break
                    else:
                        pricePropertyValue["isPreferred"] = False
                if (flag_):
                    pricePropertyValues[0]["isPreferred"] = True
                    post_CN_li.append(pricePropertyValues[0]["value"])
                    try:
                        post_id_li.append(dic_pjt_properties[pricePropertyValues[0]["value"]])
                    except KeyError as e:
                        post_id_li.append(pricePropertyValues[0]["id"])
        except KeyError as e:
            print_exc()

        for i in range(len(post_id_li)):
            if (post_id_li[i] == 10203):
                post_id_li[i] = 9625
                post_CN_li[i] = "已激活，可还原"
            elif (post_id_li[i] == 20267):
                post_id_li[i] = 20268
                post_CN_li[i] = "90%＜电池健康度≤99%"
            elif (post_id_li[i] == 2124):
                post_id_li[i] = 2125
                post_CN_li[i] = "外壳完美"
        return post_id_li, post_CN_li

    def get_jsdataByProductId(self,ProductId):
        try:
            dic_productId_allJson = self.dic_productId_allJson
            return dic_productId_allJson[str(ProductId)]
        except KeyError as e:
            pass

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
        return standardsCode_li

    def returnSearchPriceParam(self, data):
        try:
            data["damageInfor"] = json.loads(data["damageInfor"])
        except Exception as e:
            pass

        temp_model = data["model"]
        data["model"] = str(data["model"]).replace(" ", "").lower().replace("vivo iqoo", "iqoo")
        if(type(data["model"]) != int):
            try:
                data["model"] = self.model_id_dic[data["model"]]
            except KeyError as e:
                try:
                    data["model"] = self.model_id_dic2[data["model"]]
                except KeyError as e:
                    if ("红米" in data["model"] or "Redmi" in data["model"]):
                        data["model"] = str(data["model"].replace("红米", "Redmi")).lower()
                        try:
                            data["model"] = str(data["model"]).replace("5g","5G版")
                            data["model"] = self.model_id_dic[data["model"]]
                        except KeyError as e:
                            try:
                                data["model"] = self.model_id_dic2[data["model"]]
                            except KeyError as e:
                                try:
                                    data["model"] = str(data["model"]).replace("（5G版）", "").replace("(5G版)", "")
                                    data["model"] = self.model_id_dic[data["model"]]
                                except KeyError as e:
                                    try:
                                        data["model"] = self.model_id_dic2[data["model"]]
                                    except KeyError as e:
                                        return {"msg":"不存在对应机型product_id","model":temp_model}
                    else:
                        return {"msg":"不存在对应机型product_id","model":temp_model}

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
if __name__ == '__main__':

    #安卓手机数据传入 例
    data =   {
        "model": "华为 Mate 10",
        "netWork":"全网通",
        "purchase_channel":"国行",
        "color": "香槟金",
        "ram": "6G",
        "storage": "128GB",
        "warranty_period":"",
        "damageInfor":
        {"屏幕外观": "屏有硬划痕（≥10毫米）", "屏幕显示": "轻微亮度问题(亮点/亮斑/背光不均/黑角/进灰)", "边框背板": "外壳明显磕碰/掉漆（≥3毫米），或镜片破损"}
    }
    trans = paramTransfer()
    result = trans.returnSearchPriceParam(data)
    print(result)


    #苹果手机数据传入 例
    data =   {
        "model": "苹果 iPhone 12",
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
    print(len(result["pjt_post_data"]["post_id_li"]))
    print(len(result["pjt_post_data"]["post_CN_li"]))
    print(result)



