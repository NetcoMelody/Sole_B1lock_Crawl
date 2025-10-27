from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from Function.NS_export import Products_Export
from Function.Order_export import order_out
from Function.Update_price import main,update_price_main
from Function.smtp发送 import email_send
from pydantic import BaseModel
import json
import aiopandas
from aioconsole import aprint
app = FastAPI()
app.mount('/static',StaticFiles(directory='static'),name='static')
@app.get('/')
async def index():
    with open('web/Tools_Site.html', mode='r', encoding='utf-8') as file:
        dom = file.read()
    return HTMLResponse(content=dom)

@app.get('/get_NS_Export')
async def get_Ns_Export(sku:str):
    data_list = sku.split(',')
    ns_export = Products_Export()
    await ns_export.handle(data_list)
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
    my_price_factor:str='0.88'
    dw_price_factor:str='0.88'
@app.post('/post_update')
async def post_update(json_data:post_update_struct):
    form_data = json_data.model_dump()
    update_type = form_data['type']
    my_price_factor = float(form_data['my_price_factor'])
    dw_price_factor = float(form_data['dw_price_factor'])

    if update_type == '1':
        await main(my_price_factor,dw_price_factor)
    elif update_type == '2':
        skus = form_data['skus']

        data = {
            'df': skus,
            'my_price_factor': [my_price_factor],
            'dw_price_factor': [dw_price_factor],
        }
        df =  aiopandas.DataFrame(data)
        df.to_csv('D:/PythonProject_UV/Fusion/SKU_white_list.csv',index=False)
        await aprint ('白名单已写入')
        await update_price_main(skus,my_price_factor,dw_price_factor)
    return HTMLResponse(content='更新成功')

class email_struct(BaseModel):
    receiver_email:str
    msg:str
@app.post('/post_email_send')
def email_auto_send(json_data:email_struct):
    data = json_data.model_dump()
    receiver_str = data['receiver_email']
    sender = email_send(receiver_str)
    sender.email_main()
    msg = {'msg':'发送成功'}
    json_send_data = json.dumps(msg)
    return json_send_data

if __name__ == '__main__':
    uvicorn.run('后端:app', host="192.168.0.18", port=8080)
