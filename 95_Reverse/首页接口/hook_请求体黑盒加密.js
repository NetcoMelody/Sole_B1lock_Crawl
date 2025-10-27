Java.perform(() => {
    const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");
    const Base64 = Java.use("android.util.Base64");
    const Arrays = Java.use("java.util.Arrays");
    const String = Java.use("java.lang.String");

    // 你想注入的明文（和抓包那次完全一致）
    const CUSTOM_PLAINTEXT = '{"cid":"","imei":"0113cf45c7cb0f13","oaid":"","page":1,"page_size":20,"publish_timestamp":"0","rid":0,"scene_type":"95fen_android_home_personal","sn":"HomeRecommendList","ua":"Mozilla/5.0 (Linux; Android 12; ALN-AL00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Safari/537.36"}'; // 你的完整 JSON

    SwSdk.achilles.overload('[B', 'java.lang.String', 'int', 'long').implementation = function(pb, k, ap, ts) {
        // 可选：只在特定场景替换（比如 sn=HomeRecommendList）
        const originalStr = String.$new(pb).toString();
        if (originalStr.includes("HomeRecommendList")) {
            console.log("[🔄] Replacing plaintext with custom one");
            pb = String.$new(CUSTOM_PLAINTEXT).getBytes();
        }

        const out = this.achilles(pb, k, ap, ts);

        // 提取并打印密文（和抓包对比）
        const payload = out.length > 40 ? Arrays.copyOfRange(out, 40, out.length) : out;
        const b64 = Base64.encodeToString(payload, 10);
        console.log("\n[✅] Encrypted (length=" + b64.length + "):", b64.toString());

        return out;
    };

    console.log("[+] Hook ready - trigger request to get encrypted custom payload");
});