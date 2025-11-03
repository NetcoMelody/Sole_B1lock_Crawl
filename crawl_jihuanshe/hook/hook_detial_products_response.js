Java.perform(() => {
    console.log('[*] Hooking all possible Request$Builder classes...');

    // 尝试标准 okhttp3.Request$Builder
    hookRequestBuilder('okhttp3.Request$Builder');

    // 尝试系统内置（虽然不太可能）
    hookRequestBuilder('com.android.okhttp.Request$Builder');

    // 尝试常见混淆类（根据你的类列表）
    const possibleBuilders = [
        'okhttp3.Request$Builder',
        'okhttp3.ab',   // 常见混淆名
        'okhttp3.ac',
        'okhttp3.t',
        'okhttp3.u'
    ];

    possibleBuilders.forEach(cls => {
        if (cls !== 'okhttp3.Request$Builder') {
            hookRequestBuilder(cls);
        }
    });

    function hookRequestBuilder(className) {
        try {
            const Builder = Java.use(className);
            if (Builder && Builder.build) {
                const originalBuild = Builder.build;
                Builder.build.implementation = function() {
                    const request = originalBuild.call(this);
                    try {
                        const url = request.url().toString();
                        // 只关注集换社 API
                        if (url.includes('jihuanshe.com/api')) {
                            console.log('\n[📡 CAPTURED FULL URL]');
                            console.log(url);
                            // 尝试打印 Headers（可能为空，但没关系）
                            const headers = request.headers();
                            if (headers.size() > 0) {
                                console.log('[-Headers-]');
                                for (let i = 0; i < headers.size(); i++) {
                                    console.log(`  ${headers.name(i)}: ${headers.value(i)}`);
                                }
                            } else {
                                console.log('[-Headers-]: (none at build time)');
                            }
                            console.log('----------------------------------------');
                        }
                    } catch (e) {
                        console.log('[!] Error processing request:', e.message);
                    }
                    return request;
                };
                console.log('[+] Hooked: ' + className);
            }
        } catch (e) {
            // 忽略 ClassNotFoundException
        }
    }

    // ========== 保留 JSONObject Hook ==========
    try {
        const JSONObject = Java.use('org.json.JSONObject');
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
            } catch (e) {}
            return result;
        };
    } catch (e) {}
});