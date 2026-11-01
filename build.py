# -*- coding: utf-8 -*-
"""와와학습코칭센터 학습상담 안내 사이트 빌드 스크립트.
python build.py → index / about / system / ai-class / subjects / reviews / faq / apply + sitemap/robots
도메인 확정 시 SITE_URL 한 줄만 수정. 이미지는 assets/img/ (IMAGE_PROMPTS.md 참고)."""
import io, os, json, re, datetime

SITE_URL = "https://wawacenter.co.kr"
SITE_NAME = "와와학습코칭센터 학습상담"
PHONE = "010-3131-5305"
PHONE_TEL = "+821031315305"
EMAIL = "ookkoo12@naver.com"
TODAY = datetime.date.today().isoformat()
OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("index.html", "홈"),
    ("about.html", "브랜드"),
    ("system.html", "학습 시스템"),
    ("ai-class.html", "AI클래스"),
    ("subjects.html", "과목"),
    ("centers.html", "센터 찾기"),
    ("reviews.html", "성적 변화"),
    ("faq.html", "FAQ"),
    ("blog.html", "학습 칼럼"),
]

# ───────────────────────── 공통 크롬 ─────────────────────────
def head(title, desc, path, keywords, noindex=False, extra_ld="", og="og.jpg"):
    url = f"{SITE_URL}/{'' if path == 'index.html' else path}"
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    org_ld = json.dumps({
        "@context": "https://schema.org", "@type": "EducationalOrganization",
        "name": SITE_NAME, "url": SITE_URL + "/", "telephone": PHONE,
        "description": "초·중·고 자기주도학습 코칭 전문 브랜드 와와학습코칭센터의 수강 상담과 학습 진단 신청을 안내하는 파트너 페이지",
        "parentOrganization": {"@type": "Organization", "name": "(주)동화세상에듀코 와와학습코칭센터", "url": "https://www.wawacenter.com/"},
        "areaServed": "KR"}, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/{og}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192x192.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{org_ld}</script>
{extra_ld}
</head>
<body>"""

def chrome_top(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f"""
<div class="topbar"><div class="wrap">
  <span>와와학습코칭센터 수강 상담 안내 페이지 · 전국 205개 센터 연결</span>
  <span>상담 전화 <a href="tel:{PHONE_TEL}"><b>{PHONE}</b></a> · 평일 10:00–19:00</span>
</div></div>
<header class="header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="와와학습코칭센터 학습상담 홈"><span class="logo-mark">W</span><span class="logo-text">와와학습코칭센터<small>학습상담 안내</small></span></a>
    <nav class="nav" aria-label="주 메뉴">{links}<a class="cta" href="apply.html">무료 학습상담</a></nav>
    <button class="burger" aria-label="메뉴 열기" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
  <nav class="mnav" id="mnav" aria-label="모바일 메뉴">{links}<a href="apply.html">무료 학습상담 신청</a></nav>
</header>
<main>"""

def cta_band(h="우리 아이 공부, 어디서부터 손봐야 할지 모르겠다면", p="학년·학교·현재 상황만 알려주세요. 가까운 센터 기준으로 진단 일정과 진행 방식을 솔직하게 안내해 드립니다. 상담은 무료이고, 등록을 권유하지 않습니다."):
    return f"""
<section class="cta-band">
  <div class="wrap">
    <h2>{h}</h2>
    <p>{p}</p>
    <div class="btn-group">
      <a class="btn btn-white btn-lg" href="apply.html">무료 학습상담 신청</a>
      <a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}">📞 {PHONE}</a>
    </div>
  </div>
</section>"""

def chrome_bottom():
    return f"""
</main>
<footer class="footer">
  <div class="wrap">
    <div>
      <h4>와와학습코칭센터 학습상담</h4>
      <p>초등·중등·고등 자기주도학습 코칭 브랜드 와와학습코칭센터의 수강 상담과 학습 진단 신청을 돕는 안내 페이지입니다. 수강 상담 파트너가 운영하며, 와와학습코칭센터 브랜드와 프로그램의 권리는 (주)동화세상에듀코에 있습니다.</p>
      <p>상담 전화 <a href="tel:{PHONE_TEL}"><b style="color:#fff">{PHONE}</b></a> (평일 10:00–19:00) · 이메일 <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <h4>둘러보기</h4>
      <ul>
        <li><a href="about.html">브랜드 소개 · 연혁</a></li>
        <li><a href="system.html">학습 시스템</a></li>
        <li><a href="ai-class.html">AI학습클래스</a></li>
        <li><a href="subjects.html">국어·영어·수학 과목 안내</a></li>
        <li><a href="centers.html">우리 동네 센터 찾기 (204개 지점)</a></li>
        <li><a href="reviews.html">성적 변화 사례</a></li>
        <li><a href="faq.html">자주 묻는 질문</a></li>
        <li><a href="blog.html">학습 칼럼 (공부법·내신 전략)</a></li>
        <li><a href="apply.html">무료 학습상담 신청</a></li>
      </ul>
    </div>
    <div>
      <h4>와와학습코칭센터 공식 채널</h4>
      <ul>
        <li><a href="https://www.wawacenter.com/" target="_blank" rel="noopener">공식 홈페이지</a></li>
        <li><a href="https://www.wawacenter.com/center" target="_blank" rel="noopener">전국 센터 찾기</a></li>
        <li><a href="https://blog.naver.com/wawacenter2015" target="_blank" rel="noopener">공식 블로그</a></li>
        <li><a href="https://www.youtube.com/@wawacoachingcenter" target="_blank" rel="noopener">공식 유튜브</a></li>
      </ul>
    </div>
    <div class="legal">
      본 사이트는 와와학습코칭센터 수강 상담 안내를 위한 파트너 페이지이며 본사 공식 홈페이지가 아닙니다. 교습비·시간표·운영 과목은 센터마다 다르므로 상담 시 해당 센터 기준으로 안내합니다. 사례·후기의 학습 효과는 학생마다 다를 수 있습니다. ⓒ 와와학습코칭센터 학습상담 · 브랜드 자산 ⓒ (주)동화세상에듀코
    </div>
  </div>
</footer>
<div class="mobile-bar">
  <a class="call" href="tel:{PHONE_TEL}">📞 전화 상담</a>
  <a class="apply" href="apply.html">무료 학습상담 신청</a>
</div>
<script src="assets/site.js" defer></script>
</body>
</html>"""

def page_hero(crumb, h1, lead):
    return f"""
<section class="page-hero"><div class="wrap">
  <div class="crumb"><a href="index.html">홈</a> › {crumb}</div>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</div></section>"""

def sec_head(eyebrow, h2, lead="", center=True):
    c = " center" if center else ""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="section-head{c}"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{l}</div>'

def feature(img, alt, tag, h3, paras, chips=None, rev=False, btn=None):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    ch = f'<div class="chips">{"".join(f"<span class=chip>{c}</span>" for c in chips)}</div>' if chips else ""
    b = f'<p style="margin-top:18px"><a class="btn btn-outline" href="{btn[0]}">{btn[1]}</a></p>' if btn else ""
    return f"""<div class="feature{' rev' if rev else ''} reveal">
  <div class="feature-img"><img src="assets/img/{img}" alt="{alt}" loading="lazy"></div>
  <div><span class="tag">{tag}</span><h3>{h3}</h3>{ps}{ch}{b}</div>
