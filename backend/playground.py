# -*- coding: utf-8 -*-
"""Playground: 依照演算法與參數生成合成資料、訓練模型、回傳決策邊界與指標。"""

import numpy as np
from sklearn.datasets import make_classification, make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

GRID_W, GRID_H = 60, 40
X_RANGE = (-4.0, 4.0)
Y_RANGE = (-2.5, 2.5)


def _make_data(noise: float, n: int = 120, seed: int = 42):
    rng = np.random.default_rng(seed)
    X, y = make_classification(
        n_samples=n, n_features=2, n_redundant=0, n_informative=2,
        n_clusters_per_class=1, class_sep=1.5 - noise,
        random_state=int(seed),
    )
    X += rng.normal(0, noise * 0.6, X.shape)
    sc = StandardScaler()
    X = sc.fit_transform(X)
    # scale to visible range
    X[:, 0] = X[:, 0] / X[:, 0].std() * 1.6
    X[:, 1] = X[:, 1] / X[:, 1].std() * 1.0
    return X, y.astype(int)


def _grid():
    xs = np.linspace(*X_RANGE, GRID_W)
    ys = np.linspace(*Y_RANGE, GRID_H)
    xx, yy = np.meshgrid(xs, ys)
    return xx, yy, np.c_[xx.ravel(), yy.ravel()]


def _metrics(y_true, y_pred):
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 3),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 3),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 3),
        "f1": round(float(2 * precision_score(y_true, y_pred, zero_division=0)
                          * recall_score(y_true, y_pred, zero_division=0)
                          / max(precision_score(y_true, y_pred, zero_division=0)
                                + recall_score(y_true, y_pred, zero_division=0), 1e-9)), 3),
    }


def _pack(X, y, grid_pred):
    points = [{"x": round(float(x), 3), "y": round(float(yv), 3), "label": int(lv)}
              for (x, yv), lv in zip(X, y)]
    grid_flat = [int(v) for v in grid_pred]
    return {
        "points": points,
        "grid": {"w": GRID_W, "h": GRID_H, "data": grid_flat,
                 "xRange": list(X_RANGE), "yRange": list(Y_RANGE)},
    }


# ── Per-algorithm playground ─────────────────────────────────────────────────

def logistic_regression(params: dict):
    C = float(params.get("C", 1.0))
    penalty = params.get("penalty", "l2")
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    l1_ratio = 1.0 if penalty == "l1" else 0.0
    clf = LogisticRegression(C=C, l1_ratio=l1_ratio, solver="saga", max_iter=500)
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


def linear_regression(params: dict):
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    reg = LinearRegression()
    reg.fit(X[:, :1], y)
    # Treat threshold 0.5 as class boundary
    y_pred = (reg.predict(X[:, :1]) > 0.5).astype(int)
    xs = np.linspace(*X_RANGE, GRID_W)
    line_y = reg.predict(xs.reshape(-1, 1))
    # build grid (colour by which side of regression line)
    _, _, grid_pts = _grid()
    grid_pred = (grid_pts[:, 0] * reg.coef_[0] + reg.intercept_ > 0.5).astype(int)
    result = _pack(X, y, grid_pred)
    result["line"] = [{"x": round(float(x), 3), "y": round(float(yv), 3)}
                      for x, yv in zip(xs, line_y)]
    result["metrics"] = _metrics(y, y_pred)
    return result


def decision_tree(params: dict):
    max_depth = int(params.get("maxDepth", 4))
    criterion = params.get("criterion", "gini")
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    clf = DecisionTreeClassifier(max_depth=max_depth, criterion=criterion)
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


def random_forest(params: dict):
    n_est = int(params.get("nEstimators", 100))
    max_depth = int(params.get("maxDepth", 6))
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    clf = RandomForestClassifier(n_estimators=n_est, max_depth=max_depth, random_state=42)
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


def svm(params: dict):
    C = float(params.get("C", 1.0))
    kernel = params.get("kernel", "rbf")
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    clf = SVC(C=C, kernel=kernel)
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


def knn(params: dict):
    k = int(params.get("k", 5))
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


def naive_bayes(params: dict):
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise)
    clf = GaussianNB()
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


def kmeans(params: dict):
    k = int(params.get("k", 3))
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise, n=150)
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X)
    _, _, grid_pts = _grid()
    grid_pred = km.predict(grid_pts) % 2   # map to 0/1 for colouring
    cluster_labels = km.labels_
    centers = km.cluster_centers_
    result = _pack(X, cluster_labels % 2, grid_pred)
    result["centers"] = [{"x": round(float(c[0]), 3), "y": round(float(c[1]), 3)}
                         for c in centers]
    result["metrics"] = {"accuracy": None, "precision": None,
                         "recall": None, "f1": None,
                         "inertia": round(float(km.inertia_), 2)}
    return result


