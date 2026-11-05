# -*- coding: utf-8 -*-
"""지점 + 타깃 학교 기반 블로그 글 자동 생성 (Gemini).
사용:  python gen_posts.py 10          → 미사용 지점-학교 조합 10개 골라 posts/ 에 md 생성
       python gen_posts.py 10 --dry    → 어떤 조합/제목이 뽑히는지만 출력
생성 후 반드시 python build.py 로 빌드하고 출력된 글자 수와 섹션 수를 확인할 것.
조합 사용 기록: posts/USED_PAIRS.txt (지점\t학교). 우선순위: posts/PRIORITY_PAIRS.txt 상단부터.
API 키: ~/.gemini_api_key (레포 밖). 모델은 MODELS 순서로 시도, 503/429면 다음 모델."""
import io, os, re, sys, json, time, random, datetime, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(ROOT, "posts")
USED = os.path.join(POSTS, "USED_PAIRS.txt")
PRIORITY = os.path.join(POSTS, "PRIORITY_PAIRS.txt")
LOG = os.path.join(ROOT, ".gen_tmp")
KEY = io.open(os.path.expanduser("~/.gemini_api_key"), encoding="utf-8").read().strip()
MODELS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.7-flash", "gemini-3.1-flash-lite", "gemini-flash-latest"]
TODAY = datetime.date.today().isoformat()

SUBJECT_BY_LEVEL = {"초": ["수학", "영어", "국어"], "중": ["수학", "영어", "내신"], "고": ["수학", "영어", "내신"]}
SUBJECT_SLUG = {"수학": "suhak", "영어": "yeongeo", "국어": "gugeo", "내신": "naesin"}
CATEGORY = {"초": "초등", "중": "중등", "고": "고등"}
COVER = {"수학": "math.jpg", "영어": "english.jpg", "국어": "korean.jpg", "내신": "naesin.jpg"}

RULES = """[역할]
당신은 교육 분야 전문 블로거입니다. 학부모가 검색해서 들어왔을 때 끝까지 읽게 만드는, 그 지역·학교에 특화된 실질적인 글을 씁니다.

[출력 형식 — 반드시 지킬 것]
- 한국어. 순수 HTML 조각만 출력(<html>, <body>, <head>, ```코드블록, 마크다운 기호 금지).
- 첫 줄은 <h1>제목</h1> — 제목에 반드시 "{school} {subject}" 키워드를 포함, 40~60자.
- 그 다음 <p> 서론 2~3문단(공백 제외 300자 이상). 첫 문장은 <strong>으로 검색 의도에 대한 한 줄 답을 먼저 주고, 이어서 아래 [지역 정보]의 동네·통학 동선을 구체적으로 묘사할 것. "많은 학부모님이 고민하십니다" 같은 뻔한 도입 금지.
- 서론 바로 뒤에 <blockquote><p><strong>먼저 결론부터</strong>: ...</p></blockquote> 형태로 이 글의 핵심을 3~4문장으로 요약(구글 검색 요약용).
- <h2> 제목은 "1. ", "2. " 식으로 번호를 붙이고, 학부모가 확인할 기준이나 행동이 드러나게 쓸 것.
- 본문 소제목은 <h2> 정확히 6개. 각 <h2> 아래 <p> 문단 3개 이상, 공백 제외 한글 750자 이상. 짧으면 실패.
- 각 <h2> 섹션 마지막에는 <blockquote><p>그 섹션의 핵심을 한두 문장으로</p></blockquote> 를 붙일 것(페이지에서 "핵심 정리" 박스로 표시됨).
- 소제목 제목은 이 학교·지역만의 색이 드러나게 새로 지을 것(“~의 힘”, “~프로세스로” 같은 반복 패턴 금지).
- 6개 소제목 중 4개는 그 학교·지역·과목에 특화된 실질적 조언(통학 여건, 학교 시험 특성·시기, 학년별 포인트, 집에서 할 수 있는 것), 2개에서만 와와학습코칭센터의 방식을 자연스럽게 녹일 것.
- 마지막 <h2>자주 묻는 질문</h2> 아래 <h3>Q. 질문</h3><p>답</p> 형식으로 3개.
- 강조는 <strong>만 사용. 표/목록 필요하면 <ul><li>, <table> 사용 가능.
- 전체 공백 제외 4,500자 이상.
"""

