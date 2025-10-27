import frida
import os
import sys

# === 配置项 ===
WEIXIN_PATH = r"D:\App\Weixin\Weixin.exe"

# === JS Hook 代码 ===
JS_CODE = """
console.log("[+] WeChat network data interceptor started!");

// 尝试 Hook 一些可能的 JSON 序列化函数
function hookJsonFunctions() {
    console.log("[*] Hooking potential JSON/serialization functions...");
    
    // 尝试 Hook 一些常见的 JSON 库函数（如果存在）
    var jsonLibs = [
        "msvcp140.dll", "msvcp120.dll", "msvcp110.dll"
    ];
    
    jsonLibs.forEach(function(libName) {
        try {
            var lib = Process.findModuleByName(libName);
            if (lib) {
                console.log("[+] Found " + libName);
                
                // 尝试 Hook 常见的 C++ string 相关函数
                var stringFuncs = [
                    "std::string::assign", "std::string::append", "std::string::operator="
                ];
                
                stringFuncs.forEach(function(funcName) {
                    try {
                        var funcPtr = Module.findExportByName(libName, funcName);
                        if (funcPtr) {
                            Interceptor.attach(funcPtr, {
                                onEnter: function(args) {
                                    // 尝试读取字符串参数
                                    try {
                                        // 这里需要根据具体函数签名调整
                                        var str = Memory.readCString(args[1]);
                                        if (str && str.length > 5 && str.length < 500) {
                                            if (str.includes("{") && str.includes("}")) {
                                                console.log("[JSON-DATA] Potential message JSON: " + str);
                                            } else if (str.toLowerCase().includes("msg") || 
                                                      str.toLowerCase().includes("text")) {
                                                console.log("[STRING-DATA] Potential message: " + str);
                                            }
                                        }
                                    } catch (e) {
                                        // 忽略错误
                                    }
                                }
                            });
                            console.log("[+] Hooked: " + funcName);
                        }
                    } catch (e) {
                        // 函数可能不存在
                    }
                });
            }
        } catch (e) {
            // 库不存在，忽略
        }
    });
}

// Hook 网络发送函数（即使之前的失败，也尝试不同的方式）
function hookNetworkFunctions() {
    console.log("[*] Setting up network monitoring...");
    
    // Hook sendto (有时比 send 更容易捕获)
    try {
        var sendtoPtr = Module.findExportByName("ws2_32.dll", "sendto");
        if (sendtoPtr) {
            Interceptor.attach(sendtoPtr, {
                onEnter: function(args) {
                    var length = parseInt(args[2]);
                    if (length > 50 && length < 2048) {  // 可能的消息数据
                        try {
                            var buffer = Memory.readByteArray(args[1], Math.min(length, 512));
                            var str = "";
                            var bytes = new Uint8Array(buffer);
                            for (var i = 0; i < bytes.length; i++) {
                                if (bytes[i] >= 32 && bytes[i] <= 126) {
                                    str += String.fromCharCode(bytes[i]);
                                } else if (bytes[i] === 10 || bytes[i] === 13) {
                                    str += "\\n";
                                } else {
                                    str += ".";
                                }
                            }
                            
                            // 检查是否包含消息特征
                            if (str.toLowerCase().includes("msg") || 
                                str.toLowerCase().includes("message") ||
                                str.toLowerCase().includes("text") ||
                                (str.includes("{") && str.includes("}"))) {
                                console.log("[NETWORK-DATA] Potential message sent:");
                                console.log("  [SIZE] " + length + " bytes");
                                console.log("  [CONTENT] " + str);
                            }
                        } catch (e) {
                            console.log("[NETWORK] Data sent (" + length + " bytes) - can't read content");
                        }
                    }
                }
            });
            console.log("[+] Hooked sendto function");
        }
    } catch (e) {
        console.log("[!] Failed to hook sendto: " + e);
    }
    
    // Hook WSA send functions
    try {
        var WSASendPtr = Module.findExportByName("ws2_32.dll", "WSASend");
        if (WSASendPtr) {
            Interceptor.attach(WSASendPtr, {
                onEnter: function(args) {
                    try {
                        var lpBuffers = args[1];  // WSABUF array
                        var bufferCount = args[2].toInt32();
                        
                        for (var i = 0; i < bufferCount && i < 5; i++) {
                            var wsabuf = lpBuffers.add(i * Process.pointerSize * 2);
                            var bufPtr = Memory.readPointer(wsabuf);
                            var len = Memory.readU32(wsabuf.add(Process.pointerSize));
                            
                            if (len > 50 && len < 2048) {
                                var buffer = Memory.readByteArray(bufPtr, Math.min(len, 512));
                                var str = "";
                                var bytes = new Uint8Array(buffer);
                                for (var j = 0; j < bytes.length; j++) {
                                    if (bytes[j] >= 32 && bytes[j] <= 126) {
                                        str += String.fromCharCode(bytes[j]);
                                    } else if (bytes[j] === 10 || bytes[j] === 13) {
                                        str += "\\n";
                                    } else {
                                        str += ".";
                                    }
                                }
                                
                                if (str.toLowerCase().includes("msg") || 
                                    str.toLowerCase().includes("message") ||
                                    str.includes("{") && str.includes("}")) {
                                    console.log("[WSASEND-DATA] Potential message:");
                                    console.log("  [SIZE] " + len);
                                    console.log("  [CONTENT] " + str);
                                }
                            }
                        }
                    } catch (e) {
                        // 忽略错误
                    }
                }
            });
            console.log("[+] Hooked WSASend function");
        }
    } catch (e) {
        console.log("[!] Failed to hook WSASend: " + e);
    }
}

// Hook ilink2.dll 网络函数
function hookIlinkNetwork() {
    var ilink2 = Process.findModuleByName("ilink2.dll");
    if (ilink2) {
        console.log("[+] Hooking ilink2.dll for message data...");
        
        ilink2.enumerateExports().forEach(function(exp) {
            if (exp.type === 'function') {
                try {
                    Interceptor.attach(exp.address, {
                        onEnter: function(args) {
                            // 记录所有调用，但只在特定函数上尝试读取数据
                            if (exp.name.toLowerCase().includes("send") || 
                                exp.name.toLowerCase().includes("post") ||
                                exp.name.toLowerCase().includes("request")) {
                                
                                console.log("[ILINK2-CALL] " + exp.name + " called");
                                
                                // 尝试读取参数（复杂，但值得一试）
                                for (var i = 0; i < 5; i++) {
                                    try {
                                        if (args[i] && args[i].toInt32() !== 0) {
                                            var addr = args[i];
                                            // 尝试读取小块内存作为字符串
                                            try {
                                                var str = Memory.readCString(addr, 200);
                                                if (str && str.length > 5) {
                                                    if (str.includes("{") && str.includes("}") ||
                                                        str.toLowerCase().includes("msg") ||
                                                        str.toLowerCase().includes("text")) {
                                                        console.log("  [ILINK2-DATA" + i + "] " + str);
                                                    }
                                                }
                                            } catch (e) {
                                                // 尝试读取为二进制数据
                                                try {
                                                    var bytes = Memory.readByteArray(addr, 100);
                                                    var byteStr = "";
                                                    var uint8Array = new Uint8Array(bytes);
                                                    for (var j = 0; j < uint8Array.length; j++) {
                                                        if (uint8Array[j] >= 32 && uint8Array[j] <= 126) {
                                                            byteStr += String.fromCharCode(uint8Array[j]);
                                                        } else {
                                                            byteStr += ".";
                                                        }
                                                    }
                                                    if (byteStr.includes("{") || byteStr.includes("msg")) {
                                                        console.log("  [ILINK2-BYTES" + i + "] " + byteStr);
                                                    }
                                                } catch (e2) {
                                                    // 忽略
                                                }
                                            }
                                        }
                                    } catch (e) {
                                        // 忽略参数读取错误
                                    }
                                }
                            }
                        }
                    });
                } catch (e) {
                    // 忽略 Hook 失败
                }
            }
        });
    }
}

// 执行所有 Hook
setTimeout(hookJsonFunctions, 500);
setTimeout(hookNetworkFunctions, 1000);
setTimeout(hookIlinkNetwork, 1500);

// 定期状态报告
setInterval(function() {
    console.log("[STATUS] Message monitoring active - waiting for network activity");
}, 30000);

console.log("[+] Network-based message interception active!");
console.log("This approach focuses on network data which should contain messages.");
"""

