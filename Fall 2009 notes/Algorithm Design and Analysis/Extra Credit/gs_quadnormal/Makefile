
TARGETS = gs_quadnormal

UNAME := $(shell uname)

GLEW  := ../../glew

GS_QUADNORMAL_C = gs_quadnormal.c fast_teapot.c

GS_QUADNORMAL_OBJS = $(GS_QUADNORMAL_C:.c=.o) 

CC         =  gcc
CFLAGS     += -Wall
CFLAGS     += -I"$(GLEW)/include"
CFLAGS     += -DGLEW_STATIC
ifdef CG_INC_PATH
  CFLAGS   += -I"$(CG_INC_PATH)"
endif

ifdef CG_LIB_PATH
    CLINKFLAGS += -L"$(CG_LIB_PATH)"
endif


ifeq ($(UNAME), Darwin)
  CLINKFLAGS += -L"$(GLEW)"
  CLINKFLAGS += -lGLEW
  CLINKFLAGS += -framework Cg
  CLINKFLAGS += -framework GLUT
  CLINKFLAGS += -framework OpenGL
else
  ifeq ($(findstring CYGWIN, $(UNAME)), CYGWIN)
    CFLAGS     += -D_WIN32
    CFLAGS     += -DGLUT_DISABLE_ATEXIT_HACK
    CFLAGS     += -I"C:\Program Files\NVIDIA Corporation\Cg\include"
    CLINKFLAGS += -L"$(GLEW)"
    CLINKFLAGS += -lGLEW
    CLINKFLAGS += -L"C:\Program Files\NVIDIA Corporation\Cg\lib"
    CLINKFLAGS += -lcgGL -lcg
    CLINKFLAGS += -lglut32
    CLINKFLAGS += -lglu32 -lopengl32
    EXE = .exe
  else
    ifeq ($(UNAME), SunOS)
      CLINKFLAGS += -L"$(GLEW)"
      CLINKFLAGS += -lGLEW
      CLINKFLAGS += -lCgGL -lCg
      CLINKFLAGS += -L/usr/X11R6/lib64 -L/usr/X11R6/lib
      CLINKFLAGS += -lglut -lXi -lXmu -lX11 -lm
      CLINKFLAGS += -lGLU -lGL
      CLINKFLAGS += -lpthread
    else
      CLINKFLAGS += -L"$(GLEW)"
      CLINKFLAGS += -lGLEW
      CLINKFLAGS += -lCgGL -lCg
      CLINKFLAGS += -L/usr/X11R6/lib64 -L/usr/X11R6/lib
      CLINKFLAGS += -lglut -lXi -lXmu -lX11 -lm
      CLINKFLAGS += -lGLU -lGL
      CLINKFLAGS += -lpthread
    endif
  endif
endif

BINARIES := $(TARGETS:=$(EXE))

all: $(BINARIES)

glew:
	$(MAKE) -C '$(GLEW)' -f Makefile

.PHONY: glew


gs_quadnormal$(EXE): glew $(GS_QUADNORMAL_OBJS)
	$(CC) $(CFLAGS) $(GS_QUADNORMAL_OBJS) -o $@ $(CLINKFLAGS)

run: all
	./gs_quadnormal$(EXE)

clean:
	$(RM) $(BINARIES) $(GS_QUADNORMAL_OBJS) 
	$(MAKE) -C '$(GLEW)' -f Makefile clean

clobber: clean
	$(RM) *.bak *.o *~

.PHONY: all run clean clobber
