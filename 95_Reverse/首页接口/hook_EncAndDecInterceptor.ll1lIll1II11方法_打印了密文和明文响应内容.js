Java.perform(function () {
    console.log("[*] 启动：同时捕获密文与明文（页面正常加载版）");

    const EncAndDecInterceptor = Java.use("com.shizhuang.dusanwa.network.EncAndDecInterceptor");
    const Response = Java.use("okhttp3.Response");
    const ResponseBody = Java.use("okhttp3.ResponseBody");
    const MediaType = Java.use("okhttp3.MediaType");

    // 安全读取并重建 Response（避免流关闭）
    function readAndRebuildResponse(response) {
        if (response === null) return null;
        const body = response.body();
        if (body === null) {
            return { content: null, contentType: null, newResponse: response };
        }

        try {
            const source = body.source();
            const buffer = Java.use("okio.Buffer").$new();
            source.readAll(buffer);
            const content = buffer.readUtf8();
            const contentType = body.contentType() ? body.contentType().toString() : null;

            // 重建 Body 和 Response
            const mediaType = contentType ? MediaType.parse(contentType) : null;
            const newBody = ResponseBody.create(mediaType, content);
            const newResponse = response.newBuilder().body(newBody).build();

            return { content, contentType, newResponse };
        } catch (e) {
            console.warn("[!] 读取响应失败:", e.message);
            return { content: null, contentType: null, newResponse: response };
        }
    }

    const highLevel = EncAndDecInterceptor.ll1lIll1II11.overload(
        'okhttp3.Interceptor$Chain',
        'okhttp3.Request',
        'java.lang.String'
    );

    highLevel.implementation = function (chain, request, path) {
        const isTarget = path.includes("goods") || path.includes("recommendation");

        if (!isTarget) {
            return highLevel.call(this, chain, request, path);
        }

        console.log("\n" + "=".repeat(80));
        console.log("[🔄] 目标请求路径:", path);

        // 🔐 第一步：手动执行 chain.proceed() 获取原始密文响应
        let rawResponse;
        try {
            rawResponse = chain.proceed(request);
        } catch (e) {
            console.error("[!] 请求失败:", e.message);
            return highLevel.call(this, chain, request, path); // 仍走原始逻辑
        }

        // 读取并重建密文响应（rawResponse 的 body 会被消费！）
        const { content: cipherText, newResponse: rebuiltRawResponse } = readAndRebuildResponse(rawResponse);

        if (cipherText !== null) {
            console.log("[🔐] 【完整密文响应】开始");
            console.log(cipherText);
            console.log("[🔐] 【完整密文响应】结束\n");
        }

        // ✅ 第二步：构造 FakeChain，让原始逻辑处理 rebuiltRawResponse（未被消费）
        const FakeChain = Java.registerClass({
            name: 'com.shizhuang.dusanwa.FakeChain_' + Math.random().toString(36).slice(2),
            implements: [Java.use('okhttp3.Interceptor$Chain')],
            methods: {
                request: () => request,
                proceed: () => rebuiltRawResponse, // 👈 关键：传入重建后的响应
                connection: () => null,
                call: () => chain.call(),
                connectTimeoutMillis: () => chain.connectTimeoutMillis(),
                readTimeoutMillis: () => chain.readTimeoutMillis(),
                writeTimeoutMillis: () => chain.writeTimeoutMillis(),
                withConnectTimeout: (timeout, unit) => chain.withConnectTimeout(timeout, unit),
                withReadTimeout: (timeout, unit) => chain.withReadTimeout(timeout, unit),
                withWriteTimeout: (timeout, unit) => chain.withWriteTimeout(timeout, unit)
            }
        });

        const fakeChain = FakeChain.$new();

        // 执行原始解密逻辑
        const decryptedResponse = highLevel.call(this, fakeChain, request, path);

        // 读取并重建明文响应（供 App 使用）
        const { content: plainText, newResponse: finalResponse } = readAndRebuildResponse(decryptedResponse);

        if (plainText !== null) {
            console.log("[✅] 【完整明文响应】开始");
            console.log(plainText);
            console.log("[✅] 【完整明文响应】结束");
        }

        console.log("=".repeat(80) + "\n");

        // 返回重建后的明文响应，确保 App 能正常解析
        return finalResponse || decryptedResponse;
    };

    console.log("[+] Hook 成功: 同时捕获密文与明文（安全模式）");
});


//com.shizhuang.dusanwa.network.EncAndDecInterceptor.ll1lIll1II11(
//     okhttp3.Interceptor$Chain chain,
//     okhttp3.Request request,
//     java.lang.String path
// )