def on_message(message, data):
    """处理 Frida 消息"""
    if message['type'] == 'send':
        print(f"[SEND] {message['payload']}")
    elif message['type'] == 'log':
        print(f"[LOG] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[ERROR] {message['stack']}")
    else:
        print(f"[{message['type']}] {message}")

def main():
    # 检查微信路径是否存在
    if not os.path.exists(WEIXIN_PATH):
        print(f"❌ Weixin.exe not found at: {WEIXIN_PATH}")
        return

    print(f"✅ Found Weixin.exe at: {WEIXIN_PATH}")

    try:
        device = frida.get_local_device()
        print("✅ Connected to local device")
    except Exception as e:
        print(f"❌ Failed to get device: {e}")
        return

    try:
        processes = device.enumerate_processes()
        target_pid = None
        for proc in processes:
            if proc.name.lower() == "weixin.exe":
                target_pid = proc.pid
                print(f"✅ Found Weixin.exe running with PID: {target_pid}")
                break

        if target_pid is None:
            print("❌ Weixin.exe not running. Please start WeChat first.")
            return

        print(f"[*] Attaching to process {target_pid}...")
        session = device.attach(target_pid)
        print("✅ Session attached")

        script = session.create_script(JS_CODE)
        script.on('message', on_message)
        script.load()
        print("✅ Script loaded successfully")

        print(f"[+] Network-based WeChat message interceptor active (PID: {target_pid})")
        print("Now send messages in WeChat and watch for network data:")
        print("=" * 60)

        input("Press Enter to exit...\n")

        script.unload()
        session.detach()
        print("[-] Detached from process")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("Frida Network-based WeChat Message Interceptor")
    print(f"Target: {WEIXIN_PATH}")
    print("=" * 60)

    main()