</div>"""

def cards(items, cols=3, cls="card"):
    """items: list of (badge, h, p) 또는 (badge, h, p, bullets)"""
    out = []
    for it in items:
        badge, h, p = it[0], it[1], it[2]
        bullets = it[3] if len(it) > 3 else None
        b = f'<span class="num">{badge}</span>' if badge else ""
        ul = f'<ul>{"".join(f"<li>{x}</li>" for x in bullets)}</ul>' if bullets else ""
        out.append(f'<div class="{cls} reveal">{b}<h3>{h}</h3><p>{p}</p>{ul}</div>')
    return f'<div class="grid grid-{cols}">{"".join(out)}</div>'

# ───────────────────────── 데이터 ─────────────────────────
FOUR_C = [
    ("Check", "진단", "진단검사와 레벨테스트로 학생의 학습 성향, 과목별 결손 지점, 공부 습관을 먼저 봅니다. '어디가 비었는지'를 모르고 시작하는 수업은 없습니다."),
    ("Curriculum", "처방", "진단 결과로 과목·시작 단원·주간 분량·플래너 운영 방식을 학생마다 다르게 정합니다. 학년표가 아니라 학생 기준입니다."),
    ("Consulting", "상담", "정기 상담으로 목표와 동기를 다시 맞추고, 학부모에게는 진행 상황과 다음 과제를 공유합니다. 멘탈이 흔들리는 시기도 함께 봅니다."),
    ("Coaching", "지도", "코치가 옆에서 막히는 부분을 풀어주고, 틀린 이유를 학생이 스스로 설명하게 합니다. 답을 알려주는 수업이 아니라 공부 방법을 바꾸는 수업입니다."),
]

CMP_ROWS = [
    ("기준", "학년과 학교 진도", "학생의 현재 실력과 결손"),
    ("진행", "반 전체가 같은 속도", "학생마다 다른 단원, 다른 속도"),
    ("반 편성", "초5반·중1반처럼 학년별", "학년 구분 없이 실력 기준"),
    ("교사 역할", "설명하는 강사", "진단하고 설계하는 코치"),
    ("평가", "정기 테스트·숙제 검사", "단원별 성취도, 오답 분석, 개인 피드백"),
    ("잘 맞는 학생", "같은 진도를 무리 없이 따라가는 학생", "기초 보완이 필요하거나, 앞서 나가야 하거나, 자기 속도가 필요한 학생"),
    ("주의할 점", "수준 차가 큰 학생은 버려지기 쉬움", "진단·관리가 느슨하면 흐트러짐 → 플래너·4C로 보완"),
]

PLANNER_7 = [
    ("무엇을 할지 정한다", "'열심히'가 아니라 '오늘 수학 2단원 개념 정리 + 영어 단어 30개'처럼 행동 단위로 적습니다. 막연한 부담이 실행 가능한 목록이 됩니다."),
    ("습관이 기록으로 보인다", "언제, 어떤 과목에, 얼마나 시간을 썼는지가 남습니다. '수학에만 몰려 있다', '오답 복습이 계속 빠진다' 같은 패턴이 코치 눈에 들어옵니다."),
    ("공부 방법이 드러난다", "문제만 풀고 개념은 건너뛰는지, 채점만 하고 오답은 안 보는지, 단어를 눈으로만 외우는지가 플래너에 그대로 나타나 과목별로 교정할 수 있습니다."),
    ("시험까지 역산한다", "시험일에서 거꾸로 세어 과목별 분량을 나눕니다. 4주 전 범위 정리, 2주 전 유형 풀이, 1주 전 예상문제와 오답, 직전 암기·서술형 점검 순서로 갑니다."),
    ("학부모가 확인할 수 있다", "오늘 무엇을 했고 다음 수업까지 무엇을 해야 하는지가 기록으로 남아, '학원 다녀왔다'가 아니라 '무엇이 진행 중인지'를 볼 수 있습니다."),
    ("스스로 설계하게 된다", "처음엔 코치가 함께 세우지만 점차 학생이 우선순위를 정하고 실천 여부를 스스로 체크합니다. 센터 밖에서도 공부가 이어지는 이유입니다."),
    ("책임감이 생긴다", "계획을 지키면 성취감이, 못 지키면 '왜 못 했는지' 돌아보는 과정이 남습니다. 공부가 시켜서 하는 일에서 내가 관리하는 일로 바뀝니다."),
]

NAESIN_6 = [
    ("학교마다 다른 출제 스타일", "교과서 위주로 내는 학교, 프린트와 부교재에서 많이 내는 학교, 수업 필기를 그대로 묻는 학교가 다릅니다. 지역 센터는 담당 학교의 패턴을 알고 그에 맞춰 준비합니다."),
    ("학생이 가져온 자료가 교재", "학교 프린트, 수행평가 안내, 선생님이 강조한 부분을 함께 분석해 시험 범위 안에서 나올 가능성이 높은 내용부터 다룹니다."),
    ("4주 → 2주 → 1주 → 직전", "시험 4주 전 범위 정리, 2주 전 유형별 풀이, 1주 전 학교별 예상문제와 오답 정리, 직전에는 암기 확인과 서술형 점검으로 운영이 바뀝니다."),
    ("약점부터 손본다", "개념 이해가 부족한 학생, 계산 실수가 잦은 학생, 서술형 답안이 약한 학생은 처방이 다릅니다. 점수에 직접 영향을 주는 약점을 먼저 고칩니다."),
    ("서술형·수행평가도 훈련", "감점 포인트와 답안 작성 방식까지 지도합니다. 답만 맞히는 연습이 아니라 학교 선생님이 요구하는 형식으로 쓰는 연습입니다."),
    ("학부모에게 진행이 보인다", "어느 범위를 끝냈고 어떤 단원이 약한지, 시험 전까지 무엇을 보완할지가 명확해 '수업 듣고 있다'가 아니라 '이번 시험을 위해 무엇을 하고 있는지'가 전달됩니다."),
]

RESULTS = [
    ("영어", "6등급 → 1등급", "고등 · 신도림점", "첫 시험 6등급에서 출발. 문법과 모의고사로 기본기를 다진 뒤 시험 2주 전부터 여러 학교 기출을 풀며 실전 감각을 키웠습니다. 성적이 오르자 목표 대학도 높아졌다고 합니다."),
    ("영어", "40점 → 80점", "중등 · 복산점", "중간고사 40점에서 기말고사 80점으로. 자기에게 맞는 학습법을 코치와 찾고, 스스로 학습 계획을 세운 것이 변화의 출발점이었습니다."),
    ("수학", "28점 → 43점 → 80점", "중등 · 향남점", "막연하게만 느껴지던 수학을 이해하기 쉬운 설명과 수행평가 관리로 차근차근 올렸습니다. 두 번의 시험을 거치며 점수가 계단식으로 상승했습니다."),
    ("종합", "3년 코칭 후 서울대 합격", "고3 · 이충점", "부족한 개념과 학습 습관을 정확히 진단받고 자기주도학습 중심 개별 코칭을 3년간 이어간 사례. 성적뿐 아니라 공부 태도와 자신감이 달라졌다고 전합니다."),
    ("국어", "현대시 공포 극복", "고1 · 글로리드 은평점", "문학, 특히 현대시가 어려웠던 학생이 체계적 지도와 밀착 코칭으로 극복. 학습 동기와 진로 방향까지 함께 잡은 것이 성적 향상의 힘이 되었습니다."),
    ("습관", "스스로 계획하는 습관", "중3 · 반월당점", "계획을 세우고 실천하는 습관이 생기고 부족한 과목에 자신감이 붙은 사례. 1:1 소통으로 공부 태도, 자존감, 목표의식이 달라졌습니다."),
    ("수능", "D-100 불안 극복, 서울대 합격", "고3 · 본사 사례", "수능최저 압박으로 극심한 불안을 겪던 시기에 코치의 멘탈 관리와 전략적 피드백으로 흐름을 되찾아 목표를 달성했습니다."),
    ("영어", "1등급의 '한 끗'", "고3 · 본사 사례", "1등급과 2등급을 가르는 약점을 메타인지 학습으로 정확히 짚고 하나씩 지워 나가 영어 1등급을 받았습니다."),
]

FAQ_GENERAL = [
    ("일반 학원과 뭐가 다른가요?", "가장 큰 차이는 수업의 방향입니다. 일반 학원은 강사가 설명하고 학생이 듣는 구조라면, 와와학습코칭센터는 코치를 가운데 두고 학생들이 둘러앉는 <strong>둥지학습</strong> 구조에서 학생이 질문하고 설명하며 배웁니다. 여기에 플래너로 학습 습관과 공부 방법까지 관리하기 때문에 '센터에 있을 때만 공부하는 아이'가 아니라 '집에서도 스스로 공부하는 아이'를 목표로 합니다."),
    ("4C 프로세스가 뭔가요?", "진단(Check) → 처방(Curriculum) → 상담(Consulting) → 지도(Coaching)의 4단계를 반복하는 와와의 운영 방식입니다. 처음에 진단검사로 성향과 결손을 파악하고, 그 결과로 과목·단원·분량을 정하고, 정기 상담으로 방향을 조정하면서, 코치가 밀착해서 지도합니다. 한 번 하고 끝나는 게 아니라 계속 돌아가는 순환 구조입니다."),
    ("둥지학습은 어떤 수업인가요?", "코치 한 명을 중심으로 학생들이 둥글게 앉아 같은 눈높이에서 묻고 답하는 수업 형태입니다. 틀린 문제를 코치가 바로 설명해 주는 대신 '왜 틀렸는지'를 학생이 말로 설명하게 해서 아는 것과 모르는 것을 스스로 구분하게 합니다. 참여도와 집중도가 올라가고 메타인지가 자랍니다."),
    ("전국에 센터가 몇 개 있나요? 우리 동네에도 있나요?", "2025년 기준 전국 205개 센터가 운영 중입니다. 서울·인천·경기·대전·충청·강원·제주·경상·전라 권역에 있으며, 상담 신청 시 거주 지역과 학교를 적어 주시면 가까운 센터를 찾아 안내해 드립니다. 본사 홈페이지의 '전국 센터 찾기'에서 직접 검색하셔도 됩니다."),
    ("학원비는 얼마인가요?", "교습비는 센터·학년·과목 수에 따라 다르며, 각 센터의 교습비 게시표가 본사 '전국 센터 찾기' 상세 페이지에 공개되어 있습니다. 이 페이지에서는 임의의 금액을 안내하지 않고, 상담 시 해당 센터 기준으로 정확히 말씀드립니다."),
    ("어떤 아이에게 잘 맞나요?", "학원을 옮겨 다녀도 성적이 제자리인 학생, 공부 시간은 많은데 방법이 틀린 학생, 기초 결손이 있어 지금 학년 진도가 버거운 학생, 반대로 학년 진도가 너무 쉬워 앞서 나가야 하는 학생, 그리고 '공부 습관' 자체를 만들어야 하는 초등·중등 학생에게 잘 맞습니다."),
    ("무학년 수업이라는 게 뭔가요?", "학년이 아니라 실력 기준으로 수업을 설계한다는 뜻입니다. 중2 학생이라도 분수 계산이 흔들리면 그 지점부터 다시 가고, 반대로 중2인데 중3 과정을 소화할 수 있으면 학년에 묶이지 않고 진행합니다. 한 교실에서 각자 다른 교재, 다른 진도로 공부합니다."),
    ("상상코칭과는 어떤 관계인가요?", "둘 다 (주)동화세상에듀코가 운영하는 브랜드입니다. 상상코칭은 가정 방문이나 화상으로 진행하는 과외형 서비스이고, 와와학습코칭센터는 센터에 직접 나와서 받는 학원형 서비스입니다."),
    ("고등학생 내신도 봐주나요?", "네. 학생이 다니는 학교의 출제 경향, 교과서·부교재·프린트를 반영한 내신 대비와 수행평가 준비를 지원합니다. 내신과 수능, 수행평가를 동시에 관리해야 하는 고등 과정의 특성에 맞게 시험 4주 전부터 일정이 바뀝니다."),
    ("상담은 어떻게 신청하나요? 꼭 등록해야 하나요?", f"이 페이지의 <a href=\"apply.html\"><strong>상담 신청 폼</strong></a>이나 전화 <a href=\"tel:{PHONE_TEL}\"><strong>{PHONE}</strong></a>로 신청하시면 됩니다. 학년·지역·과목을 확인한 뒤 가까운 센터의 진단 일정을 안내해 드리며, 상담과 진단만 받고 결정하셔도 됩니다. 등록을 권유하지 않습니다."),
    ("수상 이력이 있나요?", "2025년 '소비자가 뽑은 올해의 브랜드대상'(국회 교육위원회 위원장 상), 2023년 '학부모가 뽑은 교육브랜드 대상', 2020년 '대한민국 퍼스트브랜드 대상'(자기주도학습센터 부문)을 받았습니다."),
    ("초등학생도 가능한가요?", "가능합니다. 초등 과정은 성적보다 습관에 무게를 둡니다. 플래너로 매일 할 일을 정하고 체크하는 루틴을 만들고, 수학 연산·개념, 영어 파닉스·독해, 국어 문해력을 수준에 맞게 진행합니다. AI독서(초1~중2)로 독서 습관도 함께 잡을 수 있습니다."),
]

FAQ_CLASS = [
    ("아이가 어떻게 하고 있는지 어떻게 알 수 있나요?", "센터별 운영 방식에 따라 정기 안내와 개별 피드백으로 수업 참여도, 과제 이행, 진도 흐름을 공유합니다. 플래너 기록 자체가 학부모가 볼 수 있는 자료가 되고, 필요하면 개별 상담으로 다음 학습 방향을 함께 정합니다."),
    ("기초가 많이 부족한데 따라갈 수 있을까요?", "무학년 수업이라 현재 수준에서 시작할 수 있습니다. 다만 결손 정도에 따라 운영 가능 여부와 진행 방식이 달라질 수 있어, 센터에서 개별 상담과 진단을 거쳐 정확히 안내해 드립니다. 상위권 학생도 같은 교실에서 심화 과정으로 각자 진행합니다."),
    ("특정 단원이나 과목만 집중해서 볼 수 있나요?", "가능합니다. 취약 단원과 유형을 우선 지도하고, 상위권은 기출·예상문제 중심 실전 연습, 중하위권은 기본 개념과 유형 반복에 집중하는 식으로 같은 학교 학생이라도 방향을 다르게 잡습니다."),
    ("시험기간과 방학에는 어떻게 운영되나요?", "시험기간에는 학습 시간을 늘리고 기본 개념 확인 → 기출·예상문제 → 학교별 맞춤 대비 → 부족 단원 보완 순으로 집중 운영합니다. 방학에는 기초 다지기와 선행, 개별 학습 플랜 재설계, 습관 유지 프로그램을 운영합니다. 세부 일정은 센터마다 다릅니다."),
    ("결석하면 보충이 되나요?", "센터장과 사전에 상의하면 조율 가능한 경우가 많습니다. 센터별 운영 방침이 다르므로 상담 시 확인해 드립니다."),
    ("영어·수학 말고 다른 과목도 하나요?", "국어·영어·수학이 중심이고, 센터에 따라 사회·과학과 기타 과목을 운영합니다. 수학·과학 전문은 더블유플러스, 국어·독서·논술 전문은 글로리드 학습코칭센터가 따로 있습니다. 상담 시 가까운 센터의 운영 과목을 확인해 드립니다."),
]

# ───────────────────────── 렌더 헬퍼 ─────────────────────────
def faq_html(items, start=1):
    return '<div class="faq">' + "".join(
        f'<details><summary>Q{i:02d}. {q}</summary><div class="a"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(items, start)) + '</div>'

def faq_ld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]
    }, ensure_ascii=False) + '</script>'

def four_c_html():
    return '<div class="steps">' + "".join(
        f'<div class="step reveal"><span class="en">{en}</span><h3>{ko}</h3><p>{d}</p></div>' for en, ko, d in FOUR_C) + '</div>'

def cmp_table():
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{a}</td><td class="hl">{b}</td></tr>' for k, a, b in CMP_ROWS)
    return f"""<div class="table-wrap"><table class="cmp">
