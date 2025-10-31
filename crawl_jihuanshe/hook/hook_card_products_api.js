// hook_products_light.js
Java.perform(() => {
    console.log('[*] Light hook for /products — only logging request URL + headers');

    const TARGET_PATH = '/api/market/card-versions/products';

    // 尝试 Hook Request.Builder.build() — 最安全的入口
    const classesToTry = [
        'okhttp3.Request$Builder',
        'okhttp3.ab', 'okhttp3.ac', 'okhttp3.ad', 'okhttp3.ae',
        'okhttp3.t', 'okhttp3.u', 'okhttp3.v'
    ];

    let hooked = false;
    for (let className of classesToTry) {
        try {
            const Builder = Java.use(className);
            if (Builder.build) {
                Builder.build.implementation = function () {
                    const request = this.build.call(this);
                    try {
                        const url = request.url().toString();
                        if (url.includes(TARGET_PATH)) {
                            console.log('\n[📡 TARGET REQUEST]');
                            console.log('URL: ' + url);
                            const headers = request.headers();
                            for (let i = 0; i < headers.size(); i++) {
                                console.log(`  ${headers.name(i)}: ${headers.value(i)}`);
                            }
                            console.log('----------------------------------------');
                        }
                    } catch (e) {
                        // silent, avoid crash
                    }
                    return request;
                };
                console.log('[+] Hooked Request$Builder: ' + className);
                hooked = true;
                break; // 只需 hook 一个成功即可
            }
        } catch (e) {
            // class not found, skip
        }
    }

    if (!hooked) {
        console.log('[-] Failed to hook any Request$Builder. Try checking with jadx.');
    }
});