/* fractal.c: draws one fractal picture for the Seahorse Valley theme, sharp at full screen size.

   Build: gcc -O3 -march=native -fopenmp -o fractal fractal.c -lm
   Usage: fractal <kind> <width> <height> <out.ppm> key=value ...
   Writes an 8-bit binary PPM (sRGB, lightly dithered so smooth gradients do not band).

   Kinds (all drawn here from their formulas, nothing downloaded):
     mandel   the Mandelbrot set, z -> z^2 + c from z = 0
     julia    a Julia set, z -> z^2 + c with c fixed (ca, cb) and z from the pixel
     ship     the Burning Ship, z -> (|Re z| + i|Im z|)^2 + c, drawn upside down as usual so the ship stands up
     newton   Newton's method for z^3 = 1: each point coloured by the root it runs to
     lyap     a Lyapunov fractal of the logistic map, x -> r x (1 - x), r taking a (x axis) and b (y axis) by seq
     buddha   the Buddhabrot: where the escaping orbits of the Mandelbrot set go, three iteration limits as three colours
     bulb     the Mandelbulb (power 8), lit and shaded in 3D

   Every pixel is ss x ss samples (ss=4: 16), each coloured, then averaged in linear light: edges and fine threads stay
   sharp without stair steps or sparkle. Common keys: cx cy (centre), w (width of the view), rot (degrees),
   maxiter, ss, grad (colour stops "pos:rrggbb,..." looping at 1), scale offset (how fast the colours cycle),
   map (log, sqrt or lin), inside (colour of points that never escape), de (darken by distance to the set, 0 = off).
*/
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXP 64
static const char *keys[MAXP];
static const char *vals[MAXP];
static int nkv;

static const char *sget(const char *k, const char *d) {
  for (int i = 0; i < nkv; i++)
    if (!strcmp(keys[i], k)) return vals[i];
  return d;
}
static double dget(const char *k, double d) {
  const char *s = sget(k, NULL);
  return s ? atof(s) : d;
}

/* ---------- colour ---------- */
typedef struct { double r, g, b; } rgb;

static double s2l(double c) { return c <= 0.04045 ? c / 12.92 : pow((c + 0.055) / 1.055, 2.4); }
static double l2s(double c) {
  if (c <= 0) return 0;
  if (c >= 1) return 1;
  return c <= 0.0031308 ? c * 12.92 : 1.055 * pow(c, 1 / 2.4) - 0.055;
}
static rgb hex(const char *h) {
  unsigned v = (unsigned)strtoul(h, NULL, 16);
  rgb c = {((v >> 16) & 255) / 255.0, ((v >> 8) & 255) / 255.0, (v & 255) / 255.0};
  return c;
}
static rgb lin(rgb c) { rgb o = {s2l(c.r), s2l(c.g), s2l(c.b)}; return o; }
static rgb mix(rgb a, rgb b, double t) { rgb o = {a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t}; return o; }
static rgb mul(rgb a, double k) { rgb o = {a.r * k, a.g * k, a.b * k}; return o; }
static rgb add(rgb a, rgb b) { rgb o = {a.r + b.r, a.g + b.g, a.b + b.b}; return o; }

/* a looping gradient: stops in sRGB, monotone cubic (Fritsch-Carlson) per channel, so no overshoot and no flat
   rings at the stops; looked up from a 4096-entry table in linear light */
#define GN 4096
typedef struct { rgb t[GN]; } grad;

