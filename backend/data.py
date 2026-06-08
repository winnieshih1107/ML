# -*- coding: utf-8 -*-
"""十大機器學習演算法的資料來源。

正式專案中這份資料可以改成從資料庫讀取;此處以 Python 結構直接提供,
讓 FastAPI 的端點回傳。每個演算法包含總覽卡片所需欄位,以及詳細頁所需的
延伸欄位(原理、優缺點、應用場景、程式片段等)。
"""

ALGORITHMS = [
    {
        "id": 1,
        "zh": "線性迴歸",
        "en": "Linear Regression",
        "color": "blue",
        "icon": "line",
        "category": "監督式",
        "task": "迴歸",
        "use": "預測連續數值",
        "desc": "預測連續數值結果,找出變數間的線性關係。",
        "idea": "找一條最能貼合資料的直線,讓預測與實際誤差的平方和最小。",
        "example": "用坪數預測房價:每多一坪價格約增加固定金額。",
        "how": "假設目標與特徵呈線性關係 y = w·x + b,透過最小平方法找出讓均方誤差最小的權重 w 與截距 b。特徵不只一個時,直線變成超平面,每個權重代表該特徵對結果的影響力與方向。",
        "pros": ["簡單、訓練快、可解釋性高", "不需大量資料即可運作,適合作為基準模型", "是理解進階模型的數學基礎"],
        "cons": ["只能捕捉線性關係", "對離群值非常敏感", "特徵高度相關時不穩定"],
        "scenarios": ["房價估價", "銷售額預測", "醫療指標預測住院天數"],
        "code": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)",
        "difficulty": 2,
        "accuracy": 3,
    },
    {
        "id": 2,
        "zh": "邏輯迴歸",
        "en": "Logistic Regression",
        "color": "teal",
        "icon": "sig",
        "category": "監督式",
        "task": "分類",
        "use": "二元分類",
        "desc": "用於二元分類問題,輸出機率值。",
        "idea": "用 S 形 sigmoid 函數把加權分數壓縮成 0~1 的機率。",
        "example": "判斷一封郵件是垃圾郵件的機率有多高。",
        "how": "前半段與線性迴歸相同,先算出加權分數 z = w·x + b;再把 z 丟進 sigmoid 函數轉成 0~1 的機率,最後依門檻(通常 0.5)判定類別。訓練時最小化交叉熵損失。",
        "pros": ["輸出機率,可解釋性高", "分類問題極佳的基準模型", "訓練快速"],
        "cons": ["本質是線性分類器,難處理複雜邊界", "對特徵尺度與離群值敏感", "類別不平衡時需調整"],
        "scenarios": ["垃圾郵件偵測", "信用違約預測", "顧客流失預測"],
        "code": "from sklearn.linear_model import LogisticRegression\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\ny_prob = model.predict_proba(X_test)",
        "difficulty": 3,
        "accuracy": 3,
    },
    {
        "id": 3,
        "zh": "決策樹",
        "en": "Decision Tree",
        "color": "amber",
        "icon": "tree",
        "category": "監督式",
        "task": "分類/迴歸",
        "use": "分類與迴歸",
        "desc": "透過樹狀結構進行決策,可用於分類與迴歸。",
        "idea": "用一連串是非題把資料逐層切分,直到分出結果。",
        "example": "銀行核卡:先問收入是否夠高,再問年齡……層層判斷。",
        "how": "每個節點選擇能把資料切得最乾淨的問題(用吉尼不純度或資訊熵衡量),反覆切分直到夠純或達深度上限。容易過擬合,需用剪枝(限制深度、最小樣本數)控制。",
        "pros": ["極易解釋、可視覺化", "不需特徵縮放,能處理數值與類別", "能捕捉非線性與特徵交互"],
        "cons": ["單棵樹容易過擬合", "對資料微小變動敏感", "連續數值預測不夠平滑"],
        "scenarios": ["銀行核貸規則", "醫療初步診斷流程", "客服問題分流"],
        "code": "from sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier(max_depth=4)\nmodel.fit(X_train, y_train)",
        "difficulty": 3,
        "accuracy": 3,
    },
    {
        "id": 4,
        "zh": "隨機森林",
        "en": "Random Forest",
        "color": "purple",
        "icon": "forest",
        "category": "監督式",
        "task": "分類/迴歸",
        "use": "強力通用預測",
        "desc": "多棵決策樹組合,提升準確度並降低過擬合。",
        "idea": "種一整片森林,讓許多棵樹各自判斷再投票表決。",
        "example": "問一百個人猜罐子裡有幾顆糖,平均後驚人地準。",
        "how": "屬於 Bagging:每棵樹用隨機抽樣的資料子集、隨機選取的特徵來訓練,使樹彼此不同。分類取多數決、迴歸取平均,個別樹的錯誤被稀釋,整體更穩定準確。可輸出特徵重要性。",
        "pros": ["準確穩定、不易過擬合、近乎開箱即用", "能評估特徵重要性", "對缺失值與離群值容忍度佳"],
        "cons": ["模型龐大,可解釋性比單棵樹差", "預測較慢、佔記憶體", "極大型或即時場景效率不足"],
        "scenarios": ["金融信用評分", "醫療診斷輔助", "電商流失與推薦"],
        "code": "from sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100)\nmodel.fit(X_train, y_train)",
        "difficulty": 3,
        "accuracy": 4,
    },
    {
        "id": 5,
        "zh": "支援向量機 (SVM)",
        "en": "Support Vector Machine",
        "color": "teal",
        "icon": "svm",
        "category": "監督式",
        "task": "分類",
        "use": "間隔明確的分類",
        "desc": "尋找最佳超平面,最大化分類間隔。",
        "idea": "在兩類之間找出離雙方都最遠的分隔線(間隔最大)。",
        "example": "在兩排對峙的人群中間走路,盡量走正中央留最大緩衝。",
        "how": "在所有可分隔的線中,選出讓間隔最大的那條;決定線位置的少數關鍵點稱為支援向量。透過核技巧把資料映射到高維,能處理複雜的非線性邊界。",
        "pros": ["高維資料表現優異", "核技巧處理非線性", "只依賴支援向量,泛化能力強"],
        "cons": ["資料量大時訓練慢", "參數(C、核、gamma)需仔細調校", "可解釋性低、不直接輸出機率"],
        "scenarios": ["文字分類", "生物資訊基因分類", "手寫數字辨識"],
        "code": "from sklearn.svm import SVC\nmodel = SVC(kernel='rbf', C=1.0)\nmodel.fit(X_train, y_train)",
        "difficulty": 2,
        "accuracy": 4,
    },
    {
        "id": 6,
        "zh": "K 近鄰演算法 (KNN)",
        "en": "K-Nearest Neighbors",
        "color": "amber",
        "icon": "knn",
        "category": "監督式",
        "task": "分類/迴歸",
        "use": "簡單分類與迴歸",
        "desc": "根據最近的 K 個鄰居進行分類或迴歸。",
        "idea": "物以類聚:看離你最近的 K 個鄰居是誰,多數決定類別。",
        "example": "搬到新社區,看左鄰右舍是什麼樣的人來推斷生活圈。",
        "how": "幾乎不訓練,只記住資料。預測時計算新點到所有點的距離,取最近 K 個投票(分類)或取平均(迴歸)。K 需自選,且因依賴距離,使用前務必做特徵標準化。",
        "pros": ["概念極簡單、無需訓練階段", "天然支援多分類", "新資料可隨時加入"],
        "cons": ["預測要算與所有資料的距離,大資料慢", "對特徵尺度極敏感", "高維下距離失去意義(維度災難)"],
        "scenarios": ["推薦系統找相似用戶", "影像辨識基礎範例", "異常偵測"],
        "code": "from sklearn.neighbors import KNeighborsClassifier\nmodel = KNeighborsClassifier(n_neighbors=5)\nmodel.fit(X_train, y_train)",
        "difficulty": 3,
        "accuracy": 3,
    },
    {
        "id": 7,
        "zh": "貝氏分類器",
        "en": "Naive Bayes",
        "color": "pink",
        "icon": "bayes",
        "category": "監督式",
        "task": "分類",
        "use": "文字分類、垃圾信偵測",
        "desc": "基於貝氏定理與特徵獨立假設,常用於文字分類。",
        "idea": "用貝氏定理計算機率,並假設每個特徵彼此獨立。",
        "example": "看到信中出現「中獎」「免費」,推算是垃圾信的機率。",
        "how": "用貝氏定理結合先驗機率與概似度算出後驗機率,比較各類別後驗機率取最高者。「單純」指假設特徵彼此獨立以簡化計算;雖不完全真實,文字分類上表現往往出色且極快。",
        "pros": ["訓練與預測都極快", "少量資料也運作良好", "對高維稀疏文字特別有效"],
        "cons": ["特徵獨立假設常不成立", "機率估計不一定準確", "未見過的詞需平滑處理"],
        "scenarios": ["垃圾郵件過濾", "新聞自動分類", "情感分析"],
        "code": "from sklearn.naive_bayes import MultinomialNB\nmodel = MultinomialNB()\nmodel.fit(X_train, y_train)",
        "difficulty": 3,
        "accuracy": 3,
    },
    {
        "id": 8,
        "zh": "K-Means 聚類",
        "en": "K-Means Clustering",
        "color": "blue",
        "icon": "kmeans",
        "category": "非監督式",
        "task": "分群",
        "use": "把相似資料分群",
        "desc": "將資料分成 K 個群,使群內相似度最高。",
        "idea": "讓資料圍繞 K 個中心點聚集,最小化群內距離。",
        "example": "電商把客戶依消費行為自動分成 VIP、小資族等群。",
        "how": "隨機放下 K 個中心,反覆「把每點指派給最近中心 → 重新計算中心位置」,直到中心不再移動。需事先指定 K,可用手肘法或輪廓係數輔助選擇。",
        "pros": ["概念直觀、計算高效", "結果易解讀與視覺化", "探索資料的標準工具"],
        "cons": ["必須事先指定 K", "假設群為圓形、大小相近", "對離群值與初始中心敏感"],
        "scenarios": ["客戶分群(RFM)", "市場區隔", "影像壓縮"],
        "code": "from sklearn.cluster import KMeans\nmodel = KMeans(n_clusters=3, n_init=10)\nmodel.fit(X)",
        "difficulty": 3,
        "accuracy": 3,
    },
    {
        "id": 9,
        "zh": "主成分分析 (PCA)",
        "en": "Principal Component Analysis",
        "color": "teal",
        "icon": "pca",
        "category": "非監督式",
        "task": "降維",
        "use": "降維、壓縮特徵",
        "desc": "降維技術,保留重要資訊、減少特徵維度。",
        "idea": "找出資料變異最大的方向當新軸,用更少維度保留最多資訊。",
        "example": "把國英數自社五科成績濃縮成「整體表現」等少數指標。",
        "how": "分析共變異數矩陣求出特徵向量與特徵值,變異最大的方向即第一主成分。保留前幾個主成分即可降維。主成分是原始特徵的加權組合,使用前需標準化。",
        "pros": ["有效降維、去除冗餘與雜訊", "可把高維資料壓到 2~3 維視覺化", "常提升後續模型速度與穩定性"],
        "cons": ["主成分失去原始特徵意義,難解釋", "只能捕捉線性關係", "對特徵尺度敏感,需先標準化"],
        "scenarios": ["資料前處理與視覺化", "影像壓縮", "基因資料分析"],
        "code": "from sklearn.decomposition import PCA\npca = PCA(n_components=2)\nX_reduced = pca.fit_transform(X)",
        "difficulty": 2,
        "accuracy": 3,
    },
    {
        "id": 10,
        "zh": "神經網路 / 深度學習",
        "en": "Neural Networks / Deep Learning",
        "color": "purple",
        "icon": "nn",
        "category": "監督 / 非監督",
        "task": "分類/迴歸",
        "use": "影像、語言、複雜模式",
        "desc": "模擬人腦結構,處理複雜模式如影像、語言。",
        "idea": "用多層連結的節點層層學出特徵,解決複雜問題。",
        "example": "辨識照片中的物體、把語音轉成文字、生成文章。",
        "how": "由輸入層、隱藏層、輸出層的節點(神經元)組成,每個連結有權重。透過前向傳播算出預測、反向傳播配合梯度下降調整權重。層數夠多即為深度學習,能自動從原始資料學出層層遞進的特徵。",
        "pros": ["在影像、語音、語言上表現壓倒性", "能自動學習特徵,省去人工特徵工程", "彈性極高,可處理超大規模資料"],
        "cons": ["需要大量資料與運算資源", "訓練慢、調參複雜", "可解釋性低(黑盒)"],
        "scenarios": ["影像辨識", "自然語言處理與大型語言模型", "語音辨識"],
        "code": "import torch.nn as nn\nmodel = nn.Sequential(\n    nn.Linear(10, 64), nn.ReLU(),\n    nn.Linear(64, 1))",
        "difficulty": 1,
        "accuracy": 4,
    },
]

