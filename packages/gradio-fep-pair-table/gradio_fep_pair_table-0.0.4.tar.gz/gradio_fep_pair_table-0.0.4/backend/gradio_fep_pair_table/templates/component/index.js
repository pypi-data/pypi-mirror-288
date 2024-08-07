const {
  SvelteComponent: Ar,
  assign: Mr,
  create_slot: xr,
  detach: Rr,
  element: zr,
  get_all_dirty_from_scope: Dr,
  get_slot_changes: Lr,
  get_spread_update: Or,
  init: Pr,
  insert: Fr,
  safe_not_equal: Ir,
  set_dynamic_element_data: lt,
  set_style: U,
  toggle_class: K,
  transition_in: Kt,
  transition_out: Qt,
  update_slot_base: Hr
} = window.__gradio__svelte__internal;
function Er(r) {
  let e, t, n;
  const i = (
    /*#slots*/
    r[18].default
  ), s = xr(
    i,
    r,
    /*$$scope*/
    r[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      r[7]
    ) },
    { id: (
      /*elem_id*/
      r[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      r[3].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let l = 0; l < o.length; l += 1)
    a = Mr(a, o[l]);
  return {
    c() {
      e = zr(
        /*tag*/
        r[14]
      ), s && s.c(), lt(
        /*tag*/
        r[14]
      )(e, a), K(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), K(
        e,
        "padded",
        /*padding*/
        r[6]
      ), K(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), K(
        e,
        "border_contrast",
        /*border_mode*/
        r[5] === "contrast"
      ), K(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), U(
        e,
        "height",
        /*get_dimension*/
        r[15](
          /*height*/
          r[0]
        )
      ), U(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : (
        /*get_dimension*/
        r[15](
          /*width*/
          r[1]
        )
      )), U(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), U(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), U(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), U(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`), U(e, "border-width", "var(--block-border-width)");
    },
    m(l, d) {
      Fr(l, e, d), s && s.m(e, null), n = !0;
    },
    p(l, d) {
      s && s.p && (!n || d & /*$$scope*/
      131072) && Hr(
        s,
        i,
        l,
        /*$$scope*/
        l[17],
        n ? Lr(
          i,
          /*$$scope*/
          l[17],
          d,
          null
        ) : Dr(
          /*$$scope*/
          l[17]
        ),
        null
      ), lt(
        /*tag*/
        l[14]
      )(e, a = Or(o, [
        (!n || d & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          l[7]
        ) },
        (!n || d & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          l[2]
        ) },
        (!n || d & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        l[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), K(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), K(
        e,
        "padded",
        /*padding*/
        l[6]
      ), K(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), K(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), K(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), d & /*height*/
      1 && U(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), d & /*width*/
      2 && U(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), d & /*variant*/
      16 && U(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), d & /*allow_overflow*/
      2048 && U(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), d & /*scale*/
      4096 && U(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), d & /*min_width*/
      8192 && U(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`);
    },
    i(l) {
      n || (Kt(s, l), n = !0);
    },
    o(l) {
      Qt(s, l), n = !1;
    },
    d(l) {
      l && Rr(e), s && s.d(l);
    }
  };
}
function Gr(r) {
  let e, t = (
    /*tag*/
    r[14] && Er(r)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Kt(t, n), e = !0);
    },
    o(n) {
      Qt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Ur(r, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: o = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: l = [] } = e, { variant: d = "solid" } = e, { border_mode: c = "base" } = e, { padding: u = !0 } = e, { type: f = "normal" } = e, { test_id: h = void 0 } = e, { explicit_call: p = !1 } = e, { container: g = !0 } = e, { visible: m = !0 } = e, { allow_overflow: _ = !0 } = e, { scale: w = null } = e, { min_width: A = 0 } = e, R = f === "fieldset" ? "fieldset" : "div";
  const y = (b) => {
    if (b !== void 0) {
      if (typeof b == "number")
        return b + "px";
      if (typeof b == "string")
        return b;
    }
  };
  return r.$$set = (b) => {
    "height" in b && t(0, s = b.height), "width" in b && t(1, o = b.width), "elem_id" in b && t(2, a = b.elem_id), "elem_classes" in b && t(3, l = b.elem_classes), "variant" in b && t(4, d = b.variant), "border_mode" in b && t(5, c = b.border_mode), "padding" in b && t(6, u = b.padding), "type" in b && t(16, f = b.type), "test_id" in b && t(7, h = b.test_id), "explicit_call" in b && t(8, p = b.explicit_call), "container" in b && t(9, g = b.container), "visible" in b && t(10, m = b.visible), "allow_overflow" in b && t(11, _ = b.allow_overflow), "scale" in b && t(12, w = b.scale), "min_width" in b && t(13, A = b.min_width), "$$scope" in b && t(17, i = b.$$scope);
  }, [
    s,
    o,
    a,
    l,
    d,
    c,
    u,
    h,
    p,
    g,
    m,
    _,
    w,
    A,
    R,
    y,
    f,
    i,
    n
  ];
}
class jr extends Ar {
  constructor(e) {
    super(), Pr(this, e, Ur, Gr, Ir, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const Br = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], ct = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Br.reduce(
  (r, { color: e, primary: t, secondary: n }) => ({
    ...r,
    [e]: {
      primary: ct[e][t],
      secondary: ct[e][n]
    }
  }),
  {}
);
var Xe = function(r, e) {
  return Xe = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(t, n) {
    t.__proto__ = n;
  } || function(t, n) {
    for (var i in n) Object.prototype.hasOwnProperty.call(n, i) && (t[i] = n[i]);
  }, Xe(r, e);
};
function Be(r, e) {
  if (typeof e != "function" && e !== null)
    throw new TypeError("Class extends value " + String(e) + " is not a constructor or null");
  Xe(r, e);
  function t() {
    this.constructor = r;
  }
  r.prototype = e === null ? Object.create(e) : (t.prototype = e.prototype, new t());
}
var me = function() {
  return me = Object.assign || function(e) {
    for (var t, n = 1, i = arguments.length; n < i; n++) {
      t = arguments[n];
      for (var s in t) Object.prototype.hasOwnProperty.call(t, s) && (e[s] = t[s]);
    }
    return e;
  }, me.apply(this, arguments);
};
function ce(r) {
  var e = typeof Symbol == "function" && Symbol.iterator, t = e && r[e], n = 0;
  if (t) return t.call(r);
  if (r && typeof r.length == "number") return {
    next: function() {
      return r && n >= r.length && (r = void 0), { value: r && r[n++], done: !r };
    }
  };
  throw new TypeError(e ? "Object is not iterable." : "Symbol.iterator is not defined.");
}
function qr(r, e) {
  var t = typeof Symbol == "function" && r[Symbol.iterator];
  if (!t) return r;
  var n = t.call(r), i, s = [], o;
  try {
    for (; (e === void 0 || e-- > 0) && !(i = n.next()).done; ) s.push(i.value);
  } catch (a) {
    o = { error: a };
  } finally {
    try {
      i && !i.done && (t = n.return) && t.call(n);
    } finally {
      if (o) throw o.error;
    }
  }
  return s;
}
function Tr(r, e, t) {
  if (t || arguments.length === 2) for (var n = 0, i = e.length, s; n < i; n++)
    (s || !(n in e)) && (s || (s = Array.prototype.slice.call(e, 0, n)), s[n] = e[n]);
  return r.concat(s || Array.prototype.slice.call(e));
}
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Yt = (
  /** @class */
  function() {
    function r(e) {
      e === void 0 && (e = {}), this.adapter = e;
    }
    return Object.defineProperty(r, "cssClasses", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(r, "strings", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(r, "numbers", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(r, "defaultAdapter", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), r.prototype.init = function() {
    }, r.prototype.destroy = function() {
    }, r;
  }()
);
/**
 * @license
 * Copyright 2019 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function Wr(r) {
  return r === void 0 && (r = window), Vr(r) ? { passive: !0 } : !1;
}
function Vr(r) {
  r === void 0 && (r = window);
  var e = !1;
  try {
    var t = {
      // This function will be called when the browser
      // attempts to access the passive property.
      get passive() {
        return e = !0, !1;
      }
    }, n = function() {
    };
    r.document.addEventListener("test", n, t), r.document.removeEventListener("test", n, t);
  } catch {
    e = !1;
  }
  return e;
}
const Xr = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  applyPassive: Wr
}, Symbol.toStringTag, { value: "Module" }));
/**
 * @license
 * Copyright 2018 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function Zr(r, e) {
  if (r.closest)
    return r.closest(e);
  for (var t = r; t; ) {
    if ($t(t, e))
      return t;
    t = t.parentElement;
  }
  return null;
}
function $t(r, e) {
  var t = r.matches || r.webkitMatchesSelector || r.msMatchesSelector;
  return t.call(r, e);
}
function Jr(r) {
  var e = r;
  if (e.offsetParent !== null)
    return e.scrollWidth;
  var t = e.cloneNode(!0);
  t.style.setProperty("position", "absolute"), t.style.setProperty("transform", "translate(-9999px, -9999px)"), document.documentElement.appendChild(t);
  var n = t.scrollWidth;
  return document.documentElement.removeChild(t), n;
}
const Nr = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  closest: Zr,
  estimateScrollWidth: Jr,
  matches: $t
}, Symbol.toStringTag, { value: "Module" }));
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Kr = {
  // Ripple is a special case where the "root" component is really a "mixin" of sorts,
  // given that it's an 'upgrade' to an existing component. That being said it is the root
  // CSS class that all other CSS classes derive from.
  BG_FOCUSED: "mdc-ripple-upgraded--background-focused",
  FG_ACTIVATION: "mdc-ripple-upgraded--foreground-activation",
  FG_DEACTIVATION: "mdc-ripple-upgraded--foreground-deactivation",
  ROOT: "mdc-ripple-upgraded",
  UNBOUNDED: "mdc-ripple-upgraded--unbounded"
}, Qr = {
  VAR_FG_SCALE: "--mdc-ripple-fg-scale",
  VAR_FG_SIZE: "--mdc-ripple-fg-size",
  VAR_FG_TRANSLATE_END: "--mdc-ripple-fg-translate-end",
  VAR_FG_TRANSLATE_START: "--mdc-ripple-fg-translate-start",
  VAR_LEFT: "--mdc-ripple-left",
  VAR_TOP: "--mdc-ripple-top"
}, dt = {
  DEACTIVATION_TIMEOUT_MS: 225,
  FG_DEACTIVATION_MS: 150,
  INITIAL_ORIGIN_SCALE: 0.6,
  PADDING: 10,
  TAP_DELAY_MS: 300
  // Delay between touch and simulated mouse events on touch devices
}, ke;
function Yr(r, e) {
  e === void 0 && (e = !1);
  var t = r.CSS, n = ke;
  if (typeof ke == "boolean" && !e)
    return ke;
  var i = t && typeof t.supports == "function";
  if (!i)
    return !1;
  var s = t.supports("--css-vars", "yes"), o = t.supports("(--css-vars: yes)") && t.supports("color", "#00000000");
  return n = s || o, e || (ke = n), n;
}
function $r(r, e, t) {
  if (!r)
    return { x: 0, y: 0 };
  var n = e.x, i = e.y, s = n + t.left, o = i + t.top, a, l;
  if (r.type === "touchstart") {
    var d = r;
    a = d.changedTouches[0].pageX - s, l = d.changedTouches[0].pageY - o;
  } else {
    var c = r;
    a = c.pageX - s, l = c.pageY - o;
  }
  return { x: a, y: l };
}
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var ut = [
  "touchstart",
  "pointerdown",
  "mousedown",
  "keydown"
], ft = [
  "touchend",
  "pointerup",
  "mouseup",
  "contextmenu"
], Ce = [], en = (
  /** @class */
  function(r) {
    Be(e, r);
    function e(t) {
      var n = r.call(this, me(me({}, e.defaultAdapter), t)) || this;
      return n.activationAnimationHasEnded = !1, n.activationTimer = 0, n.fgDeactivationRemovalTimer = 0, n.fgScale = "0", n.frame = { width: 0, height: 0 }, n.initialSize = 0, n.layoutFrame = 0, n.maxRadius = 0, n.unboundedCoords = { left: 0, top: 0 }, n.activationState = n.defaultActivationState(), n.activationTimerCallback = function() {
        n.activationAnimationHasEnded = !0, n.runDeactivationUXLogicIfReady();
      }, n.activateHandler = function(i) {
        n.activateImpl(i);
      }, n.deactivateHandler = function() {
        n.deactivateImpl();
      }, n.focusHandler = function() {
        n.handleFocus();
      }, n.blurHandler = function() {
        n.handleBlur();
      }, n.resizeHandler = function() {
        n.layout();
      }, n;
    }
    return Object.defineProperty(e, "cssClasses", {
      get: function() {
        return Kr;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "strings", {
      get: function() {
        return Qr;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "numbers", {
      get: function() {
        return dt;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "defaultAdapter", {
      get: function() {
        return {
          addClass: function() {
          },
          browserSupportsCssVars: function() {
            return !0;
          },
          computeBoundingRect: function() {
            return { top: 0, right: 0, bottom: 0, left: 0, width: 0, height: 0 };
          },
          containsEventTarget: function() {
            return !0;
          },
          deregisterDocumentInteractionHandler: function() {
          },
          deregisterInteractionHandler: function() {
          },
          deregisterResizeHandler: function() {
          },
          getWindowPageOffset: function() {
            return { x: 0, y: 0 };
          },
          isSurfaceActive: function() {
            return !0;
          },
          isSurfaceDisabled: function() {
            return !0;
          },
          isUnbounded: function() {
            return !0;
          },
          registerDocumentInteractionHandler: function() {
          },
          registerInteractionHandler: function() {
          },
          registerResizeHandler: function() {
          },
          removeClass: function() {
          },
          updateCssVariable: function() {
          }
        };
      },
      enumerable: !1,
      configurable: !0
    }), e.prototype.init = function() {
      var t = this, n = this.supportsPressRipple();
      if (this.registerRootHandlers(n), n) {
        var i = e.cssClasses, s = i.ROOT, o = i.UNBOUNDED;
        requestAnimationFrame(function() {
          t.adapter.addClass(s), t.adapter.isUnbounded() && (t.adapter.addClass(o), t.layoutInternal());
        });
      }
    }, e.prototype.destroy = function() {
      var t = this;
      if (this.supportsPressRipple()) {
        this.activationTimer && (clearTimeout(this.activationTimer), this.activationTimer = 0, this.adapter.removeClass(e.cssClasses.FG_ACTIVATION)), this.fgDeactivationRemovalTimer && (clearTimeout(this.fgDeactivationRemovalTimer), this.fgDeactivationRemovalTimer = 0, this.adapter.removeClass(e.cssClasses.FG_DEACTIVATION));
        var n = e.cssClasses, i = n.ROOT, s = n.UNBOUNDED;
        requestAnimationFrame(function() {
          t.adapter.removeClass(i), t.adapter.removeClass(s), t.removeCssVars();
        });
      }
      this.deregisterRootHandlers(), this.deregisterDeactivationHandlers();
    }, e.prototype.activate = function(t) {
      this.activateImpl(t);
    }, e.prototype.deactivate = function() {
      this.deactivateImpl();
    }, e.prototype.layout = function() {
      var t = this;
      this.layoutFrame && cancelAnimationFrame(this.layoutFrame), this.layoutFrame = requestAnimationFrame(function() {
        t.layoutInternal(), t.layoutFrame = 0;
      });
    }, e.prototype.setUnbounded = function(t) {
      var n = e.cssClasses.UNBOUNDED;
      t ? this.adapter.addClass(n) : this.adapter.removeClass(n);
    }, e.prototype.handleFocus = function() {
      var t = this;
      requestAnimationFrame(function() {
        return t.adapter.addClass(e.cssClasses.BG_FOCUSED);
      });
    }, e.prototype.handleBlur = function() {
      var t = this;
      requestAnimationFrame(function() {
        return t.adapter.removeClass(e.cssClasses.BG_FOCUSED);
      });
    }, e.prototype.supportsPressRipple = function() {
      return this.adapter.browserSupportsCssVars();
    }, e.prototype.defaultActivationState = function() {
      return {
        activationEvent: void 0,
        hasDeactivationUXRun: !1,
        isActivated: !1,
        isProgrammatic: !1,
        wasActivatedByPointer: !1,
        wasElementMadeActive: !1
      };
    }, e.prototype.registerRootHandlers = function(t) {
      var n, i;
      if (t) {
        try {
          for (var s = ce(ut), o = s.next(); !o.done; o = s.next()) {
            var a = o.value;
            this.adapter.registerInteractionHandler(a, this.activateHandler);
          }
        } catch (l) {
          n = { error: l };
        } finally {
          try {
            o && !o.done && (i = s.return) && i.call(s);
          } finally {
            if (n) throw n.error;
          }
        }
        this.adapter.isUnbounded() && this.adapter.registerResizeHandler(this.resizeHandler);
      }
      this.adapter.registerInteractionHandler("focus", this.focusHandler), this.adapter.registerInteractionHandler("blur", this.blurHandler);
    }, e.prototype.registerDeactivationHandlers = function(t) {
      var n, i;
      if (t.type === "keydown")
        this.adapter.registerInteractionHandler("keyup", this.deactivateHandler);
      else
        try {
          for (var s = ce(ft), o = s.next(); !o.done; o = s.next()) {
            var a = o.value;
            this.adapter.registerDocumentInteractionHandler(a, this.deactivateHandler);
          }
        } catch (l) {
          n = { error: l };
        } finally {
          try {
            o && !o.done && (i = s.return) && i.call(s);
          } finally {
            if (n) throw n.error;
          }
        }
    }, e.prototype.deregisterRootHandlers = function() {
      var t, n;
      try {
        for (var i = ce(ut), s = i.next(); !s.done; s = i.next()) {
          var o = s.value;
          this.adapter.deregisterInteractionHandler(o, this.activateHandler);
        }
      } catch (a) {
        t = { error: a };
      } finally {
        try {
          s && !s.done && (n = i.return) && n.call(i);
        } finally {
          if (t) throw t.error;
        }
      }
      this.adapter.deregisterInteractionHandler("focus", this.focusHandler), this.adapter.deregisterInteractionHandler("blur", this.blurHandler), this.adapter.isUnbounded() && this.adapter.deregisterResizeHandler(this.resizeHandler);
    }, e.prototype.deregisterDeactivationHandlers = function() {
      var t, n;
      this.adapter.deregisterInteractionHandler("keyup", this.deactivateHandler);
      try {
        for (var i = ce(ft), s = i.next(); !s.done; s = i.next()) {
          var o = s.value;
          this.adapter.deregisterDocumentInteractionHandler(o, this.deactivateHandler);
        }
      } catch (a) {
        t = { error: a };
      } finally {
        try {
          s && !s.done && (n = i.return) && n.call(i);
        } finally {
          if (t) throw t.error;
        }
      }
    }, e.prototype.removeCssVars = function() {
      var t = this, n = e.strings, i = Object.keys(n);
      i.forEach(function(s) {
        s.indexOf("VAR_") === 0 && t.adapter.updateCssVariable(n[s], null);
      });
    }, e.prototype.activateImpl = function(t) {
      var n = this;
      if (!this.adapter.isSurfaceDisabled()) {
        var i = this.activationState;
        if (!i.isActivated) {
          var s = this.previousActivationEvent, o = s && t !== void 0 && s.type !== t.type;
          if (!o) {
            i.isActivated = !0, i.isProgrammatic = t === void 0, i.activationEvent = t, i.wasActivatedByPointer = i.isProgrammatic ? !1 : t !== void 0 && (t.type === "mousedown" || t.type === "touchstart" || t.type === "pointerdown");
            var a = t !== void 0 && Ce.length > 0 && Ce.some(function(l) {
              return n.adapter.containsEventTarget(l);
            });
            if (a) {
              this.resetActivationState();
              return;
            }
            t !== void 0 && (Ce.push(t.target), this.registerDeactivationHandlers(t)), i.wasElementMadeActive = this.checkElementMadeActive(t), i.wasElementMadeActive && this.animateActivation(), requestAnimationFrame(function() {
              Ce = [], !i.wasElementMadeActive && t !== void 0 && (t.key === " " || t.keyCode === 32) && (i.wasElementMadeActive = n.checkElementMadeActive(t), i.wasElementMadeActive && n.animateActivation()), i.wasElementMadeActive || (n.activationState = n.defaultActivationState());
            });
          }
        }
      }
    }, e.prototype.checkElementMadeActive = function(t) {
      return t !== void 0 && t.type === "keydown" ? this.adapter.isSurfaceActive() : !0;
    }, e.prototype.animateActivation = function() {
      var t = this, n = e.strings, i = n.VAR_FG_TRANSLATE_START, s = n.VAR_FG_TRANSLATE_END, o = e.cssClasses, a = o.FG_DEACTIVATION, l = o.FG_ACTIVATION, d = e.numbers.DEACTIVATION_TIMEOUT_MS;
      this.layoutInternal();
      var c = "", u = "";
      if (!this.adapter.isUnbounded()) {
        var f = this.getFgTranslationCoordinates(), h = f.startPoint, p = f.endPoint;
        c = h.x + "px, " + h.y + "px", u = p.x + "px, " + p.y + "px";
      }
      this.adapter.updateCssVariable(i, c), this.adapter.updateCssVariable(s, u), clearTimeout(this.activationTimer), clearTimeout(this.fgDeactivationRemovalTimer), this.rmBoundedActivationClasses(), this.adapter.removeClass(a), this.adapter.computeBoundingRect(), this.adapter.addClass(l), this.activationTimer = setTimeout(function() {
        t.activationTimerCallback();
      }, d);
    }, e.prototype.getFgTranslationCoordinates = function() {
      var t = this.activationState, n = t.activationEvent, i = t.wasActivatedByPointer, s;
      i ? s = $r(n, this.adapter.getWindowPageOffset(), this.adapter.computeBoundingRect()) : s = {
        x: this.frame.width / 2,
        y: this.frame.height / 2
      }, s = {
        x: s.x - this.initialSize / 2,
        y: s.y - this.initialSize / 2
      };
      var o = {
        x: this.frame.width / 2 - this.initialSize / 2,
        y: this.frame.height / 2 - this.initialSize / 2
      };
      return { startPoint: s, endPoint: o };
    }, e.prototype.runDeactivationUXLogicIfReady = function() {
      var t = this, n = e.cssClasses.FG_DEACTIVATION, i = this.activationState, s = i.hasDeactivationUXRun, o = i.isActivated, a = s || !o;
      a && this.activationAnimationHasEnded && (this.rmBoundedActivationClasses(), this.adapter.addClass(n), this.fgDeactivationRemovalTimer = setTimeout(function() {
        t.adapter.removeClass(n);
      }, dt.FG_DEACTIVATION_MS));
    }, e.prototype.rmBoundedActivationClasses = function() {
      var t = e.cssClasses.FG_ACTIVATION;
      this.adapter.removeClass(t), this.activationAnimationHasEnded = !1, this.adapter.computeBoundingRect();
    }, e.prototype.resetActivationState = function() {
      var t = this;
      this.previousActivationEvent = this.activationState.activationEvent, this.activationState = this.defaultActivationState(), setTimeout(function() {
        return t.previousActivationEvent = void 0;
      }, e.numbers.TAP_DELAY_MS);
    }, e.prototype.deactivateImpl = function() {
      var t = this, n = this.activationState;
      if (n.isActivated) {
        var i = me({}, n);
        n.isProgrammatic ? (requestAnimationFrame(function() {
          t.animateDeactivation(i);
        }), this.resetActivationState()) : (this.deregisterDeactivationHandlers(), requestAnimationFrame(function() {
          t.activationState.hasDeactivationUXRun = !0, t.animateDeactivation(i), t.resetActivationState();
        }));
      }
    }, e.prototype.animateDeactivation = function(t) {
      var n = t.wasActivatedByPointer, i = t.wasElementMadeActive;
      (n || i) && this.runDeactivationUXLogicIfReady();
    }, e.prototype.layoutInternal = function() {
      var t = this;
      this.frame = this.adapter.computeBoundingRect();
      var n = Math.max(this.frame.height, this.frame.width), i = function() {
        var o = Math.sqrt(Math.pow(t.frame.width, 2) + Math.pow(t.frame.height, 2));
        return o + e.numbers.PADDING;
      };
      this.maxRadius = this.adapter.isUnbounded() ? n : i();
      var s = Math.floor(n * e.numbers.INITIAL_ORIGIN_SCALE);
      this.adapter.isUnbounded() && s % 2 !== 0 ? this.initialSize = s - 1 : this.initialSize = s, this.fgScale = "" + this.maxRadius / this.initialSize, this.updateLayoutCssVars();
    }, e.prototype.updateLayoutCssVars = function() {
      var t = e.strings, n = t.VAR_FG_SIZE, i = t.VAR_LEFT, s = t.VAR_TOP, o = t.VAR_FG_SCALE;
      this.adapter.updateCssVariable(n, this.initialSize + "px"), this.adapter.updateCssVariable(o, this.fgScale), this.adapter.isUnbounded() && (this.unboundedCoords = {
        left: Math.round(this.frame.width / 2 - this.initialSize / 2),
        top: Math.round(this.frame.height / 2 - this.initialSize / 2)
      }, this.adapter.updateCssVariable(i, this.unboundedCoords.left + "px"), this.adapter.updateCssVariable(s, this.unboundedCoords.top + "px"));
    }, e;
  }(Yt)
);
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var fe;
(function(r) {
  r.PROCESSING = "mdc-switch--processing", r.SELECTED = "mdc-switch--selected", r.UNSELECTED = "mdc-switch--unselected";
})(fe || (fe = {}));
var pt;
(function(r) {
  r.RIPPLE = ".mdc-switch__ripple";
})(pt || (pt = {}));
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function tn(r, e, t) {
  var n = rn(r, e), i = n.getObservers(e);
  return i.push(t), function() {
    i.splice(i.indexOf(t), 1);
  };
}
var Le = /* @__PURE__ */ new WeakMap();
function rn(r, e) {
  var t = /* @__PURE__ */ new Map();
  Le.has(r) || Le.set(r, {
    isEnabled: !0,
    getObservers: function(d) {
      var c = t.get(d) || [];
      return t.has(d) || t.set(d, c), c;
    },
    installedProperties: /* @__PURE__ */ new Set()
  });
  var n = Le.get(r);
  if (n.installedProperties.has(e))
    return n;
  var i = nn(r, e) || {
    configurable: !0,
    enumerable: !0,
    value: r[e],
    writable: !0
  }, s = me({}, i), o = i.get, a = i.set;
  if ("value" in i) {
    delete s.value, delete s.writable;
    var l = i.value;
    o = function() {
      return l;
    }, i.writable && (a = function(d) {
      l = d;
    });
  }
  return o && (s.get = function() {
    return o.call(this);
  }), a && (s.set = function(d) {
    var c, u, f = o ? o.call(this) : d;
    if (a.call(this, d), n.isEnabled && (!o || d !== f))
      try {
        for (var h = ce(n.getObservers(e)), p = h.next(); !p.done; p = h.next()) {
          var g = p.value;
          g(d, f);
        }
      } catch (m) {
        c = { error: m };
      } finally {
        try {
          p && !p.done && (u = h.return) && u.call(h);
        } finally {
          if (c) throw c.error;
        }
      }
  }), n.installedProperties.add(e), Object.defineProperty(r, e, s), n;
}
function nn(r, e) {
  for (var t = r, n; t && (n = Object.getOwnPropertyDescriptor(t, e), !n); )
    t = Object.getPrototypeOf(t);
  return n;
}
function sn(r, e) {
  var t = Le.get(r);
  t && (t.isEnabled = e);
}
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var on = (
  /** @class */
  function(r) {
    Be(e, r);
    function e(t) {
      var n = r.call(this, t) || this;
      return n.unobserves = /* @__PURE__ */ new Set(), n;
    }
    return e.prototype.destroy = function() {
      r.prototype.destroy.call(this), this.unobserve();
    }, e.prototype.observe = function(t, n) {
      var i, s, o = this, a = [];
      try {
        for (var l = ce(Object.keys(n)), d = l.next(); !d.done; d = l.next()) {
          var c = d.value, u = n[c].bind(this);
          a.push(this.observeProperty(t, c, u));
        }
      } catch (h) {
        i = { error: h };
      } finally {
        try {
          d && !d.done && (s = l.return) && s.call(l);
        } finally {
          if (i) throw i.error;
        }
      }
      var f = function() {
        var h, p;
        try {
          for (var g = ce(a), m = g.next(); !m.done; m = g.next()) {
            var _ = m.value;
            _();
          }
        } catch (w) {
          h = { error: w };
        } finally {
          try {
            m && !m.done && (p = g.return) && p.call(g);
          } finally {
            if (h) throw h.error;
          }
        }
        o.unobserves.delete(f);
      };
      return this.unobserves.add(f), f;
    }, e.prototype.observeProperty = function(t, n, i) {
      return tn(t, n, i);
    }, e.prototype.setObserversEnabled = function(t, n) {
      sn(t, n);
    }, e.prototype.unobserve = function() {
      var t, n;
      try {
        for (var i = ce(Tr([], qr(this.unobserves))), s = i.next(); !s.done; s = i.next()) {
          var o = s.value;
          o();
        }
      } catch (a) {
        t = { error: a };
      } finally {
        try {
          s && !s.done && (n = i.return) && n.call(i);
        } finally {
          if (t) throw t.error;
        }
      }
    }, e;
  }(Yt)
);
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var an = (
  /** @class */
  function(r) {
    Be(e, r);
    function e(t) {
      var n = r.call(this, t) || this;
      return n.handleClick = n.handleClick.bind(n), n;
    }
    return e.prototype.init = function() {
      this.observe(this.adapter.state, {
        disabled: this.stopProcessingIfDisabled,
        processing: this.stopProcessingIfDisabled
      });
    }, e.prototype.handleClick = function() {
      this.adapter.state.disabled || (this.adapter.state.selected = !this.adapter.state.selected);
    }, e.prototype.stopProcessingIfDisabled = function() {
      this.adapter.state.disabled && (this.adapter.state.processing = !1);
    }, e;
  }(on)
), ln = (
  /** @class */
  function(r) {
    Be(e, r);
    function e() {
      return r !== null && r.apply(this, arguments) || this;
    }
    return e.prototype.init = function() {
      r.prototype.init.call(this), this.observe(this.adapter.state, {
        disabled: this.onDisabledChange,
        processing: this.onProcessingChange,
        selected: this.onSelectedChange
      });
    }, e.prototype.initFromDOM = function() {
      this.setObserversEnabled(this.adapter.state, !1), this.adapter.state.selected = this.adapter.hasClass(fe.SELECTED), this.onSelectedChange(), this.adapter.state.disabled = this.adapter.isDisabled(), this.adapter.state.processing = this.adapter.hasClass(fe.PROCESSING), this.setObserversEnabled(this.adapter.state, !0), this.stopProcessingIfDisabled();
    }, e.prototype.onDisabledChange = function() {
      this.adapter.setDisabled(this.adapter.state.disabled);
    }, e.prototype.onProcessingChange = function() {
      this.toggleClass(this.adapter.state.processing, fe.PROCESSING);
    }, e.prototype.onSelectedChange = function() {
      this.adapter.setAriaChecked(String(this.adapter.state.selected)), this.toggleClass(this.adapter.state.selected, fe.SELECTED), this.toggleClass(!this.adapter.state.selected, fe.UNSELECTED);
    }, e.prototype.toggleClass = function(t, n) {
      t ? this.adapter.addClass(n) : this.adapter.removeClass(n);
    }, e;
  }(an)
);
function Pe(r) {
  return Object.entries(r).filter(([e, t]) => e !== "" && t).map(([e]) => e).join(" ");
}
function Se(r, e, t, n = { bubbles: !0 }, i = !1) {
  if (typeof Event > "u")
    throw new Error("Event not defined.");
  if (!r)
    throw new Error("Tried to dipatch event without element.");
  const s = new CustomEvent(e, Object.assign(Object.assign({}, n), { detail: t }));
  if (r == null || r.dispatchEvent(s), i && e.startsWith("SMUI")) {
    const o = new CustomEvent(e.replace(/^SMUI/g, () => "MDC"), Object.assign(Object.assign({}, n), { detail: t }));
    r == null || r.dispatchEvent(o), o.defaultPrevented && s.preventDefault();
  }
  return s;
}
function ht(r, e) {
  let t = Object.getOwnPropertyNames(r);
  const n = {};
  for (let i = 0; i < t.length; i++) {
    const s = t[i], o = s.indexOf("$");
    o !== -1 && e.indexOf(s.substring(0, o + 1)) !== -1 || e.indexOf(s) === -1 && (n[s] = r[s]);
  }
  return n;
}
const gt = /^[a-z]+(?::(?:preventDefault|stopPropagation|passive|nonpassive|capture|once|self))+$/, cn = /^[^$]+(?:\$(?:preventDefault|stopPropagation|passive|nonpassive|capture|once|self))+$/;
function dn(r) {
  let e, t = [];
  r.$on = (i, s) => {
    let o = i, a = () => {
    };
    return e ? a = e(o, s) : t.push([o, s]), o.match(gt) && console && console.warn('Event modifiers in SMUI now use "$" instead of ":", so that all events can be bound with modifiers. Please update your event binding: ', o), () => {
      a();
    };
  };
  function n(i) {
    const s = r.$$.callbacks[i.type];
    s && s.slice().forEach((o) => o.call(this, i));
  }
  return (i) => {
    const s = [], o = {};
    e = (a, l) => {
      let d = a, c = l, u = !1;
      const f = d.match(gt), h = d.match(cn), p = f || h;
      if (d.match(/^SMUI:\w+:/)) {
        const _ = d.split(":");
        let w = "";
        for (let A = 0; A < _.length; A++)
          w += A === _.length - 1 ? ":" + _[A] : _[A].split("-").map((R) => R.slice(0, 1).toUpperCase() + R.slice(1)).join("");
        console.warn(`The event ${d.split("$")[0]} has been renamed to ${w.split("$")[0]}.`), d = w;
      }
      if (p) {
        const _ = d.split(f ? ":" : "$");
        d = _[0];
        const w = _.slice(1).reduce((A, R) => (A[R] = !0, A), {});
        w.passive && (u = u || {}, u.passive = !0), w.nonpassive && (u = u || {}, u.passive = !1), w.capture && (u = u || {}, u.capture = !0), w.once && (u = u || {}, u.once = !0), w.preventDefault && (c = un(c)), w.stopPropagation && (c = fn(c)), w.stopImmediatePropagation && (c = pn(c)), w.self && (c = hn(i, c)), w.trusted && (c = gn(c));
      }
      const g = mt(i, d, c, u), m = () => {
        g();
        const _ = s.indexOf(m);
        _ > -1 && s.splice(_, 1);
      };
      return s.push(m), d in o || (o[d] = mt(i, d, n)), m;
    };
    for (let a = 0; a < t.length; a++)
      e(t[a][0], t[a][1]);
    return {
      destroy: () => {
        for (let a = 0; a < s.length; a++)
          s[a]();
        for (let a of Object.entries(o))
          a[1]();
      }
    };
  };
}
function mt(r, e, t, n) {
  return r.addEventListener(e, t, n), () => r.removeEventListener(e, t, n);
}
function un(r) {
  return function(e) {
    return e.preventDefault(), r.call(this, e);
  };
}
function fn(r) {
  return function(e) {
    return e.stopPropagation(), r.call(this, e);
  };
}
function pn(r) {
  return function(e) {
    return e.stopImmediatePropagation(), r.call(this, e);
  };
}
function hn(r, e) {
  return function(t) {
    if (t.target === r)
      return e.call(this, t);
  };
}
function gn(r) {
  return function(e) {
    if (e.isTrusted)
      return r.call(this, e);
  };
}
function bt(r, e) {
  let t = Object.getOwnPropertyNames(r);
  const n = {};
  for (let i = 0; i < t.length; i++) {
    const s = t[i];
    s.substring(0, e.length) === e && (n[s.substring(e.length)] = r[s]);
  }
  return n;
}
function er(r, e) {
  let t = [];
  if (e)
    for (let n = 0; n < e.length; n++) {
      const i = e[n], s = Array.isArray(i) ? i[0] : i;
      Array.isArray(i) && i.length > 1 ? t.push(s(r, i[1])) : t.push(s(r));
    }
  return {
    update(n) {
      if ((n && n.length || 0) != t.length)
        throw new Error("You must not change the length of an actions array.");
      if (n)
        for (let i = 0; i < n.length; i++) {
          const s = t[i];
          if (s && s.update) {
            const o = n[i];
            Array.isArray(o) && o.length > 1 ? s.update(o[1]) : s.update();
          }
        }
    },
    destroy() {
      for (let n = 0; n < t.length; n++) {
        const i = t[n];
        i && i.destroy && i.destroy();
      }
    }
  };
}
const { getContext: mn } = window.__gradio__svelte__internal, { applyPassive: Ae } = Xr, { matches: bn } = Nr;
function _n(r, { ripple: e = !0, surface: t = !1, unbounded: n = !1, disabled: i = !1, color: s, active: o, rippleElement: a, eventTarget: l, activeTarget: d, addClass: c = (p) => r.classList.add(p), removeClass: u = (p) => r.classList.remove(p), addStyle: f = (p, g) => r.style.setProperty(p, g), initPromise: h = Promise.resolve() } = {}) {
  let p, g = mn("SMUI:addLayoutListener"), m, _ = o, w = l, A = d;
  function R() {
    t ? (c("mdc-ripple-surface"), s === "primary" ? (c("smui-ripple-surface--primary"), u("smui-ripple-surface--secondary")) : s === "secondary" ? (u("smui-ripple-surface--primary"), c("smui-ripple-surface--secondary")) : (u("smui-ripple-surface--primary"), u("smui-ripple-surface--secondary"))) : (u("mdc-ripple-surface"), u("smui-ripple-surface--primary"), u("smui-ripple-surface--secondary")), p && _ !== o && (_ = o, o ? p.activate() : o === !1 && p.deactivate()), e && !p ? (p = new en({
      addClass: c,
      browserSupportsCssVars: () => Yr(window),
      computeBoundingRect: () => (a || r).getBoundingClientRect(),
      containsEventTarget: (b) => r.contains(b),
      deregisterDocumentInteractionHandler: (b, M) => document.documentElement.removeEventListener(b, M, Ae()),
      deregisterInteractionHandler: (b, M) => (l || r).removeEventListener(b, M, Ae()),
      deregisterResizeHandler: (b) => window.removeEventListener("resize", b),
      getWindowPageOffset: () => ({
        x: window.pageXOffset,
        y: window.pageYOffset
      }),
      isSurfaceActive: () => o ?? bn(d || r, ":active"),
      isSurfaceDisabled: () => !!i,
      isUnbounded: () => !!n,
      registerDocumentInteractionHandler: (b, M) => document.documentElement.addEventListener(b, M, Ae()),
      registerInteractionHandler: (b, M) => (l || r).addEventListener(b, M, Ae()),
      registerResizeHandler: (b) => window.addEventListener("resize", b),
      removeClass: u,
      updateCssVariable: f
    }), h.then(() => {
      p && (p.init(), p.setUnbounded(n));
    })) : p && !e && h.then(() => {
      p && (p.destroy(), p = void 0);
    }), p && (w !== l || A !== d) && (w = l, A = d, p.destroy(), requestAnimationFrame(() => {
      p && (p.init(), p.setUnbounded(n));
    })), !e && n && c("mdc-ripple-upgraded--unbounded");
  }
  R(), g && (m = g(y));
  function y() {
    p && p.layout();
  }
  return {
    update(b) {
      ({
        ripple: e,
        surface: t,
        unbounded: n,
        disabled: i,
        color: s,
        active: o,
        rippleElement: a,
        eventTarget: l,
        activeTarget: d,
        addClass: c,
        removeClass: u,
        addStyle: f,
        initPromise: h
      } = Object.assign({ ripple: !0, surface: !1, unbounded: !1, disabled: !1, color: void 0, active: void 0, rippleElement: void 0, eventTarget: void 0, activeTarget: void 0, addClass: (M) => r.classList.add(M), removeClass: (M) => r.classList.remove(M), addStyle: (M, J) => r.style.setProperty(M, J), initPromise: Promise.resolve() }, b)), R();
    },
    destroy() {
      p && (p.destroy(), p = void 0, u("mdc-ripple-surface"), u("smui-ripple-surface--primary"), u("smui-ripple-surface--secondary")), m && m();
    }
  };
}
const {
  SvelteComponent: vn,
  action_destroyer: Oe,
  append: G,
  assign: Fe,
  attr: T,
  binding_callbacks: _t,
  compute_rest_props: vt,
  detach: tt,
  element: le,
  exclude_internal_props: yn,
  get_spread_update: tr,
  init: wn,
  insert: rt,
  is_function: Ze,
  listen: kn,
  noop: yt,
  run_all: Cn,
  safe_not_equal: Sn,
  set_attributes: Ie,
  space: we,
  svg_element: Me
} = window.__gradio__svelte__internal, { onMount: An, getContext: Mn } = window.__gradio__svelte__internal, { get_current_component: xn } = window.__gradio__svelte__internal;
function wt(r) {
  let e, t, n, i, s, o, a, l, d, c, u = [
    {
      class: a = Pe({
        [
          /*icons$class*/
          r[8]
        ]: !0,
        "mdc-switch__icons": !0
      })
    },
    bt(
      /*$$restProps*/
      r[19],
      "icons$"
    )
  ], f = {};
  for (let h = 0; h < u.length; h += 1)
    f = Fe(f, u[h]);
  return {
    c() {
      e = le("div"), t = Me("svg"), n = Me("path"), i = we(), s = Me("svg"), o = Me("path"), T(n, "d", "M19.69,5.23L8.96,15.96l-4.23-4.23L2.96,13.5l6,6L21.46,7L19.69,5.23z"), T(t, "class", "mdc-switch__icon mdc-switch__icon--on"), T(t, "viewBox", "0 0 24 24"), T(o, "d", "M20 13H4v-2h16v2z"), T(s, "class", "mdc-switch__icon mdc-switch__icon--off"), T(s, "viewBox", "0 0 24 24"), Ie(e, f);
    },
    m(h, p) {
      rt(h, e, p), G(e, t), G(t, n), G(e, i), G(e, s), G(s, o), d || (c = Oe(l = er.call(
        null,
        e,
        /*icons$use*/
        r[7]
      )), d = !0);
    },
    p(h, p) {
      Ie(e, f = tr(u, [
        p[0] & /*icons$class*/
        256 && a !== (a = Pe({
          [
            /*icons$class*/
            h[8]
          ]: !0,
          "mdc-switch__icons": !0
        })) && { class: a },
        p[0] & /*$$restProps*/
        524288 && bt(
          /*$$restProps*/
          h[19],
          "icons$"
        )
      ])), l && Ze(l.update) && p[0] & /*icons$use*/
      128 && l.update.call(
        null,
        /*icons$use*/
        h[7]
      );
    },
    d(h) {
      h && tt(e), d = !1, c();
    }
  };
}
function kt(r) {
  let e;
  return {
    c() {
      e = le("div"), e.innerHTML = '<div class="mdc-switch__focus-ring"></div>', T(e, "class", "mdc-switch__focus-ring-wrapper");
    },
    m(t, n) {
      rt(t, e, n);
    },
    d(t) {
      t && tt(e);
    }
  };
}
function Rn(r) {
  let e, t, n, i, s, o, a, l, d, c, u, f, h, p, g, m, _ = (
    /*icons*/
    r[6] && wt(r)
  ), w = (
    /*focusRing*/
    r[4] && kt()
  ), A = [
    {
      class: u = Pe({
        [
          /*className*/
          r[3]
        ]: !0,
        "mdc-switch": !0,
        "mdc-switch--unselected": !/*selected*/
        r[10],
        "mdc-switch--selected": (
          /*selected*/
          r[10]
        ),
        "mdc-switch--processing": (
          /*processing*/
          r[1]
        ),
        "smui-switch--color-secondary": (
          /*color*/
          r[5] === "secondary"
        ),
        .../*internalClasses*/
        r[12]
      })
    },
    { type: "button" },
    { role: "switch" },
    {
      "aria-checked": f = /*selected*/
      r[10] ? "true" : "false"
    },
    { disabled: (
      /*disabled*/
      r[0]
    ) },
    /*inputProps*/
    r[16],
    ht(
      /*$$restProps*/
      r[19],
      ["icons$"]
    )
  ], R = {};
  for (let y = 0; y < A.length; y += 1)
    R = Fe(R, A[y]);
  return {
    c() {
      e = le("button"), t = le("div"), n = we(), i = le("div"), s = le("div"), o = le("div"), o.innerHTML = '<div class="mdc-elevation-overlay"></div>', a = we(), l = le("div"), d = we(), _ && _.c(), c = we(), w && w.c(), T(t, "class", "mdc-switch__track"), T(o, "class", "mdc-switch__shadow"), T(l, "class", "mdc-switch__ripple"), T(s, "class", "mdc-switch__handle"), T(i, "class", "mdc-switch__handle-track"), Ie(e, R);
    },
    m(y, b) {
      rt(y, e, b), G(e, t), G(e, n), G(e, i), G(i, s), G(s, o), G(s, a), G(s, l), r[28](l), G(s, d), _ && _.m(s, null), G(e, c), w && w.m(e, null), e.autofocus && e.focus(), r[29](e), g || (m = [
        Oe(h = er.call(
          null,
          e,
          /*use*/
          r[2]
        )),
        Oe(
          /*forwardEvents*/
          r[15].call(null, e)
        ),
        Oe(p = _n.call(null, e, {
          unbounded: !0,
          color: (
            /*color*/
            r[5]
          ),
          active: (
            /*rippleActive*/
            r[14]
          ),
          rippleElement: (
            /*rippleElement*/
            r[13]
          ),
          disabled: (
            /*disabled*/
            r[0]
          ),
          addClass: (
            /*addClass*/
            r[17]
          ),
          removeClass: (
            /*removeClass*/
            r[18]
          )
        })),
        kn(
          e,
          "click",
          /*click_handler*/
          r[30]
        )
      ], g = !0);
    },
    p(y, b) {
      /*icons*/
      y[6] ? _ ? _.p(y, b) : (_ = wt(y), _.c(), _.m(s, null)) : _ && (_.d(1), _ = null), /*focusRing*/
      y[4] ? w || (w = kt(), w.c(), w.m(e, null)) : w && (w.d(1), w = null), Ie(e, R = tr(A, [
        b[0] & /*className, selected, processing, color, internalClasses*/
        5162 && u !== (u = Pe({
          [
            /*className*/
            y[3]
          ]: !0,
          "mdc-switch": !0,
          "mdc-switch--unselected": !/*selected*/
          y[10],
          "mdc-switch--selected": (
            /*selected*/
            y[10]
          ),
          "mdc-switch--processing": (
            /*processing*/
            y[1]
          ),
          "smui-switch--color-secondary": (
            /*color*/
            y[5] === "secondary"
          ),
          .../*internalClasses*/
          y[12]
        })) && { class: u },
        { type: "button" },
        { role: "switch" },
        b[0] & /*selected*/
        1024 && f !== (f = /*selected*/
        y[10] ? "true" : "false") && {
          "aria-checked": f
        },
        b[0] & /*disabled*/
        1 && { disabled: (
          /*disabled*/
          y[0]
        ) },
        /*inputProps*/
        y[16],
        b[0] & /*$$restProps*/
        524288 && ht(
          /*$$restProps*/
          y[19],
          ["icons$"]
        )
      ])), h && Ze(h.update) && b[0] & /*use*/
      4 && h.update.call(
        null,
        /*use*/
        y[2]
      ), p && Ze(p.update) && b[0] & /*color, rippleActive, rippleElement, disabled*/
      24609 && p.update.call(null, {
        unbounded: !0,
        color: (
          /*color*/
          y[5]
        ),
        active: (
          /*rippleActive*/
          y[14]
        ),
        rippleElement: (
          /*rippleElement*/
          y[13]
        ),
        disabled: (
          /*disabled*/
          y[0]
        ),
        addClass: (
          /*addClass*/
          y[17]
        ),
        removeClass: (
          /*removeClass*/
          y[18]
        )
      });
    },
    i: yt,
    o: yt,
    d(y) {
      y && tt(e), r[28](null), _ && _.d(), w && w.d(), r[29](null), g = !1, Cn(m);
    }
  };
}
function zn(r, e, t) {
  const n = [
    "use",
    "class",
    "disabled",
    "focusRing",
    "color",
    "group",
    "checked",
    "value",
    "processing",
    "icons",
    "icons$use",
    "icons$class",
    "getId",
    "getElement"
  ];
  let i = vt(e, n);
  var s;
  const o = dn(xn());
  let a = () => {
  };
  function l(v) {
    return v === a;
  }
  let { use: d = [] } = e, { class: c = "" } = e, { disabled: u = !1 } = e, { focusRing: f = !1 } = e, { color: h = "primary" } = e, { group: p = a } = e, { checked: g = a } = e, { value: m = null } = e, { processing: _ = !1 } = e, { icons: w = !0 } = e, { icons$use: A = [] } = e, { icons$class: R = "" } = e, y, b, M = {}, J, Y = !1, $ = (s = Mn("SMUI:generic:input:props")) !== null && s !== void 0 ? s : {}, L = l(p) ? l(g) ? !1 : g : p.indexOf(m) !== -1, S = {
    get disabled() {
      return u;
    },
    set disabled(v) {
      t(0, u = v);
    },
    get processing() {
      return _;
    },
    set processing(v) {
      t(1, _ = v);
    },
    get selected() {
      return L;
    },
    set selected(v) {
      t(10, L = v);
    }
  }, k = g, D = l(p) ? [] : [...p], I = L;
  An(() => {
    t(11, b = new ln({
      addClass: ue,
      hasClass: Z,
      isDisabled: () => u,
      removeClass: j,
      setAriaChecked: () => {
      },
      // Handled automatically.
      setDisabled: (q) => {
        t(0, u = q);
      },
      state: S
    }));
    const v = {
      get element() {
        return ne();
      },
      get checked() {
        return L;
      },
      set checked(q) {
        L !== q && (S.selected = q, y && Se(y, "SMUISwitch:change", { selected: q, value: m }));
      },
      activateRipple() {
        u || t(14, Y = !0);
      },
      deactivateRipple() {
        t(14, Y = !1);
      }
    };
    return Se(y, "SMUIGenericInput:mount", v), b.init(), b.initFromDOM(), () => {
      Se(y, "SMUIGenericInput:unmount", v), b.destroy();
    };
  });
  function Z(v) {
    return v in M ? M[v] : ne().classList.contains(v);
  }
  function ue(v) {
    M[v] || t(12, M[v] = !0, M);
  }
  function j(v) {
    (!(v in M) || M[v]) && t(12, M[v] = !1, M);
  }
  function B() {
    return $ && $.id;
  }
  function ne() {
    return y;
  }
  function ee(v) {
    _t[v ? "unshift" : "push"](() => {
      J = v, t(13, J);
    });
  }
  function N(v) {
    _t[v ? "unshift" : "push"](() => {
      y = v, t(9, y);
    });
  }
  const te = () => b && b.handleClick();
  return r.$$set = (v) => {
    e = Fe(Fe({}, e), yn(v)), t(19, i = vt(e, n)), "use" in v && t(2, d = v.use), "class" in v && t(3, c = v.class), "disabled" in v && t(0, u = v.disabled), "focusRing" in v && t(4, f = v.focusRing), "color" in v && t(5, h = v.color), "group" in v && t(20, p = v.group), "checked" in v && t(21, g = v.checked), "value" in v && t(22, m = v.value), "processing" in v && t(1, _ = v.processing), "icons" in v && t(6, w = v.icons), "icons$use" in v && t(7, A = v.icons$use), "icons$class" in v && t(8, R = v.icons$class);
  }, r.$$.update = () => {
    if (r.$$.dirty[0] & /*group, previousSelected, selected, value, previousGroup, checked, previousChecked, element*/
    242222592) {
      let v = !1;
      if (!l(p))
        if (I !== L) {
          const q = p.indexOf(m);
          L && q === -1 ? (p.push(m), t(20, p), t(27, I), t(10, L), t(22, m), t(26, D), t(21, g), t(25, k), t(9, y)) : !L && q !== -1 && (p.splice(q, 1), t(20, p), t(27, I), t(10, L), t(22, m), t(26, D), t(21, g), t(25, k), t(9, y)), v = !0;
        } else {
          const q = D.indexOf(m), at = p.indexOf(m);
          q > -1 && at === -1 ? S.selected = !1 : at > -1 && q === -1 && (S.selected = !0);
        }
      l(g) ? I !== L && (v = !0) : g !== L && (g === k ? (t(21, g = L), v = !0) : S.selected = g), t(25, k = g), t(26, D = l(p) ? [] : [...p]), t(27, I = L), v && y && Se(y, "SMUISwitch:change", { selected: L, value: m });
    }
  }, [
    u,
    _,
    d,
    c,
    f,
    h,
    w,
    A,
    R,
    y,
    L,
    b,
    M,
    J,
    Y,
    o,
    $,
    ue,
    j,
    i,
    p,
    g,
    m,
    B,
    ne,
    k,
    D,
    I,
    ee,
    N,
    te
  ];
}
class Dn extends vn {
  constructor(e) {
    super(), wn(
      this,
      e,
      zn,
      Rn,
      Sn,
      {
        use: 2,
        class: 3,
        disabled: 0,
        focusRing: 4,
        color: 5,
        group: 20,
        checked: 21,
        value: 22,
        processing: 1,
        icons: 6,
        icons$use: 7,
        icons$class: 8,
        getId: 23,
        getElement: 24
      },
      null,
      [-1, -1]
    );
  }
  get getId() {
    return this.$$.ctx[23];
  }
  get getElement() {
    return this.$$.ctx[24];
  }
}
const nt = "-";
function Ln(r) {
  const e = Pn(r), {
    conflictingClassGroups: t,
    conflictingClassGroupModifiers: n
  } = r;
  function i(o) {
    const a = o.split(nt);
    return a[0] === "" && a.length !== 1 && a.shift(), rr(a, e) || On(o);
  }
  function s(o, a) {
    const l = t[o] || [];
    return a && n[o] ? [...l, ...n[o]] : l;
  }
  return {
    getClassGroupId: i,
    getConflictingClassGroupIds: s
  };
}
function rr(r, e) {
  var o;
  if (r.length === 0)
    return e.classGroupId;
  const t = r[0], n = e.nextPart.get(t), i = n ? rr(r.slice(1), n) : void 0;
  if (i)
    return i;
  if (e.validators.length === 0)
    return;
  const s = r.join(nt);
  return (o = e.validators.find(({
    validator: a
  }) => a(s))) == null ? void 0 : o.classGroupId;
}
const Ct = /^\[(.+)\]$/;
function On(r) {
  if (Ct.test(r)) {
    const e = Ct.exec(r)[1], t = e == null ? void 0 : e.substring(0, e.indexOf(":"));
    if (t)
      return "arbitrary.." + t;
  }
}
function Pn(r) {
  const {
    theme: e,
    prefix: t
  } = r, n = {
    nextPart: /* @__PURE__ */ new Map(),
    validators: []
  };
  return In(Object.entries(r.classGroups), t).forEach(([s, o]) => {
    Je(o, n, s, e);
  }), n;
}
function Je(r, e, t, n) {
  r.forEach((i) => {
    if (typeof i == "string") {
      const s = i === "" ? e : St(e, i);
      s.classGroupId = t;
      return;
    }
    if (typeof i == "function") {
      if (Fn(i)) {
        Je(i(n), e, t, n);
        return;
      }
      e.validators.push({
        validator: i,
        classGroupId: t
      });
      return;
    }
    Object.entries(i).forEach(([s, o]) => {
      Je(o, St(e, s), t, n);
    });
  });
}
function St(r, e) {
  let t = r;
  return e.split(nt).forEach((n) => {
    t.nextPart.has(n) || t.nextPart.set(n, {
      nextPart: /* @__PURE__ */ new Map(),
      validators: []
    }), t = t.nextPart.get(n);
  }), t;
}
function Fn(r) {
  return r.isThemeGetter;
}
function In(r, e) {
  return e ? r.map(([t, n]) => {
    const i = n.map((s) => typeof s == "string" ? e + s : typeof s == "object" ? Object.fromEntries(Object.entries(s).map(([o, a]) => [e + o, a])) : s);
    return [t, i];
  }) : r;
}
function Hn(r) {
  if (r < 1)
    return {
      get: () => {
      },
      set: () => {
      }
    };
  let e = 0, t = /* @__PURE__ */ new Map(), n = /* @__PURE__ */ new Map();
  function i(s, o) {
    t.set(s, o), e++, e > r && (e = 0, n = t, t = /* @__PURE__ */ new Map());
  }
  return {
    get(s) {
      let o = t.get(s);
      if (o !== void 0)
        return o;
      if ((o = n.get(s)) !== void 0)
        return i(s, o), o;
    },
    set(s, o) {
      t.has(s) ? t.set(s, o) : i(s, o);
    }
  };
}
const nr = "!";
function En(r) {
  const {
    separator: e,
    experimentalParseClassName: t
  } = r, n = e.length === 1, i = e[0], s = e.length;
  function o(a) {
    const l = [];
    let d = 0, c = 0, u;
    for (let m = 0; m < a.length; m++) {
      let _ = a[m];
      if (d === 0) {
        if (_ === i && (n || a.slice(m, m + s) === e)) {
          l.push(a.slice(c, m)), c = m + s;
          continue;
        }
        if (_ === "/") {
          u = m;
          continue;
        }
      }
      _ === "[" ? d++ : _ === "]" && d--;
    }
    const f = l.length === 0 ? a : a.substring(c), h = f.startsWith(nr), p = h ? f.substring(1) : f, g = u && u > c ? u - c : void 0;
    return {
      modifiers: l,
      hasImportantModifier: h,
      baseClassName: p,
      maybePostfixModifierPosition: g
    };
  }
  return t ? function(l) {
    return t({
      className: l,
      parseClassName: o
    });
  } : o;
}
function Gn(r) {
  if (r.length <= 1)
    return r;
  const e = [];
  let t = [];
  return r.forEach((n) => {
    n[0] === "[" ? (e.push(...t.sort(), n), t = []) : t.push(n);
  }), e.push(...t.sort()), e;
}
function Un(r) {
  return {
    cache: Hn(r.cacheSize),
    parseClassName: En(r),
    ...Ln(r)
  };
}
const jn = /\s+/;
function Bn(r, e) {
  const {
    parseClassName: t,
    getClassGroupId: n,
    getConflictingClassGroupIds: i
  } = e, s = /* @__PURE__ */ new Set();
  return r.trim().split(jn).map((o) => {
    const {
      modifiers: a,
      hasImportantModifier: l,
      baseClassName: d,
      maybePostfixModifierPosition: c
    } = t(o);
    let u = !!c, f = n(u ? d.substring(0, c) : d);
    if (!f) {
      if (!u)
        return {
          isTailwindClass: !1,
          originalClassName: o
        };
      if (f = n(d), !f)
        return {
          isTailwindClass: !1,
          originalClassName: o
        };
      u = !1;
    }
    const h = Gn(a).join(":");
    return {
      isTailwindClass: !0,
      modifierId: l ? h + nr : h,
      classGroupId: f,
      originalClassName: o,
      hasPostfixModifier: u
    };
  }).reverse().filter((o) => {
    if (!o.isTailwindClass)
      return !0;
    const {
      modifierId: a,
      classGroupId: l,
      hasPostfixModifier: d
    } = o, c = a + l;
    return s.has(c) ? !1 : (s.add(c), i(l, d).forEach((u) => s.add(a + u)), !0);
  }).reverse().map((o) => o.originalClassName).join(" ");
}
function Ne() {
  let r = 0, e, t, n = "";
  for (; r < arguments.length; )
    (e = arguments[r++]) && (t = ir(e)) && (n && (n += " "), n += t);
  return n;
}
function ir(r) {
  if (typeof r == "string")
    return r;
  let e, t = "";
  for (let n = 0; n < r.length; n++)
    r[n] && (e = ir(r[n])) && (t && (t += " "), t += e);
  return t;
}
function qn(r, ...e) {
  let t, n, i, s = o;
  function o(l) {
    const d = e.reduce((c, u) => u(c), r());
    return t = Un(d), n = t.cache.get, i = t.cache.set, s = a, a(l);
  }
  function a(l) {
    const d = n(l);
    if (d)
      return d;
    const c = Bn(l, t);
    return i(l, c), c;
  }
  return function() {
    return s(Ne.apply(null, arguments));
  };
}
function z(r) {
  const e = (t) => t[r] || [];
  return e.isThemeGetter = !0, e;
}
const sr = /^\[(?:([a-z-]+):)?(.+)\]$/i, Tn = /^\d+\/\d+$/, Wn = /* @__PURE__ */ new Set(["px", "full", "screen"]), Vn = /^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$/, Xn = /\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)|^0$/, Zn = /^(rgba?|hsla?|hwb|(ok)?(lab|lch))\(.+\)$/, Jn = /^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)/, Nn = /^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$/;
function re(r) {
  return pe(r) || Wn.has(r) || Tn.test(r);
}
function ie(r) {
  return be(r, "length", ni);
}
function pe(r) {
  return !!r && !Number.isNaN(Number(r));
}
function xe(r) {
  return be(r, "number", pe);
}
function _e(r) {
  return !!r && Number.isInteger(Number(r));
}
function Kn(r) {
  return r.endsWith("%") && pe(r.slice(0, -1));
}
function C(r) {
  return sr.test(r);
}
function se(r) {
  return Vn.test(r);
}
const Qn = /* @__PURE__ */ new Set(["length", "size", "percentage"]);
function Yn(r) {
  return be(r, Qn, or);
}
function $n(r) {
  return be(r, "position", or);
}
const ei = /* @__PURE__ */ new Set(["image", "url"]);
function ti(r) {
  return be(r, ei, si);
}
function ri(r) {
  return be(r, "", ii);
}
function ve() {
  return !0;
}
function be(r, e, t) {
  const n = sr.exec(r);
  return n ? n[1] ? typeof e == "string" ? n[1] === e : e.has(n[1]) : t(n[2]) : !1;
}
function ni(r) {
  return Xn.test(r) && !Zn.test(r);
}
function or() {
  return !1;
}
function ii(r) {
  return Jn.test(r);
}
function si(r) {
  return Nn.test(r);
}
function oi() {
  const r = z("colors"), e = z("spacing"), t = z("blur"), n = z("brightness"), i = z("borderColor"), s = z("borderRadius"), o = z("borderSpacing"), a = z("borderWidth"), l = z("contrast"), d = z("grayscale"), c = z("hueRotate"), u = z("invert"), f = z("gap"), h = z("gradientColorStops"), p = z("gradientColorStopPositions"), g = z("inset"), m = z("margin"), _ = z("opacity"), w = z("padding"), A = z("saturate"), R = z("scale"), y = z("sepia"), b = z("skew"), M = z("space"), J = z("translate"), Y = () => ["auto", "contain", "none"], $ = () => ["auto", "hidden", "clip", "visible", "scroll"], L = () => ["auto", C, e], S = () => [C, e], k = () => ["", re, ie], D = () => ["auto", pe, C], I = () => ["bottom", "center", "left", "left-bottom", "left-top", "right", "right-bottom", "right-top", "top"], Z = () => ["solid", "dashed", "dotted", "double", "none"], ue = () => ["normal", "multiply", "screen", "overlay", "darken", "lighten", "color-dodge", "color-burn", "hard-light", "soft-light", "difference", "exclusion", "hue", "saturation", "color", "luminosity"], j = () => ["start", "end", "center", "between", "around", "evenly", "stretch"], B = () => ["", "0", C], ne = () => ["auto", "avoid", "all", "avoid-page", "page", "left", "right", "column"], ee = () => [pe, xe], N = () => [pe, C];
  return {
    cacheSize: 500,
    separator: ":",
    theme: {
      colors: [ve],
      spacing: [re, ie],
      blur: ["none", "", se, C],
      brightness: ee(),
      borderColor: [r],
      borderRadius: ["none", "", "full", se, C],
      borderSpacing: S(),
      borderWidth: k(),
      contrast: ee(),
      grayscale: B(),
      hueRotate: N(),
      invert: B(),
      gap: S(),
      gradientColorStops: [r],
      gradientColorStopPositions: [Kn, ie],
      inset: L(),
      margin: L(),
      opacity: ee(),
      padding: S(),
      saturate: ee(),
      scale: ee(),
      sepia: B(),
      skew: N(),
      space: S(),
      translate: S()
    },
    classGroups: {
      // Layout
      /**
       * Aspect Ratio
       * @see https://tailwindcss.com/docs/aspect-ratio
       */
      aspect: [{
        aspect: ["auto", "square", "video", C]
      }],
      /**
       * Container
       * @see https://tailwindcss.com/docs/container
       */
      container: ["container"],
      /**
       * Columns
       * @see https://tailwindcss.com/docs/columns
       */
      columns: [{
        columns: [se]
      }],
      /**
       * Break After
       * @see https://tailwindcss.com/docs/break-after
       */
      "break-after": [{
        "break-after": ne()
      }],
      /**
       * Break Before
       * @see https://tailwindcss.com/docs/break-before
       */
      "break-before": [{
        "break-before": ne()
      }],
      /**
       * Break Inside
       * @see https://tailwindcss.com/docs/break-inside
       */
      "break-inside": [{
        "break-inside": ["auto", "avoid", "avoid-page", "avoid-column"]
      }],
      /**
       * Box Decoration Break
       * @see https://tailwindcss.com/docs/box-decoration-break
       */
      "box-decoration": [{
        "box-decoration": ["slice", "clone"]
      }],
      /**
       * Box Sizing
       * @see https://tailwindcss.com/docs/box-sizing
       */
      box: [{
        box: ["border", "content"]
      }],
      /**
       * Display
       * @see https://tailwindcss.com/docs/display
       */
      display: ["block", "inline-block", "inline", "flex", "inline-flex", "table", "inline-table", "table-caption", "table-cell", "table-column", "table-column-group", "table-footer-group", "table-header-group", "table-row-group", "table-row", "flow-root", "grid", "inline-grid", "contents", "list-item", "hidden"],
      /**
       * Floats
       * @see https://tailwindcss.com/docs/float
       */
      float: [{
        float: ["right", "left", "none", "start", "end"]
      }],
      /**
       * Clear
       * @see https://tailwindcss.com/docs/clear
       */
      clear: [{
        clear: ["left", "right", "both", "none", "start", "end"]
      }],
      /**
       * Isolation
       * @see https://tailwindcss.com/docs/isolation
       */
      isolation: ["isolate", "isolation-auto"],
      /**
       * Object Fit
       * @see https://tailwindcss.com/docs/object-fit
       */
      "object-fit": [{
        object: ["contain", "cover", "fill", "none", "scale-down"]
      }],
      /**
       * Object Position
       * @see https://tailwindcss.com/docs/object-position
       */
      "object-position": [{
        object: [...I(), C]
      }],
      /**
       * Overflow
       * @see https://tailwindcss.com/docs/overflow
       */
      overflow: [{
        overflow: $()
      }],
      /**
       * Overflow X
       * @see https://tailwindcss.com/docs/overflow
       */
      "overflow-x": [{
        "overflow-x": $()
      }],
      /**
       * Overflow Y
       * @see https://tailwindcss.com/docs/overflow
       */
      "overflow-y": [{
        "overflow-y": $()
      }],
      /**
       * Overscroll Behavior
       * @see https://tailwindcss.com/docs/overscroll-behavior
       */
      overscroll: [{
        overscroll: Y()
      }],
      /**
       * Overscroll Behavior X
       * @see https://tailwindcss.com/docs/overscroll-behavior
       */
      "overscroll-x": [{
        "overscroll-x": Y()
      }],
      /**
       * Overscroll Behavior Y
       * @see https://tailwindcss.com/docs/overscroll-behavior
       */
      "overscroll-y": [{
        "overscroll-y": Y()
      }],
      /**
       * Position
       * @see https://tailwindcss.com/docs/position
       */
      position: ["static", "fixed", "absolute", "relative", "sticky"],
      /**
       * Top / Right / Bottom / Left
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      inset: [{
        inset: [g]
      }],
      /**
       * Right / Left
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      "inset-x": [{
        "inset-x": [g]
      }],
      /**
       * Top / Bottom
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      "inset-y": [{
        "inset-y": [g]
      }],
      /**
       * Start
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      start: [{
        start: [g]
      }],
      /**
       * End
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      end: [{
        end: [g]
      }],
      /**
       * Top
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      top: [{
        top: [g]
      }],
      /**
       * Right
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      right: [{
        right: [g]
      }],
      /**
       * Bottom
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      bottom: [{
        bottom: [g]
      }],
      /**
       * Left
       * @see https://tailwindcss.com/docs/top-right-bottom-left
       */
      left: [{
        left: [g]
      }],
      /**
       * Visibility
       * @see https://tailwindcss.com/docs/visibility
       */
      visibility: ["visible", "invisible", "collapse"],
      /**
       * Z-Index
       * @see https://tailwindcss.com/docs/z-index
       */
      z: [{
        z: ["auto", _e, C]
      }],
      // Flexbox and Grid
      /**
       * Flex Basis
       * @see https://tailwindcss.com/docs/flex-basis
       */
      basis: [{
        basis: L()
      }],
      /**
       * Flex Direction
       * @see https://tailwindcss.com/docs/flex-direction
       */
      "flex-direction": [{
        flex: ["row", "row-reverse", "col", "col-reverse"]
      }],
      /**
       * Flex Wrap
       * @see https://tailwindcss.com/docs/flex-wrap
       */
      "flex-wrap": [{
        flex: ["wrap", "wrap-reverse", "nowrap"]
      }],
      /**
       * Flex
       * @see https://tailwindcss.com/docs/flex
       */
      flex: [{
        flex: ["1", "auto", "initial", "none", C]
      }],
      /**
       * Flex Grow
       * @see https://tailwindcss.com/docs/flex-grow
       */
      grow: [{
        grow: B()
      }],
      /**
       * Flex Shrink
       * @see https://tailwindcss.com/docs/flex-shrink
       */
      shrink: [{
        shrink: B()
      }],
      /**
       * Order
       * @see https://tailwindcss.com/docs/order
       */
      order: [{
        order: ["first", "last", "none", _e, C]
      }],
      /**
       * Grid Template Columns
       * @see https://tailwindcss.com/docs/grid-template-columns
       */
      "grid-cols": [{
        "grid-cols": [ve]
      }],
      /**
       * Grid Column Start / End
       * @see https://tailwindcss.com/docs/grid-column
       */
      "col-start-end": [{
        col: ["auto", {
          span: ["full", _e, C]
        }, C]
      }],
      /**
       * Grid Column Start
       * @see https://tailwindcss.com/docs/grid-column
       */
      "col-start": [{
        "col-start": D()
      }],
      /**
       * Grid Column End
       * @see https://tailwindcss.com/docs/grid-column
       */
      "col-end": [{
        "col-end": D()
      }],
      /**
       * Grid Template Rows
       * @see https://tailwindcss.com/docs/grid-template-rows
       */
      "grid-rows": [{
        "grid-rows": [ve]
      }],
      /**
       * Grid Row Start / End
       * @see https://tailwindcss.com/docs/grid-row
       */
      "row-start-end": [{
        row: ["auto", {
          span: [_e, C]
        }, C]
      }],
      /**
       * Grid Row Start
       * @see https://tailwindcss.com/docs/grid-row
       */
      "row-start": [{
        "row-start": D()
      }],
      /**
       * Grid Row End
       * @see https://tailwindcss.com/docs/grid-row
       */
      "row-end": [{
        "row-end": D()
      }],
      /**
       * Grid Auto Flow
       * @see https://tailwindcss.com/docs/grid-auto-flow
       */
      "grid-flow": [{
        "grid-flow": ["row", "col", "dense", "row-dense", "col-dense"]
      }],
      /**
       * Grid Auto Columns
       * @see https://tailwindcss.com/docs/grid-auto-columns
       */
      "auto-cols": [{
        "auto-cols": ["auto", "min", "max", "fr", C]
      }],
      /**
       * Grid Auto Rows
       * @see https://tailwindcss.com/docs/grid-auto-rows
       */
      "auto-rows": [{
        "auto-rows": ["auto", "min", "max", "fr", C]
      }],
      /**
       * Gap
       * @see https://tailwindcss.com/docs/gap
       */
      gap: [{
        gap: [f]
      }],
      /**
       * Gap X
       * @see https://tailwindcss.com/docs/gap
       */
      "gap-x": [{
        "gap-x": [f]
      }],
      /**
       * Gap Y
       * @see https://tailwindcss.com/docs/gap
       */
      "gap-y": [{
        "gap-y": [f]
      }],
      /**
       * Justify Content
       * @see https://tailwindcss.com/docs/justify-content
       */
      "justify-content": [{
        justify: ["normal", ...j()]
      }],
      /**
       * Justify Items
       * @see https://tailwindcss.com/docs/justify-items
       */
      "justify-items": [{
        "justify-items": ["start", "end", "center", "stretch"]
      }],
      /**
       * Justify Self
       * @see https://tailwindcss.com/docs/justify-self
       */
      "justify-self": [{
        "justify-self": ["auto", "start", "end", "center", "stretch"]
      }],
      /**
       * Align Content
       * @see https://tailwindcss.com/docs/align-content
       */
      "align-content": [{
        content: ["normal", ...j(), "baseline"]
      }],
      /**
       * Align Items
       * @see https://tailwindcss.com/docs/align-items
       */
      "align-items": [{
        items: ["start", "end", "center", "baseline", "stretch"]
      }],
      /**
       * Align Self
       * @see https://tailwindcss.com/docs/align-self
       */
      "align-self": [{
        self: ["auto", "start", "end", "center", "stretch", "baseline"]
      }],
      /**
       * Place Content
       * @see https://tailwindcss.com/docs/place-content
       */
      "place-content": [{
        "place-content": [...j(), "baseline"]
      }],
      /**
       * Place Items
       * @see https://tailwindcss.com/docs/place-items
       */
      "place-items": [{
        "place-items": ["start", "end", "center", "baseline", "stretch"]
      }],
      /**
       * Place Self
       * @see https://tailwindcss.com/docs/place-self
       */
      "place-self": [{
        "place-self": ["auto", "start", "end", "center", "stretch"]
      }],
      // Spacing
      /**
       * Padding
       * @see https://tailwindcss.com/docs/padding
       */
      p: [{
        p: [w]
      }],
      /**
       * Padding X
       * @see https://tailwindcss.com/docs/padding
       */
      px: [{
        px: [w]
      }],
      /**
       * Padding Y
       * @see https://tailwindcss.com/docs/padding
       */
      py: [{
        py: [w]
      }],
      /**
       * Padding Start
       * @see https://tailwindcss.com/docs/padding
       */
      ps: [{
        ps: [w]
      }],
      /**
       * Padding End
       * @see https://tailwindcss.com/docs/padding
       */
      pe: [{
        pe: [w]
      }],
      /**
       * Padding Top
       * @see https://tailwindcss.com/docs/padding
       */
      pt: [{
        pt: [w]
      }],
      /**
       * Padding Right
       * @see https://tailwindcss.com/docs/padding
       */
      pr: [{
        pr: [w]
      }],
      /**
       * Padding Bottom
       * @see https://tailwindcss.com/docs/padding
       */
      pb: [{
        pb: [w]
      }],
      /**
       * Padding Left
       * @see https://tailwindcss.com/docs/padding
       */
      pl: [{
        pl: [w]
      }],
      /**
       * Margin
       * @see https://tailwindcss.com/docs/margin
       */
      m: [{
        m: [m]
      }],
      /**
       * Margin X
       * @see https://tailwindcss.com/docs/margin
       */
      mx: [{
        mx: [m]
      }],
      /**
       * Margin Y
       * @see https://tailwindcss.com/docs/margin
       */
      my: [{
        my: [m]
      }],
      /**
       * Margin Start
       * @see https://tailwindcss.com/docs/margin
       */
      ms: [{
        ms: [m]
      }],
      /**
       * Margin End
       * @see https://tailwindcss.com/docs/margin
       */
      me: [{
        me: [m]
      }],
      /**
       * Margin Top
       * @see https://tailwindcss.com/docs/margin
       */
      mt: [{
        mt: [m]
      }],
      /**
       * Margin Right
       * @see https://tailwindcss.com/docs/margin
       */
      mr: [{
        mr: [m]
      }],
      /**
       * Margin Bottom
       * @see https://tailwindcss.com/docs/margin
       */
      mb: [{
        mb: [m]
      }],
      /**
       * Margin Left
       * @see https://tailwindcss.com/docs/margin
       */
      ml: [{
        ml: [m]
      }],
      /**
       * Space Between X
       * @see https://tailwindcss.com/docs/space
       */
      "space-x": [{
        "space-x": [M]
      }],
      /**
       * Space Between X Reverse
       * @see https://tailwindcss.com/docs/space
       */
      "space-x-reverse": ["space-x-reverse"],
      /**
       * Space Between Y
       * @see https://tailwindcss.com/docs/space
       */
      "space-y": [{
        "space-y": [M]
      }],
      /**
       * Space Between Y Reverse
       * @see https://tailwindcss.com/docs/space
       */
      "space-y-reverse": ["space-y-reverse"],
      // Sizing
      /**
       * Width
       * @see https://tailwindcss.com/docs/width
       */
      w: [{
        w: ["auto", "min", "max", "fit", "svw", "lvw", "dvw", C, e]
      }],
      /**
       * Min-Width
       * @see https://tailwindcss.com/docs/min-width
       */
      "min-w": [{
        "min-w": [C, e, "min", "max", "fit"]
      }],
      /**
       * Max-Width
       * @see https://tailwindcss.com/docs/max-width
       */
      "max-w": [{
        "max-w": [C, e, "none", "full", "min", "max", "fit", "prose", {
          screen: [se]
        }, se]
      }],
      /**
       * Height
       * @see https://tailwindcss.com/docs/height
       */
      h: [{
        h: [C, e, "auto", "min", "max", "fit", "svh", "lvh", "dvh"]
      }],
      /**
       * Min-Height
       * @see https://tailwindcss.com/docs/min-height
       */
      "min-h": [{
        "min-h": [C, e, "min", "max", "fit", "svh", "lvh", "dvh"]
      }],
      /**
       * Max-Height
       * @see https://tailwindcss.com/docs/max-height
       */
      "max-h": [{
        "max-h": [C, e, "min", "max", "fit", "svh", "lvh", "dvh"]
      }],
      /**
       * Size
       * @see https://tailwindcss.com/docs/size
       */
      size: [{
        size: [C, e, "auto", "min", "max", "fit"]
      }],
      // Typography
      /**
       * Font Size
       * @see https://tailwindcss.com/docs/font-size
       */
      "font-size": [{
        text: ["base", se, ie]
      }],
      /**
       * Font Smoothing
       * @see https://tailwindcss.com/docs/font-smoothing
       */
      "font-smoothing": ["antialiased", "subpixel-antialiased"],
      /**
       * Font Style
       * @see https://tailwindcss.com/docs/font-style
       */
      "font-style": ["italic", "not-italic"],
      /**
       * Font Weight
       * @see https://tailwindcss.com/docs/font-weight
       */
      "font-weight": [{
        font: ["thin", "extralight", "light", "normal", "medium", "semibold", "bold", "extrabold", "black", xe]
      }],
      /**
       * Font Family
       * @see https://tailwindcss.com/docs/font-family
       */
      "font-family": [{
        font: [ve]
      }],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-normal": ["normal-nums"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-ordinal": ["ordinal"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-slashed-zero": ["slashed-zero"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-figure": ["lining-nums", "oldstyle-nums"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-spacing": ["proportional-nums", "tabular-nums"],
      /**
       * Font Variant Numeric
       * @see https://tailwindcss.com/docs/font-variant-numeric
       */
      "fvn-fraction": ["diagonal-fractions", "stacked-fractons"],
      /**
       * Letter Spacing
       * @see https://tailwindcss.com/docs/letter-spacing
       */
      tracking: [{
        tracking: ["tighter", "tight", "normal", "wide", "wider", "widest", C]
      }],
      /**
       * Line Clamp
       * @see https://tailwindcss.com/docs/line-clamp
       */
      "line-clamp": [{
        "line-clamp": ["none", pe, xe]
      }],
      /**
       * Line Height
       * @see https://tailwindcss.com/docs/line-height
       */
      leading: [{
        leading: ["none", "tight", "snug", "normal", "relaxed", "loose", re, C]
      }],
      /**
       * List Style Image
       * @see https://tailwindcss.com/docs/list-style-image
       */
      "list-image": [{
        "list-image": ["none", C]
      }],
      /**
       * List Style Type
       * @see https://tailwindcss.com/docs/list-style-type
       */
      "list-style-type": [{
        list: ["none", "disc", "decimal", C]
      }],
      /**
       * List Style Position
       * @see https://tailwindcss.com/docs/list-style-position
       */
      "list-style-position": [{
        list: ["inside", "outside"]
      }],
      /**
       * Placeholder Color
       * @deprecated since Tailwind CSS v3.0.0
       * @see https://tailwindcss.com/docs/placeholder-color
       */
      "placeholder-color": [{
        placeholder: [r]
      }],
      /**
       * Placeholder Opacity
       * @see https://tailwindcss.com/docs/placeholder-opacity
       */
      "placeholder-opacity": [{
        "placeholder-opacity": [_]
      }],
      /**
       * Text Alignment
       * @see https://tailwindcss.com/docs/text-align
       */
      "text-alignment": [{
        text: ["left", "center", "right", "justify", "start", "end"]
      }],
      /**
       * Text Color
       * @see https://tailwindcss.com/docs/text-color
       */
      "text-color": [{
        text: [r]
      }],
      /**
       * Text Opacity
       * @see https://tailwindcss.com/docs/text-opacity
       */
      "text-opacity": [{
        "text-opacity": [_]
      }],
      /**
       * Text Decoration
       * @see https://tailwindcss.com/docs/text-decoration
       */
      "text-decoration": ["underline", "overline", "line-through", "no-underline"],
      /**
       * Text Decoration Style
       * @see https://tailwindcss.com/docs/text-decoration-style
       */
      "text-decoration-style": [{
        decoration: [...Z(), "wavy"]
      }],
      /**
       * Text Decoration Thickness
       * @see https://tailwindcss.com/docs/text-decoration-thickness
       */
      "text-decoration-thickness": [{
        decoration: ["auto", "from-font", re, ie]
      }],
      /**
       * Text Underline Offset
       * @see https://tailwindcss.com/docs/text-underline-offset
       */
      "underline-offset": [{
        "underline-offset": ["auto", re, C]
      }],
      /**
       * Text Decoration Color
       * @see https://tailwindcss.com/docs/text-decoration-color
       */
      "text-decoration-color": [{
        decoration: [r]
      }],
      /**
       * Text Transform
       * @see https://tailwindcss.com/docs/text-transform
       */
      "text-transform": ["uppercase", "lowercase", "capitalize", "normal-case"],
      /**
       * Text Overflow
       * @see https://tailwindcss.com/docs/text-overflow
       */
      "text-overflow": ["truncate", "text-ellipsis", "text-clip"],
      /**
       * Text Wrap
       * @see https://tailwindcss.com/docs/text-wrap
       */
      "text-wrap": [{
        text: ["wrap", "nowrap", "balance", "pretty"]
      }],
      /**
       * Text Indent
       * @see https://tailwindcss.com/docs/text-indent
       */
      indent: [{
        indent: S()
      }],
      /**
       * Vertical Alignment
       * @see https://tailwindcss.com/docs/vertical-align
       */
      "vertical-align": [{
        align: ["baseline", "top", "middle", "bottom", "text-top", "text-bottom", "sub", "super", C]
      }],
      /**
       * Whitespace
       * @see https://tailwindcss.com/docs/whitespace
       */
      whitespace: [{
        whitespace: ["normal", "nowrap", "pre", "pre-line", "pre-wrap", "break-spaces"]
      }],
      /**
       * Word Break
       * @see https://tailwindcss.com/docs/word-break
       */
      break: [{
        break: ["normal", "words", "all", "keep"]
      }],
      /**
       * Hyphens
       * @see https://tailwindcss.com/docs/hyphens
       */
      hyphens: [{
        hyphens: ["none", "manual", "auto"]
      }],
      /**
       * Content
       * @see https://tailwindcss.com/docs/content
       */
      content: [{
        content: ["none", C]
      }],
      // Backgrounds
      /**
       * Background Attachment
       * @see https://tailwindcss.com/docs/background-attachment
       */
      "bg-attachment": [{
        bg: ["fixed", "local", "scroll"]
      }],
      /**
       * Background Clip
       * @see https://tailwindcss.com/docs/background-clip
       */
      "bg-clip": [{
        "bg-clip": ["border", "padding", "content", "text"]
      }],
      /**
       * Background Opacity
       * @deprecated since Tailwind CSS v3.0.0
       * @see https://tailwindcss.com/docs/background-opacity
       */
      "bg-opacity": [{
        "bg-opacity": [_]
      }],
      /**
       * Background Origin
       * @see https://tailwindcss.com/docs/background-origin
       */
      "bg-origin": [{
        "bg-origin": ["border", "padding", "content"]
      }],
      /**
       * Background Position
       * @see https://tailwindcss.com/docs/background-position
       */
      "bg-position": [{
        bg: [...I(), $n]
      }],
      /**
       * Background Repeat
       * @see https://tailwindcss.com/docs/background-repeat
       */
      "bg-repeat": [{
        bg: ["no-repeat", {
          repeat: ["", "x", "y", "round", "space"]
        }]
      }],
      /**
       * Background Size
       * @see https://tailwindcss.com/docs/background-size
       */
      "bg-size": [{
        bg: ["auto", "cover", "contain", Yn]
      }],
      /**
       * Background Image
       * @see https://tailwindcss.com/docs/background-image
       */
      "bg-image": [{
        bg: ["none", {
          "gradient-to": ["t", "tr", "r", "br", "b", "bl", "l", "tl"]
        }, ti]
      }],
      /**
       * Background Color
       * @see https://tailwindcss.com/docs/background-color
       */
      "bg-color": [{
        bg: [r]
      }],
      /**
       * Gradient Color Stops From Position
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-from-pos": [{
        from: [p]
      }],
      /**
       * Gradient Color Stops Via Position
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-via-pos": [{
        via: [p]
      }],
      /**
       * Gradient Color Stops To Position
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-to-pos": [{
        to: [p]
      }],
      /**
       * Gradient Color Stops From
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-from": [{
        from: [h]
      }],
      /**
       * Gradient Color Stops Via
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-via": [{
        via: [h]
      }],
      /**
       * Gradient Color Stops To
       * @see https://tailwindcss.com/docs/gradient-color-stops
       */
      "gradient-to": [{
        to: [h]
      }],
      // Borders
      /**
       * Border Radius
       * @see https://tailwindcss.com/docs/border-radius
       */
      rounded: [{
        rounded: [s]
      }],
      /**
       * Border Radius Start
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-s": [{
        "rounded-s": [s]
      }],
      /**
       * Border Radius End
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-e": [{
        "rounded-e": [s]
      }],
      /**
       * Border Radius Top
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-t": [{
        "rounded-t": [s]
      }],
      /**
       * Border Radius Right
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-r": [{
        "rounded-r": [s]
      }],
      /**
       * Border Radius Bottom
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-b": [{
        "rounded-b": [s]
      }],
      /**
       * Border Radius Left
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-l": [{
        "rounded-l": [s]
      }],
      /**
       * Border Radius Start Start
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-ss": [{
        "rounded-ss": [s]
      }],
      /**
       * Border Radius Start End
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-se": [{
        "rounded-se": [s]
      }],
      /**
       * Border Radius End End
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-ee": [{
        "rounded-ee": [s]
      }],
      /**
       * Border Radius End Start
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-es": [{
        "rounded-es": [s]
      }],
      /**
       * Border Radius Top Left
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-tl": [{
        "rounded-tl": [s]
      }],
      /**
       * Border Radius Top Right
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-tr": [{
        "rounded-tr": [s]
      }],
      /**
       * Border Radius Bottom Right
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-br": [{
        "rounded-br": [s]
      }],
      /**
       * Border Radius Bottom Left
       * @see https://tailwindcss.com/docs/border-radius
       */
      "rounded-bl": [{
        "rounded-bl": [s]
      }],
      /**
       * Border Width
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w": [{
        border: [a]
      }],
      /**
       * Border Width X
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-x": [{
        "border-x": [a]
      }],
      /**
       * Border Width Y
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-y": [{
        "border-y": [a]
      }],
      /**
       * Border Width Start
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-s": [{
        "border-s": [a]
      }],
      /**
       * Border Width End
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-e": [{
        "border-e": [a]
      }],
      /**
       * Border Width Top
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-t": [{
        "border-t": [a]
      }],
      /**
       * Border Width Right
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-r": [{
        "border-r": [a]
      }],
      /**
       * Border Width Bottom
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-b": [{
        "border-b": [a]
      }],
      /**
       * Border Width Left
       * @see https://tailwindcss.com/docs/border-width
       */
      "border-w-l": [{
        "border-l": [a]
      }],
      /**
       * Border Opacity
       * @see https://tailwindcss.com/docs/border-opacity
       */
      "border-opacity": [{
        "border-opacity": [_]
      }],
      /**
       * Border Style
       * @see https://tailwindcss.com/docs/border-style
       */
      "border-style": [{
        border: [...Z(), "hidden"]
      }],
      /**
       * Divide Width X
       * @see https://tailwindcss.com/docs/divide-width
       */
      "divide-x": [{
        "divide-x": [a]
      }],
      /**
       * Divide Width X Reverse
       * @see https://tailwindcss.com/docs/divide-width
       */
      "divide-x-reverse": ["divide-x-reverse"],
      /**
       * Divide Width Y
       * @see https://tailwindcss.com/docs/divide-width
       */
      "divide-y": [{
        "divide-y": [a]
      }],
      /**
       * Divide Width Y Reverse
       * @see https://tailwindcss.com/docs/divide-width
       */
      "divide-y-reverse": ["divide-y-reverse"],
      /**
       * Divide Opacity
       * @see https://tailwindcss.com/docs/divide-opacity
       */
      "divide-opacity": [{
        "divide-opacity": [_]
      }],
      /**
       * Divide Style
       * @see https://tailwindcss.com/docs/divide-style
       */
      "divide-style": [{
        divide: Z()
      }],
      /**
       * Border Color
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color": [{
        border: [i]
      }],
      /**
       * Border Color X
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-x": [{
        "border-x": [i]
      }],
      /**
       * Border Color Y
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-y": [{
        "border-y": [i]
      }],
      /**
       * Border Color Top
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-t": [{
        "border-t": [i]
      }],
      /**
       * Border Color Right
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-r": [{
        "border-r": [i]
      }],
      /**
       * Border Color Bottom
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-b": [{
        "border-b": [i]
      }],
      /**
       * Border Color Left
       * @see https://tailwindcss.com/docs/border-color
       */
      "border-color-l": [{
        "border-l": [i]
      }],
      /**
       * Divide Color
       * @see https://tailwindcss.com/docs/divide-color
       */
      "divide-color": [{
        divide: [i]
      }],
      /**
       * Outline Style
       * @see https://tailwindcss.com/docs/outline-style
       */
      "outline-style": [{
        outline: ["", ...Z()]
      }],
      /**
       * Outline Offset
       * @see https://tailwindcss.com/docs/outline-offset
       */
      "outline-offset": [{
        "outline-offset": [re, C]
      }],
      /**
       * Outline Width
       * @see https://tailwindcss.com/docs/outline-width
       */
      "outline-w": [{
        outline: [re, ie]
      }],
      /**
       * Outline Color
       * @see https://tailwindcss.com/docs/outline-color
       */
      "outline-color": [{
        outline: [r]
      }],
      /**
       * Ring Width
       * @see https://tailwindcss.com/docs/ring-width
       */
      "ring-w": [{
        ring: k()
      }],
      /**
       * Ring Width Inset
       * @see https://tailwindcss.com/docs/ring-width
       */
      "ring-w-inset": ["ring-inset"],
      /**
       * Ring Color
       * @see https://tailwindcss.com/docs/ring-color
       */
      "ring-color": [{
        ring: [r]
      }],
      /**
       * Ring Opacity
       * @see https://tailwindcss.com/docs/ring-opacity
       */
      "ring-opacity": [{
        "ring-opacity": [_]
      }],
      /**
       * Ring Offset Width
       * @see https://tailwindcss.com/docs/ring-offset-width
       */
      "ring-offset-w": [{
        "ring-offset": [re, ie]
      }],
      /**
       * Ring Offset Color
       * @see https://tailwindcss.com/docs/ring-offset-color
       */
      "ring-offset-color": [{
        "ring-offset": [r]
      }],
      // Effects
      /**
       * Box Shadow
       * @see https://tailwindcss.com/docs/box-shadow
       */
      shadow: [{
        shadow: ["", "inner", "none", se, ri]
      }],
      /**
       * Box Shadow Color
       * @see https://tailwindcss.com/docs/box-shadow-color
       */
      "shadow-color": [{
        shadow: [ve]
      }],
      /**
       * Opacity
       * @see https://tailwindcss.com/docs/opacity
       */
      opacity: [{
        opacity: [_]
      }],
      /**
       * Mix Blend Mode
       * @see https://tailwindcss.com/docs/mix-blend-mode
       */
      "mix-blend": [{
        "mix-blend": [...ue(), "plus-lighter", "plus-darker"]
      }],
      /**
       * Background Blend Mode
       * @see https://tailwindcss.com/docs/background-blend-mode
       */
      "bg-blend": [{
        "bg-blend": ue()
      }],
      // Filters
      /**
       * Filter
       * @deprecated since Tailwind CSS v3.0.0
       * @see https://tailwindcss.com/docs/filter
       */
      filter: [{
        filter: ["", "none"]
      }],
      /**
       * Blur
       * @see https://tailwindcss.com/docs/blur
       */
      blur: [{
        blur: [t]
      }],
      /**
       * Brightness
       * @see https://tailwindcss.com/docs/brightness
       */
      brightness: [{
        brightness: [n]
      }],
      /**
       * Contrast
       * @see https://tailwindcss.com/docs/contrast
       */
      contrast: [{
        contrast: [l]
      }],
      /**
       * Drop Shadow
       * @see https://tailwindcss.com/docs/drop-shadow
       */
      "drop-shadow": [{
        "drop-shadow": ["", "none", se, C]
      }],
      /**
       * Grayscale
       * @see https://tailwindcss.com/docs/grayscale
       */
      grayscale: [{
        grayscale: [d]
      }],
      /**
       * Hue Rotate
       * @see https://tailwindcss.com/docs/hue-rotate
       */
      "hue-rotate": [{
        "hue-rotate": [c]
      }],
      /**
       * Invert
       * @see https://tailwindcss.com/docs/invert
       */
      invert: [{
        invert: [u]
      }],
      /**
       * Saturate
       * @see https://tailwindcss.com/docs/saturate
       */
      saturate: [{
        saturate: [A]
      }],
      /**
       * Sepia
       * @see https://tailwindcss.com/docs/sepia
       */
      sepia: [{
        sepia: [y]
      }],
      /**
       * Backdrop Filter
       * @deprecated since Tailwind CSS v3.0.0
       * @see https://tailwindcss.com/docs/backdrop-filter
       */
      "backdrop-filter": [{
        "backdrop-filter": ["", "none"]
      }],
      /**
       * Backdrop Blur
       * @see https://tailwindcss.com/docs/backdrop-blur
       */
      "backdrop-blur": [{
        "backdrop-blur": [t]
      }],
      /**
       * Backdrop Brightness
       * @see https://tailwindcss.com/docs/backdrop-brightness
       */
      "backdrop-brightness": [{
        "backdrop-brightness": [n]
      }],
      /**
       * Backdrop Contrast
       * @see https://tailwindcss.com/docs/backdrop-contrast
       */
      "backdrop-contrast": [{
        "backdrop-contrast": [l]
      }],
      /**
       * Backdrop Grayscale
       * @see https://tailwindcss.com/docs/backdrop-grayscale
       */
      "backdrop-grayscale": [{
        "backdrop-grayscale": [d]
      }],
      /**
       * Backdrop Hue Rotate
       * @see https://tailwindcss.com/docs/backdrop-hue-rotate
       */
      "backdrop-hue-rotate": [{
        "backdrop-hue-rotate": [c]
      }],
      /**
       * Backdrop Invert
       * @see https://tailwindcss.com/docs/backdrop-invert
       */
      "backdrop-invert": [{
        "backdrop-invert": [u]
      }],
      /**
       * Backdrop Opacity
       * @see https://tailwindcss.com/docs/backdrop-opacity
       */
      "backdrop-opacity": [{
        "backdrop-opacity": [_]
      }],
      /**
       * Backdrop Saturate
       * @see https://tailwindcss.com/docs/backdrop-saturate
       */
      "backdrop-saturate": [{
        "backdrop-saturate": [A]
      }],
      /**
       * Backdrop Sepia
       * @see https://tailwindcss.com/docs/backdrop-sepia
       */
      "backdrop-sepia": [{
        "backdrop-sepia": [y]
      }],
      // Tables
      /**
       * Border Collapse
       * @see https://tailwindcss.com/docs/border-collapse
       */
      "border-collapse": [{
        border: ["collapse", "separate"]
      }],
      /**
       * Border Spacing
       * @see https://tailwindcss.com/docs/border-spacing
       */
      "border-spacing": [{
        "border-spacing": [o]
      }],
      /**
       * Border Spacing X
       * @see https://tailwindcss.com/docs/border-spacing
       */
      "border-spacing-x": [{
        "border-spacing-x": [o]
      }],
      /**
       * Border Spacing Y
       * @see https://tailwindcss.com/docs/border-spacing
       */
      "border-spacing-y": [{
        "border-spacing-y": [o]
      }],
      /**
       * Table Layout
       * @see https://tailwindcss.com/docs/table-layout
       */
      "table-layout": [{
        table: ["auto", "fixed"]
      }],
      /**
       * Caption Side
       * @see https://tailwindcss.com/docs/caption-side
       */
      caption: [{
        caption: ["top", "bottom"]
      }],
      // Transitions and Animation
      /**
       * Tranisition Property
       * @see https://tailwindcss.com/docs/transition-property
       */
      transition: [{
        transition: ["none", "all", "", "colors", "opacity", "shadow", "transform", C]
      }],
      /**
       * Transition Duration
       * @see https://tailwindcss.com/docs/transition-duration
       */
      duration: [{
        duration: N()
      }],
      /**
       * Transition Timing Function
       * @see https://tailwindcss.com/docs/transition-timing-function
       */
      ease: [{
        ease: ["linear", "in", "out", "in-out", C]
      }],
      /**
       * Transition Delay
       * @see https://tailwindcss.com/docs/transition-delay
       */
      delay: [{
        delay: N()
      }],
      /**
       * Animation
       * @see https://tailwindcss.com/docs/animation
       */
      animate: [{
        animate: ["none", "spin", "ping", "pulse", "bounce", C]
      }],
      // Transforms
      /**
       * Transform
       * @see https://tailwindcss.com/docs/transform
       */
      transform: [{
        transform: ["", "gpu", "none"]
      }],
      /**
       * Scale
       * @see https://tailwindcss.com/docs/scale
       */
      scale: [{
        scale: [R]
      }],
      /**
       * Scale X
       * @see https://tailwindcss.com/docs/scale
       */
      "scale-x": [{
        "scale-x": [R]
      }],
      /**
       * Scale Y
       * @see https://tailwindcss.com/docs/scale
       */
      "scale-y": [{
        "scale-y": [R]
      }],
      /**
       * Rotate
       * @see https://tailwindcss.com/docs/rotate
       */
      rotate: [{
        rotate: [_e, C]
      }],
      /**
       * Translate X
       * @see https://tailwindcss.com/docs/translate
       */
      "translate-x": [{
        "translate-x": [J]
      }],
      /**
       * Translate Y
       * @see https://tailwindcss.com/docs/translate
       */
      "translate-y": [{
        "translate-y": [J]
      }],
      /**
       * Skew X
       * @see https://tailwindcss.com/docs/skew
       */
      "skew-x": [{
        "skew-x": [b]
      }],
      /**
       * Skew Y
       * @see https://tailwindcss.com/docs/skew
       */
      "skew-y": [{
        "skew-y": [b]
      }],
      /**
       * Transform Origin
       * @see https://tailwindcss.com/docs/transform-origin
       */
      "transform-origin": [{
        origin: ["center", "top", "top-right", "right", "bottom-right", "bottom", "bottom-left", "left", "top-left", C]
      }],
      // Interactivity
      /**
       * Accent Color
       * @see https://tailwindcss.com/docs/accent-color
       */
      accent: [{
        accent: ["auto", r]
      }],
      /**
       * Appearance
       * @see https://tailwindcss.com/docs/appearance
       */
      appearance: [{
        appearance: ["none", "auto"]
      }],
      /**
       * Cursor
       * @see https://tailwindcss.com/docs/cursor
       */
      cursor: [{
        cursor: ["auto", "default", "pointer", "wait", "text", "move", "help", "not-allowed", "none", "context-menu", "progress", "cell", "crosshair", "vertical-text", "alias", "copy", "no-drop", "grab", "grabbing", "all-scroll", "col-resize", "row-resize", "n-resize", "e-resize", "s-resize", "w-resize", "ne-resize", "nw-resize", "se-resize", "sw-resize", "ew-resize", "ns-resize", "nesw-resize", "nwse-resize", "zoom-in", "zoom-out", C]
      }],
      /**
       * Caret Color
       * @see https://tailwindcss.com/docs/just-in-time-mode#caret-color-utilities
       */
      "caret-color": [{
        caret: [r]
      }],
      /**
       * Pointer Events
       * @see https://tailwindcss.com/docs/pointer-events
       */
      "pointer-events": [{
        "pointer-events": ["none", "auto"]
      }],
      /**
       * Resize
       * @see https://tailwindcss.com/docs/resize
       */
      resize: [{
        resize: ["none", "y", "x", ""]
      }],
      /**
       * Scroll Behavior
       * @see https://tailwindcss.com/docs/scroll-behavior
       */
      "scroll-behavior": [{
        scroll: ["auto", "smooth"]
      }],
      /**
       * Scroll Margin
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-m": [{
        "scroll-m": S()
      }],
      /**
       * Scroll Margin X
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mx": [{
        "scroll-mx": S()
      }],
      /**
       * Scroll Margin Y
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-my": [{
        "scroll-my": S()
      }],
      /**
       * Scroll Margin Start
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-ms": [{
        "scroll-ms": S()
      }],
      /**
       * Scroll Margin End
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-me": [{
        "scroll-me": S()
      }],
      /**
       * Scroll Margin Top
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mt": [{
        "scroll-mt": S()
      }],
      /**
       * Scroll Margin Right
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mr": [{
        "scroll-mr": S()
      }],
      /**
       * Scroll Margin Bottom
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-mb": [{
        "scroll-mb": S()
      }],
      /**
       * Scroll Margin Left
       * @see https://tailwindcss.com/docs/scroll-margin
       */
      "scroll-ml": [{
        "scroll-ml": S()
      }],
      /**
       * Scroll Padding
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-p": [{
        "scroll-p": S()
      }],
      /**
       * Scroll Padding X
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-px": [{
        "scroll-px": S()
      }],
      /**
       * Scroll Padding Y
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-py": [{
        "scroll-py": S()
      }],
      /**
       * Scroll Padding Start
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-ps": [{
        "scroll-ps": S()
      }],
      /**
       * Scroll Padding End
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pe": [{
        "scroll-pe": S()
      }],
      /**
       * Scroll Padding Top
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pt": [{
        "scroll-pt": S()
      }],
      /**
       * Scroll Padding Right
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pr": [{
        "scroll-pr": S()
      }],
      /**
       * Scroll Padding Bottom
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pb": [{
        "scroll-pb": S()
      }],
      /**
       * Scroll Padding Left
       * @see https://tailwindcss.com/docs/scroll-padding
       */
      "scroll-pl": [{
        "scroll-pl": S()
      }],
      /**
       * Scroll Snap Align
       * @see https://tailwindcss.com/docs/scroll-snap-align
       */
      "snap-align": [{
        snap: ["start", "end", "center", "align-none"]
      }],
      /**
       * Scroll Snap Stop
       * @see https://tailwindcss.com/docs/scroll-snap-stop
       */
      "snap-stop": [{
        snap: ["normal", "always"]
      }],
      /**
       * Scroll Snap Type
       * @see https://tailwindcss.com/docs/scroll-snap-type
       */
      "snap-type": [{
        snap: ["none", "x", "y", "both"]
      }],
      /**
       * Scroll Snap Type Strictness
       * @see https://tailwindcss.com/docs/scroll-snap-type
       */
      "snap-strictness": [{
        snap: ["mandatory", "proximity"]
      }],
      /**
       * Touch Action
       * @see https://tailwindcss.com/docs/touch-action
       */
      touch: [{
        touch: ["auto", "none", "manipulation"]
      }],
      /**
       * Touch Action X
       * @see https://tailwindcss.com/docs/touch-action
       */
      "touch-x": [{
        "touch-pan": ["x", "left", "right"]
      }],
      /**
       * Touch Action Y
       * @see https://tailwindcss.com/docs/touch-action
       */
      "touch-y": [{
        "touch-pan": ["y", "up", "down"]
      }],
      /**
       * Touch Action Pinch Zoom
       * @see https://tailwindcss.com/docs/touch-action
       */
      "touch-pz": ["touch-pinch-zoom"],
      /**
       * User Select
       * @see https://tailwindcss.com/docs/user-select
       */
      select: [{
        select: ["none", "text", "all", "auto"]
      }],
      /**
       * Will Change
       * @see https://tailwindcss.com/docs/will-change
       */
      "will-change": [{
        "will-change": ["auto", "scroll", "contents", "transform", C]
      }],
      // SVG
      /**
       * Fill
       * @see https://tailwindcss.com/docs/fill
       */
      fill: [{
        fill: [r, "none"]
      }],
      /**
       * Stroke Width
       * @see https://tailwindcss.com/docs/stroke-width
       */
      "stroke-w": [{
        stroke: [re, ie, xe]
      }],
      /**
       * Stroke
       * @see https://tailwindcss.com/docs/stroke
       */
      stroke: [{
        stroke: [r, "none"]
      }],
      // Accessibility
      /**
       * Screen Readers
       * @see https://tailwindcss.com/docs/screen-readers
       */
      sr: ["sr-only", "not-sr-only"],
      /**
       * Forced Color Adjust
       * @see https://tailwindcss.com/docs/forced-color-adjust
       */
      "forced-color-adjust": [{
        "forced-color-adjust": ["auto", "none"]
      }]
    },
    conflictingClassGroups: {
      overflow: ["overflow-x", "overflow-y"],
      overscroll: ["overscroll-x", "overscroll-y"],
      inset: ["inset-x", "inset-y", "start", "end", "top", "right", "bottom", "left"],
      "inset-x": ["right", "left"],
      "inset-y": ["top", "bottom"],
      flex: ["basis", "grow", "shrink"],
      gap: ["gap-x", "gap-y"],
      p: ["px", "py", "ps", "pe", "pt", "pr", "pb", "pl"],
      px: ["pr", "pl"],
      py: ["pt", "pb"],
      m: ["mx", "my", "ms", "me", "mt", "mr", "mb", "ml"],
      mx: ["mr", "ml"],
      my: ["mt", "mb"],
      size: ["w", "h"],
      "font-size": ["leading"],
      "fvn-normal": ["fvn-ordinal", "fvn-slashed-zero", "fvn-figure", "fvn-spacing", "fvn-fraction"],
      "fvn-ordinal": ["fvn-normal"],
      "fvn-slashed-zero": ["fvn-normal"],
      "fvn-figure": ["fvn-normal"],
      "fvn-spacing": ["fvn-normal"],
      "fvn-fraction": ["fvn-normal"],
      "line-clamp": ["display", "overflow"],
      rounded: ["rounded-s", "rounded-e", "rounded-t", "rounded-r", "rounded-b", "rounded-l", "rounded-ss", "rounded-se", "rounded-ee", "rounded-es", "rounded-tl", "rounded-tr", "rounded-br", "rounded-bl"],
      "rounded-s": ["rounded-ss", "rounded-es"],
      "rounded-e": ["rounded-se", "rounded-ee"],
      "rounded-t": ["rounded-tl", "rounded-tr"],
      "rounded-r": ["rounded-tr", "rounded-br"],
      "rounded-b": ["rounded-br", "rounded-bl"],
      "rounded-l": ["rounded-tl", "rounded-bl"],
      "border-spacing": ["border-spacing-x", "border-spacing-y"],
      "border-w": ["border-w-s", "border-w-e", "border-w-t", "border-w-r", "border-w-b", "border-w-l"],
      "border-w-x": ["border-w-r", "border-w-l"],
      "border-w-y": ["border-w-t", "border-w-b"],
      "border-color": ["border-color-t", "border-color-r", "border-color-b", "border-color-l"],
      "border-color-x": ["border-color-r", "border-color-l"],
      "border-color-y": ["border-color-t", "border-color-b"],
      "scroll-m": ["scroll-mx", "scroll-my", "scroll-ms", "scroll-me", "scroll-mt", "scroll-mr", "scroll-mb", "scroll-ml"],
      "scroll-mx": ["scroll-mr", "scroll-ml"],
      "scroll-my": ["scroll-mt", "scroll-mb"],
      "scroll-p": ["scroll-px", "scroll-py", "scroll-ps", "scroll-pe", "scroll-pt", "scroll-pr", "scroll-pb", "scroll-pl"],
      "scroll-px": ["scroll-pr", "scroll-pl"],
      "scroll-py": ["scroll-pt", "scroll-pb"],
      touch: ["touch-x", "touch-y", "touch-pz"],
      "touch-x": ["touch"],
      "touch-y": ["touch"],
      "touch-pz": ["touch"]
    },
    conflictingClassGroupModifiers: {
      "font-size": ["leading"]
    }
  };
}
const he = /* @__PURE__ */ qn(oi), {
  SvelteComponent: ai,
  append: li,
  assign: Ke,
  attr: At,
  compute_rest_props: Mt,
  create_slot: ci,
  detach: di,
  element: xt,
  exclude_internal_props: Rt,
  get_all_dirty_from_scope: ui,
  get_slot_changes: fi,
  get_spread_update: pi,
  init: hi,
  insert: gi,
  safe_not_equal: mi,
  set_attributes: zt,
  transition_in: bi,
  transition_out: _i,
  update_slot_base: vi
} = window.__gradio__svelte__internal, { setContext: Re } = window.__gradio__svelte__internal;
function yi(r) {
  let e, t, n, i, s;
  const o = (
    /*#slots*/
    r[11].default
  ), a = ci(
    o,
    r,
    /*$$scope*/
    r[10],
    null
  );
  let l = [
    /*$$restProps*/
    r[4],
    {
      class: n = he(
        "w-full text-left text-sm",
        /*colors*/
        r[3][
          /*color*/
          r[2]
        ],
        /*$$props*/
        r[5].class
      )
    }
  ], d = {};
  for (let c = 0; c < l.length; c += 1)
    d = Ke(d, l[c]);
  return {
    c() {
      e = xt("div"), t = xt("table"), a && a.c(), zt(t, d), At(e, "class", i = Ne(
        /*divClass*/
        r[0],
        /*shadow*/
        r[1] && "shadow-md sm:rounded-lg"
      ));
    },
    m(c, u) {
      gi(c, e, u), li(e, t), a && a.m(t, null), s = !0;
    },
    p(c, [u]) {
      a && a.p && (!s || u & /*$$scope*/
      1024) && vi(
        a,
        o,
        c,
        /*$$scope*/
        c[10],
        s ? fi(
          o,
          /*$$scope*/
          c[10],
          u,
          null
        ) : ui(
          /*$$scope*/
          c[10]
        ),
        null
      ), zt(t, d = pi(l, [
        u & /*$$restProps*/
        16 && /*$$restProps*/
        c[4],
        (!s || u & /*color, $$props*/
        36 && n !== (n = he(
          "w-full text-left text-sm",
          /*colors*/
          c[3][
            /*color*/
            c[2]
          ],
          /*$$props*/
          c[5].class
        ))) && { class: n }
      ])), (!s || u & /*divClass, shadow*/
      3 && i !== (i = Ne(
        /*divClass*/
        c[0],
        /*shadow*/
        c[1] && "shadow-md sm:rounded-lg"
      ))) && At(e, "class", i);
    },
    i(c) {
      s || (bi(a, c), s = !0);
    },
    o(c) {
      _i(a, c), s = !1;
    },
    d(c) {
      c && di(e), a && a.d(c);
    }
  };
}
function wi(r, e, t) {
  const n = ["divClass", "striped", "hoverable", "noborder", "shadow", "color", "customeColor"];
  let i = Mt(e, n), { $$slots: s = {}, $$scope: o } = e, { divClass: a = "relative overflow-x-auto" } = e, { striped: l = !1 } = e, { hoverable: d = !1 } = e, { noborder: c = !1 } = e, { shadow: u = !1 } = e, { color: f = "default" } = e, { customeColor: h = "" } = e;
  const p = {
    default: "text-gray-500 dark:text-gray-400",
    blue: "text-blue-100 dark:text-blue-100",
    green: "text-green-100 dark:text-green-100",
    red: "text-red-100 dark:text-red-100",
    yellow: "text-yellow-100 dark:text-yellow-100",
    purple: "text-purple-100 dark:text-purple-100",
    indigo: "text-indigo-100 dark:text-indigo-100",
    pink: "text-pink-100 dark:text-pink-100",
    custom: h
  };
  return r.$$set = (g) => {
    t(5, e = Ke(Ke({}, e), Rt(g))), t(4, i = Mt(e, n)), "divClass" in g && t(0, a = g.divClass), "striped" in g && t(6, l = g.striped), "hoverable" in g && t(7, d = g.hoverable), "noborder" in g && t(8, c = g.noborder), "shadow" in g && t(1, u = g.shadow), "color" in g && t(2, f = g.color), "customeColor" in g && t(9, h = g.customeColor), "$$scope" in g && t(10, o = g.$$scope);
  }, r.$$.update = () => {
    r.$$.dirty & /*striped*/
    64 && Re("striped", l), r.$$.dirty & /*hoverable*/
    128 && Re("hoverable", d), r.$$.dirty & /*noborder*/
    256 && Re("noborder", c), r.$$.dirty & /*color*/
    4 && Re("color", f);
  }, e = Rt(e), [
    a,
    u,
    f,
    p,
    i,
    e,
    l,
    d,
    c,
    h,
    o,
    s
  ];
}
class ki extends ai {
  constructor(e) {
    super(), hi(this, e, wi, yi, mi, {
      divClass: 0,
      striped: 6,
      hoverable: 7,
      noborder: 8,
      shadow: 1,
      color: 2,
      customeColor: 9
    });
  }
}
const {
  SvelteComponent: Ci,
  attr: Dt,
  create_slot: Si,
  detach: Ai,
  element: Mi,
  get_all_dirty_from_scope: xi,
  get_slot_changes: Ri,
  init: zi,
  insert: Di,
  safe_not_equal: Li,
  transition_in: Oi,
  transition_out: Pi,
  update_slot_base: Fi
} = window.__gradio__svelte__internal;
function Ii(r) {
  let e, t;
  const n = (
    /*#slots*/
    r[2].default
  ), i = Si(
    n,
    r,
    /*$$scope*/
    r[1],
    null
  );
  return {
    c() {
      e = Mi("tbody"), i && i.c(), Dt(
        e,
        "class",
        /*tableBodyClass*/
        r[0]
      );
    },
    m(s, o) {
      Di(s, e, o), i && i.m(e, null), t = !0;
    },
    p(s, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      2) && Fi(
        i,
        n,
        s,
        /*$$scope*/
        s[1],
        t ? Ri(
          n,
          /*$$scope*/
          s[1],
          o,
          null
        ) : xi(
          /*$$scope*/
          s[1]
        ),
        null
      ), (!t || o & /*tableBodyClass*/
      1) && Dt(
        e,
        "class",
        /*tableBodyClass*/
        s[0]
      );
    },
    i(s) {
      t || (Oi(i, s), t = !0);
    },
    o(s) {
      Pi(i, s), t = !1;
    },
    d(s) {
      s && Ai(e), i && i.d(s);
    }
  };
}
function Hi(r, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { tableBodyClass: s = void 0 } = e;
  return r.$$set = (o) => {
    "tableBodyClass" in o && t(0, s = o.tableBodyClass), "$$scope" in o && t(1, i = o.$$scope);
  }, [s, i, n];
}
class Ei extends Ci {
  constructor(e) {
    super(), zi(this, e, Hi, Ii, Li, { tableBodyClass: 0 });
  }
}
const {
  SvelteComponent: Gi,
  assign: Qe,
  check_outros: Ui,
  compute_rest_props: Lt,
  create_slot: ar,
  detach: lr,
  element: cr,
  exclude_internal_props: Ot,
  get_all_dirty_from_scope: dr,
  get_slot_changes: ur,
  get_spread_update: ji,
  group_outros: Bi,
  init: qi,
  insert: fr,
  is_function: Ti,
  listen: Wi,
  safe_not_equal: Vi,
  set_attributes: Pt,
  transition_in: He,
  transition_out: Ee,
  update_slot_base: pr
} = window.__gradio__svelte__internal, { getContext: Xi } = window.__gradio__svelte__internal;
function Zi(r) {
  let e;
  const t = (
    /*#slots*/
    r[6].default
  ), n = ar(
    t,
    r,
    /*$$scope*/
    r[5],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, s) {
      n && n.m(i, s), e = !0;
    },
    p(i, s) {
      n && n.p && (!e || s & /*$$scope*/
      32) && pr(
        n,
        t,
        i,
        /*$$scope*/
        i[5],
        e ? ur(
          t,
          /*$$scope*/
          i[5],
          s,
          null
        ) : dr(
          /*$$scope*/
          i[5]
        ),
        null
      );
    },
    i(i) {
      e || (He(n, i), e = !0);
    },
    o(i) {
      Ee(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Ji(r) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    r[6].default
  ), o = ar(
    s,
    r,
    /*$$scope*/
    r[5],
    null
  );
  return {
    c() {
      e = cr("button"), o && o.c();
    },
    m(a, l) {
      fr(a, e, l), o && o.m(e, null), t = !0, n || (i = Wi(e, "click", function() {
        Ti(
          /*$$props*/
          r[1].onclick
        ) && r[1].onclick.apply(this, arguments);
      }), n = !0);
    },
    p(a, l) {
      r = a, o && o.p && (!t || l & /*$$scope*/
      32) && pr(
        o,
        s,
        r,
        /*$$scope*/
        r[5],
        t ? ur(
          s,
          /*$$scope*/
          r[5],
          l,
          null
        ) : dr(
          /*$$scope*/
          r[5]
        ),
        null
      );
    },
    i(a) {
      t || (He(o, a), t = !0);
    },
    o(a) {
      Ee(o, a), t = !1;
    },
    d(a) {
      a && lr(e), o && o.d(a), n = !1, i();
    }
  };
}
function Ni(r) {
  let e, t, n, i;
  const s = [Ji, Zi], o = [];
  function a(c, u) {
    return (
      /*$$props*/
      c[1].onclick ? 0 : 1
    );
  }
  t = a(r), n = o[t] = s[t](r);
  let l = [
    /*$$restProps*/
    r[2],
    { class: (
      /*tdClassfinal*/
      r[0]
    ) }
  ], d = {};
  for (let c = 0; c < l.length; c += 1)
    d = Qe(d, l[c]);
  return {
    c() {
      e = cr("td"), n.c(), Pt(e, d);
    },
    m(c, u) {
      fr(c, e, u), o[t].m(e, null), i = !0;
    },
    p(c, [u]) {
      let f = t;
      t = a(c), t === f ? o[t].p(c, u) : (Bi(), Ee(o[f], 1, 1, () => {
        o[f] = null;
      }), Ui(), n = o[t], n ? n.p(c, u) : (n = o[t] = s[t](c), n.c()), He(n, 1), n.m(e, null)), Pt(e, d = ji(l, [
        u & /*$$restProps*/
        4 && /*$$restProps*/
        c[2],
        (!i || u & /*tdClassfinal*/
        1) && { class: (
          /*tdClassfinal*/
          c[0]
        ) }
      ]));
    },
    i(c) {
      i || (He(n), i = !0);
    },
    o(c) {
      Ee(n), i = !1;
    },
    d(c) {
      c && lr(e), o[t].d();
    }
  };
}
function Ki(r, e, t) {
  const n = ["tdClass"];
  let i = Lt(e, n), { $$slots: s = {}, $$scope: o } = e, { tdClass: a = "px-6 py-4 whitespace-nowrap font-medium " } = e, l = "default";
  l = Xi("color");
  let d;
  return r.$$set = (c) => {
    t(1, e = Qe(Qe({}, e), Ot(c))), t(2, i = Lt(e, n)), "tdClass" in c && t(3, a = c.tdClass), "$$scope" in c && t(5, o = c.$$scope);
  }, r.$$.update = () => {
    t(0, d = he(
      a,
      l === "default" ? "text-gray-900 dark:text-white" : "text-blue-50 whitespace-nowrap dark:text-blue-100",
      e.class
    ));
  }, e = Ot(e), [d, e, i, a, l, o, s];
}
class ye extends Gi {
  constructor(e) {
    super(), qi(this, e, Ki, Ni, Vi, { tdClass: 3 });
  }
}
const {
  SvelteComponent: Qi,
  assign: Ye,
  bubble: Te,
  compute_rest_props: Ft,
  create_slot: Yi,
  detach: $i,
  element: es,
  exclude_internal_props: It,
  get_all_dirty_from_scope: ts,
  get_slot_changes: rs,
  get_spread_update: ns,
  init: is,
  insert: ss,
  listen: We,
  run_all: os,
  safe_not_equal: as,
  set_attributes: Ht,
  transition_in: ls,
  transition_out: cs,
  update_slot_base: ds
} = window.__gradio__svelte__internal, { getContext: ze } = window.__gradio__svelte__internal;
function us(r) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    r[4].default
  ), o = Yi(
    s,
    r,
    /*$$scope*/
    r[3],
    null
  );
  let a = [
    /*$$restProps*/
    r[1],
    { class: (
      /*trClass*/
      r[0]
    ) }
  ], l = {};
  for (let d = 0; d < a.length; d += 1)
    l = Ye(l, a[d]);
  return {
    c() {
      e = es("tr"), o && o.c(), Ht(e, l);
    },
    m(d, c) {
      ss(d, e, c), o && o.m(e, null), t = !0, n || (i = [
        We(
          e,
          "click",
          /*click_handler*/
          r[5]
        ),
        We(
          e,
          "contextmenu",
          /*contextmenu_handler*/
          r[6]
        ),
        We(
          e,
          "dblclick",
          /*dblclick_handler*/
          r[7]
        )
      ], n = !0);
    },
    p(d, [c]) {
      o && o.p && (!t || c & /*$$scope*/
      8) && ds(
        o,
        s,
        d,
        /*$$scope*/
        d[3],
        t ? rs(
          s,
          /*$$scope*/
          d[3],
          c,
          null
        ) : ts(
          /*$$scope*/
          d[3]
        ),
        null
      ), Ht(e, l = ns(a, [
        c & /*$$restProps*/
        2 && /*$$restProps*/
        d[1],
        (!t || c & /*trClass*/
        1) && { class: (
          /*trClass*/
          d[0]
        ) }
      ]));
    },
    i(d) {
      t || (ls(o, d), t = !0);
    },
    o(d) {
      cs(o, d), t = !1;
    },
    d(d) {
      d && $i(e), o && o.d(d), n = !1, os(i);
    }
  };
}
function fs(r, e, t) {
  const n = ["color"];
  let i = Ft(e, n), { $$slots: s = {}, $$scope: o } = e, { color: a = ze("color") } = e;
  const l = {
    default: "bg-white dark:bg-gray-800 dark:border-gray-700",
    blue: "bg-blue-500 border-blue-400",
    green: "bg-green-500 border-green-400",
    red: "bg-red-500 border-red-400",
    yellow: "bg-yellow-500 border-yellow-400",
    purple: "bg-purple-500 border-purple-400",
    custom: ""
  }, d = {
    default: "hover:bg-gray-50 dark:hover:bg-gray-600",
    blue: "hover:bg-blue-400",
    green: "hover:bg-green-400",
    red: "hover:bg-red-400",
    yellow: "hover:bg-yellow-400",
    purple: "hover:bg-purple-400",
    custom: ""
  }, c = {
    default: "odd:bg-white even:bg-gray-50 odd:dark:bg-gray-800 even:dark:bg-gray-700",
    blue: "odd:bg-blue-800 even:bg-blue-700 odd:dark:bg-blue-800 even:dark:bg-blue-700",
    green: "odd:bg-green-800 even:bg-green-700 odd:dark:bg-green-800 even:dark:bg-green-700",
    red: "odd:bg-red-800 even:bg-red-700 odd:dark:bg-red-800 even:dark:bg-red-700",
    yellow: "odd:bg-yellow-800 even:bg-yellow-700 odd:dark:bg-yellow-800 even:dark:bg-yellow-700",
    purple: "odd:bg-purple-800 even:bg-purple-700 odd:dark:bg-purple-800 even:dark:bg-purple-700",
    custom: ""
  };
  let u;
  function f(g) {
    Te.call(this, r, g);
  }
  function h(g) {
    Te.call(this, r, g);
  }
  function p(g) {
    Te.call(this, r, g);
  }
  return r.$$set = (g) => {
    t(11, e = Ye(Ye({}, e), It(g))), t(1, i = Ft(e, n)), "color" in g && t(2, a = g.color), "$$scope" in g && t(3, o = g.$$scope);
  }, r.$$.update = () => {
    t(0, u = he([
      !ze("noborder") && "border-b last:border-b-0",
      l[a],
      ze("hoverable") && d[a],
      ze("striped") && c[a],
      e.class
    ]));
  }, e = It(e), [
    u,
    i,
    a,
    o,
    s,
    f,
    h,
    p
  ];
}
class ps extends Qi {
  constructor(e) {
    super(), is(this, e, fs, us, as, { color: 2 });
  }
}
const {
  SvelteComponent: hs,
  assign: $e,
  check_outros: gs,
  compute_rest_props: Et,
  create_slot: hr,
  detach: gr,
  element: mr,
  exclude_internal_props: Gt,
  get_all_dirty_from_scope: br,
  get_slot_changes: _r,
  get_spread_update: ms,
  group_outros: bs,
  init: _s,
  insert: vr,
  safe_not_equal: vs,
  set_attributes: Ut,
  transition_in: Ge,
  transition_out: Ue,
  update_slot_base: yr
} = window.__gradio__svelte__internal, { getContext: Ve } = window.__gradio__svelte__internal;
function ys(r) {
  let e;
  const t = (
    /*#slots*/
    r[6].default
  ), n = hr(
    t,
    r,
    /*$$scope*/
    r[5],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, s) {
      n && n.m(i, s), e = !0;
    },
    p(i, s) {
      n && n.p && (!e || s & /*$$scope*/
      32) && yr(
        n,
        t,
        i,
        /*$$scope*/
        i[5],
        e ? _r(
          t,
          /*$$scope*/
          i[5],
          s,
          null
        ) : br(
          /*$$scope*/
          i[5]
        ),
        null
      );
    },
    i(i) {
      e || (Ge(n, i), e = !0);
    },
    o(i) {
      Ue(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function ws(r) {
  let e, t;
  const n = (
    /*#slots*/
    r[6].default
  ), i = hr(
    n,
    r,
    /*$$scope*/
    r[5],
    null
  );
  return {
    c() {
      e = mr("tr"), i && i.c();
    },
    m(s, o) {
      vr(s, e, o), i && i.m(e, null), t = !0;
    },
    p(s, o) {
      i && i.p && (!t || o & /*$$scope*/
      32) && yr(
        i,
        n,
        s,
        /*$$scope*/
        s[5],
        t ? _r(
          n,
          /*$$scope*/
          s[5],
          o,
          null
        ) : br(
          /*$$scope*/
          s[5]
        ),
        null
      );
    },
    i(s) {
      t || (Ge(i, s), t = !0);
    },
    o(s) {
      Ue(i, s), t = !1;
    },
    d(s) {
      s && gr(e), i && i.d(s);
    }
  };
}
function ks(r) {
  let e, t, n, i;
  const s = [ws, ys], o = [];
  function a(c, u) {
    return (
      /*defaultRow*/
      c[0] ? 0 : 1
    );
  }
  t = a(r), n = o[t] = s[t](r);
  let l = [
    /*$$restProps*/
    r[2],
    { class: (
      /*theadClassfinal*/
      r[1]
    ) }
  ], d = {};
  for (let c = 0; c < l.length; c += 1)
    d = $e(d, l[c]);
  return {
    c() {
      e = mr("thead"), n.c(), Ut(e, d);
    },
    m(c, u) {
      vr(c, e, u), o[t].m(e, null), i = !0;
    },
    p(c, [u]) {
      let f = t;
      t = a(c), t === f ? o[t].p(c, u) : (bs(), Ue(o[f], 1, 1, () => {
        o[f] = null;
      }), gs(), n = o[t], n ? n.p(c, u) : (n = o[t] = s[t](c), n.c()), Ge(n, 1), n.m(e, null)), Ut(e, d = ms(l, [
        u & /*$$restProps*/
        4 && /*$$restProps*/
        c[2],
        (!i || u & /*theadClassfinal*/
        2) && { class: (
          /*theadClassfinal*/
          c[1]
        ) }
      ]));
    },
    i(c) {
      i || (Ge(n), i = !0);
    },
    o(c) {
      Ue(n), i = !1;
    },
    d(c) {
      c && gr(e), o[t].d();
    }
  };
}
function Cs(r, e, t) {
  let n;
  const i = ["theadClass", "defaultRow"];
  let s = Et(e, i), { $$slots: o = {}, $$scope: a } = e, { theadClass: l = "text-xs uppercase" } = e, { defaultRow: d = !0 } = e, c;
  c = Ve("color");
  let u = Ve("noborder"), f = Ve("striped");
  const p = {
    default: u || f ? "" : "bg-gray-50 dark:bg-gray-700",
    blue: "bg-blue-600",
    green: "bg-green-600",
    red: "bg-red-600",
    yellow: "bg-yellow-600",
    purple: "bg-purple-600",
    custom: ""
  };
  let g = c === "default" ? "text-gray-700 dark:text-gray-400" : c === "custom" ? "" : "text-white  dark:text-white", m = f ? "" : c === "default" ? "border-gray-700" : c === "custom" ? "" : `border-${c}-400`;
  return r.$$set = (_) => {
    t(13, e = $e($e({}, e), Gt(_))), t(2, s = Et(e, i)), "theadClass" in _ && t(3, l = _.theadClass), "defaultRow" in _ && t(0, d = _.defaultRow), "$$scope" in _ && t(5, a = _.$$scope);
  }, r.$$.update = () => {
    t(1, n = he(l, g, f && m, p[c], e.class));
  }, e = Gt(e), [d, n, s, l, c, a, o];
}
class Ss extends hs {
  constructor(e) {
    super(), _s(this, e, Cs, ks, vs, { theadClass: 3, defaultRow: 0 });
  }
}
const {
  SvelteComponent: As,
  assign: et,
  bubble: oe,
  compute_rest_props: jt,
  create_slot: Ms,
  detach: xs,
  element: Rs,
  exclude_internal_props: Bt,
  get_all_dirty_from_scope: zs,
  get_slot_changes: Ds,
  get_spread_update: Ls,
  init: Os,
  insert: Ps,
  listen: ae,
  run_all: Fs,
  safe_not_equal: Is,
  set_attributes: qt,
  transition_in: Hs,
  transition_out: Es,
  update_slot_base: Gs
} = window.__gradio__svelte__internal;
function Us(r) {
  let e, t, n, i, s;
  const o = (
    /*#slots*/
    r[4].default
  ), a = Ms(
    o,
    r,
    /*$$scope*/
    r[3],
    null
  );
  let l = [
    /*$$restProps*/
    r[1],
    {
      class: t = he(
        /*padding*/
        r[0],
        /*$$props*/
        r[2].class
      )
    }
  ], d = {};
  for (let c = 0; c < l.length; c += 1)
    d = et(d, l[c]);
  return {
    c() {
      e = Rs("th"), a && a.c(), qt(e, d);
    },
    m(c, u) {
      Ps(c, e, u), a && a.m(e, null), n = !0, i || (s = [
        ae(
          e,
          "click",
          /*click_handler*/
          r[5]
        ),
        ae(
          e,
          "focus",
          /*focus_handler*/
          r[6]
        ),
        ae(
          e,
          "keydown",
          /*keydown_handler*/
          r[7]
        ),
        ae(
          e,
          "keypress",
          /*keypress_handler*/
          r[8]
        ),
        ae(
          e,
          "keyup",
          /*keyup_handler*/
          r[9]
        ),
        ae(
          e,
          "mouseenter",
          /*mouseenter_handler*/
          r[10]
        ),
        ae(
          e,
          "mouseleave",
          /*mouseleave_handler*/
          r[11]
        ),
        ae(
          e,
          "mouseover",
          /*mouseover_handler*/
          r[12]
        )
      ], i = !0);
    },
    p(c, [u]) {
      a && a.p && (!n || u & /*$$scope*/
      8) && Gs(
        a,
        o,
        c,
        /*$$scope*/
        c[3],
        n ? Ds(
          o,
          /*$$scope*/
          c[3],
          u,
          null
        ) : zs(
          /*$$scope*/
          c[3]
        ),
        null
      ), qt(e, d = Ls(l, [
        u & /*$$restProps*/
        2 && /*$$restProps*/
        c[1],
        (!n || u & /*padding, $$props*/
        5 && t !== (t = he(
          /*padding*/
          c[0],
          /*$$props*/
          c[2].class
        ))) && { class: t }
      ]));
    },
    i(c) {
      n || (Hs(a, c), n = !0);
    },
    o(c) {
      Es(a, c), n = !1;
    },
    d(c) {
      c && xs(e), a && a.d(c), i = !1, Fs(s);
    }
  };
}
function js(r, e, t) {
  const n = ["padding"];
  let i = jt(e, n), { $$slots: s = {}, $$scope: o } = e, { padding: a = "px-6 py-3" } = e;
  function l(m) {
    oe.call(this, r, m);
  }
  function d(m) {
    oe.call(this, r, m);
  }
  function c(m) {
    oe.call(this, r, m);
  }
  function u(m) {
    oe.call(this, r, m);
  }
  function f(m) {
    oe.call(this, r, m);
  }
  function h(m) {
    oe.call(this, r, m);
  }
  function p(m) {
    oe.call(this, r, m);
  }
  function g(m) {
    oe.call(this, r, m);
  }
  return r.$$set = (m) => {
    t(2, e = et(et({}, e), Bt(m))), t(1, i = jt(e, n)), "padding" in m && t(0, a = m.padding), "$$scope" in m && t(3, o = m.$$scope);
  }, e = Bt(e), [
    a,
    i,
    e,
    o,
    s,
    l,
    d,
    c,
    u,
    f,
    h,
    p,
    g
  ];
}
class Bs extends As {
  constructor(e) {
    super(), Os(this, e, js, Us, Is, { padding: 0 });
  }
}
const {
  SvelteComponent: qs,
  add_flush_callback: Ts,
  append: ge,
  attr: x,
  bind: Ws,
  binding_callbacks: Vs,
  check_outros: wr,
  create_component: W,
  destroy_component: V,
  destroy_each: kr,
  detach: O,
  element: it,
  empty: st,
  ensure_array_like: je,
  flush: E,
  group_outros: Cr,
  init: Xs,
  insert: P,
  is_function: Zs,
  listen: Sr,
  mount_component: X,
  safe_not_equal: Js,
  set_data: ot,
  set_style: De,
  space: Q,
  svg_element: de,
  text: qe,
  transition_in: F,
  transition_out: H
} = window.__gradio__svelte__internal;
function Tt(r, e, t) {
  const n = r.slice();
  return n[29] = e[t], n[30] = e, n[11] = t, n;
}
function Wt(r, e, t) {
  const n = r.slice();
  return n[31] = e[t], n;
}
function Ns(r) {
  let e, t, n, i = (
    /*sortDirection*/
    r[9] === 0 && Vt()
  ), s = (
    /*sortDirection*/
    r[9] === -1 && Xt()
  ), o = (
    /*sortDirection*/
    r[9] === 1 && Zt()
  );
  return {
    c() {
      i && i.c(), e = Q(), s && s.c(), t = Q(), o && o.c(), n = st();
    },
    m(a, l) {
      i && i.m(a, l), P(a, e, l), s && s.m(a, l), P(a, t, l), o && o.m(a, l), P(a, n, l);
    },
    p(a, l) {
      /*sortDirection*/
      a[9] === 0 ? i || (i = Vt(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), /*sortDirection*/
      a[9] === -1 ? s || (s = Xt(), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*sortDirection*/
      a[9] === 1 ? o || (o = Zt(), o.c(), o.m(n.parentNode, n)) : o && (o.d(1), o = null);
    },
    d(a) {
      a && (O(e), O(t), O(n)), i && i.d(a), s && s.d(a), o && o.d(a);
    }
  };
}
function Vt(r) {
  let e, t;
  return {
    c() {
      e = de("svg"), t = de("path"), x(t, "d", "M8.771 4.67l-2.77-3.593a.196.196 0 0 0-.312 0L2.919 4.67c-.104.134-.011.33.155.33h5.541c.166 0 .259-.196.156-.33zM8.771 7.33l-2.77 3.593a.197.197 0 0 1-.312 0L2.919 7.33c-.104-.134-.011-.33.155-.33h5.541c.166 0 .259.196.156.33z"), x(t, "fill", "currentColor"), x(e, "width", "1em"), x(e, "height", "1em"), x(e, "viewBox", "0 0 12 12"), x(e, "fill", "none"), x(e, "xmlns", "http://www.w3.org/2000/svg");
    },
    m(n, i) {
      P(n, e, i), ge(e, t);
    },
    d(n) {
      n && O(e);
    }
  };
}
function Xt(r) {
  let e, t, n;
  return {
    c() {
      e = de("svg"), t = de("path"), n = de("path"), x(t, "d", "M8.771 7.33l-2.77 3.593a.197.197 0 0 1-.312 0L2.919 7.33c-.104-.134-.011-.33.155-.33h5.541c.166 0 .259.196.156.33z"), x(t, "fill", "currentColor"), x(n, "d", "M8.771 4.67l-2.77-3.593a.196.196 0 0 0-.312 0L2.919 4.67c-.104.134-.011.33.155.33h5.541c.166 0 .259-.196.156-.33z"), x(n, "fill", "#555878"), x(e, "width", "1em"), x(e, "height", "1em"), x(e, "viewBox", "0 0 12 12"), x(e, "fill", "none"), x(e, "xmlns", "http://www.w3.org/2000/svg");
    },
    m(i, s) {
      P(i, e, s), ge(e, t), ge(e, n);
    },
    d(i) {
      i && O(e);
    }
  };
}
function Zt(r) {
  let e, t, n;
  return {
    c() {
      e = de("svg"), t = de("path"), n = de("path"), x(t, "d", "M8.771 4.67l-2.77-3.593a.196.196 0 0 0-.312 0L2.919 4.67c-.104.134-.011.33.155.33h5.541c.166 0 .259-.196.156-.33z"), x(t, "fill", "currentColor"), x(n, "d", "M8.771 7.33l-2.77 3.593a.197.197 0 0 1-.312 0L2.919 7.33c-.104-.134-.011-.33.155-.33h5.541c.166 0 .259.196.156.33z"), x(n, "fill", "#555878"), x(e, "width", "1em"), x(e, "height", "1em"), x(e, "viewBox", "0 0 12 12"), x(e, "fill", "none"), x(e, "xmlns", "http://www.w3.org/2000/svg");
    },
    m(i, s) {
      P(i, e, s), ge(e, t), ge(e, n);
    },
    d(i) {
      i && O(e);
    }
  };
}
function Ks(r) {
  let e, t = (
    /*header*/
    r[31] + ""
  ), n, i, s, o, a, l = (
    /*header*/
    r[31] === "Link" && Ns(r)
  );
  return {
    c() {
      e = it("div"), n = qe(t), i = Q(), l && l.c(), s = Q(), De(e, "text-align", "left"), De(e, "display", "flex"), De(e, "flex-direction", "row"), De(e, "align-items", "center");
    },
    m(d, c) {
      P(d, e, c), ge(e, n), ge(e, i), l && l.m(e, null), P(d, s, c), o || (a = Sr(e, "click", function() {
        Zs(
          /*header*/
          r[31] === "Link" ? (
            /*click_handler*/
            r[20]
          ) : void 0
        ) && /*header*/
        (r[31] === "Link" ? (
          /*click_handler*/
          r[20]
        ) : void 0).apply(this, arguments);
      }), o = !0);
    },
    p(d, c) {
      r = d, /*header*/
      r[31] === "Link" && l.p(r, c);
    },
    d(d) {
      d && (O(e), O(s)), l && l.d(), o = !1, a();
    }
  };
}
function Jt(r) {
  let e, t;
  return e = new Bs({
    props: {
      $$slots: { default: [Ks] },
      $$scope: { ctx: r }
    }
  }), {
    c() {
      W(e.$$.fragment);
    },
    m(n, i) {
      X(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*sortDirection*/
      512 | i[1] & /*$$scope*/
      8 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (F(e.$$.fragment, n), t = !0);
    },
    o(n) {
      H(e.$$.fragment, n), t = !1;
    },
    d(n) {
      V(e, n);
    }
  };
}
function Qs(r) {
  let e, t, n = je(
    /*headers*/
    r[12]
  ), i = [];
  for (let o = 0; o < n.length; o += 1)
    i[o] = Jt(Wt(r, n, o));
  const s = (o) => H(i[o], 1, 1, () => {
    i[o] = null;
  });
  return {
    c() {
      for (let o = 0; o < i.length; o += 1)
        i[o].c();
      e = st();
    },
    m(o, a) {
      for (let l = 0; l < i.length; l += 1)
        i[l] && i[l].m(o, a);
      P(o, e, a), t = !0;
    },
    p(o, a) {
      if (a[0] & /*headers, sortDirection*/
      4608) {
        n = je(
          /*headers*/
          o[12]
        );
        let l;
        for (l = 0; l < n.length; l += 1) {
          const d = Wt(o, n, l);
          i[l] ? (i[l].p(d, a), F(i[l], 1)) : (i[l] = Jt(d), i[l].c(), F(i[l], 1), i[l].m(e.parentNode, e));
        }
        for (Cr(), l = n.length; l < i.length; l += 1)
          s(l);
        wr();
      }
    },
    i(o) {
      if (!t) {
        for (let a = 0; a < n.length; a += 1)
          F(i[a]);
        t = !0;
      }
    },
    o(o) {
      i = i.filter(Boolean);
      for (let a = 0; a < i.length; a += 1)
        H(i[a]);
      t = !1;
    },
    d(o) {
      o && O(e), kr(i, o);
    }
  };
}
function Ys(r) {
  let e = (
    /*data*/
    r[29].ligandA + ""
  ), t;
  return {
    c() {
      t = qe(e);
    },
    m(n, i) {
      P(n, t, i);
    },
    p(n, i) {
      i[0] & /*sortedTableData*/
      1024 && e !== (e = /*data*/
      n[29].ligandA + "") && ot(t, e);
    },
    d(n) {
      n && O(t);
    }
  };
}
function $s(r) {
  let e = (
    /*data*/
    r[29].ligandB + ""
  ), t;
  return {
    c() {
      t = qe(e);
    },
    m(n, i) {
      P(n, t, i);
    },
    p(n, i) {
      i[0] & /*sortedTableData*/
      1024 && e !== (e = /*data*/
      n[29].ligandB + "") && ot(t, e);
    },
    d(n) {
      n && O(t);
    }
  };
}
function eo(r) {
  var n;
  let e = (
    /*data*/
    ((n = r[29].similarity) == null ? void 0 : n.toFixed(3)) + ""
  ), t;
  return {
    c() {
      t = qe(e);
    },
    m(i, s) {
      P(i, t, s);
    },
    p(i, s) {
      var o;
      s[0] & /*sortedTableData*/
      1024 && e !== (e = /*data*/
      ((o = i[29].similarity) == null ? void 0 : o.toFixed(3)) + "") && ot(t, e);
    },
    d(i) {
      i && O(t);
    }
  };
}
function to(r) {
  let e, t, n;
  function i(a) {
    r[21](
      a,
      /*data*/
      r[29]
    );
  }
  function s(...a) {
    return (
      /*SMUISwitch_change_handler*/
      r[22](
        /*data*/
        r[29],
        /*index*/
        r[11],
        ...a
      )
    );
  }
  let o = {};
  return (
    /*data*/
    r[29].link !== void 0 && (o.checked = /*data*/
    r[29].link), e = new Dn({ props: o }), Vs.push(() => Ws(e, "checked", i)), e.$on("SMUISwitch:change", s), {
      c() {
        W(e.$$.fragment);
      },
      m(a, l) {
        X(e, a, l), n = !0;
      },
      p(a, l) {
        r = a;
        const d = {};
        !t && l[0] & /*sortedTableData*/
        1024 && (t = !0, d.checked = /*data*/
        r[29].link, Ts(() => t = !1)), e.$set(d);
      },
      i(a) {
        n || (F(e.$$.fragment, a), n = !0);
      },
      o(a) {
        H(e.$$.fragment, a), n = !1;
      },
      d(a) {
        V(e, a);
      }
    }
  );
}
function ro(r) {
  let e, t, n;
  function i() {
    return (
      /*click_handler_1*/
      r[23](
        /*data*/
        r[29],
        /*index*/
        r[11]
      )
    );
  }
  return {
    c() {
      e = it("button"), e.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.75 5.83398C1.75 3.50065 2.91667 2.33398 5.25 2.33398" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"></path><path d="M11.6641 8.75C11.6641 11.0833 10.4974 12.25 8.16406 12.25" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"></path><path d="M8.16406 5.25065C8.16406 3.63983 9.46991 2.33398 11.0807 2.33398H12.2474V6.41732H8.16406V5.25065Z" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path><path d="M1.75 8.16602H5.83333V9.33268C5.83333 10.9435 4.52748 12.2493 2.91667 12.2493H1.75V8.16602Z" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path></svg>';
    },
    m(s, o) {
      P(s, e, o), t || (n = Sr(e, "click", i), t = !0);
    },
    p(s, o) {
      r = s;
    },
    d(s) {
      s && O(e), t = !1, n();
    }
  };
}
function no(r) {
  let e, t, n, i, s, o, a, l, d, c, u;
  return e = new ye({
    props: {
      $$slots: { default: [Ys] },
      $$scope: { ctx: r }
    }
  }), n = new ye({
    props: {
      $$slots: { default: [$s] },
      $$scope: { ctx: r }
    }
  }), s = new ye({
    props: {
      $$slots: { default: [eo] },
      $$scope: { ctx: r }
    }
  }), a = new ye({
    props: {
      $$slots: { default: [to] },
      $$scope: { ctx: r }
    }
  }), d = new ye({
    props: {
      $$slots: { default: [ro] },
      $$scope: { ctx: r }
    }
  }), {
    c() {
      W(e.$$.fragment), t = Q(), W(n.$$.fragment), i = Q(), W(s.$$.fragment), o = Q(), W(a.$$.fragment), l = Q(), W(d.$$.fragment), c = Q();
    },
    m(f, h) {
      X(e, f, h), P(f, t, h), X(n, f, h), P(f, i, h), X(s, f, h), P(f, o, h), X(a, f, h), P(f, l, h), X(d, f, h), P(f, c, h), u = !0;
    },
    p(f, h) {
      const p = {};
      h[0] & /*sortedTableData*/
      1024 | h[1] & /*$$scope*/
      8 && (p.$$scope = { dirty: h, ctx: f }), e.$set(p);
      const g = {};
      h[0] & /*sortedTableData*/
      1024 | h[1] & /*$$scope*/
      8 && (g.$$scope = { dirty: h, ctx: f }), n.$set(g);
      const m = {};
      h[0] & /*sortedTableData*/
      1024 | h[1] & /*$$scope*/
      8 && (m.$$scope = { dirty: h, ctx: f }), s.$set(m);
      const _ = {};
      h[0] & /*sortedTableData, value, tableData, gradio*/
      1283 | h[1] & /*$$scope*/
      8 && (_.$$scope = { dirty: h, ctx: f }), a.$set(_);
      const w = {};
      h[0] & /*value, sortedTableData, gradio*/
      1027 | h[1] & /*$$scope*/
      8 && (w.$$scope = { dirty: h, ctx: f }), d.$set(w);
    },
    i(f) {
      u || (F(e.$$.fragment, f), F(n.$$.fragment, f), F(s.$$.fragment, f), F(a.$$.fragment, f), F(d.$$.fragment, f), u = !0);
    },
    o(f) {
      H(e.$$.fragment, f), H(n.$$.fragment, f), H(s.$$.fragment, f), H(a.$$.fragment, f), H(d.$$.fragment, f), u = !1;
    },
    d(f) {
      f && (O(t), O(i), O(o), O(l), O(c)), V(e, f), V(n, f), V(s, f), V(a, f), V(d, f);
    }
  };
}
function Nt(r) {
  let e, t;
  return e = new ps({
    props: {
      $$slots: { default: [no] },
      $$scope: { ctx: r }
    }
  }), {
    c() {
      W(e.$$.fragment);
    },
    m(n, i) {
      X(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*value, sortedTableData, gradio, tableData*/
      1283 | i[1] & /*$$scope*/
      8 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (F(e.$$.fragment, n), t = !0);
    },
    o(n) {
      H(e.$$.fragment, n), t = !1;
    },
    d(n) {
      V(e, n);
    }
  };
}
function io(r) {
  let e, t, n = je(
    /*sortedTableData*/
    r[10]
  ), i = [];
  for (let o = 0; o < n.length; o += 1)
    i[o] = Nt(Tt(r, n, o));
  const s = (o) => H(i[o], 1, 1, () => {
    i[o] = null;
  });
  return {
    c() {
      for (let o = 0; o < i.length; o += 1)
        i[o].c();
      e = st();
    },
    m(o, a) {
      for (let l = 0; l < i.length; l += 1)
        i[l] && i[l].m(o, a);
      P(o, e, a), t = !0;
    },
    p(o, a) {
      if (a[0] & /*value, sortedTableData, gradio, tableData*/
      1283) {
        n = je(
          /*sortedTableData*/
          o[10]
        );
        let l;
        for (l = 0; l < n.length; l += 1) {
          const d = Tt(o, n, l);
          i[l] ? (i[l].p(d, a), F(i[l], 1)) : (i[l] = Nt(d), i[l].c(), F(i[l], 1), i[l].m(e.parentNode, e));
        }
        for (Cr(), l = n.length; l < i.length; l += 1)
          s(l);
        wr();
      }
    },
    i(o) {
      if (!t) {
        for (let a = 0; a < n.length; a += 1)
          F(i[a]);
        t = !0;
      }
    },
    o(o) {
      i = i.filter(Boolean);
      for (let a = 0; a < i.length; a += 1)
        H(i[a]);
      t = !1;
    },
    d(o) {
      o && O(e), kr(i, o);
    }
  };
}
function so(r) {
  let e, t, n, i;
  return e = new Ss({
    props: {
      $$slots: { default: [Qs] },
      $$scope: { ctx: r }
    }
  }), n = new Ei({
    props: {
      $$slots: { default: [io] },
      $$scope: { ctx: r }
    }
  }), {
    c() {
      W(e.$$.fragment), t = Q(), W(n.$$.fragment);
    },
    m(s, o) {
      X(e, s, o), P(s, t, o), X(n, s, o), i = !0;
    },
    p(s, o) {
      const a = {};
      o[0] & /*sortDirection*/
      512 | o[1] & /*$$scope*/
      8 && (a.$$scope = { dirty: o, ctx: s }), e.$set(a);
      const l = {};
      o[0] & /*sortedTableData, value, gradio, tableData*/
      1283 | o[1] & /*$$scope*/
      8 && (l.$$scope = { dirty: o, ctx: s }), n.$set(l);
    },
    i(s) {
      i || (F(e.$$.fragment, s), F(n.$$.fragment, s), i = !0);
    },
    o(s) {
      H(e.$$.fragment, s), H(n.$$.fragment, s), i = !1;
    },
    d(s) {
      s && O(t), V(e, s), V(n, s);
    }
  };
}
function oo(r) {
  let e, t, n, i;
  return t = new ki({
    props: {
      $$slots: { default: [so] },
      $$scope: { ctx: r }
    }
  }), {
    c() {
      e = it("div"), W(t.$$.fragment), x(e, "class", "fep-pair-container svelte-1dgkx0j"), x(e, "style", n = /*max_height*/
      r[7] ? `max-height: ${/*max_height*/
      r[7]}px` : "");
    },
    m(s, o) {
      P(s, e, o), X(t, e, null), i = !0;
    },
    p(s, o) {
      const a = {};
      o[0] & /*sortedTableData, value, gradio, tableData, sortDirection*/
      1795 | o[1] & /*$$scope*/
      8 && (a.$$scope = { dirty: o, ctx: s }), t.$set(a), (!i || o[0] & /*max_height*/
      128 && n !== (n = /*max_height*/
      s[7] ? `max-height: ${/*max_height*/
      s[7]}px` : "")) && x(e, "style", n);
    },
    i(s) {
      i || (F(t.$$.fragment, s), i = !0);
    },
    o(s) {
      H(t.$$.fragment, s), i = !1;
    },
    d(s) {
      s && O(e), V(t);
    }
  };
}
function ao(r) {
  let e, t;
  return e = new jr({
    props: {
      visible: (
        /*visible*/
        r[4]
      ),
      elem_id: (
        /*elem_id*/
        r[2]
      ),
      elem_classes: (
        /*elem_classes*/
        r[3]
      ),
      scale: (
        /*scale*/
        r[5]
      ),
      min_width: (
        /*min_width*/
        r[6]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [oo] },
      $$scope: { ctx: r }
    }
  }), {
    c() {
      W(e.$$.fragment);
    },
    m(n, i) {
      X(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*visible*/
      16 && (s.visible = /*visible*/
      n[4]), i[0] & /*elem_id*/
      4 && (s.elem_id = /*elem_id*/
      n[2]), i[0] & /*elem_classes*/
      8 && (s.elem_classes = /*elem_classes*/
      n[3]), i[0] & /*scale*/
      32 && (s.scale = /*scale*/
      n[5]), i[0] & /*min_width*/
      64 && (s.min_width = /*min_width*/
      n[6]), i[0] & /*max_height, sortedTableData, value, gradio, tableData, sortDirection*/
      1923 | i[1] & /*$$scope*/
      8 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (F(e.$$.fragment, n), t = !0);
    },
    o(n) {
      H(e.$$.fragment, n), t = !1;
    },
    d(n) {
      V(e, n);
    }
  };
}
function lo(r, e, t) {
  this && this.__awaiter;
  let { gradio: n } = e, { label: i = "Textbox" } = e, { elem_id: s = "" } = e, { elem_classes: o = [] } = e, { visible: a = !0 } = e, { value: l = "" } = e, { placeholder: d = "" } = e, { show_label: c } = e, { scale: u = null } = e, { min_width: f = void 0 } = e, { loading_status: h = void 0 } = e, { value_is_output: p = !1 } = e, { interactive: g } = e, { rtl: m = !1 } = e, { max_height: _ } = e;
  const w = ["LigandA", "LigandB", "Similarity", "Link", "Mapping"];
  let A = [], R = 1, y = 0, b = [];
  const M = () => {
    t(10, b = [
      ...y === 0 ? A : [...A].sort((k, D) => (k.link - D.link) * y)
    ]);
  }, J = () => {
    const { pairs: k } = JSON.parse(d);
    t(8, A = [
      ...k.map((D, I) => Object.assign(Object.assign({}, D), { index: I }))
    ]), t(11, R++, R);
  }, Y = () => {
    switch (y) {
      case 0:
        t(9, y = 1);
        break;
      case 1:
        t(9, y = -1);
        break;
      case -1:
        t(9, y = 0);
        break;
      default:
        t(9, y = 0);
        break;
    }
  };
  function $(k, D) {
    r.$$.not_equal(D.link, k) && (D.link = k, t(10, b));
  }
  const L = (k, D, I) => {
    t(0, l = JSON.stringify({
      res: { ...k, link: A[D].link },
      type: "Link",
      index: D
    })), n.dispatch("change");
  }, S = (k, D) => {
    t(0, l = JSON.stringify({ res: k, type: "Mapping", index: D })), n.dispatch("change");
  };
  return r.$$set = (k) => {
    "gradio" in k && t(1, n = k.gradio), "label" in k && t(13, i = k.label), "elem_id" in k && t(2, s = k.elem_id), "elem_classes" in k && t(3, o = k.elem_classes), "visible" in k && t(4, a = k.visible), "value" in k && t(0, l = k.value), "placeholder" in k && t(14, d = k.placeholder), "show_label" in k && t(15, c = k.show_label), "scale" in k && t(5, u = k.scale), "min_width" in k && t(6, f = k.min_width), "loading_status" in k && t(16, h = k.loading_status), "value_is_output" in k && t(17, p = k.value_is_output), "interactive" in k && t(18, g = k.interactive), "rtl" in k && t(19, m = k.rtl), "max_height" in k && t(7, _ = k.max_height);
  }, r.$$.update = () => {
    r.$$.dirty[0] & /*value*/
    1 && l === null && t(0, l = ""), r.$$.dirty[0] & /*value*/
    1, r.$$.dirty[0] & /*placeholder*/
    16384 && J(), r.$$.dirty[0] & /*tableData*/
    256 && M(), r.$$.dirty[0] & /*sortDirection*/
    512 && M();
  }, [
    l,
    n,
    s,
    o,
    a,
    u,
    f,
    _,
    A,
    y,
    b,
    R,
    w,
    i,
    d,
    c,
    h,
    p,
    g,
    m,
    Y,
    $,
    L,
    S
  ];
}
class co extends qs {
  constructor(e) {
    super(), Xs(
      this,
      e,
      lo,
      ao,
      Js,
      {
        gradio: 1,
        label: 13,
        elem_id: 2,
        elem_classes: 3,
        visible: 4,
        value: 0,
        placeholder: 14,
        show_label: 15,
        scale: 5,
        min_width: 6,
        loading_status: 16,
        value_is_output: 17,
        interactive: 18,
        rtl: 19,
        max_height: 7
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), E();
  }
  get label() {
    return this.$$.ctx[13];
  }
  set label(e) {
    this.$$set({ label: e }), E();
  }
  get elem_id() {
    return this.$$.ctx[2];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), E();
  }
  get elem_classes() {
    return this.$$.ctx[3];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), E();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({ visible: e }), E();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), E();
  }
  get placeholder() {
    return this.$$.ctx[14];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), E();
  }
  get show_label() {
    return this.$$.ctx[15];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), E();
  }
  get scale() {
    return this.$$.ctx[5];
  }
  set scale(e) {
    this.$$set({ scale: e }), E();
  }
  get min_width() {
    return this.$$.ctx[6];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), E();
  }
  get loading_status() {
    return this.$$.ctx[16];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), E();
  }
  get value_is_output() {
    return this.$$.ctx[17];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), E();
  }
  get interactive() {
    return this.$$.ctx[18];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), E();
  }
  get rtl() {
    return this.$$.ctx[19];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), E();
  }
  get max_height() {
    return this.$$.ctx[7];
  }
  set max_height(e) {
    this.$$set({ max_height: e }), E();
  }
}
export {
  co as default
};
