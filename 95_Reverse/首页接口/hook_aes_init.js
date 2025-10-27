Java.perform(function () {
    const targetPath = "/api/v1/goods/list/recommendation";
    let lastTargetReqId = null;
    let lastTargetTime = 0;

    // 缓存全局密钥（用于后续请求即使未触发 init）
    let globalCachedKey = null;
    let globalCachedIV = null;

    // 工具函数：bytes 转 hex
    function bytesToHex(bytes) {
        if (!bytes || bytes.length === 0) return "";
        let hex = "";
        for (let i = 0; i < bytes.length; i++) {
            hex += (bytes[i] & 0xff).toString(16).padStart(2, '0');
        }
        return hex;
    }

    function isInTargetContext() {
        return lastTargetReqId !== null && (Date.now() - lastTargetTime) <= 10000;
    }

    // ===== Hook 请求发起 =====
    const OkHttpClient = Java.use("okhttp3.OkHttpClient");
    OkHttpClient.newCall.implementation = function (request) {
        try {
            const urlStr = request.url().toString();
            if (urlStr.includes(targetPath)) {
                lastTargetReqId = Date.now() + "_" + Math.random().toString(36).substr(2, 5);
                lastTargetTime = Date.now();
                console.log("\n[🌐 捕获目标请求] URL:", urlStr, "| ID:", lastTargetReqId);
                if (globalCachedKey) {
                    console.log("[💡 提示] 已缓存密钥，可用于此请求解密");
                }
            }
        } catch (e) {
            console.warn("[!] newCall Hook 异常:", e.message);
        }
        return this.newCall(request);
    };

    // ===== 全局上下文暂存 =====
    let currentAlgorithm = null;
    let currentIV = null;

    // ===== Hook Cipher.getInstance =====
    const Cipher = Java.use("javax.crypto.Cipher");
    Cipher.getInstance.overload('java.lang.String').implementation = function (transformation) {
        if (isInTargetContext()) {
            currentAlgorithm = transformation;
            console.log("[🔧 Cipher 算法]:", transformation, "| 关联请求 ID:", lastTargetReqId);
        }
        return this.getInstance(transformation);
    };

    // ===== Hook IV =====
    const IvParameterSpec = Java.use("javax.crypto.spec.IvParameterSpec");
    IvParameterSpec.$init.overload('[B').implementation = function (iv) {
        if (isInTargetContext()) {
            currentIV = bytesToHex(iv);
            console.log("[🎯 IV 创建]:", currentIV, "| 关联请求 ID:", lastTargetReqId);
        }
        return this.$init(iv);
    };

    // ===== Hook Cipher.init（仅捕获解密操作）=====
    Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec').implementation = function (opmode, key, params) {
        if (isInTargetContext()) {
            // 仅处理解密模式（Cipher.DECRYPT_MODE == 2）
            if (opmode !== 2) {
                return this.init(opmode, key, params);
            }

            try {
                const keyBytes = key.getEncoded();
                const keyHex = bytesToHex(keyBytes);
                const algorithm = currentAlgorithm || "[未知]";
                const ivHex = currentIV || "[未捕获]";

                console.log("\n" + "=".repeat(80));
                console.log("[🔐 目标接口 AES 密钥组 - 仅限 " + targetPath + "（解密）");
                console.log("  请求 ID    :", lastTargetReqId);
                console.log("  算法模式   :", algorithm);
                console.log("  操作方向   :", "DECRYPT");
                console.log("  Key (hex)  :", keyHex);
                console.log("  IV (hex)   :", ivHex);
                console.log("=".repeat(80));

                // 可选：缓存解密用的 AES-256 密钥（32字节 = 64 hex）
                if (keyHex.length === 64) {
                    globalCachedKey = keyHex;
                    globalCachedIV = ivHex;
                    console.log("[💾] 已缓存 AES-256 解密密钥，可用于后续流量解密");
                }

            } catch (e) {
                console.warn("[!] Cipher.init 解析异常:", e.message);
            }
        }
        return this.init(opmode, key, params);
    };

    // ===== Hook doFinal（可选：用于确认解密行为）=====
    Cipher.doFinal.overload('[B').implementation = function (input) {
        if (isInTargetContext()) {
            console.log("[⚡] doFinal 被调用 | 输入长度:", input.length, "| 请求 ID:", lastTargetReqId);
        }
        return this.doFinal(input);
    };

    console.log("[✅] 已启用目标接口 AES 解密密钥捕获：", targetPath);
    console.log("[ℹ️] 仅当发生解密操作（密文 → 明文）时打印密钥");
    console.log("[ℹ️] 首次捕获的解密密钥将自动缓存，可用于手动解密后续响应");
});