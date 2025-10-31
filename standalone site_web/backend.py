from fastapi import FastAPI,Request,UploadFile,File,WebSocket
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from Function.NS_export import Products_Export
from Function.Order_export import order_out
from Function.Update_price import update_main
from Function.smtp_batch import email_send
from Function.recordChange import main
import asyncio
from pydantic import BaseModel
import json
import aiopandas
from aioconsole import aprint
import os.path
import aiofiles
from Function.update_desc_with_llm import update_desc_main
app = FastAPI()
app.mount('/static',StaticFiles(directory='static'),name='static')
@app.get('/')
async def index():
    async with aiofiles.open('web/Tools_Site.html', mode='r', encoding='utf-8') as file:
        dom = await file.read()
    return HTMLResponse(content=dom)
@app.get('/get_NS_Export')
async def get_Ns_Export(sku:str):
    ns_export = Products_Export()
    await ns_export.handle(sku)
    return FileResponse('./file/ns产品查询结果.csv')
@app.get('/get_orders_export')
async def get_orders_export(order_type:str,order_id:str=None):
    orders_export = order_out()
    if order_id is not None:
        data_list = order_id.split(',')
        await orders_export.handle(order_type, data_list)
        return FileResponse('./file/订单查询结果.csv')
    else:
        await orders_export.handle(order_type)
        return FileResponse('./file/订单查询结果.csv')

class post_update_struct(BaseModel):
    type:str
    skus:str
    flag:str= 'false'
    my_price_factor:str='0.8'
    dw_price_factor:str='0.8'