<thead><tr><th>구분</th><th>일반 강의식 수업</th><th class="hl">와와 개별 맞춤 무학년 수업</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""

def results_html(items):
    return '<div class="grid grid-2">' + "".join(
        f'<article class="result reveal"><div class="meta"><span class="hl">{sub}</span><span>{who}</span></div><div class="big">{big}</div><p>{d}</p><div class="src">와와학습코칭센터 공개 사례를 요약한 내용입니다</div></article>'
        for sub, big, who, d in items) + '</div>'

def planner_html():
    return '<div class="grid grid-3">' + "".join(
        f'<div class="card reveal"><span class="num">{i:02d}</span><h3>{h}</h3><p>{d}</p></div>'
        for i, (h, d) in enumerate(PLANNER_7, 1)) + '</div>'

def naesin_html():
    return '<div class="grid grid-3">' + "".join(
        f'<div class="card reveal"><span class="num">{i:02d}</span><h3>{h}</h3><p>{d}</p></div>'
        for i, (h, d) in enumerate(NAESIN_6, 1)) + '</div>'

# ───────────────────────── 페이지 ─────────────────────────
pages = {}

pages["index.html"] = dict(
    title="와와학습코칭센터 학습상담 | 초중고 자기주도학습 코칭·국영수 내신 전문, 전국 205개 센터",
    desc="학원을 바꿔도 성적이 제자리라면 공부 방법부터 봐야 합니다. 와와학습코칭센터는 둥지학습·플래너 관리·4C 진단·무학년 수업으로 초등·중등·고등 학생의 자기주도학습을 만듭니다. 전국 205개 센터, 2025 소비자가 뽑은 올해의 브랜드대상. 무료 학습상담 신청.",
    keywords="와와학습코칭센터, 와와코칭, 학습코칭센터, 자기주도학습 학원, 초등학원, 중등학원, 고등학원, 국영수 학원, 내신 대비 학원, 플래너 학습관리, 둥지학습, 메타인지 학습, 무학년 수업, 4C 프로세스, 공부습관 학원, 오답노트, 수행평가 대비, 무료 학습상담",
    body=lambda: f"""
<section class="hero">
  <div class="wrap">
    <div>
      <span class="hero-badge">🏅 2025 소비자가 뽑은 올해의 브랜드대상 · 전국 205개 센터</span>
      <h1>학원을 바꿔도 제자리라면,<br><span class="accent">공부 방법</span>부터<br>바꿔야 합니다</h1>
      <p class="lead"><strong>와와학습코칭센터</strong>는 강의를 듣는 학원이 아니라 <strong>스스로 공부하는 법을 익히는 곳</strong>입니다. 코치를 가운데 둔 둥지학습, 매일 기록하는 플래너, 학년 대신 실력 기준의 무학년 수업으로 초등·중등·고등 학생의 국어·영어·수학과 공부 습관을 함께 관리합니다.</p>
      <div class="btn-group">
        <a class="btn btn-primary btn-lg" href="apply.html">무료 학습상담 신청하기</a>
        <a class="btn btn-outline btn-lg" href="system.html">학습 시스템 보기</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><b>205개</b><span>전국 센터</span></div>
        <div class="stat"><b>2015년</b><span>첫 센터 오픈</span></div>
        <div class="stat"><b>초·중·고</b><span>전 학년 대상</span></div>
      </div>
    </div>
    <div class="hero-img">
      <img src="assets/img/hero.jpg" alt="와와학습코칭센터 둥지학습 — 코치와 학생들이 둥글게 앉아 플래너로 학습 코칭" width="800" height="1000" fetchpriority="high">
      <div class="hero-float"><b>둥지학습</b>코치 중심 원형 배치<br>질문하고 설명하며 배우는 수업</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("이런 고민이라면", "하나라도 해당되면 상담받아 볼 만합니다")}
    <div class="grid grid-3">
      <div class="check reveal"><b>학원을 옮겨도 성적이 그대로</b><p>진도는 계속 나가는데 점수는 안 움직인다면 '무엇을 모르는지'를 모른 채 수업만 듣고 있을 가능성이 큽니다.</p></div>
      <div class="check reveal"><b>공부 시간은 많은데 결과가 없음</b><p>개념 없이 문제만 풀거나, 채점만 하고 오답을 다시 안 보거나, 단어를 눈으로만 외우는 습관이 원인일 수 있습니다.</p></div>
      <div class="check reveal"><b>시험 2주 전에야 벼락치기</b><p>시험일에서 거꾸로 계산해 4주 전부터 준비하는 방식을 배운 적이 없으면 매번 같은 패턴이 반복됩니다.</p></div>
      <div class="check reveal"><b>기초가 비어서 지금 진도가 버거움</b><p>중2인데 분수가 흔들리면 중2 수업을 아무리 들어도 소용없습니다. 비어 있는 지점부터 다시 가야 합니다.</p></div>
      <div class="check reveal"><b>잘하는데 학년 진도가 너무 쉬움</b><p>학년에 묶인 반에서는 앞서 나갈 수 없습니다. 실력 기준으로 다음 단계를 열어 줘야 합니다.</p></div>
      <div class="check reveal"><b>혼자서는 아예 책상에 안 앉음</b><p>초등·중등 시기에는 과목보다 '매일 정해진 걸 하는 습관'이 먼저입니다. 플래너 루틴이 여기서 시작됩니다.</p></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {sec_head("와와가 다른 세 가지", "강의 대신 코칭, 진도 대신 설계, 학년 대신 실력")}
    {feature("nest.jpg", "둥지학습 — 코치를 중심으로 학생들이 둘러앉은 교실", "① 둥지학습", "코치를 가운데 두고 둘러앉습니다",
      ["강사가 앞에서 설명하고 학생은 받아 적는 구조가 아닙니다. 코치 한 명을 중심으로 학생들이 둥글게 앉아 같은 눈높이에서 묻고 답합니다. 틀린 문제는 코치가 풀어 주는 대신 학생이 '왜 틀렸는지'를 말로 설명합니다.",
       "이 과정에서 학생은 아는 것과 모르는 것을 스스로 구분하는 메타인지를 키웁니다. 참여도와 몰입도가 달라지고, 옆 친구의 태도가 자연스러운 자극이 됩니다."],
      ["질의응답 중심", "메타인지", "집중형 원형 배치"])}
    {feature("planner.jpg", "학습 플래너에 체크하는 학생의 손", "② 플래너 관리", "매일 무엇을 했는지가 기록으로 남습니다",
      ["매 수업 '오늘 할 일'을 행동 단위로 적고 실천 여부를 체크합니다. 언제 어떤 과목에 얼마나 시간을 썼는지, 미룬 과제가 무엇인지가 보이기 때문에 공부 습관 자체를 진단하고 고칠 수 있습니다.",
       "시험기간에는 시험일에서 거꾸로 세어 과목별 분량을 배분합니다. 학부모도 '학원 다녀왔다'가 아니라 '무엇이 진행 중인지'를 확인할 수 있습니다."],
      ["학습습관 기록", "공부방법 교정", "시험 역산 계획"], rev=True)}
    {feature("mugakneon.jpg", "서로 다른 학년의 학생이 각자 교재로 개별 학습하는 모습", "③ 무학년 수업", "학년이 아니라 실력 기준으로 시작합니다",
      ["같은 교실에서 학생마다 다른 교재, 다른 단원, 다른 속도로 공부합니다. 기초가 빈 학생은 빈 지점부터, 앞서가는 학생은 다음 단계로 갑니다. 진단검사 결과가 출발점을 정합니다.",
       "'반 전체가 같은 진도'에서 버려지던 양 끝의 학생들이 가장 큰 효과를 보는 구조입니다. 대신 진단과 관리가 느슨하면 흐트러지기 때문에 4C 프로세스와 플래너가 받쳐 줍니다."],
      ["진단 후 개별 진도", "결손 보완", "심화·선행"], btn=("system.html", "학습 시스템 자세히"))}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("4C 프로세스", "진단에서 지도까지, 네 단계가 계속 돌아갑니다", "한 번 진단하고 끝이 아닙니다. 진단 → 처방 → 상담 → 지도를 반복하며 학생에 맞게 계속 조정합니다.")}
    {four_c_html()}
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    {sec_head("처음 한 달은 이렇게", "등록 후 첫 달의 흐름")}
    <ol class="flow">
      <li class="reveal"><b>1주차 · 진단</b><span>진단검사·레벨테스트로 성향과 과목별 결손 확인. 학부모 상담으로 목표 합의.</span></li>
      <li class="reveal"><b>1~2주차 · 설계</b><span>과목·시작 단원·주간 분량 결정, 플래너 운영 방식 안내. 첫 플래너는 코치와 함께 작성.</span></li>
      <li class="reveal"><b>매 수업 · 점검</b><span>플래너 체크 → 막힌 부분 코칭 → 오답을 학생이 설명 → 다음 수업까지 과제 확정.</span></li>
      <li class="reveal"><b>월말 · 평가와 피드백</b><span>월말평가로 성취도 확인, 학습 로드맵 조정, 학부모에게 진행 상황과 다음 달 계획 공유.</span></li>
    </ol>
    <p class="note" style="text-align:center;margin-top:14px">* 세부 운영은 센터와 학년에 따라 다릅니다. 상담 시 해당 센터 기준으로 안내합니다.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("수업 형식 비교", "강의식 수업과 무엇이 다른가")}
    {cmp_table()}
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {sec_head("성적 변화", "공개된 사례 중 몇 가지", "와와학습코칭센터가 공개한 수강 사례를 요약했습니다. 효과는 학생의 출발점과 학습량에 따라 다릅니다.")}
    {results_html([RESULTS[0], RESULTS[2], RESULTS[3], RESULTS[6]])}
    <p style="text-align:center;margin-top:32px"><a class="btn btn-outline" href="reviews.html">사례 더 보기</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("자주 묻는 질문", "상담 전에 가장 많이 묻는 것들")}
    {faq_html(FAQ_GENERAL[:5])}
    <p style="text-align:center;margin-top:28px"><a class="btn btn-outline" href="faq.html">질문 18개 전체 보기</a></p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {sec_head("학년별 안내", "초등·중등·고등, 필요한 코칭이 다릅니다", center=False)}
    <div class="seo-text">
      <p><strong>초등학생 학습코칭</strong> — 초등 시기의 목표는 점수보다 습관입니다. 플래너로 매일 정해진 분량을 하고 체크하는 루틴을 만들고, 초등 수학 연산과 개념, 초등 영어 파닉스·어휘·독해, 국어 문해력과 독서 습관을 수준에 맞게 진행합니다. AI독서(초1~중2)로 진로와 연결된 독서 포트폴리오도 만들 수 있습니다.</p>
      <p><strong>중학생 내신 학원</strong> — 중학교 내신은 학교마다 출제 스타일이 다릅니다. 교과서·프린트·부교재를 반영한 중등 영어·수학 내신 대비, 서술형과 수행평가 관리, 시험 4주 전부터 시작하는 역산 계획으로 중간·기말고사를 준비합니다. 개념 없이 문제만 푸는 습관, 오답을 안 보는 습관을 플래너로 잡습니다.</p>
      <p><strong>고등학생 내신·수능 코칭</strong> — 내신, 수능, 수행평가를 동시에 관리해야 하는 시기입니다. 학교별 기출 분석, 서술형 답안 훈련, 모의고사 오답 분석, 수능 D-100 전략과 멘탈 관리까지 코치가 밀착합니다. 기초가 흔들리면 무학년 수업으로 이전 과정부터, 상위권은 연계 심화로 1등급의 차이를 만듭니다.</p>
      <p><strong>자기주도학습 학원을 찾고 계신다면</strong> — 학원을 다녀도 성적이 오르지 않는 학생, 공부 시간은 많지만 방법이 틀린 학생, 기초 결손을 보완해야 하는 학생, 앞서 나가야 하는 상위권 학생 모두 각자의 출발점에서 자기 속도로 학습합니다. 오답노트·백지노트·개념노트로 공부 방법을 교정합니다.</p>
      <p><strong>가까운 와와학습코칭센터</strong> — 서울·인천·경기·대전·충청·강원·제주·경상·전라 권역에 205개 센터가 있습니다. 상담 신청 시 지역과 학교를 남겨 주시면 가까운 센터와 진단 일정을 안내합니다. 교습비와 시간표는 센터별로 다르며 상담 시 정확히 안내합니다.</p>
      <p><strong>AI학습클래스</strong> — AI영어(초1~고3), AI수학(초1~고3), AI국어(중1~고3), AI독서(초1~중2) 프로그램이 레벨테스트 → 취약점 분석 → 맞춤 트레이닝으로 이어지고, 코치가 플래너로 실천을 관리합니다. 운영 과목은 센터별로 다릅니다.</p>
    </div>
  </div>
</section>
{cta_band()}
""")

