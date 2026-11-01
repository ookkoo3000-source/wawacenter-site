(function () {
  // 모바일 메뉴
  var burger = document.querySelector(".burger");
  var mnav = document.querySelector(".mnav");
  if (burger && mnav) {
    burger.addEventListener("click", function () {
      var open = mnav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // 스크롤 리빌
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  // 전화번호 자동 하이픈
  var phone = document.querySelector('input[name="연락처"]');
  if (phone) {
    phone.addEventListener("input", function () {
      var v = phone.value.replace(/\D/g, "").slice(0, 11);
      if (v.length > 7) v = v.replace(/(\d{3})(\d{4})(\d+)/, "$1-$2-$3");
      else if (v.length > 3) v = v.replace(/(\d{3})(\d+)/, "$1-$2");
      phone.value = v;
    });
  }

  // 상담 신청 폼 (FormSubmit AJAX)
  var form = document.getElementById("applyForm");
  if (form) {
    var msg = form.querySelector(".form-msg");
    var btn = form.querySelector('button[type="submit"]');
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var consent = form.querySelector('input[name="개인정보동의"]');
      if (consent && !consent.checked) {
        msg.textContent = "개인정보 수집·이용에 동의해 주세요.";
        msg.className = "form-msg err";
        return;
      }
      btn.disabled = true;
      btn.textContent = "전송 중...";
      msg.className = "form-msg";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) {
          if (!r.ok) throw new Error("bad");
          form.reset();
          msg.textContent = "상담 신청이 접수되었습니다. 확인 후 빠르게 연락드리겠습니다.";
          msg.className = "form-msg ok";
          btn.textContent = "신청 완료";
        })
        .catch(function () {
          msg.textContent = "전송에 실패했습니다. 010-3131-5305로 전화 주시면 바로 안내해 드립니다.";
          msg.className = "form-msg err";
          btn.disabled = false;
          btn.textContent = "무료 학습상담 신청하기";
        });
    });
  }
})();

// 학습 칼럼 카테고리 필터 (blog.html)
(function () {
  var filter = document.getElementById("catFilter");
  var grid = document.getElementById("postGrid");
  if (!filter || !grid) return;
  filter.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-cat]");
    if (!a) return;
    e.preventDefault();
    var cat = a.getAttribute("data-cat");
    filter.querySelectorAll("a").forEach(function (x) { x.removeAttribute("aria-current"); });
    a.setAttribute("aria-current", "true");
    grid.querySelectorAll(".post-card").forEach(function (c) {
      var mine = c.querySelector(".cat").textContent.trim();
      c.classList.toggle("hidden", cat !== "" && mine !== cat);
    });
  });
})();

// 센터 찾기 (centers.html) — 데이터는 assets/centers.js의 window.CENTERS
(function () {
  var grid = document.getElementById("centerGrid");
  if (!grid) return;
  function init() {
    var C = window.CENTERS || [];
    var countEl = document.getElementById("centerCount");
    var emptyEl = document.getElementById("centerEmpty");
    var searchEl = document.getElementById("centerSearch");
    var chips = document.getElementById("regionChips");
    var region = "all";
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function render(list) {
      grid.innerHTML = list.map(function (c) {
        return '<article class="center-card">' +
          '<div class="cc-head"><h3>' + esc(c.name) + '</h3><span class="cc-city">' + esc(c.city) + '</span></div>' +
          '<p class="cc-addr">' + esc(c.address) + (c.note ? ' <span class="cc-note">' + esc(c.note) + '</span>' : '') + '</p>' +
          '<div class="cc-schools">' + (c.schools || []).map(function (s) { return '<span>' + esc(s) + '</span>'; }).join('') + '</div>' +
          '<div class="cc-reg">' + esc(c.reg || '') + (c.director ? ' · ' + esc(c.director) + ' 원장' : '') + '</div>' +
          '<a class="btn btn-primary" href="apply.html?center=' + encodeURIComponent(c.name) + '">' + esc(c.name) + ' 상담 신청</a>' +
          '</article>';
      }).join("");
      countEl.textContent = list.length;
      emptyEl.hidden = list.length > 0;
      grid.hidden = list.length === 0;
    }
    function apply() {
      var q = (searchEl.value || "").trim().toLowerCase().replace(/\s+/g, "");
      render(C.filter(function (c) {
        if (region !== "all" && c.region !== region) return false;
        if (!q) return true;
        var hay = (c.name + c.city + c.address + (c.note || "") + (c.schools || []).join("")).toLowerCase().replace(/\s+/g, "");
        return hay.indexOf(q) !== -1;
      }));
    }
    chips.addEventListener("click", function (e) {
      var a = e.target.closest("a[data-region]");
      if (!a) return;
      e.preventDefault();
      chips.querySelectorAll("a").forEach(function (x) { x.removeAttribute("aria-current"); });
      a.setAttribute("aria-current", "true");
      region = a.getAttribute("data-region");
      apply();
    });
    searchEl.addEventListener("input", apply);
    var qs = new URLSearchParams(location.search).get("q");
    if (qs) searchEl.value = qs;
    apply();
  }
  if (window.CENTERS) init(); else window.addEventListener("load", init);
})();

// 상담 폼: ?center=지점명 으로 들어오면 지역 칸에 미리 채움
(function () {
  var r = document.getElementById("f-region");
  if (!r) return;
  var c = new URLSearchParams(location.search).get("center");
  if (c && !r.value) r.value = c;
})();
