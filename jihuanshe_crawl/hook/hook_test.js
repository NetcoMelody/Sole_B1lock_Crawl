Java.perform(() => {
    console.log('[*] Hooking target APIs only: /products & /grading-products');

    // ====== 1. Hook 请求（URL + Headers）======
    const TARGET_PATHS = [
        '/api/market/card-versions/products',
        '/api/market/card-versions/grading-products'
    ];

    function hookRequestBuilder(className) {
        try {
            const Builder = Java.use(className);
            if (Builder && Builder.build) {
                const originalBuild = Builder.build;
                Builder.build.implementation = function() {
                    const request = originalBuild.call(this);
                    try {
                        const url = request.url().toString();
                        // 精准匹配目标接口
                        if (TARGET_PATHS.some(path => url.includes(path))) {
                            console.log('\n[📡 TARGET REQUEST]');
                            console.log('URL: ' + url);
                            const headers = request.headers();
                            console.log('Headers:');
                            for (let i = 0; i < headers.size(); i++) {
                                console.log(`  ${headers.name(i)}: ${headers.value(i)}`);
                            }
                            console.log('----------------------------------------');
                        }
                    } catch (e) {
                        console.log('[!] Request hook error:', e.message);
                    }
                    return request;
                };
            }
        } catch (e) {
            // 忽略类不存在错误
        }
    }

    // 尝试多个可能的 Builder 类（兼容混淆）
    ['okhttp3.Request$Builder', 'okhttp3.ab', 'okhttp3.ac', 'okhttp3.t', 'okhttp3.u']
        .forEach(hookRequestBuilder);

    // ====== 2. Hook 响应（JSON）======
    try {
        const JSONObject = Java.use('org.json.JSONObject');
        JSONObject.$init.overload('java.lang.String').implementation = function(jsonStr) {
            const result = this.$init(jsonStr);
            try {
                const str = jsonStr.toString();
                // 精准匹配响应特征
                if (
                    (str.includes('"path":"http://api.jihuanshe.com/api/market/card-versions/products"') ||
                        str.includes('"path":"http://api.jihuanshe.com/api/market/card-versions/grading-products"')) &&
                    str.includes('"data"')
                ) {
                    console.log('\n[🎯 TARGET RESPONSE]');
                    console.log(str);
                    console.log('----------------------------------------');
                }
            } catch (e) {
                // ignore
            }
            return result;
        };
    } catch (e) {
        console.log('[-] JSONObject hook failed');
    }
});