static void grad_make(grad *g, const char *spec) {
  double pos[34], ch[3][34];
  int n = 0;
  char buf[2048];
  snprintf(buf, sizeof buf, "%s", spec);
  for (char *tok = strtok(buf, ","); tok && n < 32; tok = strtok(NULL, ",")) {
    char *c = strchr(tok, ':');
    if (!c) continue;
    *c = 0;
    pos[n + 1] = atof(tok);
    rgb v = hex(c + 1);
    ch[0][n + 1] = v.r, ch[1][n + 1] = v.g, ch[2][n + 1] = v.b;
    n++;
  }
  /* wrap: one stop before (last - 1) and one after (first + 1) */
  pos[0] = pos[n] - 1, pos[n + 1] = pos[1] + 1;
  for (int k = 0; k < 3; k++) ch[k][0] = ch[k][n], ch[k][n + 1] = ch[k][1];
  int m = n + 2;
  for (int k = 0; k < 3; k++) {
    double d[34], s[34];
    for (int i = 0; i < m - 1; i++) d[i] = (ch[k][i + 1] - ch[k][i]) / (pos[i + 1] - pos[i]);
    s[0] = d[0], s[m - 1] = d[m - 2];
    for (int i = 1; i < m - 1; i++) s[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
    for (int i = 0; i < m - 1; i++) {
      if (d[i] == 0) { s[i] = s[i + 1] = 0; continue; }
      double a = s[i] / d[i], b = s[i + 1] / d[i], h = a * a + b * b;
      if (h > 9) { double t = 3 / sqrt(h); s[i] = t * a * d[i]; s[i + 1] = t * b * d[i]; }
    }
    for (int j = 0; j < GN; j++) {
      double x = (double)j / GN;
      int i = 0;
      while (i < m - 2 && pos[i + 1] <= x) i++;
      double hh = pos[i + 1] - pos[i], t = (x - pos[i]) / hh;
      double t2 = t * t, t3 = t2 * t;
      double v = (2 * t3 - 3 * t2 + 1) * ch[k][i] + (t3 - 2 * t2 + t) * hh * s[i] + (-2 * t3 + 3 * t2) * ch[k][i + 1] +
                 (t3 - t2) * hh * s[i + 1];
      v = v < 0 ? 0 : v > 1 ? 1 : v;
      double *dst = k == 0 ? &g->t[j].r : k == 1 ? &g->t[j].g : &g->t[j].b;
      *dst = s2l(v);
    }
  }
}
static rgb glook(const grad *g, double x) {
  x -= floor(x);
  double f = x * GN;
  int i = (int)f;
  double t = f - i;
  return mix(g->t[i % GN], g->t[(i + 1) % GN], t);
}

/* ---------- small helpers ---------- */
static uint32_t hash(uint32_t x) {
  x ^= x >> 16; x *= 0x7feb352dU; x ^= x >> 15; x *= 0x846ca68bU; x ^= x >> 16;
  return x;
}
static double rnd(uint32_t a, uint32_t b) { return hash(a * 0x9E3779B1U ^ hash(b + 0x632BE5ABU)) / 4294967296.0; }

static int W, H, SS;
static double CX, CY, VW, ROT_C, ROT_S, PIX;
static grad G;
static rgb INSIDE;
static double SCALE, OFFSET, DE, GLOW, FLOOR, NULO, NUHI;
static int MAP, MAXIT;

/* sample (sx, sy) in pixel units -> point of the plane */
static void plane(double sx, double sy, double *x, double *y, int flip) {
  double u = (sx - W / 2.0) * PIX, v = (H / 2.0 - sy) * PIX;
  if (flip) v = -v;
  *x = CX + u * ROT_C - v * ROT_S;
  *y = CY + u * ROT_S + v * ROT_C;
}

static double smooth(double a, double b, double x) {
  double t = (x - a) / (b - a);
  t = t < 0 ? 0 : t > 1 ? 1 : t;
  return t * t * (3 - 2 * t);
}

/* nu: smooth escape count; de: distance to the set in plane units (-1 = not known) */
static rgb escape_colour(double nu, double de) {
  double t;
  if (MAP == 0) t = log(nu + 1);
  else if (MAP == 1) t = sqrt(nu);
  else t = nu;
  rgb c = glook(&G, t * SCALE + OFFSET);
  if (DE > 0 && de >= 0) {         /* thin threads of the set: darken close to it, like ink lines */
    double k = de / PIX / DE;
    k = k > 1 ? 1 : k;
    c = mul(c, 0.25 + 0.75 * pow(k, 0.5));
  }
  /* a dark sky: light only near the set, fading out over glow x the view's width */
  if (GLOW > 0 && de >= 0) c = mul(c, FLOOR + (1 - FLOOR) * exp(-de / (GLOW * VW)));
  if (NUHI > 0) c = mul(c, FLOOR + (1 - FLOOR) * smooth(NULO, NUHI, nu));
  return c;
}

/* ---------- escape-time kinds ---------- */
static rgb sample_escape(int kind, double x, double y) {
  const double R2 = 1e6;
  double zx, zy, cx, cy, dzx = 0, dzy = 0;
  if (kind == 1) { zx = x; zy = y; cx = dget("ca", -0.123); cy = dget("cb", 0.745); dzx = 1; }
  else { zx = 0; zy = 0; cx = x; cy = y; }
  if (kind == 0) {  /* inside the main cardioid or the period-2 bulb: never escapes */
    double q = (x - 0.25) * (x - 0.25) + y * y;
    if (q * (q + (x - 0.25)) <= 0.25 * y * y || (x + 1) * (x + 1) + y * y <= 0.0625) return INSIDE;
  }
  double px = 0, py = 0;
  int period = 8, since = 0;
  double trap = 1e9;
  for (int i = 0; i < MAXIT; i++) {
    double x2 = zx * zx, y2 = zy * zy;
    if (x2 + y2 > R2) {
      double lz = 0.5 * log(x2 + y2);
      double nu = i + 1 - log2(lz);
      double de = -1;
      if ((DE > 0 || GLOW > 0) && kind != 2) {
        double dz = sqrt(dzx * dzx + dzy * dzy);
        de = dz > 0 ? sqrt(x2 + y2) * lz / dz : 1e9;
      }
      return escape_colour(nu, de);
    }
    if (kind != 2) {  /* derivative for the distance estimate: dz -> 2 z dz (+1 for the Mandelbrot set) */
      double nx = 2 * (zx * dzx - zy * dzy) + (kind == 0 ? 1 : 0);
      double ny = 2 * (zx * dzy + zy * dzx);
      dzx = nx, dzy = ny;
    }
    double nzx, nzy;
    if (kind == 2) { nzx = x2 - y2 + cx; nzy = 2 * fabs(zx * zy) + cy; }
    else { nzx = x2 - y2 + cx; nzy = 2 * zx * zy + cy; }
    zx = nzx, zy = nzy;
    double r = zx * zx + zy * zy;
    if (r < trap) trap = r;
    /* the orbit came back to an earlier point: it is caught in a cycle and never escapes */
    if (fabs(zx - px) < 1e-15 && fabs(zy - py) < 1e-15) break;
    if (++since == period) { since = 0; period *= 2; px = zx; py = zy; }
  }
  if (kind == 1 && dget("inside_trap", 0) > 0) {   /* a Julia set's inside: shaded by how close the orbit comes to 0 */
    rgb a = INSIDE, b = lin(hex(sget("inside2", "0b1a3c")));
    double t = pow(sqrt(trap), dget("inside_trap", 1));
    return mix(b, a, t > 1 ? 1 : t);
  }
  return INSIDE;
}

/* ---------- Newton's method for z^3 = 1 ---------- */
static rgb sample_newton(double x, double y) {
  static const double rr[3][2] = {{1, 0}, {-0.5, 0.8660254037844386}, {-0.5, -0.8660254037844386}};
  const double tol = 1e-6, lt = log(tol);
  double zx = x, zy = y;
  for (int i = 0; i < MAXIT; i++) {
    for (int k = 0; k < 3; k++) {
      double dx = zx - rr[k][0], dy = zy - rr[k][1], d = sqrt(dx * dx + dy * dy);
      if (d < tol) {
        /* smooth step count: near a root each step squares the distance, so log d / log tol runs 1..2 */
        double s = i - log2(fmax(log(fmax(d, 1e-300)) / lt, 1.0));
        rgb root = glook(&G, dget("root0", 0.0) + k * dget("rootstep", 1 / 3.0));
        rgb shade = glook(&G, s * SCALE + OFFSET);
        double br = dget("bright", 0);   /* bright > 0: dark basins, light on the slow, braided borders */
        double fade = NUHI > 0 ? smooth(NULO, NUHI, s) : br > 0 ? 1 - exp(-s * br) : exp(-s * dget("fade", 0.08));
        return mul(mix(root, shade, dget("shade", 0.6)), FLOOR + (1 - FLOOR) * fade);
      }
    }
    double r2 = zx * zx - zy * zy, i2 = 2 * zx * zy;          /* z^2 */
    double fx = r2 * zx - i2 * zy - 1, fy = r2 * zy + i2 * zx;   /* z^3 - 1 */
    double gx = 3 * r2, gy = 3 * i2;                             /* 3 z^2 */
    double den = gx * gx + gy * gy;
    if (den == 0) break;
    zx -= (fx * gx + fy * gy) / den, zy -= (fy * gx - fx * gy) / den;
  }
  return INSIDE;
}

/* ---------- Lyapunov fractal ---------- */
static const char *SEQ;
static int SEQN, WARM, NLY, SWAP;
static rgb sample_lyap(double a, double b) {
  double x = 0.5, sum = 0;
  for (int n = 0; n < WARM; n++) {
    double r = SEQ[n % SEQN] == 'A' ? a : b;
    x = r * x * (1 - x);
  }
  for (int n = 0; n < NLY; n++) {
    double r = SEQ[(n + WARM) % SEQN] == 'A' ? a : b;
    x = r * x * (1 - x);
    double d = fabs(r * (1 - 2 * x));
    sum += log(d > 1e-300 ? d : 1e-300);
  }
  double lam = sum / NLY;
  if (lam < 0) {   /* order: the gold side of the gradient, brighter the more stable */
    double t = 1 - exp(lam * dget("kstable", 1.6));
    return glook(&G, dget("gold0", 0.62) - t * dget("goldspan", 0.22));
  }
  double t = 1 - exp(-lam * dget("kchaos", 3.0));  /* chaos: the blue side, deep navy at the edge of order */
  return glook(&G, dget("blue0", 0.02) + t * dget("bluespan", 0.2));
}

/* ---------- Mandelbulb ---------- */
typedef struct { double x, y, z; } v3;
static v3 V(double x, double y, double z) { v3 v = {x, y, z}; return v; }
static v3 vadd(v3 a, v3 b) { return V(a.x + b.x, a.y + b.y, a.z + b.z); }
static v3 vsub(v3 a, v3 b) { return V(a.x - b.x, a.y - b.y, a.z - b.z); }
static v3 vmul(v3 a, double k) { return V(a.x * k, a.y * k, a.z * k); }
static double dot(v3 a, v3 b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
static v3 cross(v3 a, v3 b) { return V(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x); }
static v3 norm(v3 a) { return vmul(a, 1 / sqrt(dot(a, a))); }

static double POW;
static int BITER;
static double bulb_de(v3 p, double *trap) {
  v3 z = p;
  double dr = 1, r = 0, t = 1e9;
  for (int i = 0; i < BITER; i++) {
    r = sqrt(dot(z, z));
    if (r > 2) break;
    double th = acos(z.z / r), ph = atan2(z.y, z.x);
    dr = pow(r, POW - 1) * POW * dr + 1;
    double zr = pow(r, POW);
    th *= POW, ph *= POW;
    z = vadd(vmul(V(sin(th) * cos(ph), sin(ph) * sin(th), cos(th)), zr), p);
    double q = dot(z, z);
    if (q < t) t = q;
  }
  if (trap) *trap = t;
  return 0.5 * log(r) * r / dr;
}
static v3 CAM, FWD, RIGHT, UP;
static double FOV;
static v3 LIGHT;
static rgb bulb_sky(v3 d) {
  rgb top = lin(hex(sget("sky_top", "0a1636"))), bot = lin(hex(sget("sky_bottom", "02040c")));
  double t = 0.5 + 0.5 * d.y;
  return mix(bot, top, t * t);
}
static rgb sample_bulb(double sx, double sy) {
  double u = (sx - W / 2.0) / (H / 2.0) * tan(FOV / 2), v = (H / 2.0 - sy) / (H / 2.0) * tan(FOV / 2);
  v3 d = norm(vadd(FWD, vadd(vmul(RIGHT, u), vmul(UP, v))));
  /* start on the bounding sphere (radius 1.25) */
  double b = dot(CAM, d), cc = dot(CAM, CAM) - 1.25 * 1.25, disc = b * b - cc;
  if (disc < 0) return bulb_sky(d);
  double t = -b - sqrt(disc);
  if (t < 0) t = 0;
  double tmax = -b + sqrt(disc);
  double pix = 2 * tan(FOV / 2) / H;    /* size of one pixel at distance 1 */
  int hit = 0, steps = 0;
  double trap = 0;
  for (; steps < 400 && t < tmax; steps++) {
    v3 p = vadd(CAM, vmul(d, t));
    double de = bulb_de(p, &trap);
    if (de < t * pix * 0.5) { hit = 1; break; }
    t += de * 0.9;
  }
  if (!hit) return bulb_sky(d);
  v3 p = vadd(CAM, vmul(d, t));
  double e = t * pix * 0.5;
  v3 n = norm(V(bulb_de(vadd(p, V(e, 0, 0)), NULL) - bulb_de(vsub(p, V(e, 0, 0)), NULL),
                bulb_de(vadd(p, V(0, e, 0)), NULL) - bulb_de(vsub(p, V(0, e, 0)), NULL),
                bulb_de(vadd(p, V(0, 0, e)), NULL) - bulb_de(vsub(p, V(0, 0, e)), NULL)));
  /* ambient occlusion: how open the space is along the normal */
  double ao = 0, w = 1;
  for (int k = 1; k <= 5; k++) {
    double h = 0.012 * k * k;
    ao += w * (h - bulb_de(vadd(p, vmul(n, h)), NULL));
    w *= 0.55;
  }
  ao = 1 - ao * dget("ao", 6.0);
  ao = ao < 0 ? 0 : ao > 1 ? 1 : ao;
  /* soft shadow toward the key light */
  double sh = 1, st = 4 * e + 0.002;
  for (int k = 0; k < 120 && st < 3; k++) {
    double h = bulb_de(vadd(p, vmul(LIGHT, st)), NULL);
    if (h < 1e-5) { sh = 0; break; }
    double s = 12 * h / st;
    if (s < sh) sh = s;
    st += h > 0.002 ? h : 0.002;
  }
  sh = sh < 0 ? 0 : sh;
  rgb base = glook(&G, sqrt(trap) * SCALE + OFFSET);
  double dif = dot(n, LIGHT);
  dif = dif < 0 ? 0 : dif;
  rgb key = lin(hex(sget("key", "ffd9a0"))), fill = lin(hex(sget("fill", "4f86d9")));
  double fil = 0.5 + 0.5 * dot(n, norm(V(-LIGHT.x, 0.6, -LIGHT.z)));
  v3 hv = norm(vsub(LIGHT, d));
  double spec = pow(fmax(dot(n, hv), 0), 48) * sh;
  double rim = pow(1 - fmax(dot(n, vmul(d, -1)), 0), 3);
  rgb c;
  c.r = base.r * (key.r * dif * sh * 1.6 + fill.r * fil * 0.35 * ao) + key.r * spec * 0.6 + fill.r * rim * 0.25 * ao;
  c.g = base.g * (key.g * dif * sh * 1.6 + fill.g * fil * 0.35 * ao) + key.g * spec * 0.6 + fill.g * rim * 0.25 * ao;
  c.b = base.b * (key.b * dif * sh * 1.6 + fill.b * fil * 0.35 * ao) + key.b * spec * 0.6 + fill.b * rim * 0.25 * ao;
  c = mul(c, (0.25 + 0.75 * ao) * dget("exposure", 1));
  /* a little depth fog into the sky colour */
  double fog = 1 - exp(-pow(fmax(t - dget("fog_from", 1.5), 0), 2) * dget("fog", 0.0));
  return mix(c, bulb_sky(d), fog);
}

/* ---------- Buddhabrot ---------- */
static int buddha(const char *out_path) {
  int lim[3] = {(int)dget("lim0", 50), (int)dget("lim1", 500), (int)dget("lim2", 5000)};
  /* orbits that escape in very few steps fill the whole disc |z| < 2 with haze: each layer can leave them out */
  int mn[3] = {(int)dget("min0", 0), (int)dget("min1", 0), (int)dget("min2", 0)};
  long long samples = (long long)dget("samples", 1e8);
  int maxlim = lim[0] > lim[1] ? lim[0] : lim[1];
  maxlim = maxlim > lim[2] ? maxlim : lim[2];
  size_t np = (size_t)W * H;
  uint32_t *hist = calloc(np * 3, sizeof(uint32_t));
  if (!hist) { fprintf(stderr, "no memory\n"); return 1; }
  #pragma omp parallel
  {
    double *ox = malloc(sizeof(double) * maxlim), *oy = malloc(sizeof(double) * maxlim);
    #pragma omp for schedule(dynamic, 4096)
    for (long long s = 0; s < samples; s++) {
      double cx = -2.0 + 2.5 * rnd((uint32_t)s, (uint32_t)(s >> 32) ^ 17), cy = -1.25 + 2.5 * rnd((uint32_t)s, (uint32_t)(s >> 32) ^ 91);
      double q = (cx - 0.25) * (cx - 0.25) + cy * cy;
      if (q * (q + (cx - 0.25)) <= 0.25 * cy * cy || (cx + 1) * (cx + 1) + cy * cy <= 0.0625) continue;
      double zx = 0, zy = 0;
      int n = 0, esc = 0;
      for (; n < maxlim; n++) {
        double nzx = zx * zx - zy * zy + cx;
        zy = 2 * zx * zy + cy;
        zx = nzx;
        ox[n] = zx, oy[n] = zy;
        if (zx * zx + zy * zy > 4) { esc = 1; break; }
      }
      if (!esc || n < 3) continue;
      for (int k = 0; k < 3; k++) {
        if (n >= lim[k] || n < mn[k]) continue;
        for (int i = 0; i < n; i++) {
          /* the real axis points down the screen, so the figure sits upright (its round "head" is at -2) */
          double u = oy[i], v = -ox[i];
          double sx = (u * ROT_C - v * ROT_S - (CX)) / PIX + W / 2.0;
          double sy = H / 2.0 - (u * ROT_S + v * ROT_C - (CY)) / PIX;
          int ix = (int)sx, iy = (int)sy;
          if (ix < 0 || iy < 0 || ix >= W || iy >= H) continue;
          #pragma omp atomic
          hist[((size_t)iy * W + ix) * 3 + k]++;
        }
      }
    }
    free(ox), free(oy);
  }
  /* tone: each layer scaled by a high percentile of its own counts, then a power curve */
  rgb col[3] = {lin(hex(sget("col0", "3c7fd6"))), lin(hex(sget("col1", "e8f2ff"))), lin(hex(sget("col2", "ffae2e")))};
  double gam = dget("gamma", 0.55), pct = dget("pct", 0.9995);
  double top[3];
  uint32_t *tmp = malloc(np * sizeof(uint32_t));
  for (int k = 0; k < 3; k++) {
    for (size_t i = 0; i < np; i++) tmp[i] = hist[i * 3 + k];
    /* percentile by counting */
    uint32_t mx = 0;
    for (size_t i = 0; i < np; i++) if (tmp[i] > mx) mx = tmp[i];
    size_t *cnt = calloc((size_t)mx + 1, sizeof(size_t));
    for (size_t i = 0; i < np; i++) cnt[tmp[i]]++;
    size_t want = (size_t)(pct * np), acc = 0;
    uint32_t v = 0;
    for (; v <= mx; v++) { acc += cnt[v]; if (acc >= want) break; }
    top[k] = v > 0 ? v : 1;
    free(cnt);
  }
  free(tmp);
  rgb bg = lin(hex(sget("bg", "03060f")));
  FILE *f = fopen(out_path, "wb");
  fprintf(f, "P6\n%d %d\n255\n", W, H);
  unsigned char *row = malloc((size_t)W * 3);
  for (int y = 0; y < H; y++) {
    for (int x = 0; x < W; x++) {
      rgb c = bg;
      for (int k = 0; k < 3; k++) {
        /* black: the even haze of paths that circle a while and then fly off fills the disc |z| < 2; counts below
           this share of the layer's top are dark, so only the figure glows */
        double blk = dget(k == 0 ? "black0" : k == 1 ? "black1" : "black2", 0);
        double v = (hist[((size_t)y * W + x) * 3 + k] / top[k] - blk) / (1 - blk);
        v = pow(v > 0 ? v : 0, gam);
        c = add(c, mul(col[k], v * dget(k == 0 ? "k0" : k == 1 ? "k1" : "k2", 1)));
      }
      /* soft clip so the brightest core stays white, not flat */
      double m = fmax(c.r, fmax(c.g, c.b));
      if (m > 1) c = mix(mul(c, 1 / m), (rgb){1, 1, 1}, fmin((m - 1) * 0.3, 1));
      double d = (rnd(x, y) + rnd(y + 7, x + 3) - 1) / 255.0;
      row[x * 3] = (unsigned char)fmin(255, fmax(0, l2s(c.r) * 255 + 0.5 + d * 255));
      row[x * 3 + 1] = (unsigned char)fmin(255, fmax(0, l2s(c.g) * 255 + 0.5 + d * 255));
      row[x * 3 + 2] = (unsigned char)fmin(255, fmax(0, l2s(c.b) * 255 + 0.5 + d * 255));
    }
    fwrite(row, 1, (size_t)W * 3, f);
  }
  fclose(f);
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 5) {
    fprintf(stderr, "usage: fractal <kind> <width> <height> <out.ppm> key=value ...\n");
    return 2;
  }
  const char *kind_s = argv[1];
  W = atoi(argv[2]), H = atoi(argv[3]);
  const char *out = argv[4];
  for (int i = 5; i < argc && nkv < MAXP; i++) {
    char *e = strchr(argv[i], '=');
    if (!e) continue;
    *e = 0;
    keys[nkv] = argv[i], vals[nkv] = e + 1, nkv++;
  }
  SS = (int)dget("ss", 4);
  CX = dget("cx", -0.5), CY = dget("cy", 0), VW = dget("w", 3.5);
  double rot = dget("rot", 0) * M_PI / 180;
  ROT_C = cos(rot), ROT_S = sin(rot);
  PIX = VW / W;
  MAXIT = (int)dget("maxiter", 1000);
  SCALE = dget("scale", 0.1), OFFSET = dget("offset", 0);
  DE = dget("de", 0), GLOW = dget("glow", 0), FLOOR = dget("floor", 0.15);
  NULO = dget("nulo", 0), NUHI = dget("nuhi", 0);
  const char *m = sget("map", "log");
  MAP = !strcmp(m, "log") ? 0 : !strcmp(m, "sqrt") ? 1 : 2;
  grad_make(&G, sget("grad", "0:000764,0.16:206bcb,0.42:edffff,0.6425:ffaa00,0.8575:000200"));
  INSIDE = lin(hex(sget("inside", "02040c")));

  int kind = !strcmp(kind_s, "mandel") ? 0 : !strcmp(kind_s, "julia") ? 1 : !strcmp(kind_s, "ship") ? 2
           : !strcmp(kind_s, "newton") ? 3 : !strcmp(kind_s, "lyap") ? 4 : !strcmp(kind_s, "bulb") ? 5
           : !strcmp(kind_s, "buddha") ? 6 : -1;
  if (kind < 0) { fprintf(stderr, "unknown kind %s\n", kind_s); return 2; }
  if (kind == 6) return buddha(out);
  if (kind == 4) {
    SEQ = sget("seq", "AB"), SEQN = (int)strlen(SEQ);
    WARM = (int)dget("warm", 300), NLY = (int)dget("n", 1500), SWAP = (int)dget("swap", 0);
  }
  if (kind == 5) {
    POW = dget("power", 8), BITER = (int)dget("biter", 12);
    CAM = V(dget("camx", 0), dget("camy", 0.4), dget("camz", -2.6));
    v3 at = V(dget("atx", 0), dget("aty", 0), dget("atz", 0));
    FWD = norm(vsub(at, CAM));
    RIGHT = norm(cross(V(0, 1, 0), FWD));
    UP = cross(FWD, RIGHT);
    FOV = dget("fov", 40) * M_PI / 180;
    LIGHT = norm(V(dget("lx", -0.6), dget("ly", 0.8), dget("lz", -0.5)));
  }
  int flip = kind == 2 ? 1 : 0;
  double lyA0 = dget("a0", 3.4), lyA1 = dget("a1", 4.0), lyB0 = dget("b0", 2.5), lyB1 = dget("b1", 3.4);

  unsigned char *img = malloc((size_t)W * H * 3);
  int done = 0;
  #pragma omp parallel for schedule(dynamic, 1)
  for (int y = 0; y < H; y++) {
    for (int x = 0; x < W; x++) {
      rgb acc = {0, 0, 0};
      for (int j = 0; j < SS; j++)
        for (int i = 0; i < SS; i++) {
          /* one sample in each cell of an ss x ss grid, at a fixed random spot in the cell */
          double sx = x + (i + rnd(x * 131 + i, y * 977 + j)) / SS;
          double sy = y + (j + rnd(y * 389 + j, x * 613 + i + 5)) / SS;
          rgb c;
          if (kind == 4) {
            double fx = sx / W, fy = sy / H;      /* swap=1: b across, a up the screen */
            double a = SWAP ? lyA0 + (lyA1 - lyA0) * (1 - fy) : lyA0 + (lyA1 - lyA0) * fx;
            double b = SWAP ? lyB0 + (lyB1 - lyB0) * fx : lyB1 - (lyB1 - lyB0) * fy;
            c = sample_lyap(a, b);
          } else if (kind == 5) {
            c = sample_bulb(sx, sy);
          } else {
            double px, py;
            plane(sx, sy, &px, &py, flip);
            c = kind == 3 ? sample_newton(px, py) : sample_escape(kind, px, py);
          }
          acc = add(acc, c);
        }
      acc = mul(acc, 1.0 / (SS * SS));
      /* dither: triangular noise of one step, so smooth navy skies do not band */
      double d = rnd(x, y) + rnd(y + 7, x + 3) - 1;
      unsigned char *p = img + ((size_t)y * W + x) * 3;
      p[0] = (unsigned char)fmin(255, fmax(0, l2s(acc.r) * 255 + 0.5 + d));
      p[1] = (unsigned char)fmin(255, fmax(0, l2s(acc.g) * 255 + 0.5 + d));
      p[2] = (unsigned char)fmin(255, fmax(0, l2s(acc.b) * 255 + 0.5 + d));
    }
    #pragma omp atomic
    done++;
    if (done % 216 == 0) fprintf(stderr, "\r%d%%", done * 100 / H);
  }
  fprintf(stderr, "\r100%%\n");
  FILE *f = fopen(out, "wb");
  if (!f) { perror(out); return 1; }
  fprintf(f, "P6\n%d %d\n255\n", W, H);
  fwrite(img, 1, (size_t)W * H * 3, f);
  fclose(f);
  return 0;
}
