// 在 Frida 脚本中添加
Java.enumerateLoadedClasses({
    onMatch: function(className) {
        if (className.includes("Api") || className.includes("Service")) {
            try {
                const cls = Java.use(className);
                const methods = cls.class.getDeclaredMethods();
                for (let i = 0; i < methods.length; i++) {
                    const method = methods[i];
                    const methodName = method.getName();
                    if (methodName.includes("product") || methodName.includes("card")) {
                        console.log("[🔍] Found candidate method:", className + "." + methodName);
                        // 可进一步 Hook
                    }
                }
            } catch (e) {}
        }
    },
    onComplete: function() {}
});