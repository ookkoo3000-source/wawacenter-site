# 와와학습코칭센터 학습상담 안내 사이트

본사 공식 사이트(wawacenter.com)의 공개 콘텐츠를 바탕으로 만든 와와학습코칭센터 수강 상담 파트너 페이지.
기존 wawa.primeadmit.co.kr(chaeum-coaching 레포)과는 별개의 두 번째 와와 사이트.

## 구조
- `build.py` — 모든 페이지 생성기. 헤더/푸터/CTA/FAQ/후기 데이터가 여기 한 곳에 있음.
  `python build.py` 실행하면 아래 파일이 다시 생성됨.
- 생성 페이지: `index.html`(홈) · `about.html`(브랜드소개·연혁·패밀리브랜드) · `system.html`(4C·3대관리·4대시스템·내신6강점·플래너7강점·둥지학습·비교표) · `ai-class.html`(AI영어/수학/국어/독서) · `subjects.html`(국영수·학년별·시험/방학 운영) · `reviews.html`(후기 8개) · `faq.html`(19개, FAQPage JSON-LD) · `apply.html`(상담폼, noindex)
- `sitemap.xml`, `robots.txt` — build.py가 생성.
- `assets/style.css`, `assets/site.js`, `assets/img/`(자체 제작 이미지 13장 + 파비콘)
- `IMAGE_PROMPTS.md` — 이미지 13장의 나노 바나나 프롬프트·파일명·비율. 만든 파일을 같은 이름으로 `assets/img/`에 넣으면 끝.
- `make_placeholders.py` — 이미지가 없을 때 임시 자리표시 이미지 생성(실제 이미지가 있으면 건드리지 않음).

## 2차 개편 (2026-10-30)
본사 사이트와 너무 같지 않도록 **본사 이미지 전부 제거, 문구 전면 재작성**. 사실(205센터·2015 론칭·4C·둥지학습·플래너·무학년·AI클래스 과목/대상·수상)만 유지하고 문장과 구조는 새로 씀. 로고는 본사 로고 대신 글자 로고(CSS).

## 학습 칼럼(블로그)
`posts/YYYY-MM-DD-slug.md`(frontmatter + 마크다운) 추가 → `python build.py` → `blog-<slug>.html` + `blog.html` 목록 + `rss.xml` + sitemap 자동. 작성 규칙·주제 목록은 `BLOG_GUIDE.md`.

## 센터 찾기
`assets/centers.json`(204개 지점, 기존 wawa 사이트 CENTERS 배열과 동일) → build.py가 `assets/centers.js`로 변환 → `centers.html`에서 지역/학교명 검색. 새 지점은 centers.json에 추가 후 재빌드.

## 지점+학교 글 자동 생성
`gen_posts.py N` — centers.json의 지점-학교 조합 중 미사용(posts/USED_PAIRS.txt 기준, PRIORITY_PAIRS.txt 우선)을 골라 Gemini로 초안 생성 → posts/*.md. 이후 `python build.py`. 자세한 건 BLOG_GUIDE.md.

## 도메인
`build.py` 맨 위 `SITE_URL` 한 줄을 실제 도메인으로 바꾸고 다시 빌드하면 canonical/og:url/sitemap/robots 전부 갱신됨.
GitHub Pages 배포 시 `CNAME` 파일 추가 필요.

## 상담 연락처
- 전화 010-3131-5305 / 폼 → FormSubmit → ookkoo12@naver.com
- 본사 대표번호·사업자정보는 표기하지 않음(파트너 페이지 고지 + 저작권 (주)동화세상에듀코 표기만).