@app.post('/post_update')
async def post_update(json_data:post_update_struct):
    data = json_data.model_dump()
    update_type = data['type']
    my_price_factor = float(data['my_price_factor'])
    dw_price_factor = float(data['dw_price_factor'])
    flag = data['flag']

    if update_type == '1':
        await main(my_price_factor,dw_price_factor,flag)

    elif update_type == '2':
        skus = data['skus']
        match_value_1 = data['my_price_factor'].strip()
        match_value_2 = data['dw_price_factor'].strip()
        skus = skus.split(',')
        len_max = len(skus)
        data_dict = {
            'sku': skus,
            'My_price_factor_new': [my_price_factor] * len_max,
            'Dw_price_factor_new': [dw_price_factor] * len_max,
        }
        df_sku = aiopandas.DataFrame(data_dict)
        flag_data_dict = {
            'sku': skus,
            'flag_new': [flag] * len_max,
        }
        flag_df = aiopandas.DataFrame(flag_data_dict)
        if flag == 'true':
            if os.path.exists('D:/PythonProject_UV/Fusion/sale_white_list.csv'):
                df_old = aiopandas.read_csv('D:/PythonProject_UV/Fusion/sale_white_list.csv')
                df_merge = aiopandas.merge(df_old, flag_df, how='left', on='sku')
                mask = df_merge['flag_new'].notna()
                df_merge.loc[mask, 'flag'] = df_merge.loc[mask, 'flag_new']
                df_merge = df_merge[['sku','flag']]
                df_merge.to_csv('D:/PythonProject_UV/Fusion/sale_white_list.csv', index=False)
                sku_list = df_merge['sku'].tolist()
                not_in_list = []
                for sku in skus:
                    if sku not in sku_list:
                        not_in_list.append(sku)
                if not_in_list:
                    new_data = {
                        'sku': not_in_list,
                        'flag': [flag] * len(not_in_list)
                    }
                    df_new = aiopandas.DataFrame(new_data)
                    df_merge_new = aiopandas.concat([df_merge, df_new], ignore_index=True)
                    df_merge_new = df_merge_new[['sku', 'flag']]
                    df_merge_new.to_csv('D:/PythonProject_UV/Fusion/sale_white_list.csv', index=False)
                    await aprint('促销名单已创建')

            else:
                flag_df.rename(columns={'flag_new': 'flag'}, inplace=True)
                print (flag_df)
                flag_df.to_csv('D:/PythonProject_UV/Fusion/sale_white_list.csv', index=False)
                await aprint('促销名单已创建')

        elif flag == 'false':
            if os.path.exists('D:/PythonProject_UV/Fusion/sale_white_list.csv'):
                df_old = aiopandas.read_csv('D:/PythonProject_UV/Fusion/sale_white_list.csv')
                df_merge = aiopandas.merge(df_old, flag_df, how='left', on='sku')
                mask = df_merge['flag_new'].notna()
                df_merge.loc[mask, 'flag'] = df_merge.loc[mask, 'flag_new']
                df_merge = df_merge[['sku', 'flag']]
                mask = df_merge['flag'] == 'false'
                df_merge_new = df_merge[~mask]
                df_merge_new.to_csv('D:/PythonProject_UV/Fusion/sale_white_list.csv', index=False)
                await aprint('促销名单已更新')

        if (match_value_1 != '0.8' or match_value_2 != '0.8') or (match_value_1 != '0.8' and match_value_2 != '0.8'):
            if os.path.exists('SKU_white_list.csv'):
                df_old = aiopandas.read_csv('SKU_white_list.csv')
                df_old.to_csv('df_old.csv',index=False)
                df_merge = aiopandas.merge(df_old, df_sku, how='left', on='sku')
                df_merge.to_csv('df_merge.csv', index=False)
                mask = df_merge['My_price_factor_new'].notna()
                df_merge.loc[mask, 'My_price_factor'] = df_merge.loc[mask, 'My_price_factor_new']
                mask = df_merge['Dw_price_factor_new'].notna()
                df_merge.loc[mask, 'Dw_price_factor'] = df_merge.loc[mask, 'Dw_price_factor_new']
                sku_list = df_merge['sku'].tolist()
                not_in_list = []
                for sku in skus:
                    if sku not in sku_list:
                        not_in_list.append(sku)
                if not_in_list:
                    new_data = {
                        'sku': not_in_list,
                        'My_price_factor': [my_price_factor] * len(not_in_list),
                        'Dw_price_factor': [dw_price_factor] * len(not_in_list)
                    }
                    df_new = aiopandas.DataFrame(new_data)
                    df_merge_new = aiopandas.concat([df_merge, df_new], ignore_index=True)
                    df_merge_new = df_merge_new[['sku', 'My_price_factor', 'Dw_price_factor']]
                    df_merge_new.to_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', index=False)
                else:
                    df_merge_new = df_merge[['sku', 'My_price_factor', 'Dw_price_factor']]
                    df_merge_new.to_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', index=False)
                await aprint('白名单已写入')
            else:
                df_sku.rename(columns={'My_price_factor_new': 'My_price_factor', 'Dw_price_factor_new': 'Dw_price_factor'},inplace=True)
                await aprint('白名单已创建')
                df_sku.to_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv',index=False)

        else:
            df_sku = aiopandas.DataFrame(data_dict)
            if os.path.exists('D:/PythonProject_UV/Fusion/SKU_white_list.csv'):
                df_old = aiopandas.read_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv')
                df_merge = aiopandas.merge(df_old, df_sku, how='left', on='sku')
                mask = df_merge['My_price_factor_new'].notna()
                df_merge.loc[mask, 'My_price_factor'] = df_merge.loc[mask, 'My_price_factor_new']
                mask = df_merge['Dw_price_factor_new'].notna()
                df_merge.loc[mask, 'Dw_price_factor'] = df_merge.loc[mask, 'Dw_price_factor_new']
                df_merge = df_merge[['sku', 'My_price_factor', 'Dw_price_factor']]
                mask = (df_merge['My_price_factor'] == 0.8) & (df_merge['My_price_factor'] == 0.8)
                df_merge_new = df_merge[~mask]
                df_merge_new.to_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv', index=False)
        await update_main(skus,my_price_factor,dw_price_factor,flag)
    return HTMLResponse(content='更新成功')



# @app.get('/data_visualization')
# async def data_visualization():
#     dom = main()
#     return HTMLResponse(content=dom)

class update_desc_verify(BaseModel):
    skus:str
@app.post('/update_desc')
async def update_desc(data_json:update_desc_verify):
    data = data_json.model_dump()
    skus = data['skus']
    await update_desc_main(skus)
    return {
        'msg':'更新完成'
    }

if __name__ == '__main__':
    uvicorn.run('backend:app', host="192.168.0.18", port=8080)
