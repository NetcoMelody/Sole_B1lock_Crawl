import asyncio

import raw_generate
import data_title_handle
import data_size_handle
import data_handle_final

async def handle_main():
    sku_list_str = "IM6687-262,DR5415-100,FV5029-100,DM7866-202,IB8958-001,DM7866-200,IB8958-001,HF4340-800,553558-414,FQ8138-001,DZ4137-700,IH0296-400,IO3372-700,IB8967-004,DV4982-004,DZ5485-008"
    await raw_generate.main(sku_list_str)
    await data_title_handle.main(sku_list_str)
    await data_size_handle.main(sku_list_str)
    await data_handle_final.main(sku_list_str)

if __name__ == '__main__':
    asyncio.run(handle_main())
