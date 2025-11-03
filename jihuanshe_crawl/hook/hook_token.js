Java.perform(() => {
    // Hook 所有可能使用 token 的地方
    const Interceptor = Java.use('okhttp3.Interceptor');
    // 或直接 Hook URL 拼接
    const StringBuilder = Java.use('java.lang.StringBuilder');
    StringBuilder.toString.implementation = function() {
        const str = this.toString();
        if (str.includes('token=') && str.includes('eyJ')) {
            console.log('[🔍 TOKEN IN URL] ' + str);
        }
        return str;
    };
});