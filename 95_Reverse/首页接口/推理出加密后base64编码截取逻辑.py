import base64

# achilles 输出的完整 Base64（标准）
full_b64 = "MDAyNGE5dzNHS0RFNk93MzVEYzRzYmx5dXFxUDRwN2V6cUNxQThxNDgxRDczQUEwNUFFODgwRDI5QjAwMkQ5NkNGMUVDMTY2LmNHRnlZVzBmWXpBMU9UUm1PVGN0TURaalpTMDBORFZrTFRnd09HVXRPVFkyTjJJMU5URmlNVFEzSG5abGNuTnBiMjRmTVI1d2JHRjBabTl5YlI5aGJtUnliMmxrSG1Wakh6RT0umO4PayTowfyOCL9NqLFiSMfCskGIqVThWggR1oq4U9o6qnn8x5EEVFZofxHapDE87PeJyj6LN4Ab229tZ5lD0yeYM3_BPJWwFPDDxppies09xvERMVIOKjriMC4eamiRRdz9HRssf8aNvN5JXHQe_T1F2cANel_dTWGoVJGCFZiqoUU1xj7NAg1v8P0WLYy2EgUOeTzBmMDdAC86caUzPBVe7yEC8wQmYw2kW670TgiJNVzqYTH0r-mYZhE28riGa2CC0MCNmgVNbQTlYJ_DwBcqQ4XAxdZBLwdBlAGd-ITG030mEEJEd56bQ5ximwMHUXqtfIE3LYGHpA0qvZKUWnLu3Dlfkc_x37xg2BImkDptLzc5Ya_K-6E3tiruU2YbKFzKoGpndgpet86IXMN_H6Grjd5jsiLnveyChceFT47ISovMw7RVjw=="

# 抓包密文（URL 安全）
capture_urlsafe = "ODFENzNBQTA1QUU4ODBEMjlCMDAyRDk2Q0YxRUMxNjYuY0dGeVlXMGZZekExT1RSbU9UY3RNRFpqWlMwME5EVmtMVGd3T0dVdE9UWTJOMkkxTlRGaU1UUTNIblpsY25OcGIyNGZNUjV3YkdGMFptOXliUjloYm1SeWIybGtIbVZqSHpFPS6Y7g9rJOjB_I4Iv02osWJIx8KyQYipVOFaCBHWirhT2jqqefzHkQRUVmh_EdqkMTzs94nKPos3gBvbb21nmUPTJ5gzf8E8lbAU8MPGmmJ6zT3G8RExUg4qOuIwLh5qaJFF3P0dGyx_xo283klcdB79PUXZwA16X91NYahUkYIVmKqhRTXGPs0CDW_w_RYtjLYSBQ55PMGYwN0ALzpxpTM8FV7vIQLzBCZjDaRbrvROCIk1XOphMfSv6ZhmETbyuIZrYILQwI2aBU1tBOVgn8PAFypDhcDF1kEvB0GUAZ34hMbTfSYQQkR3nptDnGKbAwdReq18gTctgYekDSq9kpRacu7cOV-Rz_HfvGDYEiaQOm0vNzlhr8r7oTe2Ku5TZhsoXMqgamd2Cl63zohcw38foauN3mOyIue97IKFx4VPjshKi8zDtFWP"

# Step 1: 解码 achilles 的完整 Base64
full_bytes = base64.b64decode(full_b64)

# Step 2: 尝试跳过前 N 字节（N=5, 8, 16, 32...）
for skip in [5, 8, 16, 24, 32, 40]:
    if skip < len(full_bytes):
        payload = full_bytes[skip:]
        # 编码为 URL 安全 Base64
        b64_urlsafe = base64.urlsafe_b64encode(payload).decode().rstrip('=')
        if b64_urlsafe == capture_urlsafe:
            print(f"✅ 匹配成功！跳过前 {skip} 字节")
            exit(0)
        # 检查开头是否匹配（避免长度差异）
        if b64_urlsafe.startswith(capture_urlsafe[:50]):
            print(f"🔍 可能匹配（跳过 {skip} 字节），开头一致")
print("❌ 未找到匹配的 skip 值")