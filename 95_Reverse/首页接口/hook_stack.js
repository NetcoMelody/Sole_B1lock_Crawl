// hook_gson_with_stacktrace.js
Java.perform(function () {
    console.log("[*] 正在 Hook JSON 解析，并捕获调用栈...");

    const candidates = [
        'com.google.gson.Gson',
        'com.alibaba.fastjson.JSON',
        'org.json.JSONObject',
        'com.jiuwu.utils.JsonParser',
        'com.jiuwu.net.JsonUtil'
    ];

    let hookedCount = 0;

    // 辅助函数：获取当前 Java 调用栈（字符串形式）
    function getJavaStackTrace() {
        const Exception = Java.use('java.lang.Exception');
        const StringWriter = Java.use('java.io.StringWriter');
        const PrintWriter = Java.use('java.io.PrintWriter');

        const sw = StringWriter.$new();
        const pw = PrintWriter.$new(sw);
        const e = Exception.$new();
        e.printStackTrace(pw);
        pw.flush();
        return sw.toString();
    }

    for (let clsName of candidates) {
        try {
            let Cls = Java.use(clsName);
            console.log("[+] 尝试 Hook:", clsName);

            if (clsName.endsWith('Gson')) {
                Cls.fromJson.overload('java.lang.String', 'java.lang.Class').implementation = function (json, clazz) {
                    if (json && typeof json === 'string' && (json.includes("goods_id") || json.includes("recommendation"))) {
                        console.log("\n" + "=".repeat(60));
                        console.log("[✅] 商品数据（Gson）:");
                        console.log(json);
                        console.log("\n[🔍] 调用栈（Gson.fromJson）:");
                        console.log(getJavaStackTrace());
                        console.log("=".repeat(60) + "\n");
                    }
                    return this.fromJson(json, clazz);
                };
                hookedCount++;
            }
            else if (clsName.includes('fastjson')) {
                Cls.parseObject.overload('java.lang.String', 'java.lang.Class').implementation = function (text, clazz) {
                    if (text && typeof text === 'string' && text.includes("goods_id")) {
                        console.log("\n" + "=".repeat(60));
                        console.log("[✅] 商品数据（Fastjson）:");
                        console.log(text);
                        console.log("\n[🔍] 调用栈（Fastjson.parseObject）:");
                        console.log(getJavaStackTrace());
                        console.log("=".repeat(60) + "\n");
                    }
                    return this.parseObject(text, clazz);
                };
                hookedCount++;
            }
            else if (clsName.includes('JSONObject')) {
                Cls.$init.overload('java.lang.String').implementation = function (json) {
                    if (json && typeof json === 'string' && json.includes("goods_id")) {
                        console.log("\n" + "=".repeat(60));
                        console.log("[✅] 商品数据（JSONObject）:");
                        console.log(json);
                        console.log("\n[🔍] 调用栈（JSONObject.<init>）:");
                        console.log(getJavaStackTrace());
                        console.log("=".repeat(60) + "\n");
                    }
                    return this.$init(json);
                };
                hookedCount++;
            }
            else {
                if (clsName === 'com.jiuwu.utils.JsonParser') {
                    if (Cls.parse) {
                        Cls.parse.implementation = function (json) {
                            if (json && typeof json === 'string' && (json.includes("goods_id") || json.includes("recommendation"))) {
                                console.log("\n" + "=".repeat(60));
                                console.log("[✅] 商品数据（JsonParser）:");
                                console.log(json);
                                console.log("\n[🔍] 调用栈（JsonParser.parse）:");
                                console.log(getJavaStackTrace());
                                console.log("=".repeat(60) + "\n");
                            }
                            return this.parse(json);
                        };
                        hookedCount++;
                    }
                }
                else if (clsName === 'com.jiuwu.net.JsonUtil') {
                    if (Cls.fromJson) {
                        Cls.fromJson.overload('java.lang.String', 'java.lang.Class').implementation = function (json, clazz) {
                            if (json && typeof json === 'string' && json.includes("goods_id")) {
                                console.log("\n" + "=".repeat(60));
                                console.log("[✅] 商品数据（JsonUtil）:");
                                console.log(json);
                                console.log("\n[🔍] 调用栈（JsonUtil.fromJson）:");
                                console.log(getJavaStackTrace());
                                console.log("=".repeat(60) + "\n");
                            }
                            return this.fromJson(json, clazz);
                        };
                        hookedCount++;
                    }
                }
            }

            console.log("[+] Hook 成功:", clsName);
        } catch (e) {
            console.log("[-] Hook 失败:", clsName, e.message);
        }
    }

    console.log(`[*] 共成功 Hook ${hookedCount} 个 JSON 解析类`);
});