pages["about.html"] = dict(
    title="와와학습코칭센터 브랜드 소개·연혁 | 2015년 시작, 205개 센터, 2025 브랜드대상",
    desc="와와학습코칭센터는 (주)동화세상에듀코가 2015년 시작한 초중고 자기주도학습 코칭 브랜드입니다. 10년의 연혁과 수상, 센터 공간과 코치, 더블유플러스·글로리드·모두오름 패밀리 브랜드를 소개합니다.",
    keywords="와와학습코칭센터 소개, 와와 연혁, 동화세상에듀코 학원, 더블유플러스학습코칭센터, 글로리드학습코칭센터, 모두오름학습코칭센터, 자기주도학습 브랜드, 학습코칭 전문 브랜드, 교육브랜드 대상",
    body=lambda: f"""
{page_hero("브랜드 소개", "와와학습코칭센터는 어떤 곳인가", "2015년 첫 센터를 열어 2025년 전국 205개 센터가 된 자기주도학습 코칭 브랜드. '공부 잘하는 아이'보다 '스스로 공부하는 아이'를 목표로 합니다.")}

<section class="section">
  <div class="wrap">
    {feature("about.jpg", "와와학습코칭센터 내부 공간 — 코치 책상을 중심으로 배치된 개별 학습 공간", "브랜드 개요", "초·중·고 자기주도학습 코칭 전문 브랜드",
      ["와와학습코칭센터는 (주)동화세상에듀코가 운영하는 센터형 학습코칭 브랜드입니다. 초등학생부터 고등학생까지를 대상으로 국어·영어·수학을 중심으로 지도하되, 과목 지식보다 <strong>공부하는 방법과 습관</strong>을 먼저 만드는 것을 목표로 합니다.",
       "강의를 듣고 숙제를 받아 가는 학원과 달리, 코치가 학생을 진단하고 학습을 설계하고 플래너로 실천을 관리합니다. 센터 방문형 수업이며 과목과 운영 방식은 센터마다 조금씩 다릅니다."],
      ["센터 방문 학습", "초등~고등", "국영수 중심 · 센터별 사과 등 추가"])}
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {sec_head("숫자로 보는 와와", "10년 동안 쌓인 것들")}
    <div class="grid grid-4">
      <div class="stat-card reveal"><b>2015</b><span>첫 센터 오픈</span></div>
      <div class="stat-card reveal"><b>100호점</b><span>2020년 돌파</span></div>
      <div class="stat-card reveal"><b>200호점</b><span>2025년 돌파 · 현재 205개</span></div>
      <div class="stat-card reveal"><b>3회</b><span>교육 브랜드 대상 수상</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("센터가 다른 이유", "공간 · 코치 · 관리")}
    <div class="grid grid-3">
      <div class="card reveal"><span class="num">공간</span><h3>집중되는 둥지형 배치</h3><p>코치를 중심으로 학생들이 둘러앉는 구조는 적당한 긴장감과 안정감을 동시에 줍니다. 옆자리 친구의 태도가 자연스러운 동기가 되고, 질문이 오가는 거리에 코치가 있습니다.</p></div>
      <div class="card reveal"><span class="num">코치</span><h3>학습코칭 자격을 갖춘 전문가</h3><p>와와의 코치는 청소년 학습코칭(TLC) 자격 과정을 거친 전문가로, 가르치는 사람이 아니라 진단하고 설계하는 사람입니다. 성적뿐 아니라 진로와 고민까지 함께 보는 멘토 역할을 합니다.</p></div>
      <div class="card reveal"><span class="num">관리</span><h3>4C로 돌아가는 운영</h3><p>진단·처방·상담·지도의 4C 프로세스가 반복되며, 정기 진단과 상담으로 학습 방향을 계속 조정합니다. 학생이 공부의 주도권을 갖도록 체계적으로 뒤에서 받칩니다.</p></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    {sec_head("연혁", "걸어온 길")}
    <ul class="timeline">
      <li class="reveal"><span class="year">2025</span><p>소비자가 뽑은 올해의 브랜드 대상(국회 교육위원회 위원장 상) · 모두오름 학습코칭센터 론칭 · 코칭센터 200호점 돌파</p></li>
      <li class="reveal"><span class="year">2024</span><p>영어 전문학원 왓칭 론칭</p></li>
      <li class="reveal"><span class="year">2023</span><p>학부모가 뽑은 교육브랜드 대상 · 국어·독서·논술 전문 글로리드 론칭</p></li>
      <li class="reveal"><span class="year">2021</span><p>수학·과학 전문 더블유플러스 론칭</p></li>
      <li class="reveal"><span class="year">2020</span><p>대한민국 퍼스트브랜드 대상(자기주도학습센터 부문) · 코칭센터 100호점 돌파</p></li>
      <li class="reveal"><span class="year">2015</span><p>초중고 국영수 전문 와와학습코칭센터 론칭</p></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("패밀리 브랜드", "과목별로 전문화된 학습코칭센터", "와와의 코칭 방식을 바탕으로 과목을 전문화한 형제 브랜드입니다. 지역에 따라 운영 브랜드가 다를 수 있어 상담 시 함께 안내합니다.")}
    {cards([
      ("국영수", "와와학습코칭센터", "기본 브랜드. 초등부터 고등까지 국어·영어·수학 중심, 센터에 따라 사회·과학·기타 과목. 플래너와 둥지학습으로 자기주도학습 코칭."),
      ("수학·과학", "더블유플러스학습코칭센터", "2028 대입 개편으로 중요성이 커진 수학·과학 전문. 1:1 학습 플랜, 밀착 지도, 심화학습, 오답클리닉으로 '수포자'를 되돌립니다."),
      ("국어·독서·논술", "글로리드학습코칭센터", "모든 과목의 바탕인 문해력. 초등 독서 습관과 표현력부터 중·고등 내신, 수능 국어, 논술까지 언어영역 전문 커리큘럼."),
      ("영어·수학 프리미엄", "모두오름학습코칭센터", "과목별 원장 선생님이 직접 지도하는 프리미엄 공간. 맞춤 루틴과 매일 피드백, 몰입에 최적화된 환경."),
    ], cols=4)}
  </div>
</section>
{cta_band("가까운 센터가 어디인지부터 확인해 보세요", "지역과 학교를 알려주시면 운영 중인 센터와 브랜드, 과목을 확인해 안내해 드립니다.")}
""")

