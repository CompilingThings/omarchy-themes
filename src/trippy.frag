// trippy.frag: Good Trip's moving patterns, drawn on the graphics chip by trippygl.c (see trippyvid.py for the keys).
// src/trippyvid.py puts a header in front of this file: #version, KIND, the keys as #defines and the colour stops
// (GN, GP[], GC[] in linear light). uT runs 0 -> 1 over the loop; every motion below comes back to its start at
// uT = 1, so the video loops without a seam:
//   colours flow round the gradient CYC times, the kaleidoscope turns SPIN wedges, the Julia constant c walks a
//   circle of radius CRAD, the tunnel falls ZOOM tiles deeper, the liquid's noise walks a circle of radius FLOW.

const float PI = 3.14159265358979;
const float TAU = 6.28318530717959;

vec3 glook(float x) {
  x = fract(x);
  for (int i = 0; i < GN - 1; i++) {
    if (x >= GP[i] && x < GP[i + 1]) return mix(GC[i], GC[i + 1], smoothstep(0.0, 1.0, (x - GP[i]) / (GP[i + 1] - GP[i])));
  }
  // the wrap: from the last stop round to the first
  float span = GP[0] + 1.0 - GP[GN - 1];
  float u = x >= GP[GN - 1] ? x - GP[GN - 1] : x + 1.0 - GP[GN - 1];
  return mix(GC[GN - 1], GC[0], smoothstep(0.0, 1.0, u / span));
}

float l2s1(float c) { return c <= 0.0031308 ? c * 12.92 : 1.055 * pow(c, 1.0 / 2.4) - 0.055; }
vec3 l2s(vec3 c) { c = clamp(c, 0.0, 1.0); return vec3(l2s1(c.r), l2s1(c.g), l2s1(c.b)); }

float OFF() { return OFFSET + CYC * uT; }

vec2 kfold(vec2 p) {
  float r = length(p), th = atan(p.y, p.x);
  if (TWIST != 0.0 && r > 0.0) th += TWIST * log(r);
  if (FOLD > 0.0) {
    float seg = TAU / FOLD;
    th += SPIN * seg * uT;
    th = mod(th, seg);
    if (MIRROR > 0.5) th = abs(th - seg * 0.5);
  }
  return r * vec2(cos(th), sin(th));
}

vec2 cconst() { return vec2(CA, CB) + CRAD * vec2(cos(TAU * uT), sin(TAU * uT)); }

// mandala (lace) and bloom (petals): a Julia set with orbit traps
vec3 orbit(vec2 p, bool bloom) {
  vec2 z = p * ZS + vec2(ZX, ZY), c = cconst();
  float tc = 1e9, tx = 1e9, m = 0.0;
  int n = 0;
  bool esc = false;
  vec3 petals = vec3(0.0);
  float dec = 1.0;
  for (int i = 0; i < MAXIT; i++) {
    z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
    m = dot(z, z);
    float r = sqrt(m);
    tc = min(tc, abs(r - TR));
    tx = min(tx, min(abs(z.x), abs(z.y)));
    if (bloom) {
      float a = atan(z.y, z.x);
      float pr = PR * (1.0 + PA * cos(PK * a));
      float dp = abs(r - pr);
      petals += glook(OFF() + float(i) * TSTEP) * exp(-dp / PETW) * dec;
      dec *= PDEC;
    }
    n = i;
    if (m > 1e4) { esc = true; break; }
  }
  vec3 col = BG;
  if (esc) {
    float nu = float(n) + 2.0 - log(log(m) / 2.0 / log(2.0)) / log(2.0);
    float e = pow(clamp(nu / float(MAXIT) * ESCK, 0.0, 1.0), ESCG);
    col += glook(SCALE * log(nu + 1.0) + OFF()) * e;
  }
  if (bloom) col += petals * LACE;
  else {
    col += glook(OFF() + 0.33 + tc * 3.0) * exp(-tc / LACEK) * LACE;
    col += glook(OFF() + 0.66 + tx * 3.0) * exp(-tx / (LACEK * 0.6)) * LACE * CROSS;
  }
  return col;
}

// liquid: domain-warped value noise
float hash2(vec2 q) {
  uvec2 u = uvec2(ivec2(q) + 32768);
  uint h = u.x * 0x9E3779B1u ^ (u.y * 0x85EBCA77u);
  h ^= h >> 16; h *= 0x7feb352du; h ^= h >> 15; h *= 0x846ca68bu; h ^= h >> 16;
  return float(h) / 4294967296.0;
}
float vnoise(vec2 p) {
  vec2 i = floor(p), f = p - i;
  vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
  float a = hash2(i), b = hash2(i + vec2(1.0, 0.0)), c = hash2(i + vec2(0.0, 1.0)), d = hash2(i + vec2(1.0, 1.0));
  return a + (b - a) * u.x + (c - a) * u.y + (a - b - c + d) * u.x * u.y;
}
float fbm(vec2 p) {
  float s = 0.0, a = 0.5;
  for (int i = 0; i < 6; i++) {
    s += a * vnoise(p);
    p = mat2(1.6, -1.2, 1.2, 1.6) * p + vec2(17.3, 9.1);
    a *= 0.5;
  }
  return s;
}
vec3 liquid(vec2 p) {
  vec2 x = p * WS + FLOW * vec2(cos(TAU * uT), sin(TAU * uT));
  vec2 q = vec2(fbm(x), fbm(x + vec2(5.2, 1.3)));
  vec2 r = vec2(fbm(x + WK * q + vec2(1.7, 9.2)), fbm(x + WK * q + vec2(8.3, 2.8)));
  float f = fbm(x + WK * r);
  float t = f * SCALE + length(q) * 0.6 + r.x * 0.4 + OFF();
  float v = pow(clamp(f * 1.6 - 0.25, 0.0, 1.0), LGAM);
  vec3 col = BG + glook(t) * v;
  col += glook(t + 0.5) * exp(-abs(f - 0.5) / RIDGEK) * RIDGE;
  return col;
}

