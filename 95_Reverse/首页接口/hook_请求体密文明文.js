// hook_精准请求体构建.js
Java.perform(() => {
    console.log("[+] 开始精准Hook请求体构建");

    const JSONObject = Java.use("org.json.JSONObject");
    const HashMap = Java.use("java.util.HashMap");
    const RequestBody = Java.use("okhttp3.RequestBody");
    const ByteString = Java.use("com.android.okhttp.okio.ByteString");
    const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");

    // 1. 精准监控业务明文数据构建
    JSONObject.put.overload('java.lang.String', 'java.lang.Object').implementation = function(key, value) {
        if (value !== null) {
            const valueStr = value.toString();
            // 只捕获包含核心业务关键词的明文数据
            if (key === "data" && valueStr.includes("words_list")) {
                console.log("\n[🎯] 核心业务明文数据捕获");
                console.log("Key:", key);
                console.log("完整明文数据:", valueStr);

                // 获取调用栈追踪数据流向
                const stack = Java.use("java.lang.Thread").currentThread().getStackTrace();
                console.log("调用栈:");
                for (let i = 0; i < Math.min(stack.length, 5); i++) {
                    console.log("  ", stack[i].toString());
                }
            }
        }
        return this.put(key, value);
    };

    // 2. 精准监控Map中的核心业务数据
    HashMap.put.implementation = function(key, value) {
        if (key !== null && value !== null) {
            const keyStr = key.toString();
            const valueStr = value.toString();

            // 只捕获与请求体构建相关的核心数据
            if (keyStr === "data" && valueStr.includes("words_list")) {
                console.log("\n[📦] 核心请求体数据Map");
                console.log("Key:", keyStr);
                console.log("Value:", valueStr);
            }
        }
        return this.put(key, value);
    };

    // 3. 监控请求体创建过程
    RequestBody.create.overload('okhttp3.MediaType', 'java.lang.String').implementation = function(contentType, content) {
        if (content && content.includes('"data":')) {
            console.log("\n[📝] 最终请求体创建");
            console.log("Content-Type:", contentType ? contentType.toString() : "null");
            console.log("完整请求体:", content);
        }
        return this.create(contentType, content);
    };

    // 4. 监控请求体加密过程
    SwSdk.heracles.overload('[B', 'int', 'int').implementation = function(a, b, c) {
        // 只关注请求体加密（输入较小）
        if (a.length < 1000 && a.length > 50) {
            console.log("\n[🔐] 请求体加密过程");
            console.log("输入长度:", a.length, "参数b:", b, "参数c:", c);

            try {
                const inputStr = ByteString.of(a).utf8();
                // 只输出看起来像明文的数据
                if (inputStr.includes("words_list") || inputStr.includes("show_word")) {
                    console.log("明文输入:", inputStr);
                }
            } catch (e) {
                console.log("输入为二进制数据");
            }

            const result = this.heracles(a, b, c);
            console.log("加密输出长度:", result.length);

            try {
                const outputStr = ByteString.of(result).utf8();
                if (outputStr.includes('.')) {
                    console.log("🎯 加密结果:", outputStr);
                }
            } catch (e) {
                console.log("输出分析失败");
            }

            return result;
        }
        return this.heracles(a, b, c);
    };

    console.log("[+] 精准Hook已就绪");
});
