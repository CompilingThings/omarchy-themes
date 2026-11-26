/* trippygl.c: runs one fragment shader on the graphics chip, frame after frame, and writes the frames as raw RGB24
   to standard output (for ffmpeg to encode). No window: an EGL surfaceless context and an offscreen framebuffer.

   Build: gcc -O2 -o trippygl trippygl.c -lEGL -lGLESv2
   Usage: trippygl <shader.frag> <width> <height> <frames> [first] [step] > frames.rgb
   The shader (GLSL ES 3.10) gets   uniform vec2 uRes   (width, height in pixels)
                                    uniform float uT    (loop phase: frame / frames, 0 <= uT < 1)
   and writes   out vec4 oColor   in sRGB. The frames are drawn in tiles of 256 rows, so a heavy shader never runs
   long enough in one go for the driver to reset the chip. With first/step only every step-th frame from first is drawn
   (a quick preview of a long loop).
*/
#include <EGL/egl.h>
#include <EGL/eglext.h>
#include <GLES3/gl31.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *slurp(const char *path) {
  FILE *f = fopen(path, "rb");
  if (!f) { perror(path); exit(1); }
  fseek(f, 0, SEEK_END);
  long n = ftell(f);
  fseek(f, 0, SEEK_SET);
  char *s = malloc(n + 1);
  if (fread(s, 1, n, f) != (size_t)n) { perror(path); exit(1); }
  s[n] = 0;
  fclose(f);
  return s;
}

static GLuint shader(GLenum kind, const char *src) {
  GLuint s = glCreateShader(kind);
  glShaderSource(s, 1, &src, NULL);
  glCompileShader(s);
  GLint ok;
  glGetShaderiv(s, GL_COMPILE_STATUS, &ok);
  if (!ok) {
    char log[8192];
    glGetShaderInfoLog(s, sizeof log, NULL, log);
    fprintf(stderr, "shader error:\n%s\n", log);
    exit(1);
  }
  return s;
}

int main(int argc, char **argv) {
  if (argc < 5) {
    fprintf(stderr, "usage: trippygl <shader.frag> <width> <height> <frames> [first] [step]\n");
    return 2;
  }
  const char *frag = slurp(argv[1]);
  int W = atoi(argv[2]), H = atoi(argv[3]), N = atoi(argv[4]);
  int first = argc > 5 ? atoi(argv[5]) : 0, step = argc > 6 ? atoi(argv[6]) : 1;

  PFNEGLGETPLATFORMDISPLAYEXTPROC getdisp = (PFNEGLGETPLATFORMDISPLAYEXTPROC)eglGetProcAddress("eglGetPlatformDisplayEXT");
  EGLDisplay dpy = getdisp ? getdisp(EGL_PLATFORM_SURFACELESS_MESA, EGL_DEFAULT_DISPLAY, NULL) : EGL_NO_DISPLAY;
  if (dpy == EGL_NO_DISPLAY) dpy = eglGetDisplay(EGL_DEFAULT_DISPLAY);
  if (!eglInitialize(dpy, NULL, NULL)) { fprintf(stderr, "eglInitialize failed\n"); return 1; }
  eglBindAPI(EGL_OPENGL_ES_API);
  EGLint cfga[] = {EGL_RENDERABLE_TYPE, EGL_OPENGL_ES3_BIT, EGL_NONE};
  EGLConfig cfg;
  EGLint ncfg = 0;
  eglChooseConfig(dpy, cfga, &cfg, 1, &ncfg);
  EGLint ctxa[] = {EGL_CONTEXT_MAJOR_VERSION, 3, EGL_CONTEXT_MINOR_VERSION, 1, EGL_NONE};
  EGLContext ctx = eglCreateContext(dpy, ncfg ? cfg : EGL_NO_CONFIG_KHR, EGL_NO_CONTEXT, ctxa);
  if (ctx == EGL_NO_CONTEXT) { fprintf(stderr, "eglCreateContext failed\n"); return 1; }
  eglMakeCurrent(dpy, EGL_NO_SURFACE, EGL_NO_SURFACE, ctx);
  fprintf(stderr, "GPU: %s\n", glGetString(GL_RENDERER));

  GLuint tex, fbo;
  glGenTextures(1, &tex);
  glBindTexture(GL_TEXTURE_2D, tex);
  glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA8, W, H);
  glGenFramebuffers(1, &fbo);
  glBindFramebuffer(GL_FRAMEBUFFER, fbo);
  glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0);

  const char *vert = "#version 310 es\nvoid main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);"
                     "gl_Position=vec4(p*2.0-1.0,0.0,1.0);}\n";
  GLuint prog = glCreateProgram();
  glAttachShader(prog, shader(GL_VERTEX_SHADER, vert));
  glAttachShader(prog, shader(GL_FRAGMENT_SHADER, frag));
  glLinkProgram(prog);
  GLint ok;
  glGetProgramiv(prog, GL_LINK_STATUS, &ok);
  if (!ok) { fprintf(stderr, "link failed\n"); return 1; }
  glUseProgram(prog);
  GLuint vao;
  glGenVertexArrays(1, &vao);
  glBindVertexArray(vao);
  glUniform2f(glGetUniformLocation(prog, "uRes"), (float)W, (float)H);
  GLint uT = glGetUniformLocation(prog, "uT");
  glViewport(0, 0, W, H);
  glEnable(GL_SCISSOR_TEST);

  unsigned char *rgba = malloc((size_t)W * H * 4), *rgb = malloc((size_t)W * H * 3);
  for (int f = first; f < N; f += step) {
    glUniform1f(uT, (float)f / N);
    for (int y0 = 0; y0 < H; y0 += 256) {
      glScissor(0, y0, W, 256);
      glDrawArrays(GL_TRIANGLES, 0, 3);
      glFinish();
    }
    glReadPixels(0, 0, W, H, GL_RGBA, GL_UNSIGNED_BYTE, rgba);
    /* GL rows run bottom up; the video runs top down */
    for (int y = 0; y < H; y++) {
      const unsigned char *s = rgba + (size_t)(H - 1 - y) * W * 4;
      unsigned char *d = rgb + (size_t)y * W * 3;
      for (int x = 0; x < W; x++) d[x * 3] = s[x * 4], d[x * 3 + 1] = s[x * 4 + 1], d[x * 3 + 2] = s[x * 4 + 2];
    }
    fwrite(rgb, 1, (size_t)W * H * 3, stdout);
    fflush(stdout);
    fprintf(stderr, "\rframe %d/%d", f + 1, N);
  }
  fprintf(stderr, "\n");
  return 0;
}
