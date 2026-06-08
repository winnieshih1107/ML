const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function get(path) {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API 錯誤 ${res.status}: ${path}`);
  }
  return res.json();
}

export const api = {
  algorithms: () => get("/api/algorithms"),
  algorithm: (id) => get(`/api/algorithms/${id}`),
  comparison: () => get("/api/comparison"),
  learningPath: () => get("/api/learning-path"),
  quiz: (id) => get(`/api/algorithms/${id}/quiz`),
  params: (id) => get(`/api/algorithms/${id}/params`),
};

// 每個演算法配色對應的 [淺底, 主色, 深字]
export const COLORS = {
  blue: ["#E6F1FB", "#185FA5", "#0C447C"],
  teal: ["#E1F5EE", "#0F6E56", "#085041"],
  amber: ["#FAEEDA", "#854F0B", "#633806"],
  purple: ["#EEEDFE", "#534AB7", "#3C3489"],
  pink: ["#FBEAF0", "#993556", "#72243E"],
};
