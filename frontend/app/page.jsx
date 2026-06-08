import { api } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import AlgorithmCard from "@/components/AlgorithmCard";
import { ComparisonTable, LearningPath } from "@/components/ComparisonTable";

export default async function HomePage() {
  let algorithms = [];
  let comparison = null;
  let path = null;
  let error = null;

  try {
    [algorithms, comparison, path] = await Promise.all([
      api.algorithms(),
      api.comparison(),
      api.learningPath(),
    ]);
  } catch (e) {
    error = e.message;
  }

  return (
    <div className="flex max-w-[1180px] mx-auto bg-[#faf9f5] min-h-screen">
      <Sidebar algorithms={algorithms} activeId={null} />
      <main className="flex-1 min-w-0 p-4 md:p-6">
        <Header />

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4 text-sm mb-5">
            無法連線到後端 API({error})。請確認 FastAPI 後端已啟動於 http://localhost:8000。
          </div>
        )}

        <SectionTitle>十大機器學習演算法總覽</SectionTitle>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
          {algorithms.map((a) => (
            <AlgorithmCard key={a.id} algo={a} />
          ))}
        </div>

        <SectionTitle className="mt-6">演算法比較總覽</SectionTitle>
        <ComparisonTable data={comparison} />

        <SectionTitle className="mt-6">初學者建議學習順序</SectionTitle>
        <div className="bg-white border border-[var(--border)] rounded-lg p-4">
          <LearningPath path={path} />
        </div>

        <div className="mt-4 text-[10px] text-gray-400 bg-white border border-[var(--border)] rounded-md px-3 py-2 font-mono">
          資料來源:FastAPI 後端　GET /api/algorithms · /api/comparison · /api/learning-path
        </div>
      </main>
    </div>
  );
}

function SectionTitle({ children, className = "" }) {
  return (
    <h2
      className={`text-sm font-medium text-gray-900 border-l-[3px] border-[#185FA5] pl-2 mb-3 ${className}`}
    >
      {children}
    </h2>
  );
}
