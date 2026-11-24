import streamlit as st
import requests
import re

# ==========================================
# [PAGE CONFIG]
# ==========================================
st.set_page_config(
    page_title="NICHERADAR // TECHNICAL GEAR ARCHIVE",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# [MODERN EDITORIAL & DARK MINIMALIST CSS]
# ==========================================
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&display=swap');

/* 전체 배경 및 기본 타이포그래피 */
.stApp {
    background-color: #0A0A0A;
    color: #EAEAEA;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 기본 Streamlit 상단 여백/헤더/푸터 정리 */
header[data-testid="stHeader"] {
    background-color: rgba(10, 10, 10, 0.85);
    backdrop-filter: blur(10px);
}
#MainMenu, footer {visibility: hidden;}
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1380px;
}

/* 상단 에디토리얼 마스트헤드 */
.masthead {
    border-bottom: 1px solid #222222;
    padding-bottom: 1.2rem;
    margin-bottom: 1.8rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 12px;
}
.masthead-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #FFFFFF;
    line-height: 1;
}
.masthead-accent {
    color: #D4FF00;
}
.masthead-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #777777;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* 라디오 버튼 -> 모던 엣지 탭 스타일 변환 */
div[role="radiogroup"] {
    flex-direction: row;
    gap: 8px;
    flex-wrap: wrap;
    border-bottom: 1px solid #1E1E1E;
    padding-bottom: 14px;
    margin-bottom: 24px;
}
div[role="radiogroup"] > label {
    background-color: #111111;
    border: 1px solid #262626;
    border-radius: 0px !important;
    padding: 8px 16px !important;
    margin: 0 !important;
    transition: all 0.15s ease;
    cursor: pointer;
}
div[role="radiogroup"] > label:hover {
    border-color: #666666;
    background-color: #181818;
}
div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #EAEAEA !important;
    border-color: #EAEAEA !important;
}
div[role="radiogroup"] > label[data-checked="true"] p {
    color: #0A0A0A !important;
    font-weight: 700 !important;
}
div[role="radiogroup"] label > div:first-child {
    display: none !important;
}
div[role="radiogroup"] p {
    font-family: 'JetBrains Mono', 'Pretendard', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.03em;
    color: #A0A0A0;
}

/* 컨테이너 보더(카드) 미니멀 샤프 스타일 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 0px !important;
    padding: 16px !important;
    transition: border-color 0.2s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #555555 !important;
}

/* 태그 & 배지 */
.tag-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #0A0A0A;
    background-color: #D4FF00;
    padding: 3px 7px;
    display: inline-block;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.tag-outline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #999999;
    border: 1px solid #333333;
    padding: 2px 7px;
    display: inline-block;
    margin-bottom: 10px;
    text-transform: uppercase;
}