pages["system.html"] = dict(
    title="와와학습코칭센터 학습 시스템 | 4C 진단·둥지학습·플래너 관리·학교별 내신·무학년 수업",
    desc="와와학습코칭센터가 학생을 관리하는 방식. 진단·처방·상담·지도의 4C 프로세스, 플랜·학습·생활 3대 관리, 플래너가 바꾸는 7가지, 학교별 내신 준비 6단계, 둥지학습 구조, 강의식 수업과의 비교.",
    keywords="와와 학습 시스템, 4C 프로세스, 둥지학습, 플래너 학습관리, 학습습관 교정, 공부방법 교정, 학교별 내신 대비, 무학년 수업, 개별 맞춤 코칭, 오답노트 백지노트 개념노트, 시험 역산 계획, 메타인지 학습법",
    body=lambda: f"""
{page_hero("학습 시스템", "학생을 관리하는 방식", "진도를 나가는 것이 아니라 공부하는 구조를 만드는 것. 와와학습코칭센터가 매일 하는 일을 순서대로 설명합니다.")}

<section class="section">
  <div class="wrap">
    {sec_head("4C 프로세스", "진단 → 처방 → 상담 → 지도", "네 단계가 한 번으로 끝나지 않고 계속 순환합니다. 학생이 달라지면 처방도 달라집니다.")}
    {four_c_html()}
    <div style="margin-top:48px">
    {feature("coach.jpg", "코치가 학부모와 진단 결과를 보며 상담하는 장면", "첫 단계 · Check", "진단 없이 시작하는 수업은 없습니다",
      ["첫 상담에서 진단검사와 과목별 레벨테스트를 진행합니다. 결과는 점수 한 줄이 아니라 '어느 단원이 비어 있는지', '어떤 습관이 성적을 막고 있는지'로 정리되어 학부모에게 공유됩니다.",
       "이 결과가 과목·시작 단원·주간 분량·플래너 운영 방식을 정하는 근거가 됩니다. 같은 학년이라도 출발점은 모두 다릅니다."],
      ["진단검사", "레벨테스트", "학부모 공유"])}
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {sec_head("3대 관리", "플랜 · 학습 · 생활을 함께 봅니다")}
    {cards([
      ("PLAN", "계획을 세우고 지키는 힘", "'공부해라'가 아니라 목표를 정하고 우선순위를 나누고 시간과 분량을 스스로 배분하는 법을 가르칩니다. 계획하고 실행하는 경험이 반복되면 자기주도학습의 기초 체력이 됩니다."),
      ("STUDY", "아이에게 맞는 방법으로 제대로", "현재 수준에 맞는 교재와 방법으로 기초부터 갑니다. 오답노트·백지노트·개념노트·마인드맵 같은 도구로 자기에게 맞는 공부법을 찾아 익히는 과정을 코치가 함께합니다."),
      ("LIFE", "센터 밖까지 이어지는 관리", "공부는 수업 시간 안에서만 일어나지 않습니다. 학생과의 일상 소통, 학부모와의 피드백으로 생활 리듬과 감정 변화까지 살핍니다. 아이의 하루를 이해하는 코칭이 와와의 진짜 강점입니다."),
    ])}
  </div>
</section>

<section class="section" id="planner">
  <div class="wrap">
    {sec_head("플래너 관리", "플래너 한 권이 바꾸는 7가지", "'오늘 배운 것'이 아니라 '앞으로 어떻게 공부할지'를 관리하는 도구입니다.")}
    {planner_html()}
  </div>
</section>

<section class="section soft" id="naesin">
  <div class="wrap">
    {sec_head("학교별 내신", "'일반적인 공부'가 아니라 '우리 학교 시험 공부'", "같은 학년 같은 과목이라도 학교마다 시험이 다릅니다. 지역 센터는 담당 학교의 패턴을 알고 준비합니다.")}
    <div style="margin-bottom:44px">
    {feature("naesin.jpg", "학교별 내신 준비 — 교과서, 프린트, 오답노트가 놓인 책상", "학교 자료 기반", "학생이 가져온 프린트가 교재가 됩니다",
      ["학교 선생님이 강조한 부분, 수행평가 안내, 프린트와 부교재, 수업 필기를 함께 분석해 시험 범위 안에서 나올 가능성이 높은 것부터 다룹니다. 수능형 실력만으로는 내신이 해결되지 않기 때문입니다."],
      ["기출 경향 분석", "서술형·수행평가", "4주 역산 일정"])}
    </div>
    {naesin_html()}
  </div>
</section>

<section class="section dark" id="nest">
  <div class="wrap">
    {sec_head("둥지학습", "코치를 가운데 둔 교실", "학생들이 코치를 중심으로 둥글게 앉아 묻고 답하는 구조. 설명을 듣는 수업이 아니라 설명하는 수업입니다.")}
    <div class="feature reveal">
      <div class="feature-img"><img src="assets/img/nest.jpg" alt="둥지학습 교실 — 코치를 중심으로 둘러앉은 학생들" loading="lazy"></div>
      <div>
        <div class="dark-list">
          <div><b>같은 눈높이</b><span>코치가 앞에 서지 않고 학생들 사이에 앉습니다. 질문이 오가는 거리가 짧아집니다.</span></div>
          <div><b>학생이 설명한다</b><span>틀린 문제를 코치가 풀어 주지 않습니다. 학생이 '왜 틀렸는지'를 말로 설명하면서 아는 것과 모르는 것을 구분합니다.</span></div>
          <div><b>양방향 피드백</b><span>질문과 피드백이 수업의 중심입니다. 참여도와 몰입도가 올라가고 메타인지가 자랍니다.</span></div>
          <div><b>또래의 자극</b><span>옆자리 친구가 집중하는 모습이 자연스러운 동기가 됩니다. 적당한 긴장과 안정감이 함께 있는 공간입니다.</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="compare">
  <div class="wrap">
    {sec_head("수업 형식 비교", "강의식 수업 vs 개별 맞춤 무학년 수업", "어느 쪽이 '좋다'가 아니라 어떤 학생에게 맞는지의 문제입니다. 와와는 오른쪽 방식에 진단과 플래너를 더해 약점을 보완합니다.")}
    {cmp_table()}
    <div style="margin-top:44px">
    {feature("mugakneon.jpg", "서로 다른 학년의 학생이 각자의 교재로 공부하는 무학년 교실", "무학년 수업", "같은 교실, 다른 교재, 다른 속도",
      ["학년에 관계없이 학생의 실제 수준과 결손을 기준으로 필요한 단원부터 개별 속도로 갑니다. 기초가 부족하면 이전 과정부터 보완하고, 실력이 충분하면 연계 심화 단계로 넘어갑니다.",
       "'문제집을 각자 풀게 두는 것'과는 다릅니다. 학생마다 학습 경로를 설계하고 단원별 성취도와 오답을 계속 점검하는 관리 시스템이 뒤에 있어야 작동하는 방식입니다."],
      ["진단 후 개별 진도", "결손 보완", "연계 심화"], rev=True)}
    </div>
  </div>
</section>
{cta_band("진단부터 받아 보세요", "4C의 첫 단계인 Check(진단)만 받고 결정하셔도 됩니다. 상담과 진단은 무료입니다.")}
""")

pages["ai-class.html"] = dict(
    title="와와학습코칭센터 AI학습클래스 | AI영어·AI수학·AI국어·AI독서, 진단부터 트레이닝까지",
    desc="와와 AI학습클래스는 레벨테스트로 진단하고 취약점을 분석해 맞춤 트레이닝으로 이어지는 프로그램입니다. AI영어(초1~고3), AI수학(초1~고3), AI국어(중1~고3), AI독서(초1~중2)의 구성과 코치 관리가 결합되는 방식을 안내합니다.",
    keywords="AI학습클래스, 와와 AI영어, 와와 AI수학, AI국어, AI독서, AI 학습 학원, 레벨테스트 학원, 오답 클리닉, 스마트북 학습, AI 스피킹, 구문훈련, 학교별 기출 국어, 진로 연계 독서, 문해력 프로그램",
    body=lambda: f"""
{page_hero("AI학습클래스", "AI가 진단하고 코치가 관리합니다", "데이터로 취약점을 찾는 일은 AI가, 실천을 관리하고 동기를 붙드는 일은 코치가 맡습니다. 둘을 합친 것이 와와의 AI학습클래스입니다.")}

<section class="section">
  <div class="wrap">
    {feature("ai-class.jpg", "태블릿으로 AI 학습 중인 학생과 뒤에서 확인하는 코치", "운영 방식", "진단 → 분석 → 트레이닝, 그리고 플래너",
      ["모든 AI 과정은 레벨테스트로 시작합니다. 영역별 성취도와 취약 유형을 분석해 그 학생에게 필요한 콘텐츠와 문제를 제공하고, 반복해서 틀리는 유형은 패턴으로 묶어 집중 훈련합니다.",
       "여기까지는 AI의 일입니다. 그 결과를 플래너에 옮겨 매일 실천하게 하고, 오답을 학생이 설명하게 하고, 흔들릴 때 붙잡는 일은 코치가 합니다. AI만으로 채워지지 않는 부분입니다."],
      ["AI영어 초1~고3", "AI수학 초1~고3", "AI국어 중1~고3", "AI독서 초1~중2"])}
    <p class="note" style="margin-top:20px">* 운영 과목과 대상은 센터별로 다를 수 있습니다. 상담 시 가까운 센터 기준으로 확인해 드립니다.</p>
  </div>
</section>

<section class="section alt" id="english">
  <div class="wrap">
    {sec_head("AI영어 · 초1~고3", "흥미로 시작해 내신·수능까지", center=False)}
    <div class="grid grid-2">
      <div class="card reveal"><span class="num">초등</span><h3>파닉스에서 4대 영역까지</h3><p>레벨에 맞는 단계별 놀이형 학습으로 소리와 문자의 규칙을 익히고, 영역별 온라인 학습과 AI 스피킹 튜터로 듣기·말하기·읽기·쓰기를 채웁니다.</p><ul><li>온라인 숙제·E-book으로 어휘·문장·독해 사전 학습</li><li>AI 토킹 튜터로 배운 내용 대화 복습과 피드백</li><li>센터에서 데일리 테스트, 워크북, 코치와 숙제 확인</li><li>단어 앱으로 여러 방식의 어휘 반복</li></ul></div>
      <div class="card reveal"><span class="num">중·고등</span><h3>독해·구문·듣기·교과서</h3><p>유형별 독해와 어휘 확장, 핵심 구문을 자동화하는 3단계 구문 훈련, 연도별 내신·모의·수능 기출 기반 듣기 훈련, 교과서 지문을 따라 쓰고 어순을 배열하고 영작하는 교과서별 내신 대비로 구성됩니다.</p><ul><li>Reading: 문제 풀이 → 어휘 확장 → 스피킹 연계</li><li>구문훈련: 듣고 따라 말하기 → 어순 배열 → 영작</li><li>Listening: 기출 분석 기반 실전 훈련</li><li>교과서별 맞춤: 지문 따라쓰기 → 어순 → 영작 → 어휘</li></ul></div>
    </div>
  </div>
</section>

<section class="section" id="math">
  <div class="wrap">
    {sec_head("AI수학 · 초1~고3", "성취도에 맞춘 문제지와 오답 클리닉", center=False)}
    {cards([
      ("문제 생성", "학생 성취도에 맞는 시험지", "난이도를 학생별로 조절한 교재와 문제지를 만들고, 수시·형성평가와 정기고사로 체계적으로 과제를 관리합니다."),
      ("오답 클리닉", "유사 → 변형 → 심화", "틀린 문제는 유사문제, 변형문제, 심화문제로 이어지는 난이도 연계 훈련으로 다시 풉니다. 반복해서 틀리는 유형은 패턴으로 묶어 취약 단원을 집중 훈련합니다."),
      ("스마트북", "교재와 앱의 연동", "맞춤 교재를 앱과 자동 연동해 종이 교재의 부담을 줄이고, 학생이 혼자서도 학습을 이어갈 수 있게 합니다."),
    ])}
  </div>
</section>

<section class="section alt" id="korean">
  <div class="wrap">
    {sec_head("AI국어 · 중1~고3", "독서·문학·문법 전 영역, 학교별 기출 기반 실전", center=False)}
    <div class="steps" style="margin-bottom:32px">
      <div class="step reveal"><span class="en">01</span><h3>진단</h3><p>학습 실력과 학업 성취도 진단</p></div>
      <div class="step reveal"><span class="en">02</span><h3>분석</h3><p>성취도와 취약점 분석</p></div>
      <div class="step reveal"><span class="en">03</span><h3>예측</h3><p>성취도 기반 점수·백분위·석차 예측</p></div>
      <div class="step reveal"><span class="en">04</span><h3>트레이닝</h3><p>취약 개념 맞춤 문제와 오답 해설 강의</p></div>
    </div>
    {cards([
      ("", "내신·수능 맞춤", "약 140만 개 국어 문항 콘텐츠와 학교별 기출문제·시험지 기반 실전 훈련"),
      ("", "어휘·어법", "온라인 어휘·어법 학습을 단계별로 쌓아 문해력의 바탕을 만듭니다"),
      ("", "개별 클리닉", "실시간 성취도 분석으로 맞춤 문제를 제공하고 약점 유형을 짚어 줍니다"),
      ("", "약점 집중 훈련", "오답 분석과 해설 강의, 빅데이터 기반 학습 자료 추천"),
    ], cols=4)}
  </div>
</section>

<section class="section" id="reading">
  <div class="wrap">
    {sec_head("AI독서 · 초1~중2", "독서를 진로와 연결하는 포트폴리오", center=False)}
    {cards([
      ("커리큘럼", "진로 검사로 시작하는 독서", "도서지수와 진로 심리 검사로 관심 분야를 파악하고, 진로와 흥미에 맞는 책을 추천해 개인 맞춤 커리큘럼을 설계합니다."),
      ("포트폴리오", "기록이 남는 독서", "독서 활동 데이터를 기록·분석하고 성취 리포트를 제공해 성취감을 쌓습니다. 초등 핵심 문해력과 꾸준한 독서 습관이 동시에 만들어집니다."),
    ], cols=2)}
  </div>
</section>
{cta_band("AI학습클래스, 레벨부터 확인해 보세요", "레벨테스트 결과로 영어·수학·국어·독서 중 어떤 과정이 맞는지, 가까운 센터에서 운영하는지 안내해 드립니다.")}
""")

