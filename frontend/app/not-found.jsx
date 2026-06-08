import Link from "next/link";

export default function NotFound() {
  return (
    <div className="max-w-md mx-auto text-center py-20">
      <h2 className="text-2xl font-medium text-gray-800">找不到這個演算法</h2>
      <p className="text-gray-500 mt-2 text-sm">演算法編號只有 1 到 10。</p>
      <Link
        href="/"
        className="inline-block mt-6 px-4 py-2 bg-navy text-white rounded-md text-sm"
      >
        回總覽首頁
      </Link>
    </div>
  );
}
