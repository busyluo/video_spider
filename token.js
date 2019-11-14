
function bin_stringToBytes(e) {
    for (var t = [], r = 0; r < e.length; r++) t.push(255 & e.charCodeAt(r));
    return t
  }
function bin_bytesToString(e) {
    for (var t = [], r = 0; r < e.length; r++) t.push(String.fromCharCode(e[r]));
    return t.join("")
  }

function stringToBytes(e) {
    return bin_stringToBytes(unescape(encodeURIComponent(e)))
}

function bytesToWords(e) {
    for (var t = [], r = 0, n = 0; r < e.length; r++, n += 8) t[n >>> 5] |= e[r] << 24 - n % 32;
    return t
}

function rotl(e, t) {
    return e << t | e >>> 32 - t
}

function endian(e) {
    if (e.constructor == Number) return 16711935 & rotl(e, 8) | 4278255360 & rotl(e, 24);
    for (var t = 0; t < e.length; t++) e[t] = endian(e[t]);
    return e
}

function wordsToBytes(e) {
  for (var t = [], r = 0; r < 32 * e.length; r += 8) t.push(e[r >>> 5] >>> 24 - r % 32 & 255);
  return t
}

function bytesToHex(e) {
  for (var t = [], r = 0; r < e.length; r++) t.push((e[r] >>> 4).toString(16)), t.push((15 & e[r]).toString(16));
  return t.join("")
}

_ff = function (e, t, r, n, o, a, i) {
  var c = e + (t & r | ~t & n) + (o >>> 0) + i;
  return (c << a | c >>> 32 - a) + t
};
_gg = function (e, t, r, n, o, a, i) {
  var c = e + (t & n | r & ~n) + (o >>> 0) + i;
  return (c << a | c >>> 32 - a) + t
};
_hh = function (e, t, r, n, o, a, i) {
  var c = e + (t ^ r ^ n) + (o >>> 0) + i;
  return (c << a | c >>> 32 - a) + t
};
_ii = function (e, t, r, n, o, a, i) {
  var c = e + (r ^ (t | ~n)) + (o >>> 0) + i;
  return (c << a | c >>> 32 - a) + t
}

function c(e) {
    e = stringToBytes(e)
    for (var r = bytesToWords(e), s = 8 * e.length, l = 1732584193, u = -271733879, _ = -1732584194, d = 271733878, p = 0; p < r.length; p++) r[p] = 16711935 & (r[p] << 8 | r[p] >>> 24) | 4278255360 & (r[p] << 24 | r[p] >>> 8);
    r[s >>> 5] |= 128 << s % 32, r[14 + (s + 64 >>> 9 << 4)] = s;
    var f = _ff,
      h = _gg,
      m = _hh,
      v = _ii;
    for (p = 0; p < r.length; p += 16) {
      var g = l,
        b = u,
        y = _,
        M = d;
      u = v(u = v(u = v(u = v(u = m(u = m(u = m(u = m(u = h(u = h(u = h(u = h(u = f(u = f(u = f(u = f(u, _ = f(_, d = f(d, l = f(l, u, _, d, r[p + 0], 7, -680876936), u, _, r[p + 1], 12, -389564586), l, u, r[p + 2], 17, 606105819), d, l, r[p + 3], 22, -1044525330), _ = f(_, d = f(d, l = f(l, u, _, d, r[p + 4], 7, -176418897), u, _, r[p + 5], 12, 1200080426), l, u, r[p + 6], 17, -1473231341), d, l, r[p + 7], 22, -45705983), _ = f(_, d = f(d, l = f(l, u, _, d, r[p + 8], 7, 1770035416), u, _, r[p + 9], 12, -1958414417), l, u, r[p + 10], 17, -42063), d, l, r[p + 11], 22, -1990404162), _ = f(_, d = f(d, l = f(l, u, _, d, r[p + 12], 7, 1804603682), u, _, r[p + 13], 12, -40341101), l, u, r[p + 14], 17, -1502002290), d, l, r[p + 15], 22, 1236535329), _ = h(_, d = h(d, l = h(l, u, _, d, r[p + 1], 5, -165796510), u, _, r[p + 6], 9, -1069501632), l, u, r[p + 11], 14, 643717713), d, l, r[p + 0], 20, -373897302), _ = h(_, d = h(d, l = h(l, u, _, d, r[p + 5], 5, -701558691), u, _, r[p + 10], 9, 38016083), l, u, r[p + 15], 14, -660478335), d, l, r[p + 4], 20, -405537848), _ = h(_, d = h(d, l = h(l, u, _, d, r[p + 9], 5, 568446438), u, _, r[p + 14], 9, -1019803690), l, u, r[p + 3], 14, -187363961), d, l, r[p + 8], 20, 1163531501), _ = h(_, d = h(d, l = h(l, u, _, d, r[p + 13], 5, -1444681467), u, _, r[p + 2], 9, -51403784), l, u, r[p + 7], 14, 1735328473), d, l, r[p + 12], 20, -1926607734), _ = m(_, d = m(d, l = m(l, u, _, d, r[p + 5], 4, -378558), u, _, r[p + 8], 11, -2022574463), l, u, r[p + 11], 16, 1839030562), d, l, r[p + 14], 23, -35309556), _ = m(_, d = m(d, l = m(l, u, _, d, r[p + 1], 4, -1530992060), u, _, r[p + 4], 11, 1272893353), l, u, r[p + 7], 16, -155497632), d, l, r[p + 10], 23, -1094730640), _ = m(_, d = m(d, l = m(l, u, _, d, r[p + 13], 4, 681279174), u, _, r[p + 0], 11, -358537222), l, u, r[p + 3], 16, -722521979), d, l, r[p + 6], 23, 76029189), _ = m(_, d = m(d, l = m(l, u, _, d, r[p + 9], 4, -640364487), u, _, r[p + 12], 11, -421815835), l, u, r[p + 15], 16, 530742520), d, l, r[p + 2], 23, -995338651), _ = v(_, d = v(d, l = v(l, u, _, d, r[p + 0], 6, -198630844), u, _, r[p + 7], 10, 1126891415), l, u, r[p + 14], 15, -1416354905), d, l, r[p + 5], 21, -57434055), _ = v(_, d = v(d, l = v(l, u, _, d, r[p + 12], 6, 1700485571), u, _, r[p + 3], 10, -1894986606), l, u, r[p + 10], 15, -1051523), d, l, r[p + 1], 21, -2054922799), _ = v(_, d = v(d, l = v(l, u, _, d, r[p + 8], 6, 1873313359), u, _, r[p + 15], 10, -30611744), l, u, r[p + 6], 15, -1560198380), d, l, r[p + 13], 21, 1309151649), _ = v(_, d = v(d, l = v(l, u, _, d, r[p + 4], 6, -145523070), u, _, r[p + 11], 10, -1120210379), l, u, r[p + 2], 15, 718787259), d, l, r[p + 9], 21, -343485551), l = l + g >>> 0, u = u + b >>> 0, _ = _ + y >>> 0, d = d + M >>> 0
    }
    return endian([l, u, _, d])
}

function enc(e) {
    var cres = c(e)
    var r = wordsToBytes(cres);
    return bytesToHex(r)
}

function get_token(x_time) {
    t = "5ec029c599f7abec29ebf1c50fcc05a0";
    // r = Math.round((new Date).getTime() / 1e3).toString(16);
    var pp = "".concat(t).concat(x_time);
    var tt = enc(pp);

    return tt.toLowerCase()
}