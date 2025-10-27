Java.perform(() => {
    const TARGET = "/api/v1/goods/list/recommendation";
    let currentUrl = null;
    let capturedKey = null;   // ← 替代 global.key
    let capturedIV = null;    // ← 替代 global.iv

    // 1. 标记目标请求
    const OkHttpClient = Java.use("okhttp3.OkHttpClient");
    OkHttpClient.newCall.implementation = function (request) {
        const url = request.url().toString();
        if (url.includes(TARGET)) {
            console.log("[📡] 目标请求:", url);
            currentUrl = url;
            capturedKey = null;
            capturedIV = null;
            setTimeout(() => { currentUrl = null; }, 15000);
        }
        return this.newCall(request);
    };

    // 2. Hook IV
    const IvParameterSpec = Java.use("javax.crypto.spec.IvParameterSpec");
    IvParameterSpec.$init.overload('[B').implementation = function (iv) {
        if (currentUrl) {
            try {
                const ivHex = bytesToHex(iv);
                console.log("[🔑 IV (from IvParameterSpec)]:", ivHex);
                capturedIV = ivHex;
            } catch (e) {
                console.warn("[⚠️] IV 获取失败:", e.message);
            }
        }
        return this.$init(iv);
    };

    // 3. Hook Key
    const SecretKeySpec = Java.use("javax.crypto.spec.SecretKeySpec");
    SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function (key, algorithm) {
        if (currentUrl && algorithm.toLowerCase().includes("aes")) {
            try {
                const keyHex = bytesToHex(key);
                console.log("[🔑 Key (from SecretKeySpec)]:", keyHex);
                capturedKey = keyHex;
            } catch (e) {
                console.warn("[⚠️] Key 获取失败:", e.message);
            }
        }
        return this.$init(key, algorithm);
    };

    // 4. Hook 解密结果
    const Cipher = Java.use("javax.crypto.Cipher");
    Cipher.doFinal.overload('[B').implementation = function (input) {
        const result = this.doFinal(input);
        if (currentUrl) {
            try {
                const encryptedHex = bytesToHex(input);
                const String = Java.use("java.lang.String");
                const decryptedStr = String.$new(result).toString();

                console.log("\n" + "=".repeat(60));
                console.log("[✅] 响应解密成功!");
                console.log("URL       :", currentUrl);
                console.log("Key       :", capturedKey || "N/A");
                console.log("IV        :", capturedIV || "N/A");
                console.log("密文(hex) :", encryptedHex);
                console.log("明文      :", decryptedStr);
                console.log("=".repeat(60) + "\n");

                // 可选：清空（但不影响）
                // capturedKey = null;
                // capturedIV = null;
            } catch (e) {
                console.error("[❌] doFinal 解析失败:", e.message);
            }
        }
        return result;
    };

    // 安全的 bytes -> hex
    function bytesToHex(bytes) {
        if (!bytes || bytes.length === 0) return "";
        let hex = "";
        for (let i = 0; i < bytes.length; i++) {
            hex += (bytes[i] & 0xff).toString(16).padStart(2, '0');
        }
        return hex;
    }

    console.log("[+] 已启动：Hook SecretKeySpec + IvParameterSpec + doFinal");
});