FACTS = """[반드시 지켜야 할 사실 — 지어내지 말 것]
- 브랜드: 와와학습코칭센터 ((주)동화세상에듀코 운영, 2015년 시작, 전국 205개 센터, 2025 소비자가 뽑은 올해의 브랜드대상)
- 방식: 4C 프로세스(Check 진단 → Curriculum 처방 → Consulting 상담 → Coaching 지도), 학습 플래너로 매일 공부 습관 기록·관리, 개별 맞춤형 무학년 수업(학년이 아니라 실력 기준으로 시작), 둥지학습(코치를 중심으로 둘러앉아 학생이 설명하고 질문하는 양방향 수업), 학교별 내신 대비(교과서·프린트·부교재 반영, 시험 4주 전부터 역산 일정), 오답노트·백지노트·개념노트
- 이번 글에서 강조할 와와 방식: {emphasize}. 나머지는 언급하지 않아도 됨.
- 상담·학습진단은 무료. 교습비는 센터별로 다르며 상담 시 안내(금액을 쓰지 말 것).
- 절대 금지: 특정 학생 이름·점수·등급 상승·합격 실적 지어내기, 학교의 시험 평균·등급 비율 같은 통계 지어내기, 지점 전화번호 쓰기(상담은 "무료 학습상담 신청"으로만 안내), 원장·코치가 1인칭으로 말하는 문장, 타 학원 비교·비하, 본사 홈페이지 문장 그대로 쓰기.
- 지점 원장 이름은 마지막 지점 소개에서 "OOO 원장이 운영" 수준으로 3인칭 1회만.
- 학교에 대한 정보는 아래에 주어진 것(지역, 담당 지점, 함께 관리하는 학교)만 사실로 쓰고, 학교의 교육과정·시험 방식은 "일반적인 {level_name} 학교의 경우"로 일반화해서 쓸 것(그 학교만의 제도를 단정하지 말 것).
"""

def log(msg):
    os.makedirs(LOG, exist_ok=True)
    io.open(os.path.join(LOG, f"gen-{TODAY}.log"), "a", encoding="utf-8").write(msg + "\n")
    print(msg)

def call_gemini(prompt):
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                              "generationConfig": {"temperature": 0.9, "maxOutputTokens": 8192}}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    d = json.loads(resp.read().decode("utf-8"))
                    return model, "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
            except urllib.error.HTTPError as e:
                if e.code in (503, 429):
                    time.sleep(5); continue
                log(f"  HTTP {e.code} on {model}"); break
            except Exception as ex:
                log(f"  err {model}: {ex}"); time.sleep(3)
    return None, None

def fix_faq(html):
    """FAQ 헤딩 보정: <h3>자주 묻는 질문</h3> → <h2>, 헤딩 없이 <h3>Q.로 시작하면 <h2> 삽입 (build.py는 <h2>로만 FAQ를 구분)."""
    html = re.sub(r"<h3[^>]*>\s*(자주 묻는 질문|FAQ)[^<]*</h3>", "<h2>자주 묻는 질문</h2>", html)
    if not re.search(r"<h2[^>]*>[^<]*(자주 묻는|FAQ)", html):
        m = re.search(r"<h3[^>]*>\s*Q\.", html)
        if m: html = html[:m.start()] + "<h2>자주 묻는 질문</h2>\n" + html[m.start():]
    return html

def measure(html):
    """(섹션별 글자수 리스트, FAQ 개수, 서론 글자수)"""
    html = re.sub(r"^```\w*\s*|```\s*$", "", html.strip())
    h1 = re.search(r"<h1>(.*?)</h1>", html, re.S)
    rest = html[h1.end():] if h1 else html
    parts = re.split(r"<h2[^>]*>", rest)
    intro = len(re.sub(r"<[^>]+>|\s", "", parts[0]))
    secs, faq = [], 0
    for p in parts[1:]:
        title, _, body = p.partition("</h2>")
        if "자주" in title or "FAQ" in title.upper():
            faq = len(re.findall(r"<h3>", body)); continue
        secs.append(len(re.sub(r"<[^>]+>|\s", "", body)))
    return secs, faq, intro

