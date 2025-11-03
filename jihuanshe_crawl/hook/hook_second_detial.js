Java.perform(() => {
    console.log('[*] Hooking JSONObject constructors...');

    try {
        const JSONObject = Java.use('org.json.JSONObject');

        // Hook String 构造函数
        JSONObject.$init.overload('java.lang.String').implementation = function(jsonStr) {
            const result = this.$init(jsonStr);
            try {
                const str = jsonStr.toString();
                if ((str.includes('"data"') || str.includes('history')) &&
                    (str.includes('price') || str.includes('pop') || str.includes('card_version_id'))) {
                    console.log('\n[🎯 CAPTURED JSON OBJECT]');
                    console.log(str);
                    console.log('----------------------------------------');
                }
            } catch (e) {
                // ignore
            }
            return result;
        };

        // Hook Map 构造函数（备用）
        JSONObject.$init.overload('java.util.Map').implementation = function(map) {
            console.log('[Map to JSONObject]', map);
            return this.$init(map);
        };
    } catch (e) {
        console.log('[-] JSONObject not found');
    }
});