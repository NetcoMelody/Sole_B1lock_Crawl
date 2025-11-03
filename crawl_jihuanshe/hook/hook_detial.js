// 临时调试：打印所有请求（可选）
RequestBuilder.build.implementation = function() {
    const request = this.build();
    const url = request.url().toString();
    console.log('[DEBUG] ALL URL:', url); // 先观察哪些是详情页
    // ...原有逻辑
    return request;
}