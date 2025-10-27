// /api/v1/goods/list/recommendation关于这个接口的响应体黑盒解密

Java.perform(() => {
    // 获取目标类
    const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");

    // 创建测试函数 - 支持Base64URL解码
    function testHeraclesDecryption() {
        console.log("[🔍] 开始黑盒解密测试");

        try {
            // Base64URL编码的密文
            const base64UrlCipher = "";

            // 使用Base64URL解码
            const Base64 = Java.use("java.util.Base64");
            // Base64URL解码需要将 '-' 替换为 '+'，'_' 替换为 '/'，并根据需要添加填充
            let standardBase64 = base64UrlCipher.replace(/-/g, '+').replace(/_/g, '/');
            // 添加必要的填充
            while (standardBase64.length % 4 !== 0) {
                standardBase64 += '=';
            }

            const cipherBytes = Base64.getDecoder().decode(standardBase64);

            // 调用 heracles 方法进行解密
            // 根据之前分析，heracles([B, int, int)
            const oriLen = cipherBytes.length;  // 原始长度
            const extraLen = 0;                 // 额外长度，可根据实际情况调整

            console.log("[🔧] 调用参数:");
            console.log("  密文长度:", oriLen);
            console.log("  额外长度:", extraLen);

            // 执行解密
            const result = SwSdk.heracles(cipherBytes, oriLen, extraLen);

            // 尝试转换为明文
            if (result) {
                try {
                    const plainText = Java.use("java.lang.String").$new(result);
                    console.log("[✅] 解密成功:");
                    console.log("  明文:", plainText);
                    return plainText;
                } catch (e) {
                    console.log("[⚠️] 解密结果非UTF-8文本，字节长度:", result.length);
                    // 可以进一步处理二进制数据
                    return result;
                }
            } else {
                console.log("[❌] 解密返回空结果");
                return null;
            }

        } catch (e) {
            console.log("[❌] 解密过程出错:", e.message);
            console.log("[🔧] 错误堆栈:", e.stack);
            return null;
        }
    }

    // 暴露到全局作用域，方便在 Frida 控制台调用
    globalThis.testHeraclesDecryption = testHeraclesDecryption;

    console.log("[+] 黑盒解密功能已准备就绪");
    console.log("[💡] 使用方法: testHeraclesDecryption()");

    // 自动运行解密功能
    console.log("[🚀] 自动执行解密测试...");
    setTimeout(() => {
        testHeraclesDecryption();
    }, 1000);
});