pages["subjects.html"] = dict(
    title="와와학습코칭센터 과목 안내 | 국어·영어·수학 초등·중등·고등 학습코칭과 시험·방학 운영",
    desc="와와학습코칭센터에서 수학·영어·국어를 어떻게 코칭하는지, 초등·중등·고등 단계별로 무엇이 달라지는지, 시험기간과 방학에는 어떻게 운영되는지, 오답노트·백지노트·개념노트는 어떻게 쓰는지 정리했습니다.",
    keywords="초등 수학학원, 중등 수학학원, 고등 수학학원, 초등 영어학원, 중등 영어학원, 고등 영어학원, 국어학원, 내신 영어, 내신 수학, 수행평가 대비, 서술형 대비, 시험대비 특강, 방학특강, 오답노트 쓰는법, 백지노트, 개념노트, 와와 과목",
    body=lambda: f"""
{page_hero("과목 안내", "국어 · 영어 · 수학, 과목마다 코칭이 다릅니다", "국어·영어·수학이 중심이고 센터에 따라 사회·과학 등을 더합니다. 정기평가와 월말평가로 상태를 점검하고 개별 로드맵을 조정합니다.")}

<section class="section">
  <div class="wrap">
    <div class="grid grid-3">
      <div class="card card-img reveal"><img src="assets/img/math.jpg" alt="수학 학습코칭 — 그리드 노트에 풀이를 쓰는 손" loading="lazy"><div class="body"><h3>수학</h3><p>초·중·고 개념이 사슬처럼 이어지는 과목이라 빈 고리가 있으면 그 위로 쌓이지 않습니다. 진단으로 빈 지점을 찾아 거기서부터 개별 속도로 가고, 틀린 문제는 학생이 '왜'를 설명하게 합니다. AI수학의 맞춤 문제지와 유사→변형→심화 오답 클리닉으로 취약 유형을 반복 훈련합니다.</p><div class="chips"><span class="chip">연산·개념</span><span class="chip">내신 수학</span><span class="chip">오답 클리닉</span><span class="chip">심화·선행</span></div></div></div>
      <div class="card card-img reveal"><img src="assets/img/english.jpg" alt="영어 학습코칭 — 영어책을 소리 내어 읽는 학생" loading="lazy"><div class="body"><h3>영어</h3><p>초등은 파닉스와 네 영역의 균형, 중·고등은 독해·구문·듣기와 교과서별 내신 대비로 갑니다. 단어를 눈으로만 보고 외웠다고 믿는 습관은 데일리 테스트와 단어 앱으로 잡고, 서술형·수행평가(영작, 발표)는 학교가 요구하는 형식에 맞춰 답안 쓰는 연습을 합니다.</p><div class="chips"><span class="chip">파닉스</span><span class="chip">내신 영어</span><span class="chip">구문·독해</span><span class="chip">듣기·수능</span></div></div></div>
      <div class="card card-img reveal"><img src="assets/img/korean.jpg" alt="국어 학습코칭 — 책을 읽으며 밑줄 긋는 학생" loading="lazy"><div class="body"><h3>국어</h3><p>문제를 읽고도 뜻을 못 잡는 학생은 다른 과목도 막힙니다. 국어는 문해력의 과목이라 초등 독서 습관과 표현력부터 시작하고, 중·고등은 문학·독서·문법 내신과 수능, 논술까지 체계적으로 갑니다. AI국어의 학교별 기출과 대량 문항으로 실전 감각을 붙입니다.</p><div class="chips"><span class="chip">문해력</span><span class="chip">내신 국어</span><span class="chip">문학·독서·문법</span><span class="chip">수능·논술</span></div></div></div>
    </div>
    <p class="note" style="margin-top:20px">* 사회·과학과 기타 과목은 센터별로 운영 여부가 다릅니다. 수학·과학 전문은 더블유플러스, 국어·독서·논술 전문은 글로리드 학습코칭센터에서도 운영합니다.</p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {sec_head("학년별", "초등 · 중등 · 고등, 코칭의 무게가 다릅니다")}
    {cards([
      ("초등", "습관이 먼저", "점수보다 '매일 정해진 것을 하는 루틴'을 만듭니다. 플래너로 오늘 할 일을 정하고 체크하는 습관, 수학 연산·개념, 영어 파닉스·어휘·독해, 국어 문해력과 독서를 수준에 맞게 진행합니다. AI독서로 진로 연계 독서 포트폴리오를 만들 수 있습니다."),
      ("중등", "학교별 내신과 공부법 교정", "학교마다 다른 출제 스타일에 맞춰 교과서·프린트·부교재 기반으로 영어·수학 내신을 준비합니다. 서술형·수행평가 관리, 4주 전 범위 정리부터 직전 암기 점검까지의 역산 일정, 그리고 개념 없이 문제만 푸는 습관과 오답을 안 보는 습관을 플래너로 잡습니다."),
      ("고등", "내신·수능·수행평가 동시 관리", "학교별 기출 분석, 서술형 답안 훈련, 모의고사 오답 분석, D-100 전략과 멘탈 관리까지 코치가 밀착합니다. 기초가 흔들리면 무학년 수업으로 이전 과정부터 보완하고, 상위권은 연계 심화로 1등급과 2등급의 차이를 만듭니다."),
    ])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("시험기간 · 방학", "평소와 다르게 움직이는 시기")}
    <div class="grid grid-2">
      <div class="card reveal"><h3>시험기간</h3><ul><li>평소보다 학습 시간을 늘림</li><li>기본 개념 확인 → 기출·예상문제 연습</li><li>상·중·하 수준에 따른 학교별 맞춤 대비</li><li>부족한 단원 중심 보완, 필요 시 보충·추가 자습</li><li>4주 전 범위 정리 → 2주 전 유형 풀이 → 1주 전 예상문제·오답 → 직전 암기·서술형 점검</li></ul></div>
      <div class="card reveal"><h3>방학</h3><ul><li>방학특강으로 기초 다지기와 선행</li><li>수준과 목표에 맞춘 개별 학습 플랜 재설계</li><li>습관이 끊기지 않도록 유지 프로그램 운영</li><li>새 학기 전 결손 보완과 연계 심화</li></ul><p class="note" style="margin-top:12px">세부 일정은 센터마다 다릅니다.</p></div>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    {sec_head("공부 도구", "오답노트 · 백지노트 · 개념노트 · 마인드맵", "공부 시간은 많은데 성적이 안 오르는 학생 대부분은 방법이 문제입니다. 플래너에 방식이 드러나기 때문에 과목별로 고칠 수 있습니다.")}
    {cards([
      ("", "오답노트", "채점에서 끝내지 않고 틀린 이유를 분류해 다시 풉니다. 같은 유형의 실수가 줄어듭니다."),
      ("", "백지노트", "배운 단원을 아무것도 보지 않고 백지에 써 봅니다. 아는 것과 모르는 것이 그대로 드러나는 메타인지 훈련입니다."),
      ("", "개념노트", "문제만 많이 푸는 대신 개념을 자기 말로 정리합니다. 서술형과 응용 문제의 바탕이 됩니다."),
      ("", "마인드맵", "단원 사이의 연결 구조를 한 장에 정리합니다. 암기 과목과 범위가 긴 시험에 씁니다."),
    ], cols=4)}
  </div>
</section>
{cta_band("어떤 과목부터 손봐야 할지 모르겠다면", "학년·학교·현재 성적대를 알려주시면 진단 후 과목과 순서를 함께 정해 드립니다.")}
""")

