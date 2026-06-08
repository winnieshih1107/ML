# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import data, playground as pg

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ML Platform — 十大機器學習演算法",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
HEX = {
    "blue":   ["#E6F1FB", "#185FA5", "#0C447C"],
    "teal":   ["#E1F5EE", "#0F6E56", "#085041"],
    "amber":  ["#FAEEDA", "#854F0B", "#633806"],
    "purple": ["#EEEDFE", "#534AB7", "#3C3489"],
    "pink":   ["#FBEAF0", "#993556", "#72243E"],
}

ALGORITHMS = data.ALGORITHMS

# ── Session state ─────────────────────────────────────────────────────────────
if "algo_id" not in st.session_state:
    st.session_state.algo_id = None   # None = home page

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 ML Platform")
    st.markdown("十大機器學習演算法")
    st.divider()

    if st.button("⌂  首頁總覽", use_container_width=True,
                 type="primary" if st.session_state.algo_id is None else "secondary"):
        st.session_state.algo_id = None
        st.rerun()

    st.markdown("**演算法列表**")
    for a in ALGORITHMS:
        c = HEX.get(a["color"], HEX["blue"])
        label = f"{a['id']}. {a['zh']}"
        active = st.session_state.algo_id == a["id"]
        if st.button(label, key=f"nav_{a['id']}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.algo_id = a["id"]
            st.rerun()

# ── Helper: draw decision boundary ───────────────────────────────────────────
def draw_boundary(result):
    if result is None:
        return None

    from matplotlib.colors import ListedColormap

    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor("#13151f")
    ax.set_facecolor("#13151f")

    grid = result.get("grid", {})
    points = result.get("points", [])
    centers = result.get("centers")

    xmin, xmax = grid.get("xRange", [-4, 4])
    ymin, ymax = grid.get("yRange", [-2.5, 2.5])

    # Draw decision region (RGBA tuples, values 0-1)
    gdata = grid.get("data", [])
    if gdata:
        w, h = grid["w"], grid["h"]
        img = np.array(gdata, dtype=float).reshape(h, w)
        cmap = ListedColormap([
            (0.937, 0.267, 0.267, 0.35),   # red  — class 0
            (0.376, 0.647, 0.980, 0.35),   # blue — class 1
        ])
        ax.imshow(img, origin="lower", extent=[xmin, xmax, ymin, ymax],
                  aspect="auto", cmap=cmap, vmin=0, vmax=1)

    # Data points
    xs0 = [p["x"] for p in points if p["label"] == 0]
    ys0 = [p["y"] for p in points if p["label"] == 0]
    xs1 = [p["x"] for p in points if p["label"] == 1]
    ys1 = [p["y"] for p in points if p["label"] == 1]
    ax.scatter(xs0, ys0, c="#ef4444", s=22, edgecolors="white", linewidths=0.5,
               label="類別 0", zorder=3)
    ax.scatter(xs1, ys1, c="#60a5fa", s=22, edgecolors="white", linewidths=0.5,
               label="類別 1", zorder=3)

    # K-Means centers
    if centers:
        cx = [c["x"] for c in centers]
        cy = [c["y"] for c in centers]
        ax.scatter(cx, cy, c="#facc15", s=120, marker="*", edgecolors="white",
                   linewidths=1, label="群心", zorder=4)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Use hex with alpha (#rrggbbaa) — supported by matplotlib
    ax.tick_params(colors="#969baa", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor((0.31, 0.31, 0.39, 0.4))
    ax.grid(color=(0.5, 0.5, 0.5, 0.15), linewidth=0.5)
    ax.legend(fontsize=8, facecolor="#1e2030", edgecolor="#333",
              labelcolor="white", loc="upper right")
    fig.tight_layout(pad=0.5)
    return fig


# ── Home page ─────────────────────────────────────────────────────────────────
def page_home():
    st.title("十大機器學習演算法")
    st.caption("點擊左側演算法可查看詳情、互動 Playground 與小測驗")
    st.divider()

    # Cards grid (2 rows × 5 cols)
    cols = st.columns(5)
    for i, a in enumerate(ALGORITHMS):
        c = HEX.get(a["color"], HEX["blue"])
        with cols[i % 5]:
            st.markdown(f"""
<div style="background:{c[0]};border:1px solid {c[1]}33;border-radius:10px;
            padding:12px 10px;margin-bottom:8px;min-height:100px;">
  <div style="font-size:11px;font-weight:700;color:{c[2]};margin-bottom:4px;">
    {a['id']}. {a['zh']}</div>
  <div style="font-size:9px;color:{c[1]};margin-bottom:6px;">{a['en']}</div>
  <div style="font-size:9px;color:#555;line-height:1.4;">{a['desc']}</div>
  <div style="margin-top:6px;display:flex;gap:4px;flex-wrap:wrap;">
    <span style="font-size:8px;background:{c[1]}22;color:{c[2]};
                 padding:1px 6px;border-radius:99px;">{a['category']}</span>
    <span style="font-size:8px;background:{c[1]}22;color:{c[2]};
                 padding:1px 6px;border-radius:99px;">{a['task']}</span>
  </div>
</div>""", unsafe_allow_html=True)

    st.divider()

    # Comparison table
    st.subheader("演算法比較總覽")
    ct = data.comparison_table()
    headers = [""] + [f"{c['zh']}" for c in ct["columns"]]
    rows = []
    for row in ct["rows"]:
        rows.append([row["label"]] + list(row["values"]))

    col_widths = [150] + [110] * 10
    table_html = "<div style='overflow-x:auto'><table style='border-collapse:collapse;font-size:11px;width:100%'>"
    table_html += "<tr>" + "".join(
        f"<th style='padding:6px 8px;background:#f0f0f0;border:1px solid #ddd;"
        f"text-align:center;font-weight:600'>{h}</th>" for h in headers
    ) + "</tr>"
    for r in rows:
        table_html += "<tr>"
        for j, cell in enumerate(r):
            bg = "#fafafa" if j > 0 else "#f5f5f5"
            table_html += (f"<td style='padding:5px 8px;border:1px solid #ddd;"
                           f"text-align:center;background:{bg}'>{cell}</td>")
        table_html += "</tr>"
    table_html += "</table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    st.divider()

    # Learning path
    st.subheader("初學者建議學習順序")
    path = data.learning_path()
    cols = st.columns(len(path))
    for i, step in enumerate(path):
        c = HEX.get(step["color"], HEX["blue"])
        with cols[i]:
            st.markdown(f"""
<div style="text-align:center;padding:6px 2px;">
  <div style="font-size:9px;color:#999;margin-bottom:2px;">STEP {step['step']}</div>
  <div style="background:{c[1]};color:white;border-radius:6px;
              padding:4px 2px;font-size:10px;font-weight:600;
              line-height:1.3">{step['zh'].replace(' (', '<br>(')}</div>
</div>""", unsafe_allow_html=True)


# ── Algorithm detail page ─────────────────────────────────────────────────────
def page_algorithm(algo_id: int):
    detail = data.get_detail(algo_id)
    if not detail:
        st.error("找不到演算法")
        return

    c = HEX.get(detail["color"], HEX["blue"])

    # Header
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
  <div style="background:{c[1]};color:white;border-radius:8px;
              width:36px;height:36px;display:flex;align-items:center;
              justify-content:center;font-weight:700;font-size:16px;
              flex-shrink:0">{detail['id']}</div>
  <div>
    <span style="font-size:18px;font-weight:700;">{detail['zh']}</span>
    <span style="font-size:13px;color:#666;margin-left:8px;">{detail['en']}</span>
  </div>
</div>""", unsafe_allow_html=True)

    tab_playground, tab_guide, tab_code, tab_quiz = st.tabs(
        ["▷ 實驗室 Playground", "□ 學習指引 Guide", ">_ 程式實作 Code", "📝 小測驗 Quiz"]
    )

    # ── Playground tab ────────────────────────────────────────────────────────
    with tab_playground:
        param_defs = pg.get_param_defs(algo_id)
        if not param_defs:
            st.info("此演算法暫無互動 Playground。")
        else:
            col_ctrl, col_viz = st.columns([1, 2.5])

            with col_ctrl:
                st.markdown("**控制面板 (Parameters)**")
                params = {}
                for d in param_defs:
                    if d["type"] == "slider":
                        params[d["key"]] = st.slider(
                            d["label"], min_value=float(d["min"]),
                            max_value=float(d["max"]), step=float(d["step"]),
                            value=float(d["default"]), key=f"sl_{algo_id}_{d['key']}"
                        )
                    elif d["type"] == "select":
                        opts = d["options"]
                        labels = [o["label"] for o in opts]
                        vals   = [o["value"] for o in opts]
                        default_idx = vals.index(d["default"]) if d["default"] in vals else 0
                        sel = st.selectbox(d["label"], labels, index=default_idx,
                                           key=f"sel_{algo_id}_{d['key']}")
                        params[d["key"]] = vals[labels.index(sel)]

                run_btn = st.button("▶ 開始執行模型", type="primary",
                                    use_container_width=True, key=f"run_{algo_id}")

            with col_viz:
                result_key = f"result_{algo_id}"
                if run_btn or result_key not in st.session_state:
                    with st.spinner("執行中…"):
                        st.session_state[result_key] = pg.run(algo_id, params)

                result = st.session_state.get(result_key)
                if result:
                    fig = draw_boundary(result)
                    if fig:
                        st.pyplot(fig, use_container_width=True)
                        plt.close(fig)

                    metrics = result.get("metrics", {})
                    m_cols = st.columns(4)
                    metric_map = [
                        ("ACCURACY",  metrics.get("accuracy")),
                        ("PRECISION", metrics.get("precision")),
                        ("RECALL",    metrics.get("recall")),
                        ("F1 SCORE",  metrics.get("f1")),
                    ]
                    extra = []
                    if metrics.get("inertia") is not None:
                        extra.append(("INERTIA", metrics["inertia"], True))
                    if metrics.get("var1") is not None:
                        extra.append(("PC1 變異", f"{metrics['var1']}%", True))
                    if metrics.get("var2") is not None:
                        extra.append(("PC2 變異", f"{metrics['var2']}%", True))

                    shown = [(k, v) for k, v in metric_map if v is not None]
                    shown += [(k, v, True) for k, v, *_ in extra]

                    if shown:
                        cols_m = st.columns(len(shown))
                        for i, item in enumerate(shown):
                            key_m, val = item[0], item[1]
                            raw = len(item) > 2
                            display = str(val) if raw else f"{val*100:.1f}%"
                            color = ("#0F6E56" if not raw and val >= 0.8
                                     else "#185FA5" if not raw and val >= 0.6
                                     else "#993C1D" if not raw
                                     else "#185FA5")
                            cols_m[i].metric(key_m, display)

    # ── Guide tab ─────────────────────────────────────────────────────────────
    with tab_guide:
        badge_html = "".join(
            f"<span style='font-size:10px;background:{c[0]};color:{c[2]};"
            f"padding:2px 10px;border-radius:99px;margin-right:4px'>{t}</span>"
            for t in [detail["category"], detail["task"], detail["use"]]
        )
        st.markdown(badge_html, unsafe_allow_html=True)
        st.markdown("")

        for label, content in [
            ("核心概念", detail["idea"]),
            ("運作原理", detail["how"]),
            ("典型例子", detail["example"]),
        ]:
            col_l, col_r = st.columns([1, 5])
            col_l.markdown(f"<span style='color:#999;font-size:12px'>{label}</span>",
                           unsafe_allow_html=True)
            col_r.markdown(content)

        col_pros, col_cons = st.columns(2)
        with col_pros:
            st.markdown(f"<div style='background:#E1F5EE;border-radius:8px;padding:12px'>"
                        f"<div style='color:#0F6E56;font-weight:600;margin-bottom:6px'>優點</div>"
                        + "".join(f"<div style='font-size:12px;color:#333;margin-bottom:4px'>"
                                  f"✓ {p}</div>" for p in detail["pros"])
                        + "</div>", unsafe_allow_html=True)
        with col_cons:
            st.markdown(f"<div style='background:#FAECE7;border-radius:8px;padding:12px'>"
                        f"<div style='color:#993C1D;font-weight:600;margin-bottom:6px'>缺點</div>"
                        + "".join(f"<div style='font-size:12px;color:#333;margin-bottom:4px'>"
                                  f"✗ {p}</div>" for p in detail["cons"])
                        + "</div>", unsafe_allow_html=True)

        st.markdown("")
        col_l, col_r = st.columns([1, 5])
        col_l.markdown("<span style='color:#999;font-size:12px'>應用場景</span>",
                       unsafe_allow_html=True)
        col_r.markdown("、".join(detail["scenarios"]))

    # ── Code tab ──────────────────────────────────────────────────────────────
    with tab_code:
        st.markdown("**程式片段 (scikit-learn / PyTorch)**")
        st.code(detail["code"], language="python")

    # ── Quiz tab ──────────────────────────────────────────────────────────────
    with tab_quiz:
        questions = data.get_quiz(algo_id)
        if not questions:
            st.info("此演算法暫無測驗題目。")
        else:
            score = 0
            answers = {}
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}. {q['q']}**")
                choice = st.radio("", q["opts"],
                                  key=f"quiz_{algo_id}_{i}", index=None,
                                  label_visibility="collapsed")
                answers[i] = choice
                if choice is not None:
                    if q["opts"].index(choice) == q["ans"]:
                        st.success("✓ 正確！")
                        score += 1
                    else:
                        st.error(f"✗ 正確答案：{q['opts'][q['ans']]}")
                st.markdown("")

            answered = sum(1 for v in answers.values() if v is not None)
            if answered == len(questions):
                st.divider()
                pct = score / len(questions)
                color = "#0F6E56" if pct == 1 else "#185FA5" if pct >= 0.5 else "#993C1D"
                msg = "全對！掌握得非常好！" if pct == 1 else "不錯！繼續加油！" if pct >= 0.5 else "再複習一遍試試看！"
                st.markdown(f"<h3 style='color:{color};text-align:center'>"
                            f"成績 {score}/{len(questions)} — {msg}</h3>",
                            unsafe_allow_html=True)


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.algo_id is None:
    page_home()
else:
    page_algorithm(st.session_state.algo_id)