/* 카드 텍스트 */
.card-brand {
    font-family: 'JetBrains Mono', 'Pretendard', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin-bottom: 6px;
}
.card-desc {
    font-size: 0.82rem;
    color: #7A7A7A;
    line-height: 1.45;
    min-height: 38px;
    margin-bottom: 14px;
}
.prod-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #F2F2F2;
    line-height: 1.4;
    min-height: 42px;
    margin-bottom: 6px;
}
.prod-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #6E6E6E;
    margin-bottom: 12px;
}
.price-strike {
    font-family: 'JetBrains Mono', monospace;
    text-decoration: line-through;
    color: #555555;
    font-size: 0.82rem;
}
.price-main {
    font-family: 'JetBrains Mono', monospace;
    color: #FFFFFF;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}

/* 버튼 & 링크 버튼 미니멀 고대비 */
.stButton > button, .stLinkButton > a {
    background-color: #161616 !important;
    color: #EAEAEA !important;
    border: 1px solid #333333 !important;
    border-radius: 0px !important;
    font-family: 'JetBrains Mono', 'Pretendard', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 0.5rem 0.8rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover, .stLinkButton > a:hover {
    background-color: #D4FF00 !important;
    color: #0A0A0A !important;
    border-color: #D4FF00 !important;
}

/* 입력창 다크 톤 */
input[type="text"], input[type="number"] {
    background-color: #111111 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 0px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# [AFFILIATE CONFIG]
# ==========================================
COUPANG_SUB_ID = "AF1234567"

def make_affiliate_url(product_name):
    encoded = requests.utils.quote(product_name)
    return f"https://www.coupang.com/np/search?component=&q={encoded}&channel=user"

# ==========================================
# [AUTOMATED GLOBAL FEED ENGINE]
# ==========================================
@st.cache_data(ttl=1800)
def fetch_live_exchange_rate():
    try:
        res = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        if res.status_code == 200:
            rate = res.json().get("rates", {}).get("KRW")
            if rate:
                return float(rate)
    except Exception:
        pass
    return 1390.0

@st.cache_data(ttl=900)
def fetch_global_store_feed(search_query, krw_rate):
    stores = [
        {"name": "HAVEN // CA", "domain": "https://havenshop.com", "rate_mult": 0.72},
        {"name": "BODEGA // US", "domain": "https://bdgastore.com", "rate_mult": 1.0},
        {"name": "EXTRA BUTTER // US", "domain": "https://extrabutterny.com", "rate_mult": 1.0},
        {"name": "CONCEPTS // US", "domain": "https://cncpts.com", "rate_mult": 1.0},
        {"name": "CIELE OFFICIAL", "domain": "https://cieleathletics.com", "rate_mult": 1.0},
        {"name": "NORDA OFFICIAL", "domain": "https://nordarun.com", "rate_mult": 1.0},
        {"name": "SATISFY OFFICIAL", "domain": "https://satisfyrunning.com", "rate_mult": 1.0}
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    results = []
    encoded_q = requests.utils.quote(search_query)

    for store in stores:
        try:
            url = f"{store['domain']}/search/suggest.json?q={encoded_q}&resources[type]=product&resources[limit]=6"
            res = requests.get(url, headers=headers, timeout=4)
            if res.status_code != 200:
                continue
            items = res.json().get("resources", {}).get("results", {}).get("products", [])
            for item in items:
                title = item.get("title", "").strip()
                raw_price = str(item.get("price", "0"))
                try:
                    price_val = float(re.sub(r"[^0-9.]", "", raw_price))
                except ValueError:
                    price_val = 0.0

                if not title or price_val <= 0:
                    continue

                usd_equiv = price_val * store["rate_mult"]
                krw_price = int(usd_equiv * krw_rate)
                kr_retail_est = int(krw_price * 1.24)
                discount_pct = max(8, int((1 - krw_price / kr_retail_est) * 100))

                img_url = item.get("image") or item.get("featured_image", {}).get("url") or ""
                if img_url.startswith("//"):
                    img_url = "https:" + img_url

                prod_path = item.get("url", "")
                source_url = store["domain"] + prod_path if prod_path.startswith("/") else prod_path

                results.append({
                    "name": title,
                    "store": store["name"],
                    "usd_price": usd_equiv,
                    "sale_price": krw_price,
                    "orig_price": kr_retail_est,
                    "discount_pct": discount_pct,
                    "img_url": img_url if img_url.startswith("http") else "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80",
                    "source_url": source_url,
                    "affiliate_url": make_affiliate_url(title)
                })
                if len(results) >= 9:
                    return results
        except Exception:
            continue

    return results

def get_curated_backup_items(brand_name, krw_rate):
    catalog_db = {
        "SATISFY": [
            ("Satisfy MothTech™ T-Shirt (Aged Black)", 120, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80", "https://satisfyrunning.com"),
            ("Satisfy Justice™ Cordura® 5\" Shorts", 190, "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=600&q=80", "https://satisfyrunning.com"),
            ("Satisfy PeaceShell™ Trail Cap", 75, "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=600&q=80", "https://satisfyrunning.com")
        ],
        "PORTAL": [
            ("Portal Ultra-Light Trail Shell Jacket", 240, "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80", "https://www.google.com/search?q=Portal+running+apparel"),
            ("Portal Technical Merino Base Tee", 95, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80", "https://www.google.com/search?q=Portal+running+apparel"),
            ("Portal Ripstop Performance Shorts", 135, "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=600&q=80", "https://www.google.com/search?q=Portal+running+apparel")
        ],
        "CANNONDALE": [
            ("Cannondale SuperSix EVO Carbon Disc", 4200, "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=600&q=80", "https://www.cannondale.com"),
            ("Cannondale CAAD13 Disc 105", 2300, "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=600&q=80", "https://www.cannondale.com"),
            ("Cannondale Topstone Carbon Gravel", 3100, "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=600&q=80", "https://www.cannondale.com")
        ],
        "RAPHA": [
            ("Rapha Pro Team Bib Shorts II", 295, "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600&q=80", "https://www.rapha.cc"),
            ("Rapha Classic Flyweight Jersey", 155, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80", "https://www.rapha.cc"),
            ("Rapha Pro Team Powerweave Shoes", 380, "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=600&q=80", "https://www.rapha.cc")
        ]
    }

    default_items = [
        (f"{brand_name} — Flagship Performance Edition", 185, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80", "https://www.endclothing.com"),
        (f"{brand_name} — Pro Racing / Trail Spec", 145, "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&q=80", "https://havenshop.com"),
        (f"{brand_name} — Lightweight Technical Essential", 110, "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80", "https://www.ssense.com")
    ]

    selected = catalog_db.get(brand_name, default_items)
    output = []
    for title, usd, img, link in selected:
        krw_price = int(usd * krw_rate)
        orig_price = int(krw_price * 1.22)
        output.append({
            "name": title,
            "store": "GLOBAL DIRECT // INDEX",
            "usd_price": usd,
            "sale_price": krw_price,
            "orig_price": orig_price,
            "discount_pct": 18,
            "img_url": img,
            "source_url": link,
            "affiliate_url": make_affiliate_url(title)
        })
    return output

def get_global_sourcing_deals():
    return [
        {
            "name": "Satisfy MothTech™ T-Shirt",
            "store": "SSENSE // SATISFY",
            "usd_price": 115.0,
            "kr_market_price": 245000,
            "img_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80",
            "sourcing_url": "https://satisfyrunning.com"
        },
        {
            "name": "Salomon XT-6 GTX (Black/Ebony)",
            "store": "END. CLOTHING // UK",
            "usd_price": 145.0,
            "kr_market_price": 289000,
            "img_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80",
            "sourcing_url": "https://www.endclothing.com/kr/catalogsearch/results?q=salomon+xt-6"
        },
        {
            "name": "POC Ventral Air MIPS Helmet",
            "store": "BIKEINN // EU",
            "usd_price": 158.0,
            "kr_market_price": 320000,
            "img_url": "https://images.unsplash.com/photo-1557803175-2f8c4c272074?w=600&q=80",
            "sourcing_url": "https://www.tradeinn.com/bikeinn/ko"
        },
        {
            "name": "norda™ 001 Dyneema Trail",
            "store": "HAVEN // NORDA",
            "usd_price": 195.0,
            "kr_market_price": 399000,
            "img_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&q=80",
            "sourcing_url": "https://nordarun.com"
        },
        {
            "name": "Arc'teryx Norvan Windshell",
            "store": "BACKCOUNTRY // US",
            "usd_price": 165.0,
            "kr_market_price": 330000,
            "img_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80",
            "sourcing_url": "https://www.backcountry.com"
        },
        {
            "name": "Shimano S-Phyre RC903",
            "store": "BIKE24 // DE",
            "usd_price": 265.0,
            "kr_market_price": 490000,
            "img_url": "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=600&q=80",
            "sourcing_url": "https://www.bike24.com"
        }
    ]

# 실시간 환율 로드
live_usd_krw = fetch_live_exchange_rate()

# ==========================================
# [MASTHEAD & TOP NAVIGATION]
# ==========================================
st.markdown(f"""
<div class="masthead">
    <div>
        <div class="masthead-title">NICHERADAR<span class="masthead-accent">.ARCHIVE</span></div>
    </div>
    <div class="masthead-meta">
        LIVE FX: {live_usd_krw:,.1f} KRW/USD &nbsp;//&nbsp; CURATED TECHNICAL GEAR & GLOBAL ARBITRAGE
    </div>
</div>
""", unsafe_allow_html=True)

menu = st.radio(
    "INDEX",
    [
        "01 // ARBITRAGE FEED",
        "02 // RUNNING",
        "03 // CYCLING",
        "04 // TRAIL",
        "05 // APPAREL",
        "06 // HARDWARE"
    ],
    label_visibility="collapsed"
)

# ==========================================
# [VIEW 1] GLOBAL ARBITRAGE & SOURCING FEED
# ==========================================
if menu == "01 // ARBITRAGE FEED":
    c1, c2, c3 = st.columns(3)
    with c1:
        ex_rate = st.number_input("FX RATE (KRW/USD)", value=float(int(live_usd_krw)), step=10.0)
    with c2:
        ship_fee = st.number_input("INTL SHIPPING (KRW)", value=15000, step=1000)
    with c3:
        fee_pct = st.number_input("PLATFORM FEE (%)", value=6.0, step=0.5)

    st.write("")
    sourcing_items = get_global_sourcing_deals()

    cols = st.columns(3)
    for idx, item in enumerate(sourcing_items):
        krw_cost = item["usd_price"] * ex_rate
        tax = (krw_cost * 0.18) if item["usd_price"] > 200 else 0
        market_fee = item["kr_market_price"] * (fee_pct / 100.0)
        net_profit = item["kr_market_price"] - (krw_cost + ship_fee + tax + market_fee)
        margin_pct = (net_profit / item["kr_market_price"]) * 100

        with cols[idx % 3]:
            with st.container(border=True):
                st.image(item["img_url"], use_container_width=True)
                st.markdown(f"<span class='tag-pill'>NET SPREAD +{int(net_profit):,} KRW ({margin_pct:.1f}%)</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='prod-title'>{item['name']}</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='prod-meta'>SOURCE: {item['store']} &nbsp;|&nbsp; TAX: {'INCLUDED' if tax > 0 else 'EXEMPT (<$200)'}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span class='price-strike'>GLOBAL ${item['usd_price']:.0f} (₩{int(krw_cost):,})</span><br>"
                    f"<span class='price-main'>KRW {item['kr_market_price']:,}</span>",
                    unsafe_allow_html=True
                )
                st.write("")
                st.link_button("DIRECT SOURCE ↗", item["sourcing_url"], use_container_width=True)
                st.link_button("KR MARKET COMPARE ↗", make_affiliate_url(item["name"]), use_container_width=True)

# ==========================================
# [VIEW 2~6] BRAND INDEX -> LIVE FEED DRILLDOWN
# ==========================================
else:
    brand_catalog = {
        "02 // RUNNING": {
            "brands": {
                "NIKE": {"sub": "Alphafly 3 · Vaporfly 3 · Pegasus", "queries": ["Nike Alphafly", "Nike Vaporfly", "Nike Pegasus", "Nike Vomero"]},
                "ASICS": {"sub": "Metaspeed Sky · Superblast 2 · Gel-Kayano", "queries": ["ASICS Metaspeed", "ASICS Superblast", "ASICS Novablast", "ASICS Gel-Kayano"]},
                "ADIDAS": {"sub": "Adios Pro 4 · Boston 12 · Evo SL", "queries": ["Adidas Adios Pro", "Adidas Boston 12", "Adidas Evo SL", "Adidas Takumi Sen"]},
                "HOKA": {"sub": "Mach 6 · Clifton 9 · Cielo X1", "queries": ["HOKA Mach", "HOKA Clifton", "HOKA Cielo", "HOKA Bondi"]},
                "ON RUNNING": {"sub": "Cloudmonster 2 · Cloudboom Strike", "queries": ["On Cloudmonster", "On Cloudboom", "On Cloudsurfer", "On Cloudtilt"]},
                "NEW BALANCE": {"sub": "FuelCell SC Elite v4 · Rebel v4 · 1080v14", "queries": ["New Balance FuelCell", "New Balance Rebel", "New Balance 1080", "New Balance 990"]},
                "SAUCONY": {"sub": "Endorphin Pro 4 · Speed 4 · Triumph", "queries": ["Saucony Endorphin Pro", "Saucony Endorphin Speed", "Saucony Triumph", "Saucony Kinvara"]},
                "BROOKS": {"sub": "Hyperion Max 2 · Glycerin Max · Ghost 16", "queries": ["Brooks Hyperion", "Brooks Glycerin", "Brooks Ghost", "Brooks Adrenaline"]}
            }
        },
        "03 // CYCLING": {
            "brands": {
                "CANNONDALE": {"sub": "SuperSix EVO · CAAD13 · Topstone Gravel", "queries": ["Cannondale SuperSix", "Cannondale CAAD13", "Cannondale Topstone", "Cannondale"]},
                "SPECIALIZED": {"sub": "Tarmac SL8 · S-Works Torch · Prevail 3", "queries": ["Specialized S-Works", "Specialized Tarmac", "Specialized Prevail", "Specialized"]},
                "TREK": {"sub": "Madone SLR · Émonda · Domane · Bontrager", "queries": ["Trek Madone", "Trek Emonda", "Trek Domane", "Bontrager"]},
                "CANYON": {"sub": "Aeroad CFR · Ultimate · Grail", "queries": ["Canyon Aeroad", "Canyon Ultimate", "Canyon Grail", "Canyon"]},
                "CERVÉLO": {"sub": "S5 · R5 · Soloist · Caledonia", "queries": ["Cervelo S5", "Cervelo R5", "Cervelo Soloist", "Cervelo"]},
                "GIANT": {"sub": "Propel Advanced · TCR · Surge Pro", "queries": ["Giant TCR", "Giant Propel", "Giant Surge", "Giant Cycling"]},
                "BIANCHI": {"sub": "Oltre RC · Specialissima · Sprint", "queries": ["Bianchi Oltre", "Bianchi Specialissima", "Bianchi Sprint", "Bianchi"]},
                "SHIMANO": {"sub": "S-Phyre RC903 · Dura-Ace · Ultegra", "queries": ["Shimano RC903", "Shimano S-Phyre", "Shimano Dura-Ace", "Shimano"]},
                "FIZIK": {"sub": "Vento Infinito · Tempo Overcurve · Antares", "queries": ["Fizik Vento", "Fizik Tempo", "Fizik Antares", "Fizik"]},
                "SIDI": {"sub": "Shot 2 · Wire 2 · Genius 10", "queries": ["SIDI Shot", "SIDI Wire", "SIDI Genius", "SIDI"]},
                "LAKE & BONT": {"sub": "CX332 Wide · Vaypor S Heat-Moldable", "queries": ["Lake CX332", "Lake Cycling", "Bont Vaypor", "Bont Cycling"]},
                "RAPHA": {"sub": "Pro Team Bib Shorts · Classic Jersey", "queries": ["Rapha Pro Team", "Rapha Classic", "Rapha Jersey", "Rapha"]}
            }
        },
        "04 // TRAIL": {
            "brands": {
                "SALOMON": {"sub": "XT-6 · S/LAB Ultra · Speedcross 6", "queries": ["Salomon XT-6", "Salomon S/LAB", "Salomon Speedcross", "Salomon ACS"]},
                "NORDA": {"sub": "001 · 002 · 003 Bio-Dyneema® Trail", "queries": ["norda 001", "norda 002", "norda 003", "norda"]},
                "HOKA TRAIL": {"sub": "Speedgoat 6 · Mafate Speed 4 · Tecton X3", "queries": ["HOKA Speedgoat", "HOKA Mafate", "HOKA Tecton", "HOKA Anacapa"]},
                "ALTRA": {"sub": "Lone Peak 8 · Olympus 6 · Timp 5", "queries": ["Altra Lone Peak", "Altra Olympus", "Altra Timp", "Altra Mont Blanc"]},
                "THE NORTH FACE": {"sub": "Vectiv Enduris 3 · Summit Vectiv Pro", "queries": ["North Face Vectiv", "North Face Summit", "North Face Trail", "The North Face"]},
                "LA SPORTIVA": {"sub": "Bushido III · Akasha II · Ultra Raptor II", "queries": ["La Sportiva Bushido", "La Sportiva Akasha", "La Sportiva Raptor", "La Sportiva"]},
                "SCARPA": {"sub": "Ribelle Run · Spin Planet · Mojito", "queries": ["Scarpa Ribelle", "Scarpa Spin", "Scarpa Mojito", "Scarpa"]},
                "MERRELL & ARC'TERYX": {"sub": "Agility Peak 5 · Norvan LD3 · Moab 3 GTX", "queries": ["Merrell Agility Peak", "Arc'teryx Norvan", "Merrell Moab", "Arc'teryx Konseal"]}
            }
        },
        "05 // APPAREL": {
            "brands": {
                "SATISFY": {"sub": "MothTech™ Tee · Justice™ Shorts · PeaceShell", "queries": ["Satisfy MothTech", "Satisfy Running", "Satisfy Shorts", "Satisfy"]},
                "PORTAL": {"sub": "Ultra-Light Trail Shell · Technical Tee", "queries": ["Portal Running", "Portal Trail", "Portal Jacket", "Portal"]},
                "CIELE ATHLETICS": {"sub": "GOCap · ALZCap · Elite Singlet", "queries": ["Ciele GOCap", "Ciele ALZCap", "Ciele Athletics", "Ciele"]},
                "SOAR RUNNING": {"sub": "Elite Race Singlet · Marathon Shorts", "queries": ["SOAR Running", "SOAR Singlet", "SOAR Shorts", "SOAR"]},
                "SAYSKY": {"sub": "Pace Shorts · Combat Singlet · Merino", "queries": ["SAYSKY", "SAYSKY Singlet", "SAYSKY Shorts", "SAYSKY Jacket"]},
                "DISTRICT VISION": {"sub": "Technical Apparel · Keiichi / Koharu Eyewear", "queries": ["District Vision", "District Vision Sunglasses", "District Vision Running", "District"]},
                "PATAGONIA": {"sub": "Strider Pro Shorts · Houdini · Baggies", "queries": ["Patagonia Strider", "Patagonia Houdini", "Patagonia Baggies", "Patagonia"]},
                "ARC'TERYX": {"sub": "Norvan Windshell · Cormac Crew · Beta", "queries": ["Arc'teryx Norvan", "Arc'teryx Cormac", "Arc'teryx Beta", "Arc'teryx Squamish"]},
                "CAYL": {"sub": "Mountain Trail Jacket · Nylon Shorts", "queries": ["CAYL", "CAYL Jacket", "CAYL Pants", "CAYL Bag"]},
                "SAN SAN GEAR / UNAFFECTED": {"sub": "Technical Trail Pants · Windblock Shell", "queries": ["San San Gear", "Unaffected", "Techwear Jacket", "Trail Pants"]},
                "RAB & MONTANE": {"sub": "Phantom Pull-On · Minimus Waterproof Shell", "queries": ["Rab Phantom", "Montane Minimus", "Rab Jacket", "Montane"]},
                "ON APPAREL": {"sub": "Performance Tee · Lightweight Shorts · Weather Jacket", "queries": ["On Running Jacket", "On Running Shorts", "On Running Tee", "On Apparel"]}
            }
        },
        "06 // HARDWARE": {
            "brands": {
                "GARMIN": {"sub": "Forerunner 265 / 965 · Fenix 8 · Edge 840", "queries": ["Garmin Forerunner", "Garmin Fenix", "Garmin Edge", "Garmin"]},
                "POC": {"sub": "Ventral Air MIPS · Octal · Aspire Eyewear", "queries": ["POC Ventral", "POC Octal", "POC Aspire", "POC Helmet"]},
                "KASK": {"sub": "Protone Icon · Valegro · Utopia Y", "queries": ["KASK Protone", "KASK Valegro", "KASK Utopia", "KASK"]},
                "OAKLEY": {"sub": "Sutro Lite · Radar EV · Encoder", "queries": ["Oakley Sutro", "Oakley Radar", "Oakley Encoder", "Oakley"]},
                "SALOMON GEAR": {"sub": "ADV Skin 12 · Sense Pro 10 · Soft Flask", "queries": ["Salomon ADV Skin", "Salomon Sense Pro", "Salomon Flask", "Salomon Vest"]},
                "BLACK DIAMOND": {"sub": "Distance Carbon Z · Spot 400 Headlamp", "queries": ["Black Diamond Distance", "Black Diamond Spot", "Black Diamond", "Black Diamond Poles"]},
                "SUUNTO & COROS": {"sub": "Suunto Race · COROS Pace 3 · Apex 2 Pro", "queries": ["Suunto Race", "COROS Pace", "COROS Apex", "Suunto"]},
                "SHOKZ": {"sub": "OpenRun Pro 2 · OpenSwim Pro · OpenFit", "queries": ["Shokz OpenRun", "Shokz OpenSwim", "Shokz OpenFit", "Shokz"]}
            }
        }
    }

    cat_data = brand_catalog[menu]

    if st.session_state.get("active_category") != menu:
        st.session_state["active_category"] = menu
        st.session_state["selected_brand"] = None
        st.session_state["selected_model"] = None

    selected_brand = st.session_state.get("selected_brand")

    if not selected_brand:
        brand_names = list(cat_data["brands"].keys())
        cols_per_row = 4

        for row_start in range(0, len(brand_names), cols_per_row):
            row_brands = brand_names[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            for i, b_name in enumerate(row_brands):
                b_info = cat_data["brands"][b_name]
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"<div class='tag-outline'>IDX // {row_start + i + 1:02d}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='card-brand'>{b_name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='card-desc'>{b_info['sub']}</div>", unsafe_allow_html=True)
                        if st.button("EXPLORE FEED →", key=f"open_{menu}_{b_name}", use_container_width=True):
                            st.session_state["selected_brand"] = b_name
                            st.session_state["selected_model"] = b_info["queries"][0]
                            st.rerun()

    else:
        b_info = cat_data["brands"][selected_brand]

        top_c1, top_c2 = st.columns([1, 5])
        with top_c1:
            if st.button("← ALL BRANDS", use_container_width=True):
                st.session_state["selected_brand"] = None
                st.session_state["selected_model"] = None
                st.rerun()
        with top_c2:
            st.markdown(f"<div class='masthead-title' style='font-size:1.5rem;'>{selected_brand} <span class='masthead-accent'>// FEED</span></div>", unsafe_allow_html=True)

        st.write("")
        m_cols = st.columns(len(b_info["queries"]))
        for idx, q_name in enumerate(b_info["queries"]):
            if m_cols[idx].button(q_name.upper(), key=f"model_{q_name}", use_container_width=True):
                st.session_state["selected_model"] = q_name

        current_query = st.text_input(
            "QUERY FILTER",
            value=st.session_state.get("selected_model", b_info["queries"][0]),
            label_visibility="collapsed"
        )

        with st.spinner(f"SCANNING GLOBAL INDEX FOR '{current_query.upper()}'..."):
            deals = fetch_global_store_feed(current_query, live_usd_krw)
            if not deals:
                deals = get_curated_backup_items(selected_brand, live_usd_krw)

        st.write("")
        cols = st.columns(3)
        for idx, prod in enumerate(deals):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(prod["img_url"], use_container_width=True)
                    st.markdown(f"<span class='tag-pill'>-{prod['discount_pct']}% VS KR RETAIL</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='prod-title'>{prod['name'][:52]}{'...' if len(prod['name']) > 52 else ''}</div>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='prod-meta'>{prod['store']} &nbsp;//&nbsp; ${prod['usd_price']:,.0f} USD</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<span class='price-strike'>EST. KRW {prod['orig_price']:,}</span><br>"
                        f"<span class='price-main'>KRW {prod['sale_price']:,}</span>",
                        unsafe_allow_html=True
                    )
                    st.write("")
                    st.link_button("GLOBAL STORE ↗", prod["source_url"], use_container_width=True)
                    st.link_button("KR LOWEST PRICE ↗", prod["affiliate_url"], use_container_width=True)
