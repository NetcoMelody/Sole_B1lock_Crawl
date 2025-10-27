Java.perform(() => {
    const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");
    const Base64 = Java.use("android.util.Base64");
    const Arrays = Java.use("java.util.Arrays");

    SwSdk.achilles.overload('[B', 'java.lang.String', 'int', 'long').implementation = function(pb, k, ap, ts) {
        const out = this.achilles(pb, k, ap, ts);
        const payload = out.length > 40 ? Arrays.copyOfRange(out, 40, out.length) : out;
        const b64 = Base64.encodeToString(payload, 10);
        const result = b64.replace(/\+/g, '-').replace(/\//g, '');

        console.log("\n[✅] Final encrypted data (length=" + result.length + "):");
        console.log(result);

        return out;
    };
    console.log("[+] Hook ready - trigger request to see final encrypted data");
});