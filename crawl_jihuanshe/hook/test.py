# test_send.py
import frida
import json
import threading
import time

FRIDA_SCRIPT = """
// frida_hook_send.js
const cache = {};

Java.perform(() => {
    const L5D = Java.use("l5.d");
    const Uri = Java.use("android.net.Uri");
    const originalIntercept = L5D.intercept;

    L5D.intercept.implementation = function(chain) {
        const originalUrl = chain.request().url().toString();
        const response = originalIntercept.call(this, chain);
        const finalUrl = response.request().url().toString();

        if (originalUrl.includes("card_version_id") && finalUrl.includes("raw_data=")) {
            try {
                const uri = Uri.parse(originalUrl);
                const paramMap = {};
                const names = uri.getQueryParameterNames();
                const iter = names.iterator();
                while (iter.hasNext()) {
                    const key = iter.next();
                    if (key !== "token") {
                        paramMap[key] = uri.getQueryParameter(key);
                    }
                }
                const plaintextJson = JSON.stringify(paramMap, Object.keys(paramMap).sort());
                const rawMatch = /raw_data=([^&]+)/.exec(finalUrl);
                if (rawMatch) {
                    const rawData = decodeURIComponent(rawMatch[1]);
                    cache[plaintextJson] = rawData;
                    console.log("[💾] 缓存: " + plaintextJson);
                }
            } catch (e) {
                console.log("[⚠️] Error: " + e.message);
            }
        }
        return response;
    };
});

// 监听来自 Python 的消息
recv('get_raw_data', function(message) {
    const plaintextJson = message.payload;
    if (cache.hasOwnProperty(plaintextJson)) {
        send({ type: 'raw_data', payload: cache[plaintextJson] });
    } else {
        send({ type: 'error', payload: 'Not found: ' + plaintextJson + '. Keys: ' + Object.keys(cache).join(', ') });
    }
});

recv('list_cache', function() {
    send({ type: 'cache_keys', payload: Object.keys(cache) });
});
"""

class RawDataFetcher:
    def __init__(self):
        self.raw_data = None
        self.error = None
        self.received = threading.Event()

    def on_message(self, message, data):
        print("[📩] 收到消息:", message)
        if message['type'] == 'send':
            payload = message['payload']
            if isinstance(payload, dict):
                if payload['type'] == 'raw_data':
                    self.raw_data = payload['payload']
                    self.received.set()
                elif payload['type'] == 'error':
                    self.error = payload['payload']
                    self.received.set()
                elif payload['type'] == 'cache_keys':
                    print("[📋] 缓存 keys:", payload['payload'])
                    self.received.set()

    def get_raw_data(self, device, plaintext_json):
        session = device.attach("集换社")
        script = session.create_script(FRIDA_SCRIPT)
        script.on('message', self.on_message)
        script.load()

        # 发送请求
        script.post({'type': 'get_raw_data', 'payload': plaintext_json})

        # 等待回复（5秒超时）
        if self.received.wait(timeout=5):
            if self.error:
                raise Exception(self.error)
            return self.raw_data
        else:
            raise Exception("Timeout: 未收到回复")

def main():
    device = frida.get_device_manager().add_remote_device("127.0.0.1:1234")
    fetcher = RawDataFetcher()

    params = {
        "card_version_id": "31257",
        "condition": "1",
        "page": "1",
        "game_key": "pkm",
        "game_sub_key": "en"
    }
    plaintext_json = json.dumps(params, separators=(',', ':'), sort_keys=True)

    input("👉 打开商品页后按回车...")
    try:
        raw_data = fetcher.get_raw_data(device, plaintext_json)
        print("[✅] 成功:", raw_data[:80] + "...")
    except Exception as e:
        print("[❌] 失败:", e)

if __name__ == "__main__":
    main()