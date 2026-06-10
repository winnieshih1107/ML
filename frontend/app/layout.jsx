import "./globals.css";
import ThemeProvider from "@/components/ThemeProvider";
import ChatAssistant from "@/components/ChatAssistant";

export const metadata = {
  title: "ML Platform — 十大機器學習演算法",
  description: "互動式機器學習學習平台",
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-Hant" suppressHydrationWarning>
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap"
        />
        <script dangerouslySetInnerHTML={{
          __html: `(function(){var t=localStorage.getItem('theme')||'dark';document.documentElement.setAttribute('data-theme',t);})()`
        }} />
      </head>
      <body className="font-sans">
        <ThemeProvider>
          {children}
          <ChatAssistant />
        </ThemeProvider>
      </body>
    </html>
  );
}