def romanize(s):
    """한글 학교명 → 로마자 슬러그 (간이 표기)"""
    CHO = ["g","kk","n","d","tt","r","m","b","pp","s","ss","","j","jj","ch","k","t","p","h"]
    JUNG = ["a","ae","ya","yae","eo","e","yeo","ye","o","wa","wae","oe","yo","u","wo","we","wi","yu","eu","ui","i"]
    JONG = ["","k","k","k","n","n","n","t","l","k","m","l","l","l","p","l","m","p","l","t","t","ng","t","t","k","t","p","t"]
    out = []
    for ch in s:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3:
            o -= 0xAC00; out.append(CHO[o // 588] + JUNG[(o % 588) // 28] + JONG[o % 28])
        elif ch.isalnum(): out.append(ch.lower())
    return "".join(out)

def load_pairs():
    centers = json.load(io.open(os.path.join(ROOT, "assets", "centers.json"), encoding="utf-8"))
    by_name = {c["name"]: c for c in centers}
    used = set()
    if os.path.exists(USED):
        for l in io.open(USED, encoding="utf-8"):
            if "\t" in l: a, b = l.rstrip("\n").split("\t")[:2]; used.add((a, b))
    # 이미 posts/에 같은 학교+과목 슬러그가 있으면 사용된 것으로 간주
    existing = {f[:-3] for f in os.listdir(POSTS) if f.endswith(".md")}
    order = []
    if os.path.exists(PRIORITY):
        for l in io.open(PRIORITY, encoding="utf-8"):
            if l.startswith("#") or "\t" not in l: continue
            br, sc, lv = l.rstrip("\n").split("\t")[:3]
            if br in by_name: order.append((br, sc, lv))
    for c in centers:  # 우선순위 뒤에 전체 조합(초·중·고 추정)
        for s in c.get("schools", []):
            lv = "초" if s.endswith("초") else "중" if s.endswith("중") else "고" if s.endswith("고") else "중"
            order.append((c["name"], s, lv))
    seen, out = set(), []
    for br, sc, lv in order:
        if (br, sc) in used or (br, sc) in seen: continue
        seen.add((br, sc)); out.append((by_name[br], sc, lv))
    return out

def pick(n):
    pairs = load_pairs()
    chosen, used_centers, used_schools = [], set(), set()
    for c, sc, lv in pairs:           # 한 배치 안에서 지점·학교 중복 피하기
        if c["name"] in used_centers or sc in used_schools: continue
        used_centers.add(c["name"]); used_schools.add(sc); chosen.append((c, sc, lv))
        if len(chosen) >= n: break
    return chosen

def build_prompt(c, school, lv, subject, emphasize):
    level_name = {"초": "초등학교", "중": "중학교", "고": "고등학교"}[lv]
    schools_all = ", ".join(c.get("schools", []))
    return RULES.format(school=school, subject=subject) + FACTS.format(emphasize=emphasize, level_name=level_name) + f"""
[주제]
키워드: {school} {subject} (학원·공부법을 찾는 학부모 대상). 대상: {level_name} 학생.
검색 의도: "{school} 다니는 아이 {subject}, 어디서 어떻게 시켜야 하나"에 대한 구체적 답.

[지역 정보]
- 지역: {c['city']} ({c['region']} 권역)
- 담당 지점: 와와학습코칭센터 {c['name']} — 주소 {c['address']}{(' / ' + c['note']) if c.get('note') else ''}
- 이 지점이 함께 관리하는 학교: {schools_all}
- 교육지원청 등록: {c.get('reg','')}
- 원장: {c.get('director','')}
- 운영 과목·학년: {", ".join(f"{k} {v}" for k, v in (c.get("subjects") or {{}}).items()) or "상담 시 안내"}
- 수업 시간: {c.get('hours') or '상담 시 안내'} / 주말: {c.get('weekend') or '상담 시 안내'}
위 운영 과목·시간은 사실이므로 통학·시간 활용 소제목에서 그대로 활용하되, "센터 사정에 따라 바뀔 수 있어 상담 시 확인"이라는 단서를 한 번 넣을 것. 이 글의 과목({subject})이 운영 학년에 포함되는지 확인하고, 대상 학년이 운영 범위 밖이면 "해당 학년 운영 여부는 상담 시 확인"으로 쓸 것.
서론은 이 지역(동네 이름, 주변 환경, 통학 동선)을 구체적으로 묘사하며 시작할 것. 본문 중 1개 소제목은 "{school}에서 {c['name']}까지"처럼 통학·동선·방과후 활용에 대한 실질적 내용으로. 마지막 소제목(6번째) 끝에 지점 소개와 "무료 학습상담 신청" 안내를 자연스럽게 넣을 것.
"""

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
    dry = "--dry" in sys.argv
    chosen = pick(n)
    if not chosen:
        print("남은 조합이 없습니다."); return
    emph_pool = ["플래너 학습관리", "둥지학습", "개별 맞춤 무학년 수업", "4C 프로세스(진단→처방→상담→지도)", "학교별 내신 대비와 역산 일정", "오답노트·백지노트"]
    os.makedirs(POSTS, exist_ok=True)
    for i, (c, school, lv) in enumerate(chosen):
        subject = SUBJECT_BY_LEVEL[lv][i % 3]
        emphasize = emph_pool[i % len(emph_pool)]
        slug = f"{romanize(school)}-{SUBJECT_SLUG[subject]}"
        fn = f"{TODAY}-{slug}.md"
        print(f"[{i+1}/{len(chosen)}] {c['name']} / {school}({lv}) / {subject} → {fn}")
        if dry: continue
        if os.path.exists(os.path.join(POSTS, fn)):
            log(f"  이미 존재: {fn}"); continue
        prompt = build_prompt(c, school, lv, subject, emphasize)
        best = None
        for attempt in range(3):
            model, text = call_gemini(prompt)
            if not text: continue
            text = fix_faq(re.sub(r"^```\w*\s*|```\s*$", "", text.strip()))
            secs, faq, intro = measure(text)
            score = (faq >= 3 and len(secs) == 6, faq >= 3, min(len(secs), 6), min(secs) if secs else 0)
            log(f"  try{attempt+1} {model}: h2={len(secs)} min={min(secs) if secs else 0} faq={faq} intro={intro}")
            if best is None or score > best[0]: best = (score, text, secs, faq)
            if len(secs) == 6 and faq >= 3 and min(secs) >= 600 and intro >= 250: break
        if not best:
            log(f"  FAIL {fn}"); continue
        _, text, secs, faq = best
        h1 = re.search(r"<h1>(.*?)</h1>", text, re.S)
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else f"{school} {subject}, {c['city']}에서 준비하는 법"
        body = text[h1.end():].strip() if h1 else text
        desc = re.sub(r"<[^>]+>", "", re.search(r"<p>(.*?)</p>", body, re.S).group(1)).strip()
        desc = (desc[:140] + "…") if len(desc) > 140 else desc
        kws = f"{school} {subject}, {school} {subject}학원, {c['city']} {subject}학원, {c['city']} 학습코칭, 와와학습코칭센터 {c['name']}, {CATEGORY[lv]} {subject} 공부법, {school} 내신, {c['city'].split()[-1]} 학원"
        md = f"""---
title: {title}
date: {TODAY}
description: {desc}
keywords: {kws}
category: {CATEGORY[lv]} {subject}
cover: {COVER[subject]}
center: {c['name']}
school: {school}
---

{body}
"""
        io.open(os.path.join(POSTS, fn), "w", encoding="utf-8", newline="\n").write(md)
        io.open(USED, "a", encoding="utf-8", newline="\n").write(f"{c['name']}\t{school}\t{subject}\t{TODAY}\t{fn}\n")
        log(f"  저장 {fn}  섹션={secs} faq={faq}")
    print("done. 다음: python build.py")

if __name__ == "__main__":
    main()