LEARNING_ORDER = [1, 2, 6, 3, 4, 7, 5, 8, 9, 10]

QUIZ = {
    1: [
        {"q": "線性迴歸的目標是？", "opts": ["最大化分類間隔", "最小化預測誤差的平方和", "把資料分成K群", "壓縮特徵維度"], "ans": 1},
        {"q": "線性迴歸只適用於哪種輸出？", "opts": ["類別標籤", "機率值", "連續數值", "群集編號"], "ans": 2},
        {"q": "線性迴歸最大的弱點是？", "opts": ["訓練速度慢", "只能捕捉線性關係", "需要大量資料", "不能輸出機率"], "ans": 1},
    ],
    2: [
        {"q": "邏輯迴歸使用哪個函數輸出機率？", "opts": ["ReLU", "tanh", "Sigmoid", "Softmax"], "ans": 2},
        {"q": "邏輯迴歸最適合處理哪類問題？", "opts": ["房價預測", "二元分類", "影像辨識", "資料壓縮"], "ans": 1},
        {"q": "邏輯迴歸的本質是什麼分類器？", "opts": ["非線性", "線性", "樹狀", "距離型"], "ans": 1},
    ],
    3: [
        {"q": "決策樹用什麼標準選擇最佳切分點？", "opts": ["距離最近", "吉尼不純度或資訊熵", "加權平均", "主成分方向"], "ans": 1},
        {"q": "單棵決策樹最常見的問題是？", "opts": ["訓練太慢", "無法分類", "容易過擬合", "不能處理數值"], "ans": 2},
        {"q": "決策樹最大的優點是？", "opts": ["準確度最高", "訓練最快", "可視覺化、易解釋", "使用記憶體最少"], "ans": 2},
    ],
    4: [
        {"q": "隨機森林屬於哪種整體學習方法？", "opts": ["Boosting", "Bagging", "Stacking", "Dropout"], "ans": 1},
        {"q": "隨機森林怎麼做最終預測（分類）？", "opts": ["取最深的樹結果", "取誤差最小的樹", "多數決投票", "加權平均梯度"], "ans": 2},
        {"q": "隨機森林相比單棵決策樹的優點？", "opts": ["速度更快", "更不易過擬合且更穩定", "可解釋性更強", "需要更少資料"], "ans": 1},
    ],
    5: [
        {"q": "SVM 的核心目標是？", "opts": ["最小化損失函數", "最大化分類間隔", "把資料分成K群", "降低維度"], "ans": 1},
        {"q": "SVM 如何處理非線性資料？", "opts": ["增加訓練輪數", "透過核技巧映射到高維", "用隨機森林輔助", "刪除離群值"], "ans": 1},
        {"q": "哪些資料稱為「支援向量」？", "opts": ["所有訓練資料", "距離決策邊界最遠的點", "距離決策邊界最近的關鍵點", "被誤分類的點"], "ans": 2},
    ],
    6: [
        {"q": "KNN 在訓練階段做了什麼？", "opts": ["計算最佳權重", "幾乎什麼都不做，只記憶資料", "建立決策樹", "找出主成分"], "ans": 1},
        {"q": "KNN 預測時依據什麼？", "opts": ["全部資料的統計分布", "最近K個鄰居的多數決", "機率模型", "梯度方向"], "ans": 1},
        {"q": "KNN 最嚴重的缺點是？", "opts": ["難以解釋", "預測時需計算與所有資料的距離", "無法做多分類", "只能線性分類"], "ans": 1},
    ],
    7: [
        {"q": "貝氏分類器的「單純」假設是指？", "opts": ["資料完全隨機", "特徵彼此獨立", "資料呈常態分布", "特徵都是數值型"], "ans": 1},
        {"q": "貝氏分類器最擅長哪種應用？", "opts": ["影像辨識", "時序預測", "文字分類與垃圾信過濾", "資料降維"], "ans": 2},
        {"q": "貝氏分類器的主要優點？", "opts": ["準確度最高", "訓練與預測都極快且適合小資料", "不需任何假設", "能處理影像"], "ans": 1},
    ],
    8: [
        {"q": "K-Means 屬於哪種學習類型？", "opts": ["監督式學習", "非監督式學習", "強化學習", "半監督學習"], "ans": 1},
        {"q": "K-Means 需要使用者事先指定什麼？", "opts": ["每個群的大小", "群的數量K", "資料標籤", "核函數"], "ans": 1},
        {"q": "K-Means 目標是最小化什麼？", "opts": ["分類邊界的長度", "群內各點到中心的距離總和", "特徵的變異數", "損失函數交叉熵"], "ans": 1},
    ],
    9: [
        {"q": "PCA 的主要用途是？", "opts": ["分類資料", "降低特徵維度、保留最大變異", "聚類資料", "偵測異常值"], "ans": 1},
        {"q": "使用 PCA 前必須先做什麼？", "opts": ["移除重複資料", "特徵標準化", "標記資料標籤", "訓練分類器"], "ans": 1},
        {"q": "主成分的方向代表什麼？", "opts": ["資料的平均方向", "資料變異最大的方向", "特徵相關性最高的方向", "誤差最小的方向"], "ans": 1},
    ],
    10: [
        {"q": "神經網路調整權重的主要方法是？", "opts": ["基因演算法", "反向傳播 + 梯度下降", "決策樹切分", "最小平方法"], "ans": 1},
        {"q": "「深度學習」中的「深」是指？", "opts": ["資料量非常大", "模型有許多層隱藏層", "準確度很高", "訓練很久"], "ans": 1},
        {"q": "神經網路能自動學習什麼？", "opts": ["最佳的K值", "特徵表示（feature representation）", "群集中心", "主成分方向"], "ans": 1},
    ],
}


def get_quiz(algo_id: int):
    return QUIZ.get(algo_id)


def list_cards():
    """總覽卡片需要的精簡欄位。"""
    keys = ["id", "zh", "en", "color", "icon", "category", "task", "use", "desc"]
    return [{k: a[k] for k in keys} for a in ALGORITHMS]


def get_detail(algo_id: int):
    for a in ALGORITHMS:
        if a["id"] == algo_id:
            return a
    return None


def comparison_table():
    """比較總覽表資料。"""
    return {
        "columns": [{"id": a["id"], "zh": a["zh"], "en": a["en"]} for a in ALGORITHMS],
        "rows": [
            {"label": "監督類型", "values": [a["task"] for a in ALGORITHMS]},
            {"label": "容易程度", "values": ["★" * a["difficulty"] for a in ALGORITHMS]},
            {"label": "準確度", "values": ["★" * a["accuracy"] for a in ALGORITHMS]},
        ],
    }


def learning_path():
    order = []
    for step, aid in enumerate(LEARNING_ORDER, start=1):
        a = get_detail(aid)
        order.append({"step": step, "id": a["id"], "zh": a["zh"], "en": a["en"], "color": a["color"]})
    return order
