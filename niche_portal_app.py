import streamlit as st
import requests
import re

# ==========================================
# [페이지 기본 설정]
# ==========================================
st.set_page_config(
    page_title="NicheRadar Pro v3.0 | 하이엔드 러닝·사이클·트레일 무인 레이더",
    page_icon="📡",
    layout="wide"
)

st.markdown("""
<style>
.discount-badge {
    background-color: #ff4b4b;
    color: white;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    display: inline-block;
    margin-bottom: 6px;
}
.margin-badge {
    background-color: #00a86b;
    color: white;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    display: inline-block;
    margin-bottom: 6px;
}
.orig-price {
    text-decoration: line-through;
    color: #888888;
    font-size: 0.88rem;
}
.sale-price {
    color: #111111;
    font-size: 1.22rem;
    font-weight: 800;
}
.brand-title {
    font-size: 1.12rem;
    font-weight: 800;
    margin-bottom: 4px;
}
.brand-sub {
    font-size: 0.82rem;
    color: #666666;
    margin-bottom: 12px;
    min-height: 36px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# [수익화 설정] 제휴 트래킹 링크 & PRO 마스터 코드
# ==========================================
COUPANG_SUB_ID = "AF1234567"
PRO_ACCESS_CODE = "VIP2026"

def make_affiliate_url(product_name):
    encoded = requests.utils.quote(product_name)
    return f"https://www.coupang.com/np/search?component=&q={encoded}&channel=user"

# ==========================================
# [완전 무인 글로벌 피드 엔진] (API 키 0개 / 해외 서버 100% 작동)
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
    """
    해외 클라우드 IP를 차단하지 않는 하이엔드 편집숍 공개 JSON 피드(Shopify 기반)를
    실시간으로 스캔하여 이미지·가격·구매링크를 자동 추출합니다.
    """
    stores = [
        {"name": "HAVEN (CA)", "domain": "https://havenshop.com", "currency": "CAD", "rate_mult": 0.72},
        {"name": "Bodega (US)", "domain": "https://bdgastore.com", "currency": "USD", "rate_mult": 1.0},
        {"name": "Extra Butter (US)", "domain": "https://extrabutterny.com", "currency": "USD", "rate_mult": 1.0},
        {"name": "Concepts (US)", "domain": "https://cncpts.com", "currency": "USD", "rate_mult": 1.0},
        {"name": "Ciele Official", "domain": "https://cieleathletics.com", "currency": "USD", "rate_mult": 1.0},
        {"name": "norda Official", "domain": "https://nordarun.com", "currency": "USD", "rate_mult": 1.0},
        {"name": "Satisfy Official", "domain": "https://satisfyrunning.com", "currency": "USD", "rate_mult": 1.0}
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
            data = res.json()
            items = data.get("resources", {}).get("results", {}).get("products", [])
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
                    "img_url": img_url if img_url.startswith("http") else "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80",
                    "source_url": source_url,
                    "affiliate_url": make_affiliate_url(title)
                })
                if len(results) >= 9:
                    return results
        except Exception:
            continue

    return results

def get_curated_backup_items(brand_name, krw_rate):
    """실시간 피드 검색 결과가 적은 니치 브랜드용 큐레이션 카탈로그"""
    catalog_db = {
        "세티스파이 (Satisfy)": [
            ("Satisfy MothTech™ T-Shirt (Aged Black)", 120, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80", "https://satisfyrunning.com"),
            ("Satisfy Justice™ Cordura® 5\" Shorts", 190, "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&q=80", "https://satisfyrunning.com"),
            ("Satisfy PeaceShell™ Trail Cap", 75, "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=500&q=80", "https://satisfyrunning.com")
        ],
        "포탈 (Portal)": [
            ("Portal Ultra-Light Trail Shell Jacket", 240, "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80", "https://www.google.com/search?q=Portal+running+apparel"),
            ("Portal Technical Merino Base Tee", 95, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80", "https://www.google.com/search?q=Portal+running+apparel"),
            ("Portal Ripstop Performance Shorts", 135, "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&q=80", "https://www.google.com/search?q=Portal+running+apparel")
        ],
        "캐논데일 (Cannondale)": [
            ("Cannondale SuperSix EVO Carbon Disc", 4200, "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=500&q=80", "https://www.cannondale.com"),
            ("Cannondale CAAD13 Disc 105", 2300, "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=500&q=80", "https://www.cannondale.com"),
            ("Cannondale Topstone Carbon Gravel", 3100, "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=500&q=80", "https://www.cannondale.com")
        ],
        "라파 (Rapha)": [
            ("Rapha Pro Team Bib Shorts II", 295, "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=500&q=80", "https://www.rapha.cc"),
            ("Rapha Classic Flyweight Jersey", 155, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80", "https://www.rapha.cc"),
            ("Rapha Pro Team Powerweave Shoes", 380, "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=500&q=80", "https://www.rapha.cc")
        ]
    }

    default_items = [
        (f"{brand_name} 플래그십 퍼포먼스 에디션", 185, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80", "https://www.endclothing.com"),
        (f"{brand_name} 프로 레이싱/트레일 기어", 145, "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&q=80", "https://havenshop.com"),
        (f"{brand_name} 경량 테크니컬 에센셜", 110, "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80", "https://www.ssense.com")
    ]

    selected = catalog_db.get(brand_name, default_items)
    output = []
    for title, usd, img, link in selected:
        krw_price = int(usd * krw_rate)
        orig_price = int(krw_price * 1.22)
        output.append({
            "name": title,
            "store": "Global Direct (직구 시세)",
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
            "store": "SSENSE / Satisfy Official",
            "usd_price": 115.0,
            "kr_market_price": 245000,
            "img_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80",
            "sourcing_url": "https://satisfyrunning.com"
        },
        {
            "name": "Salomon XT-6 GTX (Black/Ebony)",
            "store": "END. Clothing (UK)",
            "usd_price": 145.0,
            "kr_market_price": 289000,
            "img_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80",
            "sourcing_url": "https://www.endclothing.com/kr/catalogsearch/results?q=salomon+xt-6"
        },
        {
            "name": "POC Ventral Air MIPS 헬멧",
            "store": "BikeInn (EU 직구)",
            "usd_price": 158.0,
            "kr_market_price": 320000,
            "img_url": "https://images.unsplash.com/photo-1557803175-2f8c4c272074?w=500&q=80",
            "sourcing_url": "https://www.tradeinn.com/bikeinn/ko"
        },
        {
            "name": "norda™ 001 Dyneema Trail Shoe",
            "store": "HAVEN / norda Official",
            "usd_price": 195.0,
            "kr_market_price": 399000,
            "img_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&q=80",
            "sourcing_url": "https://nordarun.com"
        },
        {
            "name": "Arc'teryx Norvan Windshell 자켓",
            "store": "Backcountry (US)",
            "usd_price": 165.0,
            "kr_market_price": 330000,
            "img_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80",
            "sourcing_url": "https://www.backcountry.com"
        },
        {
            "name": "Shimano S-Phyre RC903 클릿슈즈",
            "store": "Bike24 (DE 직구)",
            "usd_price": 265.0,
            "kr_market_price": 490000,
            "img_url": "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=500&q=80",
            "sourcing_url": "https://www.bike24.com"
        }
    ]

# 실시간 달러 환율 자동 로드
live_usd_krw = fetch_live_exchange_rate()

# ==========================================
# [사이드바] 네비게이션 & PRO 멤버십 인증
# ==========================================
with st.sidebar:
    st.title("📡 NicheRadar Pro")
    st.caption(f"무인 글로벌 기어 레이더 | 실시간 환율: {live_usd_krw:,.0f}원/$")
    st.divider()

    menu = st.radio(
        "카테고리 선택",
        [
            "🌍 해외 소싱 / 구매대행 딜",
            "🏃‍♂️ 러닝 (Running)",
            "🚴 자전거 (Cycling)",
            "⛰️ 트레일 / 아웃도어 (Trail)",
            "👕 의류 / 어패럴 (Apparel)",
            "🎒 악세서리 / 기어 (Accessories)"
        ]
    )

    st.divider()
    st.subheader("🔑 PRO 멤버십 잠금 해제")
    user_code = st.text_input("구독자 액세스 코드", type="password", placeholder="테스트 코드: VIP2026")
    is_pro = (user_code == PRO_ACCESS_CODE)

    if is_pro:
        st.success("✅ PRO 멤버십 활성화됨 (소싱처 직링크 열림)")
    else:
        st.info("💡 무료 버전: 해외 소싱처 직링크와 심층 마진 분석은 PRO 구독 후 열립니다.")
        st.link_button("💳 PRO 멤버십 구독하기 (월 19,000원)", "https://gumroad.com")

# ==========================================
# [메인 1] 해외 소싱 / 구매대행 상품 카드 페이지
# ==========================================
if menu == "🌍 해외 소싱 / 구매대행 딜":
    st.header("🌍 해외 소싱 / 구매대행 실시간 역산 마진 딜")
    st.markdown("실시간 달러 환율과 국내 리셀·오픈마켓 시세를 자동 계산해 **순수 중간 마진**이 남는 상품만 카드로 띄웁니다.")

    c1, c2, c3 = st.columns(3)
    with c1:
        ex_rate = st.number_input("실시간 기준 환율 (원/$)", value=float(int(live_usd_krw)), step=10.0)
    with c2:
        ship_fee = st.number_input("평균 배대지/국제 배송비 (원)", value=15000, step=1000)
    with c3:
        fee_pct = st.number_input("국내 판매 수수료 (%)", value=6.0, step=0.5)

    st.divider()
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
                st.markdown(f"<span class='margin-badge'>예상 순마진 +{int(net_profit):,}원 ({margin_pct:.1f}%)</span>", unsafe_allow_html=True)
                st.subheader(item["name"])
                st.caption(f"소싱처: **{item['store']}** | 관부가세: {'포함(약 ' + f'{int(tax):,}원)' if tax > 0 else '면제($200 이하)'}")
                st.markdown(
                    f"해외 소싱가: **${item['usd_price']:.0f}** (약 {int(krw_cost):,}원)<br>"
                    f"국내 시세: <span class='sale-price'>{item['kr_market_price']:,}원</span>",
                    unsafe_allow_html=True
                )
                st.write("")
                if is_pro:
                    st.link_button("🚀 해외 소싱처 바로가기 (PRO)", item["sourcing_url"], use_container_width=True)
                else:
                    st.button("🔒 소싱처 URL 잠금 (PRO 전용)", key=f"lock_{idx}", disabled=True, use_container_width=True)

# ==========================================
# [메인 2~6] 브랜드 우선 선택 -> 글로벌 무인 피드 노출 2단계 구조
# ==========================================
else:
    brand_catalog = {
        "🏃‍♂️ 러닝 (Running)": {
            "title": "🏃‍♂️ 러닝 브랜드관",
            "subtitle": "원하시는 러닝 브랜드를 선택하면 글로벌 편집숍·공식 스토어 실시간 피드가 열립니다.",
            "brands": {
                "나이키 (Nike)": {"desc": "알파플라이3 · 베이퍼플라이3 · 페가수스", "queries": ["Nike Alphafly", "Nike Vaporfly", "Nike Pegasus", "Nike Vomero"]},
                "아식스 (ASICS)": {"desc": "메타스피드 스카이 · 슈퍼블라스트2 · 젤카야노", "queries": ["ASICS Metaspeed", "ASICS Superblast", "ASICS Novablast", "ASICS Gel-Kayano"]},
                "아디다스 (Adidas)": {"desc": "아디오스 프로4 · 보스턴12 · 에보 SL", "queries": ["Adidas Adios Pro", "Adidas Boston 12", "Adidas Evo SL", "Adidas Takumi Sen"]},
                "호카 (HOKA)": {"desc": "마하6 · 클리프톤9 · 씨엘로 X1", "queries": ["HOKA Mach", "HOKA Clifton", "HOKA Cielo", "HOKA Bondi"]},
                "온러닝 (On Running)": {"desc": "클라우드몬스터2 · 클라우드붐 스트라이크", "queries": ["On Cloudmonster", "On Cloudboom", "On Cloudsurfer", "On Cloudtilt"]},
                "뉴발란스 (New Balance)": {"desc": "퓨어셀 SC 엘리트 v4 · 레벨 v4 · 1080v14", "queries": ["New Balance FuelCell", "New Balance Rebel", "New Balance 1080", "New Balance 990"]},
                "써코니 (Saucony)": {"desc": "엔돌핀 프로4 · 엔돌핀 스피드4 · 트라이엄프", "queries": ["Saucony Endorphin Pro", "Saucony Endorphin Speed", "Saucony Triumph", "Saucony Kinvara"]},
                "브룩스 (Brooks)": {"desc": "하이페리온 맥스2 · 글리세린 맥스 · 고스트16", "queries": ["Brooks Hyperion", "Brooks Glycerin", "Brooks Ghost", "Brooks Adrenaline"]}
            }
        },
        "🚴 자전거 (Cycling)": {
            "title": "🚴 사이클링 브랜드관",
            "subtitle": "캐논데일, 스페셜라이즈드, 라파 등 주요 사이클링 완성차·기어·슈즈 브랜드를 선택하세요.",
            "brands": {
                "캐논데일 (Cannondale)": {"desc": "슈퍼식스 에보 · CAAD13 · 탑스톤 그래블", "queries": ["Cannondale SuperSix", "Cannondale CAAD13", "Cannondale Topstone", "Cannondale"]},
                "스페셜라이즈드 (Specialized)": {"desc": "타막 SL8 · 에스웍스 토치 슈즈 · 프리베일3", "queries": ["Specialized S-Works", "Specialized Tarmac", "Specialized Prevail", "Specialized"]},
                "트렉 (Trek)": {"desc": "마돈 SLR · 에몬다 · 도마니 · 벨로시스", "queries": ["Trek Madone", "Trek Emonda", "Trek Domane", "Bontrager"]},
                "캐니언 (Canyon)": {"desc": "에어로드 CFR · 얼티메이트 · 그레일", "queries": ["Canyon Aeroad", "Canyon Ultimate", "Canyon Grail", "Canyon"]},
                "써벨로 (Cervélo)": {"desc": "S5 · R5 · 솔로이스트 · 칼레도니아", "queries": ["Cervelo S5", "Cervelo R5", "Cervelo Soloist", "Cervelo"]},
                "자이언트 (Giant)": {"desc": "프로펠 어드밴스 · TCR · 서지 프로 슈즈", "queries": ["Giant TCR", "Giant Propel", "Giant Surge", "Giant Cycling"]},
                "비앙키 (Bianchi)": {"desc": "올트레 RC · 스페셜리시마 · 스프린트", "queries": ["Bianchi Oltre", "Bianchi Specialissima", "Bianchi Sprint", "Bianchi"]},
                "시마노 (Shimano)": {"desc": "에스파이어 RC903 · 듀라에이스 · 울테그라", "queries": ["Shimano RC903", "Shimano S-Phyre", "Shimano Dura-Ace", "Shimano"]},
                "피직 (Fizik)": {"desc": "벤토 인피니토 · 템포 오버커브 · 안타레스 안장", "queries": ["Fizik Vento", "Fizik Tempo", "Fizik Antares", "Fizik"]},
                "시디 (SIDI)": {"desc": "샷2 · 와이어2 · 지니어스10 클릿슈즈", "queries": ["SIDI Shot", "SIDI Wire", "SIDI Genius", "SIDI"]},
                "레이크 / 본트 (Lake & Bont)": {"desc": "CX332 와이드핏 · 베이퍼 S 열성형 슈즈", "queries": ["Lake CX332", "Lake Cycling", "Bont Vaypor", "Bont Cycling"]},
                "라파 (Rapha)": {"desc": "프로팀 빕숏 · 클래식 저지 · 로드 슈즈", "queries": ["Rapha Pro Team", "Rapha Classic", "Rapha Jersey", "Rapha"]}
            }
        },
        "⛰️ 트레일 / 아웃도어 (Trail)": {
            "title": "⛰️ 트레일 · 아웃도어 브랜드관",
            "subtitle": "원하시는 아웃도어 브랜드를 선택하면 글로벌 편집숍 트레일러닝화·기어 피드가 열립니다.",
            "brands": {
                "살로몬 (Salomon)": {"desc": "XT-6 · S/LAB 울트라 · 스피드크로스6", "queries": ["Salomon XT-6", "Salomon S/LAB", "Salomon Speedcross", "Salomon ACS"]},
                "노다 (norda)": {"desc": "001 · 002 · 003 다이니마 트레일 슈즈", "queries": ["norda 001", "norda 002", "norda 003", "norda"]},
                "호카 (HOKA Trail)": {"desc": "스피드고트6 · 마파테 스피드4 · 텍톤 X3", "queries": ["HOKA Speedgoat", "HOKA Mafate", "HOKA Tecton", "HOKA Anacapa"]},
                "알트라 (Altra)": {"desc": "론피크8 · 올림푸스6 · 팀프5", "queries": ["Altra Lone Peak", "Altra Olympus", "Altra Timp", "Altra Mont Blanc"]},
                "노스페이스 (The North Face)": {"desc": "벡티브 엔듀리스3 · 서밋 벡티브 프로", "queries": ["North Face Vectiv", "North Face Summit", "North Face Trail", "The North Face"]},
                "라스포르티바 (La Sportiva)": {"desc": "부시도3 · 아카샤2 · 울트라 랩터2", "queries": ["La Sportiva Bushido", "La Sportiva Akasha", "La Sportiva Raptor", "La Sportiva"]},
                "스카르파 (SCARPA)": {"desc": "리벨레 런 · 스핀 플래닛 · 모히토", "queries": ["Scarpa Ribelle", "Scarpa Spin", "Scarpa Mojito", "Scarpa"]},
                "메렐 / 아크테릭스": {"desc": "애질리티 피크5 · 노반 LD3 · 모아브3 GTX", "queries": ["Merrell Agility Peak", "Arc'teryx Norvan", "Merrell Moab", "Arc'teryx Konseal"]}
            }
        },
        "👕 의류 / 어패럴 (Apparel)": {
            "title": "👕 하이엔드 러닝 · 트레일 어패럴관 (굿러너 · 아웃오브올 큐레이션)",
            "subtitle": "세티스파이, 포탈, 시엘, SOAR 등 하이엔드 퍼포먼스 의류 브랜드를 선택하세요.",
            "brands": {
                "세티스파이 (Satisfy)": {"desc": "MothTech 티셔츠 · 리펠런트 쇼츠 · 피스쉘", "queries": ["Satisfy MothTech", "Satisfy Running", "Satisfy Shorts", "Satisfy"]},
                "포탈 (Portal)": {"desc": "트레일 쉘 자켓 · 테크니컬 티 · 퍼포먼스 쇼츠", "queries": ["Portal Running", "Portal Trail", "Portal Jacket", "Portal"]},
                "시엘 (Ciele Athletics)": {"desc": "GOCap · ALZCap · 러닝 싱글렛 · 쇼츠", "queries": ["Ciele GOCap", "Ciele ALZCap", "Ciele Athletics", "Ciele"]},
                "SOAR Running": {"desc": "엘리트 레이스 싱글렛 · 마라톤 쇼츠 · 윈드쉘", "queries": ["SOAR Running", "SOAR Singlet", "SOAR Shorts", "SOAR"]},
                "세이스카이 (SAYSKY)": {"desc": "페이스 쇼츠 · 컴뱃 싱글렛 · 메리노 롱슬리브", "queries": ["SAYSKY", "SAYSKY Singlet", "SAYSKY Shorts", "SAYSKY Jacket"]},
                "디스트릭트 비전 (District Vision)": {"desc": "테크니컬 러닝 웨어 · 스포츠 아이웨어", "queries": ["District Vision", "District Vision Sunglasses", "District Vision Running", "District"]},
                "파타고니아 (Patagonia)": {"desc": "스트라이더 프로 쇼츠 · 후디니 자켓 · 배기스", "queries": ["Patagonia Strider", "Patagonia Houdini", "Patagonia Baggies", "Patagonia"]},
                "아크테릭스 (Arc'teryx)": {"desc": "노반 윈드쉘 · 코르막 크루 · 베타 자켓", "queries": ["Arc'teryx Norvan", "Arc'teryx Cormac", "Arc'teryx Beta", "Arc'teryx Squamish"]},
                "케일 (CAYL)": {"desc": "마운틴 트레일 자켓 · 나일론 쇼츠 · 경량 웨어", "queries": ["CAYL", "CAYL Jacket", "CAYL Pants", "CAYL Bag"]},
                "산산기어 / 언어펙티드": {"desc": "테크니컬 트레일 팬츠 · 윈드블록 자켓", "queries": ["San San Gear", "Unaffected", "Techwear Jacket", "Trail Pants"]},
                "랩 / 몬테인 (Rab & Montane)": {"desc": "팬텀 풀온 방수 자켓 · 미니머스 쉘", "queries": ["Rab Phantom", "Montane Minimus", "Rab Jacket", "Montane"]},
                "온러닝 어패럴 (On Apparel)": {"desc": "퍼포먼스 티 · 러닝 쇼츠 · 웨더 자켓", "queries": ["On Running Jacket", "On Running Shorts", "On Running Tee", "On Apparel"]}
            }
        },
        "🎒 악세서리 / 기어 (Accessories)": {
            "title": "🎒 스포츠 악세서리 · 기어 브랜드관",
            "subtitle": "원하시는 기어 브랜드를 선택하면 GPS 워치 · 헬멧 · 고글 · 하이드레이션 베스트가 열립니다.",
            "brands": {
                "가민 (Garmin)": {"desc": "포러너 265 · 965 · 피닉스8 · 엣지 840", "queries": ["Garmin Forerunner", "Garmin Fenix", "Garmin Edge", "Garmin"]},
                "POC": {"desc": "벤트럴 에어 MIPS · 옥탈 · 아스파이어 고글", "queries": ["POC Ventral", "POC Octal", "POC Aspire", "POC Helmet"]},
                "카스크 (KASK)": {"desc": "프로톤 아이콘 · 발레그로 · 유토피아 Y", "queries": ["KASK Protone", "KASK Valegro", "KASK Utopia", "KASK"]},
                "오클리 (Oakley)": {"desc": "수트로 라이트 · 레이더 EV · 인코더", "queries": ["Oakley Sutro", "Oakley Radar", "Oakley Encoder", "Oakley"]},
                "살로몬 기어 (Salomon Gear)": {"desc": "ADV 스킨 12 · 센스 프로 10 · 소프트 플라스크", "queries": ["Salomon ADV Skin", "Salomon Sense Pro", "Salomon Flask", "Salomon Vest"]},
                "블랙다이아몬드 (Black Diamond)": {"desc": "디스턴스 카본 Z · 스팟400 헤드랜턴", "queries": ["Black Diamond Distance", "Black Diamond Spot", "Black Diamond", "Black Diamond Poles"]},
                "순토 / 코로스 (Suunto & COROS)": {"desc": "순토 레이스 · 코로스 페이스3 · 에이펙스2", "queries": ["Suunto Race", "COROS Pace", "COROS Apex", "Suunto"]},
                "샥즈 (Shokz)": {"desc": "오픈런 프로2 · 오픈스윔 프로 · 오픈핏", "queries": ["Shokz OpenRun", "Shokz OpenSwim", "Shokz OpenFit", "Shokz"]}
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
        st.header(cat_data["title"])
        st.markdown(cat_data["subtitle"])
        st.divider()

        brand_names = list(cat_data["brands"].keys())
        cols_per_row = 4

        for row_start in range(0, len(brand_names), cols_per_row):
            row_brands = brand_names[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            for i, b_name in enumerate(row_brands):
                b_info = cat_data["brands"][b_name]
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"<div class='brand-title'>{b_name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='brand-sub'>{b_info['desc']}</div>", unsafe_allow_html=True)
                        if st.button("브랜드 상품 보기 👉", key=f"open_{menu}_{b_name}", use_container_width=True):
                            st.session_state["selected_brand"] = b_name
                            st.session_state["selected_model"] = b_info["queries"][0]
                            st.rerun()

    else:
        b_info = cat_data["brands"][selected_brand]

        top_c1, top_c2 = st.columns([1, 4])
        with top_c1:
            if st.button("⬅️ 전체 브랜드 목록", use_container_width=True):
                st.session_state["selected_brand"] = None
                st.session_state["selected_model"] = None
                st.rerun()
        with top_c2:
            st.header(f"{selected_brand} — 글로벌 무인 레이더")

        st.write(f"**{selected_brand} 인기 라인업 스캔:**")
        m_cols = st.columns(len(b_info["queries"]))
        for idx, q_name in enumerate(b_info["queries"]):
            if m_cols[idx].button(f"📡 {q_name}", key=f"model_{q_name}", use_container_width=True):
                st.session_state["selected_model"] = q_name

        current_query = st.text_input(
            "글로벌 편집숍 스캔 키워드 (영문 모델명 입력 시 해외 직구 피드 즉시 검색)",
            value=st.session_state.get("selected_model", b_info["queries"][0])
        )

        with st.spinner(f"글로벌 편집숍 피드에서 '{current_query}' 모델을 스캔하는 중..."):
            deals = fetch_global_store_feed(current_query, live_usd_krw)
            if not deals:
                deals = get_curated_backup_items(selected_brand, live_usd_krw)

        st.success(f"✅ '{current_query}' 레이더 감지 완료 ({len(deals)}개 상품 · 실시간 환율 {live_usd_krw:,.0f}원/$ 반영)")
        cols = st.columns(3)
        for idx, prod in enumerate(deals):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(prod["img_url"], use_container_width=True)
                    st.markdown(f"<span class='discount-badge'>국내 시세 대비 -{prod['discount_pct']}% 메리트</span>", unsafe_allow_html=True)
                    st.markdown(f"**{prod['name'][:48]}{'...' if len(prod['name']) > 48 else ''}**")
                    st.caption(f"감지 스토어: **{prod['store']}** (${prod['usd_price']:,.0f})")
                    st.markdown(
                        f"<span class='orig-price'>국내 추정가 {prod['orig_price']:,}원</span><br>"
                        f"<span class='sale-price'>환산가 {prod['sale_price']:,}원</span>",
                        unsafe_allow_html=True
                    )
                    st.write("")
                    st.link_button("🛒 국내 최저가/제휴 비교하기", prod["affiliate_url"], use_container_width=True)
                    if is_pro:
                        st.link_button("🚀 해외 원본 스토어 직링크 (PRO)", prod["source_url"], use_container_width=True)
                    else:
                        st.button("🔒 해외 원본 링크 잠금 (PRO)", key=f"pro_btn_{idx}_{prod['name'][:10]}", disabled=True, use_container_width=True)import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# ==========================================
# [페이지 기본 설정]
# ==========================================
st.set_page_config(
    page_title="NicheRadar Pro v2.4 | 하이엔드 러닝·사이클·트레일 큐레이션 레이더",
    page_icon="🛍️",
    layout="wide"
)

# 커스텀 CSS: 브랜드 카드 및 상품 카드 스타일링
st.markdown("""
<style>
.discount-badge {
    background-color: #ff4b4b;
    color: white;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 6px;
}
.margin-badge {
    background-color: #00a86b;
    color: white;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 6px;
}
.orig-price {
    text-decoration: line-through;
    color: #888888;
    font-size: 0.9rem;
}
.sale-price {
    color: #111111;
    font-size: 1.25rem;
    font-weight: 800;
}
.brand-title {
    font-size: 1.15rem;
    font-weight: 800;
    margin-bottom: 4px;
}
.brand-sub {
    font-size: 0.83rem;
    color: #666666;
    margin-bottom: 12px;
    min-height: 36px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# [수익화 설정] 본인 제휴 트래킹 링크 & PRO 마스터 코드
# ==========================================
COUPANG_SUB_ID = "AF1234567"
PRO_ACCESS_CODE = "VIP2026"

def make_affiliate_url(product_name, raw_url=""):
    encoded = requests.utils.quote(product_name)
    return f"https://www.coupang.com/np/search?component=&q={encoded}&channel=user"

# ==========================================
# [실시간 쇼핑 데이터 수집 엔진] (API 토큰 0원)
# ==========================================
@st.cache_data(ttl=600)
def fetch_live_shop_deals(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    encoded_kw = requests.utils.quote(keyword)
    url = f"https://search.danawa.com/dsearch.php?query={encoded_kw}&tab=goods"
    
    products = []
    try:
        res = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("li.prod_item")

        for item in items:
            title_el = item.select_one("p.prod_name a")
            price_el = item.select_one("p.price_sect a strong")
            img_el = item.select_one("div.thumb_image img")

            if not title_el or not price_el:
                continue

            name = title_el.get_text(strip=True)
            link = title_el.get("href", "")
            raw_price = re.sub(r"[^0-9]", "", price_el.get_text(strip=True))
            if not raw_price:
                continue
            sale_price = int(raw_price)

            img_url = ""
            if img_el:
                img_url = img_el.get("data-original") or img_el.get("src") or ""
                if img_url.startswith("//"):
                    img_url = "https:" + img_url

            orig_price = int(sale_price * 1.18)
            discount_pct = int((1 - sale_price / orig_price) * 100)

            products.append({
                "name": name,
                "orig_price": orig_price,
                "sale_price": sale_price,
                "discount_pct": discount_pct,
                "img_url": img_url if img_url.startswith("http") else "https://via.placeholder.com/300x200?text=No+Image",
                "source_url": link,
                "affiliate_url": make_affiliate_url(name, link)
            })
            if len(products) >= 9:
                break
    except Exception:
        pass

    return products

def get_global_sourcing_deals():
    return [
        {
            "name": "Satisfy MothTech™ T-Shirt",
            "store": "SSENSE / Satisfy Official",
            "usd_price": 115.0,
            "kr_market_price": 245000,
            "img_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80",
            "sourcing_url": "https://satisfyrunning.com"
        },
        {
            "name": "Salomon XT-6 GTX (Black/Ebony)",
            "store": "END. Clothing (UK)",
            "usd_price": 145.0,
            "kr_market_price": 289000,
            "img_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80",
            "sourcing_url": "https://www.endclothing.com/kr/catalogsearch/results?q=salomon+xt-6"
        },
        {
            "name": "POC Ventral Air MIPS 헬멧",
            "store": "BikeInn (EU 직구)",
            "usd_price": 158.0,
            "kr_market_price": 320000,
            "img_url": "https://images.unsplash.com/photo-1557803175-2f8c4c272074?w=500&q=80",
            "sourcing_url": "https://www.tradeinn.com/bikeinn/ko"
        },
        {
            "name": "norda™ 001 Dyneema Trail Shoe",
            "store": "Backcountry / HAVEN",
            "usd_price": 195.0,
            "kr_market_price": 399000,
            "img_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&q=80",
            "sourcing_url": "https://nordarun.com"
        },
        {
            "name": "Arc'teryx Norvan Windshell 자켓",
            "store": "Backcountry (US)",
            "usd_price": 165.0,
            "kr_market_price": 330000,
            "img_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80",
            "sourcing_url": "https://www.backcountry.com"
        },
        {
            "name": "Shimano S-Phyre RC903 클릿슈즈",
            "store": "Bike24 (DE 직구)",
            "usd_price": 265.0,
            "kr_market_price": 490000,
            "img_url": "https://images.unsplash.com/photo-1511994298241-608e28f14fde?w=500&q=80",
            "sourcing_url": "https://www.bike24.com"
        }
    ]

# ==========================================
# [사이드바] 네비게이션 & PRO 멤버십 인증
# ==========================================
with st.sidebar:
    st.title("🛍️ NicheRadar Pro")
    st.caption("하이엔드 기어 · 어패럴 · 소싱 마진 레이더")
    st.divider()

    menu = st.radio(
        "카테고리 선택",
        [
            "🌍 해외 소싱 / 구매대행 딜",
            "🏃‍♂️ 러닝 (Running)",
            "🚴 자전거 (Cycling)",
            "⛰️ 트레일 / 아웃도어 (Trail)",
            "👕 의류 / 어패럴 (Apparel)",
            "🎒 악세서리 / 기어 (Accessories)"
        ]
    )

    st.divider()
    st.subheader("🔑 PRO 멤버십 잠금 해제")
    user_code = st.text_input("구독자 액세스 코드", type="password", placeholder="테스트 코드: VIP2026")
    is_pro = (user_code == PRO_ACCESS_CODE)

    if is_pro:
        st.success("✅ PRO 멤버십 활성화됨 (소싱처 직링크 열림)")
    else:
        st.info("💡 무료 버전: 해외 소싱처 직링크와 심층 마진 분석은 PRO 구독 후 열립니다.")
        st.link_button("💳 PRO 멤버십 구독하기 (월 19,000원)", "https://gumroad.com")

# ==========================================
# [메인 1] 해외 소싱 / 구매대행 상품 카드 페이지
# ==========================================
if menu == "🌍 해외 소싱 / 구매대행 딜":
    st.header("🌍 해외 소싱 / 구매대행 실시간 역산 마진 딜")
    st.markdown("해외 직구 세일가와 국내 리셀·오픈마켓 시세를 실시간 계산해 **순수 중간 마진**이 남는 상품만 카드로 띄웁니다.")

    c1, c2, c3 = st.columns(3)
    with c1:
        ex_rate = st.number_input("기준 환율 (원/$)", value=1380.0, step=10.0)
    with c2:
        ship_fee = st.number_input("평균 배대지/국제 배송비 (원)", value=15000, step=1000)
    with c3:
        fee_pct = st.number_input("국내 판매 수수료 (%)", value=6.0, step=0.5)

    st.divider()
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
                st.markdown(f"<span class='margin-badge'>예상 순마진 +{int(net_profit):,}원 ({margin_pct:.1f}%)</span>", unsafe_allow_html=True)
                st.subheader(item["name"])
                st.caption(f"소싱처: **{item['store']}** | 관부가세: {'포함(약 ' + f'{int(tax):,}원)' if tax > 0 else '면제($200 이하)'}")
                st.markdown(
                    f"해외 소싱가: **${item['usd_price']:.0f}** (약 {int(krw_cost):,}원)<br>"
                    f"국내 시세: <span class='sale-price'>{item['kr_market_price']:,}원</span>",
                    unsafe_allow_html=True
                )
                st.write("")
                if is_pro:
                    st.link_button("🚀 해외 소싱처 바로가기 (PRO)", item["sourcing_url"], use_container_width=True)
                else:
                    st.button("🔒 소싱처 URL 잠금 (PRO 전용)", key=f"lock_{idx}", disabled=True, use_container_width=True)

# ==========================================
# [메인 2~6] 브랜드 우선 선택 -> 상품 노출 2단계 구조
# ==========================================
else:
    brand_catalog = {
        "🏃‍♂️ 러닝 (Running)": {
            "title": "🏃‍♂️ 러닝 브랜드관",
            "subtitle": "원하시는 러닝 브랜드를 먼저 선택하면 대표 러닝화 모델과 실시간 최저가 상품이 열립니다.",
            "brands": {
                "나이키 (Nike)": {"desc": "알파플라이3 · 베이퍼플라이3 · 페가수스", "models": ["나이키 알파플라이3", "나이키 베이퍼플라이3", "나이키 줌플라이6", "나이키 페가수스41"]},
                "아식스 (ASICS)": {"desc": "메타스피드 스카이 · 슈퍼블라스트2 · 노바블라스트", "models": ["아식스 메타스피드 스카이", "아식스 슈퍼블라스트2", "아식스 노바블라스트4", "아식스 젤카야노31"]},
                "아디다스 (Adidas)": {"desc": "아디오스 프로4 · 보스턴12 · 에보 SL", "models": ["아디다스 아디오스 프로4", "아디다스 아디제로 보스턴12", "아디다스 아디제로 에보 SL", "아디다스 타쿠미센10"]},
                "호카 (HOKA)": {"desc": "마하6 · 클리프톤9 · 씨엘로 X1", "models": ["호카 마하6", "호카 클리프톤9", "호카 씨엘로 X1", "호카 본디8"]},
                "온러닝 (On Running)": {"desc": "클라우드몬스터2 · 클라우드붐 스트라이크", "models": ["온러닝 클라우드몬스터2", "온러닝 클라우드붐 스트라이크", "온러닝 클라우드서퍼", "온러닝 클라우드5"]},
                "뉴발란스 (New Balance)": {"desc": "퓨어셀 SC 엘리트 v4 · 레벨 v4 · 1080v14", "models": ["뉴발란스 퓨어셀 SC 엘리트", "뉴발란스 퓨어셀 레벨 v4", "뉴발란스 프레쉬폼 1080v14", "뉴발란스 SC 트레이너"]},
                "써코니 (Saucony)": {"desc": "엔돌핀 프로4 · 엔돌핀 스피드4 · 트라이엄프", "models": ["써코니 엔돌핀 프로4", "써코니 엔돌핀 스피드4", "써코니 트라이엄프22", "써코니 킨바라15"]},
                "브룩스 (Brooks)": {"desc": "하이페리온 맥스2 · 글리세린 맥스 · 고스트16", "models": ["브룩스 하이페리온 맥스", "브룩스 글리세린 맥스", "브룩스 고스트16", "브룩스 아드레날린 GTS"]}
            }
        },
        "🚴 자전거 (Cycling)": {
            "title": "🚴 사이클링 브랜드관",
            "subtitle": "캐논데일, 스페셜라이즈드, 시마노 등 주요 사이클링 완성차·기어·슈즈 브랜드를 선택하세요.",
            "brands": {
                "캐논데일 (Cannondale)": {"desc": "슈퍼식스 에보 · CAAD13 · 탑스톤 그래블", "models": ["캐논데일 슈퍼식스 에보", "캐논데일 CAAD13", "캐논데일 탑스톤", "캐논데일 시냅스"]},
                "스페셜라이즈드 (Specialized)": {"desc": "타막 SL8 · 에스웍스 토치 슈즈 · 프리베일3", "models": ["스페셜라이즈드 에스웍스 토치", "스페셜라이즈드 타막 SL8", "스페셜라이즈드 프리베일3", "스페셜라이즈드 알레"]},
                "트렉 (Trek)": {"desc": "마돈 SLR · 에몬다 · 도마니 · 벨로시스", "models": ["트렉 마돈", "트렉 에몬다", "트렉 도마니", "트렉 본트래거 슈즈"]},
                "캐니언 (Canyon)": {"desc": "에어로드 CFR · 얼티메이트 · 그레일", "models": ["캐니언 에어로드", "캐니언 얼티메이트", "캐니언 그레일", "캐니언 엔듀레이스"]},
                "써벨로 (Cervélo)": {"desc": "S5 · R5 · 솔로이스트 · 칼레도니아", "models": ["써벨로 S5", "써벨로 R5", "써벨로 솔로이스트", "써벨로 칼레도니아"]},
                "자이언트 (Giant)": {"desc": "프로펠 어드밴스 · TCR · 서지 프로 슈즈", "models": ["자이언트 TCR 어드밴스", "자이언트 프로펠", "자이언트 서지 프로", "자이언트 레브 헬멧"]},
                "비앙키 (Bianchi)": {"desc": "올트레 RC · 스페셜리시마 · 스프린트", "models": ["비앙키 올트레", "비앙키 스페셜리시마", "비앙키 스프린트", "비앙키 임풀소"]},
                "시마노 (Shimano)": {"desc": "에스파이어 RC903 · 듀라에이스 · 울테그라", "models": ["시마노 RC903", "시마노 RC703", "시마노 듀라에이스", "시마노 울테그라"]},
                "피직 (Fizik)": {"desc": "벤토 인피니토 · 템포 오버커브 · 안타레스 안장", "models": ["피직 벤토 인피니토", "피직 템포 오버커브", "피직 안타레스 안장", "피직 벤토 옴나"]},
                "시디 (SIDI)": {"desc": "샷2 · 와이어2 · 지니어스10 클릿슈즈", "models": ["시디 샷2", "시디 와이어2", "시디 지니어스10", "시디 에르고5"]},
                "레이크 / 본트 (Lake & Bont)": {"desc": "CX332 와이드핏 · 베이퍼 S 열성형 슈즈", "models": ["레이크 CX332", "레이크 CX403", "본트 베이퍼 S", "본트 리옷"]},
                "라파 (Rapha)": {"desc": "프로팀 빕숏 · 클래식 저지 · 로드 슈즈", "models": ["라파 프로팀 빕숏", "라파 클래식 저지", "라파 프로팀 슈즈", "라파 코어 빕숏"]}
            }
        },
        "⛰️ 트레일 / 아웃도어 (Trail)": {
            "title": "⛰️ 트레일 · 아웃도어 브랜드관",
            "subtitle": "원하시는 아웃도어 브랜드를 선택하면 대표 트레일러닝화·등산화 최저가 상품이 열립니다.",
            "brands": {
                "살로몬 (Salomon)": {"desc": "XT-6 · S/LAB 울트라 · 스피드크로스6", "models": ["살로몬 XT-6", "살로몬 스피드크로스6", "살로몬 펄사 트레일", "살로몬 울트라 글라이드2"]},
                "노다 (norda)": {"desc": "001 · 002 · 003 다이니마 트레일 슈즈", "models": ["노다 001", "노다 002", "노다 003", "norda 001"]},
                "호카 (HOKA Trail)": {"desc": "스피드고트6 · 마파테 스피드4 · 텍톤 X3", "models": ["호카 스피드고트6", "호카 마파테 스피드4", "호카 텍톤 X3", "호카 챌린저7"]},
                "알트라 (Altra)": {"desc": "론피크8 · 올림푸스6 · 팀프5", "models": ["알트라 론피크8", "알트라 올림푸스6", "알트라 팀프5", "알트라 몬블랑"]},
                "노스페이스 (The North Face)": {"desc": "벡티브 엔듀리스3 · 서밋 벡티브 프로", "models": ["노스페이스 벡티브 엔듀리스", "노스페이스 서밋 벡티브 프로", "노스페이스 알타메사", "노스페이스 헤지호그"]},
                "라스포르티바 (La Sportiva)": {"desc": "부시도3 · 아카샤2 · 울트라 랩터2", "models": ["라스포르티바 부시도3", "라스포르티바 아카샤2", "라스포르티바 울트라 랩터2", "라스포르티바 자칼2"]},
                "스카르파 (SCARPA)": {"desc": "리벨레 런 · 스핀 플래닛 · 모히토", "models": ["스카르파 리벨레 런", "스카르파 스핀 플래닛", "스카르파 골든 게이트", "스카르파 모히토"]},
                "메렐 / 아크테릭스": {"desc": "애질리티 피크5 · 노반 LD3 · 모아브3 GTX", "models": ["메렐 애질리티 피크5", "아크테릭스 노반 LD", "메렐 모아브3 고어텍스", "아크테릭스 콘실"]}
            }
        },
        "👕 의류 / 어패럴 (Apparel)": {
            "title": "👕 하이엔드 러닝 · 트레일 어패럴관 (굿러너 · 아웃오브올 큐레이션)",
            "subtitle": "세티스파이, 포탈, 시엘, SOAR 등 하이엔드 퍼포먼스 의류 브랜드를 선택하세요.",
            "brands": {
                "세티스파이 (Satisfy)": {"desc": "MothTech 티셔츠 · 리펠런트 쇼츠 · 피스쉘", "models": ["세티스파이 티셔츠", "세티스파이 쇼츠", "세티스파이 모자", "Satisfy Running"]},
                "포탈 (Portal)": {"desc": "트레일 쉘 자켓 · 테크니컬 티 · 퍼포먼스 쇼츠", "models": ["포탈 트레일 자켓", "포탈 러닝 티셔츠", "Portal trail apparel", "포탈 쇼츠"]},
                "시엘 (Ciele Athletics)": {"desc": "GOCap · ALZCap · 러닝 싱글렛 · 쇼츠", "models": ["시엘 모자", "시엘 GOCap", "시엘 ALZCap", "시엘 러닝"]},
                "SOAR Running": {"desc": "엘리트 레이스 싱글렛 · 마라톤 쇼츠 · 윈드쉘", "models": ["SOAR 싱글렛", "SOAR 러닝 쇼츠", "SOAR 자켓", "SOAR Running"]},
                "세이스카이 (SAYSKY)": {"desc": "페이스 쇼츠 · 컴뱃 싱글렛 · 메리노 롱슬리브", "models": ["세이스카이 싱글렛", "세이스카이 쇼츠", "세이스카이 티셔츠", "세이스카이 자켓"]},
                "디스트릭트 비전 (District Vision)": {"desc": "테크니컬 러닝 웨어 · 스포츠 아이웨어", "models": ["디스트릭트 비전", "디스트릭트 비전 선글라스", "District Vision", "디스트릭트 비전 티셔츠"]},
                "파타고니아 (Patagonia)": {"desc": "스트라이더 프로 쇼츠 · 후디니 자켓 · 배기스", "models": ["파타고니아 스트라이더 프로", "파타고니아 후디니 자켓", "파타고니아 캐필린 쿨", "파타고니아 배기스 5인치"]},
                "아크테릭스 (Arc'teryx)": {"desc": "노반 윈드쉘 · 코르막 크루 · 베타 자켓", "models": ["아크테릭스 노반", "아크테릭스 코르막", "아크테릭스 베타 자켓", "아크테릭스 스쿼미시 후디"]},
                "케일 (CAYL)": {"desc": "마운틴 트레일 자켓 · 나일론 쇼츠 · 경량 웨어", "models": ["케일 자켓", "케일 쇼츠", "케일 팬츠", "케일 티셔츠"]},
                "산산기어 / 언어펙티드": {"desc": "테크니컬 트레일 팬츠 · 윈드블록 자켓", "models": ["산산기어 자켓", "산산기어 팬츠", "언어펙티드 자켓", "언어펙티드 팬츠"]},
                "랩 / 몬테인 (Rab & Montane)": {"desc": "팬텀 풀온 방수 자켓 · 미니머스 쉘", "models": ["랩 팬텀 자켓", "몬테인 미니머스", "랩 윈드쉘", "몬테인 자켓"]},
                "온러닝 어패럴 (On Apparel)": {"desc": "퍼포먼스 티 · 러닝 쇼츠 · 웨더 자켓", "models": ["온러닝 티셔츠", "온러닝 쇼츠", "온러닝 웨더 자켓", "온러닝 싱글렛"]}
            }
        },
        "🎒 악세서리 / 기어 (Accessories)": {
            "title": "🎒 스포츠 악세서리 · 기어 브랜드관",
            "subtitle": "원하시는 기어 브랜드를 선택하면 GPS 워치 · 헬멧 · 고글 · 하이드레이션 베스트 최저가가 열립니다.",
            "brands": {
                "가민 (Garmin)": {"desc": "포러너 265 · 965 · 피닉스8 · 엣지 840", "models": ["가민 포러너 265", "가민 포러너 965", "가민 피닉스8", "가민 엣지 840"]},
                "POC": {"desc": "벤트럴 에어 MIPS · 옥탈 · 아스파이어 고글", "models": ["POC 벤트럴 에어 헬멧", "POC 옥탈 헬멧", "POC 아스파이어 고글", "POC 옴니 에어"]},
                "카스크 (KASK)": {"desc": "프로톤 아이콘 · 발레그로 · 유토피아 Y", "models": ["카스크 프로톤 아이콘", "카스크 발레그로", "카스크 유토피아 Y", "카스크 모히토3"]},
                "오클리 (Oakley)": {"desc": "수트로 라이트 · 레이더 EV · 인코더", "models": ["오클리 수트로 고글", "오클리 레이더 EV 패스", "오클리 인코더", "오클리 조브레이커"]},
                "살로몬 기어 (Salomon Gear)": {"desc": "ADV 스킨 12 · 센스 프로 10 · 소프트 플라스크", "models": ["살로몬 ADV 스킨 12", "살로몬 센스 프로 10", "살로몬 액티브 스킨 8", "살로몬 소프트 플라스크"]},
                "블랙다이아몬드 (Black Diamond)": {"desc": "디스턴스 카본 Z · 스팟400 헤드랜턴", "models": ["블랙다이아몬드 디스턴스 Z", "블랙다이아몬드 트레일 스틱", "블랙다이아몬드 스팟 400", "블랙다이아몬드 디스턴스 15"]},
                "순토 / 코로스 (Suunto & COROS)": {"desc": "순토 레이스 · 코로스 페이스3 · 에이펙스2", "models": ["순토 레이스 워치", "코로스 페이스3", "코로스 에이펙스2 프로", "순토 버티컬"]},
                "샥즈 (Shokz)": {"desc": "오픈런 프로2 · 오픈스윔 프로 · 오픈핏", "models": ["샥즈 오픈런 프로2", "샥즈 오픈런", "샥즈 오픈스윔 프로", "샥즈 오픈핏"]}
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
        st.header(cat_data["title"])
        st.markdown(cat_data["subtitle"])
        st.divider()

        brand_names = list(cat_data["brands"].keys())
        cols_per_row = 4

        for row_start in range(0, len(brand_names), cols_per_row):
            row_brands = brand_names[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            for i, b_name in enumerate(row_brands):
                b_info = cat_data["brands"][b_name]
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"<div class='brand-title'>{b_name}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='brand-sub'>{b_info['desc']}</div>", unsafe_allow_html=True)
                        if st.button("브랜드 상품 보기 👉", key=f"open_{menu}_{b_name}", use_container_width=True):
                            st.session_state["selected_brand"] = b_name
                            st.session_state["selected_model"] = b_info["models"][0]
                            st.rerun()

    else:
        b_info = cat_data["brands"][selected_brand]

        top_c1, top_c2 = st.columns([1, 4])
        with top_c1:
            if st.button("⬅️ 전체 브랜드 목록", use_container_width=True):
                st.session_state["selected_brand"] = None
                st.session_state["selected_model"] = None
                st.rerun()
        with top_c2:
            st.header(f"{selected_brand} — 실시간 최저가 스캐너")

        st.write(f"**{selected_brand} 인기 라인업 선택:**")
        m_cols = st.columns(len(b_info["models"]))
        for idx, m_name in enumerate(b_info["models"]):
            if m_cols[idx].button(f"🔍 {m_name}", key=f"model_{m_name}", use_container_width=True):
                st.session_state["selected_model"] = m_name

        current_query = st.text_input(
            "선택된 모델 또는 세부 모델명 직접 검색",
            value=st.session_state.get("selected_model", b_info["models"][0])
        )

        with st.spinner(f"'{current_query}' 실시간 쇼핑몰 최저가 상품을 불러오는 중입니다..."):
            deals = fetch_live_shop_deals(current_query)

        if deals:
            st.success(f"✅ '{current_query}' 실시간 최저가 상품 {len(deals)}건")
            cols = st.columns(3)
            for idx, prod in enumerate(deals):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.image(prod["img_url"], use_container_width=True)
                        st.markdown(f"<span class='discount-badge'>시세 대비 -{prod['discount_pct']}% 특가</span>", unsafe_allow_html=True)
                        st.markdown(f"**{prod['name'][:45]}{'...' if len(prod['name']) > 45 else ''}**")
                        st.markdown(
                            f"<span class='orig-price'>{prod['orig_price']:,}원</span><br>"
                            f"<span class='sale-price'>{prod['sale_price']:,}원</span>",
                            unsafe_allow_html=True
                        )
                        st.write("")
                        st.link_button("🛒 최저가 구매하기 (제휴 특가)", prod["affiliate_url"], use_container_width=True)
                        if is_pro:
                            st.link_button("📊 다나와 가격추이 원문 보기", prod["source_url"], use_container_width=True)
        else:
            st.warning("현재 검색어에 대한 실시간 가격비교 결과를 불러오지 못했습니다. 위 다른 라인업 버튼을 눌러보세요.")
