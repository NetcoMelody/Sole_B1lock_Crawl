Java.perform(() => {
    try {
        const RequestBuilder = Java.use('okhttp3.Request$Builder');

        // 仅 Hook build() 方法，不碰 Body
        RequestBuilder.build.implementation = function() {
            try {
                const request = this.build();
                const url = request.url().toString();
                const method = request.method();

                // 只打印可疑路径（避免刷屏）
                if (url.includes('api') ||
                    url.includes('card') ||
                    url.includes('product') ||
                    url.includes('item') ||
                    url.includes('shop') ||
                    method === 'POST') {
                    console.log(`[API] ${method} ${url}`);
                }
                return request;
            } catch (e) {
                // 不抛出异常，避免崩溃
                console.log('[!] build() error:', e.message);
                return this.build();
            }
        };
    } catch (e) {
        console.log('[!] OkHttp not found or protected');
    }
});