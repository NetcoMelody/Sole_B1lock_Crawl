from adbutils import adb

# 列出所有连接的设备
devices = adb.device_list()
print("已连接设备数量:", len(devices))

if devices:
    d = devices[0]  # 获取第一个设备
    print("设备序列号:", d.serial)
    print("设备状态:", d.get_state())

    # 执行 shell 命令（例如获取 Android 版本）
    android_version = d.shell("getprop ro.build.version.release").strip()
    print("Android 版本:", android_version)

    # 检查是否能正常通信
    print("ADB 连接测试成功！")
else:
    print("未检测到任何 ADB 设备，请检查连接和 USB 调试设置。")