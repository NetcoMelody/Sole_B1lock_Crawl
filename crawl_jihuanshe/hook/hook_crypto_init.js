// hook_cipher_init.js
Java.perform(() => {
    console.log("[🔍] Hooking Cipher.init to capture key and algorithm...");

    const Cipher = Java.use("javax.crypto.Cipher");
    const SecretKeySpec = Java.use("javax.crypto.spec.SecretKeySpec");
    const IvParameterSpec = Java.use("javax.crypto.spec.IvParameterSpec");
    const String = Java.use("java.lang.String");

    // Hook SecretKeySpec 构造（捕获密钥）
    SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function(keyBytes, algorithm) {
        console.log("\n[🗝️] SecretKeySpec 被创建");
        console.log("  算法:", algorithm);
        console.log("  密钥长度 (bytes):", keyBytes.length);

        // 尝试将密钥转为字符串
        try {
            const keyStr = String.$new(keyBytes);
            if (/^[A-Za-z0-9!@#$%^&*()_+\-=]+$/.test(keyStr)) {
                console.log("  密钥 (ASCII):", keyStr);
            } else {
                // 转为 hex
                const hex = Array.from(keyBytes).map(b => b.toString(16).padStart(2, '0')).join('');
                console.log("  密钥 (hex):", hex);
            }
        } catch (e) {
            const hex = Array.from(keyBytes).map(b => b.toString(16).padStart(2, '0')).join('');
            console.log("  密钥 (hex):", hex);
        }

        return this.$init(keyBytes, algorithm);
    };

    // Hook IvParameterSpec 构造（捕获 IV）
    IvParameterSpec.$init.overload('[B').implementation = function(ivBytes) {
        console.log("\n[🌀] IvParameterSpec 被创建");
        console.log("  IV 长度:", ivBytes.length);
        const hex = Array.from(ivBytes).map(b => b.toString(16).padStart(2, '0')).join('');
        console.log("  IV (hex):", hex);
        return this.$init(ivBytes);
    };

    // Hook Cipher.init
    Cipher.init.overload('int', 'java.security.Key').implementation = function(opmode, key) {
        console.log("\n[⚙️] Cipher.init (无 IV)");
        console.log("  模式:", opmode === 1 ? "ENCRYPT_MODE" : "DECRYPT_MODE");
        return this.init(opmode, key);
    };

    Cipher.init.overload('int', 'java.security.Key', 'java.security.spec.AlgorithmParameterSpec').implementation = function(opmode, key, params) {
        console.log("\n[⚙️] Cipher.init (带参数)");
        console.log("  模式:", opmode === 1 ? "ENCRYPT_MODE" : "DECRYPT_MODE");
        return this.init(opmode, key, params);
    };

    console.log("[✅] Hook 安装完成，触发请求...");
});