pages["centers.html"] = dict(
    title="와와학습코칭센터 전국 센터 찾기 | 지역·학교명으로 가까운 지점 검색 (204개)",
    desc="와와학습코칭센터 전국 204개 지점을 지역명이나 학교명으로 검색하세요. 지점 주소, 찾아오는 길, 담당 학교, 교육지원청 등록번호를 확인하고 바로 무료 학습상담을 신청할 수 있습니다.",
    keywords="와와학습코칭센터 지점, 와와 센터 찾기, 와와학습코칭센터 위치, 우리동네 학습코칭, 와와 지점 주소, 와와학습코칭센터 서울, 와와학습코칭센터 경기, 와와학습코칭센터 부산, 와와학습코칭센터 대구, 와와학습코칭센터 인천, 학교 근처 학원",
    body=lambda: f"""
{page_hero("센터 찾기", "우리 동네 와와 찾기", "전국 204개 지점의 주소와 담당 학교를 지역명·학교명으로 검색하세요. 목록에 없는 지역은 상담 신청 시 지역만 남겨 주시면 가까운 센터를 확인해 안내해 드립니다.")}
<section class="section"><div class="wrap">
  <div class="finder reveal">
    <input type="search" id="centerSearch" placeholder="지역명, 동 이름, 학교명으로 검색 (예: 고양, 원흥초, 첨단중)" autocomplete="off" aria-label="센터 검색">
    <div class="faq-cats" id="regionChips">
      <a href="#" data-region="all" aria-current="true">전체</a><a href="#" data-region="서울·인천">서울·인천</a><a href="#" data-region="경기">경기</a><a href="#" data-region="대전·충청">대전·충청</a><a href="#" data-region="강원·제주">강원·제주</a><a href="#" data-region="경상·전라">경상·전라</a>
    </div>
    <p class="note"><b id="centerCount">0</b>개 지점 표시 중 · 주소·담당 학교는 각 센터가 등록한 정보 기준이며 변동될 수 있습니다.</p>
  </div>
  <div class="center-grid" id="centerGrid"></div>
  <div class="card" id="centerEmpty" hidden style="text-align:center;padding:40px">
    <p>이 지역은 아직 목록에 없습니다. 지역과 학년만 남겨 주시면 가까운 센터를 확인해 안내해 드립니다.</p>
    <a class="btn btn-primary" href="apply.html">무료 학습상담 신청</a>
  </div>
</div></section>
{cta_band("가까운 센터가 안 보이시나요?", "지역과 학년만 남겨 주시면 가까운 센터와 운영 과목·시간표를 확인해 안내해 드립니다.")}
<script src="assets/centers.js" defer></script>
""")

pages["reviews.html"] = dict(
    title="와와학습코칭센터 성적 변화 사례 | 영어 6등급→1등급, 수학 28점→80점, 서울대 합격",
    desc="와와학습코칭센터가 공개한 수강 사례를 과목·학년별로 요약했습니다. 영어 등급 상승, 수학 점수 변화, 국어 극복, 습관 변화, 서울대 합격 사례와 성적이 오른 학생들의 공통점.",
    keywords="와와학습코칭센터 후기, 와와 성적향상 사례, 학습코칭 후기, 영어 등급 올리기, 수학 점수 올리기, 서울대 합격 학원, 자기주도학습 후기, 와와 수강후기",
    body=lambda: f"""
{page_hero("성적 변화", "공개된 사례로 보는 변화", "와와학습코칭센터가 공식 채널에 공개한 수강 사례를 과목·학년별로 요약했습니다. 학생 이름은 본사 표기대로 가렸고, 효과는 학생마다 다릅니다.")}
<section class="section">
  <div class="wrap">
    {results_html(RESULTS)}
    <div class="card" style="margin-top:36px;background:var(--bg-alt)">
      <h3>사례 안내</h3>
      <p>위 내용은 와와학습코칭센터 공식 홈페이지와 공식 채널에 공개된 수강 사례를 이 페이지 운영자가 요약한 것입니다. 특정 성적이나 합격을 보장하지 않으며, 결과는 학생의 출발점·학습량·센터 운영 방식에 따라 달라집니다. 원문과 영상 후기는 <a href="https://www.wawacenter.com/review" target="_blank" rel="noopener"><strong>본사 후기 페이지</strong></a>에서 확인하실 수 있습니다.</p>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    {feature("success.jpg", "코치와 학생이 하이파이브하는 모습", "공통점", "성적이 오른 학생들이 공통으로 한 것",
      ["사례들을 모아 보면 패턴이 보입니다. 처음부터 기출을 푼 게 아니라 <strong>기본기를 먼저</strong> 다졌고, 시험 2주 전부터 <strong>여러 학교 기출</strong>로 실전 감각을 붙였으며, 코치와 함께 <strong>자기에게 맞는 공부법</strong>을 찾아 스스로 계획을 세웠습니다.",
       "그리고 공통적으로 '공부 태도가 달라졌다', '자신감이 생겼다', '목표가 높아졌다'고 말합니다. 점수는 그 결과로 따라왔습니다."],
      ["기본기 먼저", "기출은 2주 전부터", "나에게 맞는 방법", "1:1 소통"])}
  </div>
</section>
{cta_band("다음 사례의 주인공이 우리 아이라면", "현재 성적과 공부 습관을 진단받고, 가까운 센터의 코칭 방식을 들어 보세요.")}
""")

ALL_FAQ = FAQ_GENERAL + FAQ_CLASS
pages["faq.html"] = dict(
    title="와와학습코칭센터 자주 묻는 질문 18개 | 학원비·센터 위치·둥지학습·무학년·시험기간 운영",
    desc="와와학습코칭센터 상담 전에 학부모가 가장 많이 묻는 18가지. 일반 학원과의 차이, 4C, 둥지학습, 전국 센터, 교습비, 잘 맞는 학생, 무학년 수업, 상상코칭과의 관계, 고등 내신, 상담 신청, 수상, 초등 가능 여부, 진도 공유, 기초 부족, 집중 과목, 시험·방학 운영, 보충, 운영 과목.",
    keywords="와와학습코칭센터 FAQ, 와와 학원비, 와와 교습비, 와와 센터 위치, 둥지학습이란, 4C 프로세스란, 무학년 수업이란, 상상코칭 와와 차이, 와와 초등학생, 와와 보충수업, 학습코칭 질문",
    extra_ld=lambda: faq_ld(ALL_FAQ),
    body=lambda: f"""
{page_hero("자주 묻는 질문", "상담 전에 궁금한 것들", "학부모님들이 가장 많이 묻는 질문을 두 묶음으로 정리했습니다. 여기 없는 질문은 전화나 상담 신청으로 바로 물어보셔도 됩니다.")}
<section class="section">
  <div class="wrap">
    <div class="faq-cats"><a href="#general">와와에 대해</a><a href="#class">수업·운영에 대해</a><a href="apply.html">직접 질문하기</a></div>
    <h2 id="general">와와에 대해</h2>
    {faq_html(FAQ_GENERAL, 1)}
    <h2 id="class" style="margin-top:56px">수업·운영에 대해</h2>
    {faq_html(FAQ_CLASS, len(FAQ_GENERAL) + 1)}
  </div>
</section>
{cta_band("아직 남은 질문이 있다면", "학년·지역·과목을 알려주시면 가까운 센터 기준으로 정확히 답해 드립니다.")}
""")

pages["apply.html"] = dict(
    title="무료 학습상담 신청 | 와와학습코칭센터 학습상담",
    desc="와와학습코칭센터 무료 학습상담 신청. 학부모 성함, 자녀 학년, 연락처, 지역을 남겨 주시면 가까운 센터의 진단 일정을 안내해 드립니다.",
    keywords="와와학습코칭센터 상담신청, 무료 학습상담, 학습진단 신청, 학원 상담 예약",
    noindex=True,
    body=lambda: f"""
{page_hero("상담 신청", "무료 학습상담 신청", "접수 후 평일 기준 빠르게 연락드립니다. 학년·지역·과목을 확인하고 가까운 센터의 진단 일정을 안내해 드리며, 등록을 권유하지 않습니다.")}
<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="grid-template-columns:1.3fr .8fr;align-items:start">
      <form class="form" id="applyForm" action="https://formsubmit.co/ajax/{EMAIL}" method="POST">
        <input type="hidden" name="_subject" value="[와와학습코칭센터 학습상담] 무료 학습상담 신청">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <div class="field-row">
          <div class="field"><label for="f-parent">학부모 성함 <span class="req">*</span></label><input id="f-parent" name="학부모성함" type="text" required autocomplete="name"></div>
          <div class="field"><label for="f-grade">자녀 학년 <span class="req">*</span></label>
            <select id="f-grade" name="자녀학년" required>
              <option value="">선택</option>
              <optgroup label="초등"><option>초1</option><option>초2</option><option>초3</option><option>초4</option><option>초5</option><option>초6</option></optgroup>
              <optgroup label="중등"><option>중1</option><option>중2</option><option>중3</option></optgroup>
              <optgroup label="고등"><option>고1</option><option>고2</option><option>고3</option></optgroup>
              <option>기타/예비</option>
            </select></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="f-phone">연락처 <span class="req">*</span></label><input id="f-phone" name="연락처" type="tel" inputmode="numeric" placeholder="010-0000-0000" required autocomplete="tel"></div>
          <div class="field"><label for="f-region">거주 지역 / 학교 <span class="req">*</span></label><input id="f-region" name="지역" type="text" placeholder="예: 고양시 덕양구 원흥동 / OO중" required></div>
        </div>
        <div class="field"><label>관심 과목</label>
          <div class="radio-row">
            <label><input type="checkbox" name="관심과목" value="수학">수학</label>
            <label><input type="checkbox" name="관심과목" value="영어">영어</label>
            <label><input type="checkbox" name="관심과목" value="국어">국어</label>
            <label><input type="checkbox" name="관심과목" value="사회/과학">사회·과학</label>
            <label><input type="checkbox" name="관심과목" value="AI학습클래스">AI학습클래스</label>
            <label><input type="checkbox" name="관심과목" value="학습습관/플래너">학습습관·플래너</label>
          </div>
        </div>
        <div class="field"><label>상담 방식</label>
          <div class="radio-row">
            <label><input type="radio" name="상담방식" value="전화상담" checked>전화 상담</label>
            <label><input type="radio" name="상담방식" value="대면상담">센터 방문 상담</label>
          </div>
        </div>
        <div class="field"><label for="f-msg">상담 내용 (선택)</label><textarea id="f-msg" name="상담내용" placeholder="현재 성적대, 고민되는 점, 다녀 본 학원, 희망 시간대 등을 적어 주시면 더 정확히 안내해 드립니다."></textarea></div>
        <label class="consent"><input type="checkbox" name="개인정보동의" value="동의" required> <span>[필수] 개인정보 수집·이용 동의 — 수집항목: 학부모 성함, 연락처, 자녀 학년, 지역 / 이용목적: 학습상담 응대 및 센터 안내 / 보유기간: 상담 완료 후 2개월 보관 후 파기. 동의를 거부할 수 있으나 비동의 시 상담 서비스 제공이 어렵습니다.</span></label>
        <button type="submit" class="btn btn-primary btn-lg" style="width:100%">무료 학습상담 신청하기</button>
        <div class="form-msg" role="status" aria-live="polite"></div>
      </form>
      <aside>
        <div class="contact-box">
          <h3>전화로 바로 상담</h3>
          <a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a>
          <p>평일 10:00–19:00 (주말·공휴일은 문자 남겨 주시면 순차 연락)</p>
          <p>이메일 <a href="mailto:{EMAIL}" style="color:#fff">{EMAIL}</a></p>
        </div>
        <div class="card" style="margin-top:20px">
          <h3>신청 후 진행</h3>
          <ul>
            <li><strong>접수 확인</strong> — 학년·지역·과목 확인 전화</li>
            <li><strong>센터 안내</strong> — 가까운 센터와 운영 과목·시간표</li>
            <li><strong>진단(Check)</strong> — 센터 방문, 진단검사·레벨테스트</li>
            <li><strong>처방(Curriculum)</strong> — 결과를 보고 과목·진도·플래너 설계</li>
          </ul>
        </div>
        <div class="card" style="margin-top:20px">
          <h3>교습비</h3>
          <p>센터·학년·과목 수에 따라 다르며, 각 센터의 교습비 게시표가 본사 '전국 센터 찾기'에 공개되어 있습니다. 상담 시 해당 센터 기준으로 정확히 안내합니다.</p>
        </div>
      </aside>
    </div>
  </div>
</section>
""")

