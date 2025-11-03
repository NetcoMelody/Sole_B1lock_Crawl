import asyncio
import pandas

async def stream_output(stream, prefix):
    """异步流式读取并打印输出"""
    while True:
        line = await stream.readline()
        if not line:
            break
        print(f"{prefix}{line.decode().rstrip()}")

async def main():
    df = pandas.read_csv("itemcodes.csv")

    browser_item_codes = ""
    for index,row in df.iterrows():
        itemCode = row["itemCode"]

        if pandas.isna(itemCode):
            continue
        itemCode = str(int(itemCode))
        browser_item_code =  f"v1|{itemCode}|0,"
        browser_item_codes += browser_item_code
        print ("browseCode:",browser_item_code)
    print(browser_item_codes)

    # ✅ 启动进程（不等待结束）
    diy  = f"v1|389157683429|0"
    process = await asyncio.create_subprocess_exec(
        "go", "run", "ebay_getItem_with_itemcode.go", browser_item_codes,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # ✅ 同时异步流式读取 stdout 和 stderr
    stdout_task = asyncio.create_task(stream_output(process.stdout, "🟢 "))
    stderr_task = asyncio.create_task(stream_output(process.stderr, "🔴 "))

    # ✅ 等待进程结束
    await process.wait()

    # ✅ 等待所有输出流读取完成
    await asyncio.gather(stdout_task, stderr_task)

    # ✅ 打印执行状态
    if process.returncode == 0:
        print("\n✅ Go 程序执行成功")
    else:
        print(f"\n❌ Go 程序执行失败，退出码: {process.returncode}")

if __name__ == '__main__':
    asyncio.run(main())