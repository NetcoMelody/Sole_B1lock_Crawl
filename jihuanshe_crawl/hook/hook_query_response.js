Java.perform(() => {
    // 用于临时存储最近的请求信息（简化版，适用于单线程搜索）
    let lastRequestInfo = null;

    // ===== Hook 请求构建（打印 Headers）=====
    const RequestBuilder = Java.use('okhttp3.Request$Builder');
    RequestBuilder.build.implementation = function() {
        const request = this.build();
        const url = request.url().toString();
        const method = request.method();

        // 只关注目标接口
        if (url.includes('match-product')) {
            const headers = request.headers();
            const headerCount = headers.size();
            let headerObj = {};
            for (let i = 0; i < headerCount; i++) {
                const name = headers.name(i);
                const value = headers.value(i);
                headerObj[name] = value;
            }

            lastRequestInfo = {
                url: url,
                method: method,
                headers: headerObj,
                timestamp: Date.now()
            };

            console.log('[📤 REQUEST] ' + method + ' ' + url);
            console.log('[📤 HEADERS] ' + JSON.stringify(headerObj, null, 2));
        }

        return request;
    };

    // ===== Hook 响应 JSON（打印商品列表）=====
    const JSONObject = Java.use('org.json.JSONObject');
    JSONObject.$init.overload('java.lang.String').implementation = function(jsonStr) {
        const obj = this.$init(jsonStr);

        if (jsonStr && typeof jsonStr === 'string') {
            // 判断是否为商品列表响应（含 data 数组或 items）
            if (jsonStr.includes('"data"') && jsonStr.includes('"min_price"')) {
                console.log('[📥 RESPONSE] ' + (lastRequestInfo ? lastRequestInfo.url : 'Unknown URL'));
                console.log('[📥 BODY] ' + jsonStr);

                // 可选：清空 lastRequestInfo 避免错乱（或保留用于下一次）
                // lastRequestInfo = null;
            }
        }

        return obj;
    };
});