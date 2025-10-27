// hook_请求体编码位置监控.js
Java.perform(() => {
    console.log("[+] 开始监控请求体编码位置");

    // 监控目标类
    const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");
    const EncAndDecInterceptor = Java.use("com.shizhuang.dusanwa.network.EncAndDecInterceptor");
    const RequestBody = Java.use("okhttp3.RequestBody");
    const JSONObject = Java.use("org.json.JSONObject");

    // 1. 监控 Achilles 加密方法（简化版避免崩溃）
    if (SwSdk.achilles && SwSdk.achilles.overloads) {
        SwSdk.achilles.overload('[B', 'java.lang.String', 'int', 'long').implementation = function(a, b, c, d) {
            console.log("\n[🔐] Achilles加密调用");
            console.log("密钥:", b);
            console.log("算法参数:", c);
            console.log("时间戳:", d);
            console.log("输入长度:", a.length);

            // 直接调用原方法避免复杂处理
            const result = this.achilles(a, b, c, d);
            console.log("输出长度:", result.length);

            return result;
        };
    }

    // 2. 监控拦截器处理过程
    if (EncAndDecInterceptor.ll1lIll1II11 && EncAndDecInterceptor.ll1lIll1II11.overloads) {
        EncAndDecInterceptor.ll1lIll1II11.overload('okhttp3.Request', 'boolean').implementation = function(request, flag) {
            console.log("\n[🔄] 拦截器处理");
            console.log("URL:", request.url().toString());
            console.log("Method:", request.method());

            const result = this.ll1lIll1II11(request, flag);
            return result;
        };
    }

    // 3. 监控 RequestBody 创建过程
    if (RequestBody.create && RequestBody.create.overloads) {
        RequestBody.create.overload('okhttp3.MediaType', 'java.lang.String').implementation = function(contentType, content) {
            if (content && content.includes('"data":')) {
                console.log("\n[📝] RequestBody创建");
                console.log("Content-Type:", contentType ? contentType.toString() : "null");
                console.log("请求体内容长度:", content.length);
            }

            return this.create(contentType, content);
        };
    }

    // 4. 监控 JSON 数据构建过程
    if (JSONObject.put && JSONObject.put.overloads) {
        JSONObject.put.overload('java.lang.String', 'java.lang.Object').implementation = function(key, value) {
            if (key === "data") {
                console.log("\n[📊] JSON构建data字段");
                console.log("data值长度:", value ? value.toString().length : 0);
            }

            return this.put(key, value);
        };
    }

    console.log("[+] 监控已就绪");
});
