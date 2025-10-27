Java.perform(function () {
    let currentLtk = null;

    const SZStone = Java.use("com.shizhuang.stone.SZStone");
    SZStone.getLtk.overload('android.content.Context').implementation = function (ctx) {
        const ltk = this.getLtk(ctx);
        currentLtk = ltk;
        console.log("\n[🔑 FULL LTK]: " + ltk);
        return ltk;
    };

    const Buffer = Java.use("okio.Buffer");
    const originalReadUtf8 = Buffer.readUtf8.overload();
    originalReadUtf8.implementation = function () {
        const content = originalReadUtf8.call(this);
        try {
            if (content.includes('"data"') && content.length > 200) {
                const json = JSON.parse(content);
                if (json.data && typeof json.data === 'string' && json.data.length > 100) {
                    console.log("\n[🔐 FULL CIPHER DATA]: " + json.data);
                    if (currentLtk) {
                        console.log("[💡 FULL LTK FOR THIS REQUEST]: " + currentLtk);
                    }
                }
            }
        } catch (e) {
            // ignore parse errors
        }
        return content;
    };
});