// tunnel: a folded Julia flower repeated down a log-polar spiral
float tri(float x) { x = fract(x); return 1.0 - abs(2.0 * x - 1.0); }
vec3 tunnel(vec2 p) {
  float r = max(length(p), 1e-6), th = atan(p.y, p.x);
  float lr = log(r);
  float u = tri(lr * DEPTH + th / TAU * SPIRAL - ZOOM * uT), v = tri(th / TAU * REP);
  vec2 q = (vec2(u, v) - 0.5) * TS;
  q = kfold(q);
  vec3 col = orbit(q, INNER_BLOOM > 0.5);
  col = mix(BG, col, pow(clamp(r / FADE, 0.0, 1.0), 0.9));
  col += glook(OFF() + 0.5) * CORE * exp(-r / CORES);
  return col;
}

// hyper: a hyperbolic {p,q} tiling, turning round its centre
vec3 hyper(vec2 p) {
  vec2 z = p;
  if (MODEL > 0.5) {               // band model: tanh maps the strip |Im w| < pi/4 onto the disk
    float e2 = exp(2.0 * z.x), cs = cos(2.0 * z.y), sn = sin(2.0 * z.y);
    float den = e2 * e2 + 2.0 * e2 * cs + 1.0;
    z = vec2((e2 * e2 - 1.0) / den, 2.0 * e2 * sn / den);
  }
  float rr = dot(z, z);
  if (rr >= 1.0) return BG;
  float HA = PI / HP, HB = PI / HQ;
  float HD = cos(HB) / sqrt(cos(HB) * cos(HB) - sin(HA) * sin(HA)), HR = sqrt(HD * HD - 1.0);
  // turn by SPIN tile-corners over the loop (a symmetry of the tiling, so it loops)
  float a0 = SPIN * 2.0 * HA * uT;
  z = mat2(cos(a0), sin(a0), -sin(a0), cos(a0)) * z;
  float count = 0.0;
  for (int it = 0; it < 200; it++) {
    float r = length(z), th = atan(z.y, z.x);
    float seg = 2.0 * HA;
    float t2 = mod(th, seg);
    if (t2 > HA) { t2 = seg - t2; count += 1.0; }
    z = r * vec2(cos(t2), sin(t2));
    vec2 d = z - vec2(HD, 0.0);
    float d2 = dot(d, d);
    if (d2 < HR * HR) { z = vec2(HD, 0.0) + d * (HR * HR / d2); count += 1.0; }
    else break;
  }
  float dline = abs(-sin(HA) * z.x + cos(HA) * z.y);
  float dcirc = abs(length(z - vec2(HD, 0.0)) - HR);
  float inner = length(z);
  vec3 tile = glook(OFF() + count * CSTEP + inner * SCALE);
  float fill = 0.25 + 0.75 * pow(clamp(1.0 - inner / (HD - HR), 0.0, 1.0), TILEK);
  vec3 col = BG + tile * fill * TFILL;
  col += glook(OFF() + count * CSTEP + 0.5) * EDGE * exp(-dcirc / EDGEK);
  col += glook(OFF() + count * CSTEP + 0.25) * EDGE * 0.6 * exp(-dline / EDGEK);
  return mix(BG, col, clamp((1.0 - rr) * 6.0, 0.0, 1.0));
}

vec3 sample1(vec2 px) {
  vec2 uv = (px - 0.5 * uRes) * (VW / uRes.x);
  uv.y = -uv.y;
  float ro = ROT * PI / 180.0;
  vec2 p = vec2(CX, CY) + mat2(cos(ro), sin(ro), -sin(ro), cos(ro)) * uv;
#if KIND == 0
  return orbit(kfold(p), false);
#elif KIND == 1
  return orbit(kfold(p), true);
#elif KIND == 2
  return liquid(kfold(p));
#elif KIND == 3
  return tunnel(p);
#else
  return hyper(p);
#endif
}

void main() {
  vec2 fc = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y);
  vec3 acc = vec3(0.0);
  for (int j = 0; j < SS; j++)
    for (int i = 0; i < SS; i++) acc += sample1(fc - 0.5 + (vec2(float(i), float(j)) + 0.5) / float(SS));
  acc *= GAIN / float(SS * SS);
  float mx = max(acc.r, max(acc.g, acc.b));
  if (mx > 1.0) acc = mix(acc / mx, vec3(1.0), min((mx - 1.0) * 0.25, 1.0));
  // a little dither so smooth glows do not band
  float d = (hash2(fc * 1.37) + hash2(fc.yx * 2.11 + 7.0) - 1.0) / 255.0;
  oColor = vec4(l2s(acc) + d, 1.0);
}