def pca(params: dict):
    noise = float(params.get("noise", 0.3))
    X, y = _make_data(noise, n=150)
    pca_model = PCA(n_components=2)
    X_red = pca_model.fit_transform(X)
    # normalise for display
    for i in range(2):
        s = X_red[:, i].std() or 1
        X_red[:, i] = X_red[:, i] / s * 1.5
    var = pca_model.explained_variance_ratio_
    # no decision boundary for PCA — just show transformed points
    result = {"points": [{"x": round(float(x), 3), "y": round(float(yv), 3), "label": int(lv)}
                         for (x, yv), lv in zip(X_red, y)],
              "grid": {"w": 1, "h": 1, "data": [], "xRange": list(X_RANGE), "yRange": list(Y_RANGE)},
              "metrics": {"accuracy": None, "precision": None, "recall": None, "f1": None,
                          "var1": round(float(var[0]) * 100, 1),
                          "var2": round(float(var[1]) * 100, 1)}}
    return result


def neural_network(params: dict):
    noise = float(params.get("noise", 0.3))
    from sklearn.neural_network import MLPClassifier
    hidden = int(params.get("hiddenSize", 32))
    layers = int(params.get("layers", 2))
    X, y = _make_data(noise)
    clf = MLPClassifier(hidden_layer_sizes=tuple([hidden] * layers),
                        max_iter=500, random_state=42)
    clf.fit(X, y)
    _, _, grid_pts = _grid()
    grid_pred = clf.predict(grid_pts)
    return {**_pack(X, y, grid_pred), "metrics": _metrics(y, clf.predict(X))}


RUNNERS = {
    1: linear_regression,
    2: logistic_regression,
    3: decision_tree,
    4: random_forest,
    5: svm,
    6: knn,
    7: naive_bayes,
    8: kmeans,
    9: pca,
    10: neural_network,
}

PARAM_DEFS = {
    1: [
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    2: [
        {"key": "C", "label": "正則化強度 (C)", "type": "select",
         "options": [{"label": "0.01", "value": 0.01}, {"label": "0.1", "value": 0.1},
                     {"label": "1.0", "value": 1.0}, {"label": "10", "value": 10}], "default": 0.1},
        {"key": "penalty", "label": "懲罰項種類 (Penalty)", "type": "select",
         "options": [{"label": "L2 正則化", "value": "l2"}, {"label": "L1 正則化", "value": "l1"}], "default": "l2"},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    3: [
        {"key": "maxDepth", "label": "最大深度 (Max Depth)", "type": "select",
         "options": [{"label": "1", "value": 1}, {"label": "2", "value": 2},
                     {"label": "4", "value": 4}, {"label": "8", "value": 8}, {"label": "無限制", "value": 20}], "default": 4},
        {"key": "criterion", "label": "切分標準 (Criterion)", "type": "select",
         "options": [{"label": "Gini 不純度", "value": "gini"}, {"label": "資訊熵 (Entropy)", "value": "entropy"}], "default": "gini"},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    4: [
        {"key": "nEstimators", "label": "樹的數量", "type": "select",
         "options": [{"label": "10", "value": 10}, {"label": "50", "value": 50},
                     {"label": "100", "value": 100}, {"label": "200", "value": 200}], "default": 100},
        {"key": "maxDepth", "label": "每棵樹最大深度", "type": "select",
         "options": [{"label": "2", "value": 2}, {"label": "4", "value": 4},
                     {"label": "6", "value": 6}, {"label": "無限制", "value": 20}], "default": 6},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    5: [
        {"key": "C", "label": "正則化強度 (C)", "type": "select",
         "options": [{"label": "0.1", "value": 0.1}, {"label": "1.0", "value": 1.0},
                     {"label": "10", "value": 10}, {"label": "100", "value": 100}], "default": 1.0},
        {"key": "kernel", "label": "核函數 (Kernel)", "type": "select",
         "options": [{"label": "RBF (高斯)", "value": "rbf"}, {"label": "線性 (Linear)", "value": "linear"},
                     {"label": "多項式 (Poly)", "value": "poly"}], "default": "rbf"},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    6: [
        {"key": "k", "label": "鄰居數 K", "type": "select",
         "options": [{"label": "1", "value": 1}, {"label": "3", "value": 3},
                     {"label": "5", "value": 5}, {"label": "10", "value": 10}, {"label": "20", "value": 20}], "default": 5},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    7: [
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    8: [
        {"key": "k", "label": "群數 K", "type": "select",
         "options": [{"label": "2", "value": 2}, {"label": "3", "value": 3},
                     {"label": "4", "value": 4}, {"label": "5", "value": 5}], "default": 3},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    9: [
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
    10: [
        {"key": "hiddenSize", "label": "隱藏層神經元數", "type": "select",
         "options": [{"label": "8", "value": 8}, {"label": "16", "value": 16},
                     {"label": "32", "value": 32}, {"label": "64", "value": 64}], "default": 32},
        {"key": "layers", "label": "隱藏層數", "type": "select",
         "options": [{"label": "1", "value": 1}, {"label": "2", "value": 2},
                     {"label": "3", "value": 3}], "default": 2},
        {"key": "noise", "label": "資料雜訊 (Noise)", "type": "slider", "min": 0, "max": 1, "step": 0.05, "default": 0.3},
    ],
}


def run(algo_id: int, params: dict):
    runner = RUNNERS.get(algo_id)
    if runner is None:
        return None
    return runner(params)


def get_param_defs(algo_id: int):
    return PARAM_DEFS.get(algo_id, [])
