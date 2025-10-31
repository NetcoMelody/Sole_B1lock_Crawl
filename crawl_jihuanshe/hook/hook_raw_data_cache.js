// frida_raw_data_generator.js
Java.perform(() => {
    const L5D = Java.use("l5.d");
    const Uri = Java.use("android.net.Uri");
    const originalIntercept = L5D.intercept;

    // 存储映射：明文JSON → raw_data
    const cache = {};

    L5D.intercept.implementation = function(chain) {
        const originalUrl = chain.request().url().toString();
        const response = originalIntercept.call(this, chain);
        const finalUrl = response.request().url().toString();

        if (finalUrl.includes("raw_data=") && originalUrl.includes("card_version_id")) {
            // 提取明文参数（不含 token）
            const uri = Uri.parse(originalUrl);
            const paramMap = {};
            const names = uri.getQueryParameterNames();
            const iter = names.iterator();
            while (iter.hasNext()) {
                const key = iter.next();
                if (key !== "token") {
                    paramMap[key] = uri.getQueryParameter(key);
                }
            }
            const plaintextJson = JSON.stringify(paramMap);

            // 提取 raw_data
            const rawMatch = /raw_data=([^&]+)/.exec(finalUrl);
            if (rawMatch) {
                const rawData = decodeURIComponent(rawMatch[1]);
                cache[plaintextJson] = rawData;
                console.log("[💾] 缓存:", plaintextJson, "→", rawData.substring(0, 50) + "...");
            }
        }

        return response;
    };

    // 暴露给 Python 的 RPC 方法
    rpc.exports = {
        getRawData: function(plaintextJson) {
            const key = plaintextJson;
            if (cache.hasOwnProperty(key)) {
                return cache[key];
            } else {
                throw new Error("未找到 raw_data，请先触发对应请求");
            }
        },

        listCache: function() {
            return Object.keys(cache);
        }
    };
});