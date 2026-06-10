"use client";
import { useState, useRef, useEffect } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function ChatAssistant() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", content: "你好！我是 ML 助教，有任何機器學習問題都可以問我 😊" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;

    const newMessages = [...messages, { role: "user", content: text }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await res.json();
      setMessages([...newMessages, { role: "assistant", content: data.reply || data.detail }]);
    } catch {
      setMessages([...newMessages, { role: "assistant", content: "⚠️ 無法連線到後端，請確認服務是否啟動。" }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* 浮動按鈕 */}
      <button
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg flex items-center justify-center text-2xl hover:bg-blue-700 transition"
        title="AI 助教"
      >
        {open ? "✕" : "🤖"}
      </button>

      {/* 聊天視窗 */}
      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-80 h-96 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl flex flex-col border border-gray-200 dark:border-gray-700">
          {/* 標題 */}
          <div className="bg-blue-600 text-white px-4 py-3 rounded-t-2xl font-semibold text-sm">
            🤖 AI 助教
          </div>

          {/* 訊息區 */}
          <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2 text-sm">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] px-3 py-2 rounded-xl whitespace-pre-wrap ${
                    m.role === "user"
                      ? "bg-blue-600 text-white rounded-br-none"
                      : "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded-bl-none"
                  }`}
                >
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-700 text-gray-500 px-3 py-2 rounded-xl rounded-bl-none text-xs">
                  思考中...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* 輸入區 */}
          <div className="flex border-t border-gray-200 dark:border-gray-700 p-2 gap-2">
            <input
              className="flex-1 text-sm px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="輸入問題..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50 transition"
            >
              送出
            </button>
          </div>
        </div>
      )}
    </>
  );
}