# ───────────────────────── 블로그(학습 칼럼) ─────────────────────────
# posts/<slug>.md : 맨 위 frontmatter(--- ... ---) + 마크다운 본문. BLOG_GUIDE.md 참고.
import markdown, email.utils, time

POSTS_DIR = os.path.join(OUT, "posts")

def load_posts():
    posts = []
    if not os.path.isdir(POSTS_DIR):
        return posts
    for fn in sorted(os.listdir(POSTS_DIR)):
        if not fn.endswith(".md"):
            continue
        raw = io.open(os.path.join(POSTS_DIR, fn), encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"frontmatter 없음: {fn}")
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        body_md = m.group(2).strip()
        for k in ("title", "date", "description", "keywords"):
            if k not in meta:
                raise SystemExit(f"{fn}: frontmatter에 {k} 없음")
        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", fn[:-3])
        html_body = markdown.markdown(body_md, extensions=["extra", "sane_lists"])
        text = re.sub(r"<[^>]+>", "", html_body)
        chars = len(re.sub(r"\s", "", text))
        posts.append(dict(meta, slug=slug, file=f"blog-{slug}.html", body=html_body, chars=chars,
                          cover=meta.get("cover", "planner.jpg"), category=meta.get("category", "공부법"),
                          minutes=max(3, chars // 500)))
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts

def post_card(p):
    return f"""<a class="post-card reveal" href="{p['file']}">
  <img src="assets/img/{p['cover']}" alt="" loading="lazy">
  <div class="body"><div class="meta"><span class="cat">{p['category']}</span><time datetime="{p['date']}">{p['date']}</time> · {p['minutes']}분</div>
  <h3>{p['title']}</h3><p>{p['description']}</p></div></a>"""

def render_post(p, all_posts):
    url = f"{SITE_URL}/{p['file']}"
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
        "description": p["description"], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
        "image": f"{SITE_URL}/assets/img/{p['cover']}", "mainEntityOfPage": url,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL + "/"}}, ensure_ascii=False)
    related = [q for q in all_posts if q["slug"] != p["slug"]][:3]
    rel = ""
    if related:
        rel = '<section class="section alt"><div class="wrap"><h2 style="margin-bottom:24px">함께 읽을 글</h2><div class="grid grid-3">' + "".join(post_card(q) for q in related) + '</div></div></section>'
    body = f"""
<section class="page-hero"><div class="wrap">
  <div class="crumb"><a href="index.html">홈</a> › <a href="blog.html">학습 칼럼</a> › {p['category']}</div>
  <h1>{p['title']}</h1>
  <p class="lead">{p['description']}</p>
  <div class="post-meta"><time datetime="{p['date']}">{p['date']}</time> · 읽는 시간 약 {p['minutes']}분 · {p['category']}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="post-layout">
    <article class="prose">
      <img class="post-cover" src="assets/img/{p['cover']}" alt="{p['title']}" loading="lazy">
      {p['body']}
      <div class="post-cta">
        <h3>우리 아이에게 맞는 방법인지 확인하고 싶다면</h3>
        <p>학년·학교·현재 상황을 알려주시면 가까운 와와학습코칭센터 기준으로 진단 일정과 진행 방식을 안내해 드립니다. 상담과 진단은 무료이고 등록을 권유하지 않습니다.</p>
        <div class="btn-group"><a class="btn btn-primary" href="apply.html">무료 학습상담 신청</a><a class="btn btn-outline" href="tel:{PHONE_TEL}">📞 {PHONE}</a></div>
      </div>
      <p class="post-back"><a href="blog.html">← 학습 칼럼 목록으로</a></p>
    </article>
    <aside class="post-side">
      <div class="card"><h3>이 글은</h3><p>와와학습코칭센터 학습상담 파트너가 쓴 공부법·내신 전략 칼럼입니다. 센터 운영 방식은 지점마다 다를 수 있습니다.</p></div>
      <div class="card" style="margin-top:16px"><h3>바로가기</h3><ul><li><a href="system.html">학습 시스템</a></li><li><a href="subjects.html">과목 안내</a></li><li><a href="faq.html">자주 묻는 질문</a></li><li><a href="apply.html">무료 학습상담</a></li></ul></div>
    </aside>
  </div>
</div></section>
{rel}
{cta_band()}
"""
    return head(p["title"] + " | 와와학습코칭센터 학습 칼럼", p["description"], p["file"], p["keywords"],
                extra_ld=f'<script type="application/ld+json">{ld}</script>', og=p["cover"]) \
        + chrome_top("blog.html") + body + chrome_bottom()

def render_blog_index(posts):
    cats = sorted({p["category"] for p in posts})
    chips = "".join(f'<a href="#" data-cat="{c}">{c}</a>' for c in cats)
    grid = "".join(post_card(p) for p in posts) if posts else '<p class="note">첫 글을 준비 중입니다.</p>'
    body = f"""
{page_hero("학습 칼럼", "학습 칼럼", "공부 습관, 플래너, 내신 전략, 과목별 공부법을 학부모와 학생이 바로 써먹을 수 있게 정리합니다. 와와학습코칭센터 학습상담 파트너가 꾸준히 발행합니다.")}
<section class="section"><div class="wrap">
  <div class="faq-cats" id="catFilter"><a href="#" data-cat="" aria-current="true">전체 ({len(posts)})</a>{chips}</div>
  <div class="grid grid-3" id="postGrid">{grid}</div>
</div></section>
{cta_band()}
"""
    return head("와와학습코칭센터 학습 칼럼 | 공부습관·플래너·내신 전략·과목별 공부법",
                "초중고 학부모를 위한 공부법 칼럼. 자기주도학습 습관, 플래너 활용, 내신 4주 전략, 오답노트, 과목별 공부법을 와와학습코칭센터 학습상담 파트너가 꾸준히 발행합니다.",
                "blog.html", "공부법 칼럼, 자기주도학습 방법, 플래너 쓰는 법, 내신 공부 전략, 오답노트 쓰는 법, 중학생 공부법, 고등학생 내신, 초등 공부습관, 와와학습코칭센터 칼럼") \
        + chrome_top("blog.html") + body + chrome_bottom()

def render_rss(posts):
    items = []
    for p in posts[:30]:
        t = time.mktime(time.strptime(p["date"], "%Y-%m-%d"))
        items.append(f"""  <item>
    <title>{p['title'].replace('&', '&amp;')}</title>
    <link>{SITE_URL}/{p['file']}</link>
    <guid>{SITE_URL}/{p['file']}</guid>
    <pubDate>{email.utils.formatdate(t)}</pubDate>
    <description>{p['description'].replace('&', '&amp;')}</description>
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>와와학습코칭센터 학습 칼럼</title>
  <link>{SITE_URL}/blog.html</link>
  <description>공부 습관·플래너·내신 전략·과목별 공부법 칼럼</description>
  <language>ko</language>
{chr(10).join(items)}
</channel></rss>
"""

# ───────────────────────── 빌드 ─────────────────────────
def build():
    for fname, p in pages.items():
        extra = p["extra_ld"]() if "extra_ld" in p else ""
        html = head(p["title"], p["desc"], fname, p["keywords"], p.get("noindex", False), extra) \
             + chrome_top(fname) + p["body"]() + chrome_bottom()
        with io.open(os.path.join(OUT, fname), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("wrote", fname, len(html))

    # 센터 데이터 → assets/centers.js (file:// 미리보기에서도 fetch 없이 동작)
    centers = json.load(io.open(os.path.join(OUT, "assets", "centers.json"), encoding="utf-8"))
    with io.open(os.path.join(OUT, "assets", "centers.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("window.CENTERS = " + json.dumps(centers, ensure_ascii=False) + ";\n")
    print(f"wrote assets/centers.js ({len(centers)} centers)")

    posts = load_posts()
    for p in posts:
        with io.open(os.path.join(OUT, p["file"]), "w", encoding="utf-8", newline="\n") as f:
            f.write(render_post(p, posts))
        print(f"wrote {p['file']}  ({p['chars']}자, {p['date']})")
    with io.open(os.path.join(OUT, "blog.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render_blog_index(posts))
    with io.open(os.path.join(OUT, "rss.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(render_rss(posts))
    print(f"wrote blog.html ({len(posts)} posts), rss.xml")

    urls = [f for f in pages if not pages[f].get("noindex")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in urls:
        loc = f"{SITE_URL}/" if f == "index.html" else f"{SITE_URL}/{f}"
        sm.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if f == 'index.html' else '0.8'}</priority></url>")
    sm.append(f"  <url><loc>{SITE_URL}/blog.html</loc><lastmod>{posts[0]['date'] if posts else TODAY}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>")
    for p in posts:
        sm.append(f"  <url><loc>{SITE_URL}/{p['file']}</loc><lastmod>{p.get('updated', p['date'])}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>")
    sm.append("</urlset>")
    with io.open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sm) + "\n")
    with io.open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /apply.html\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
