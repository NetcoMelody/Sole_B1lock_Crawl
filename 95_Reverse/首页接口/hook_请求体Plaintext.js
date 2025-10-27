// 监控achilles方法调用
Java.perform(() => {
    const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");

    // Hook四参数版本，专门监控请求体加密
    SwSdk.achilles.overload('[B', 'java.lang.String', 'int', 'long').implementation = function(a, b, c, d) {
        console.log("\n[🔐] 请求体加密调用(Achilles)");
        console.log("密钥/标识:", b);
        console.log("算法参数:", c);
        console.log("时间戳:", d);

        // 记录明文输入
        try {
            const inputStr = Java.use("com.android.okhttp.okio.ByteString").of(a).utf8();
            console.log("明文输入:", inputStr);
        } catch (e) {
            console.log("输入为二进制数据");
        }

        const result = this.achilles(a, b, c, d);
        console.log("加密输出长度:", result.length);

        return result;
    };
});
