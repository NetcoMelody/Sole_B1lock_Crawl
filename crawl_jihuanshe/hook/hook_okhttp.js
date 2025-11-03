// hook_all_network_safe.js
Java.perform(() => {
    const RealCall = Java.use("okhttp3.RealCall");
    RealCall.execute.implementation = function () {
        try {
            const request = this.request();
            const url = request.url().toString();
            if (url.startsWith("https://")) {
                console.log("\n[🌐 HTTPS REQUEST]");
                console.log("[URL] " + url);

                const method = request.method();
                console.log("[METHOD] " + method);

                // 仅对 POST/PUT 等有 body 的方法尝试读取
                if (method === "POST" || method === "PUT") {
                    const body = request.body();
                    if (body !== null) {
                        try {
                            // 创建新 Buffer，避免污染原请求
                            const bufferClass = Java.use("okhttp3.Buffer");
                            const buffer = bufferClass.$new();
                            // 关键：只读一次
                            body.writeTo(buffer);
                            const byteArr = buffer.readByteArray();
                            if (byteArr !== null && byteArr.length > 0) {
                                // 尝试 UTF-8 解码（仅当看起来像文本）
                                const str = Java.use("java.lang.String").$new(byteArr);
                                if (str.length < 1000 && (str.indexOf("{") !== -1 || str.indexOf("=") !== -1)) {
                                    console.log("[BODY] " + str);
                                } else {
                                    console.log("[BODY] <binary or encrypted, len=" + byteArr.length + ">");
                                }
                            }
                        } catch (e) {
                            console.log("[BODY] <read failed: " + e.message + ">");
                        }
                    }
                }
            }
        } catch (e) {
            console.log("[!] Error in hook: " + e.message);
            // 即使出错，也必须返回原结果，否则 crash
        }

        // ⚠️ 必须调用原始方法并返回结果
        return this.execute();
    };
});