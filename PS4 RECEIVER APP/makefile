# إعدادات OpenOrbis SDK لبناء PKG البلايستيشن
TITLE_ID    := ODAI00001
APP_TITLE   := Bisan Remote Receiver
BOOSTER     := 1
ICON        := icon0.png

# المترجم والأدوات
CC          := clang
CFLAGS      := -O2 -Wall
LDFLAGS     := -lkernel -lSceNet -lpthread

SRCS        := main.c
OBJS        := $(SRCS:.c=.o)
TARGET      := $(TITLE_ID).elf
PKG_OUTPUT  := $(TITLE_ID).pkg

all: $(TARGET) pkg

$(TARGET): $(OBJS)
\t$(CC) $(OBJS) $(LDFLAGS) -o $@

%.o: %.c
\t$(CC) $(CFLAGS) -c $< -o $@

pkg: $(TARGET)
\t@echo "=== Building PKG ==="
\t@ls -la $(ICON) || (echo "ERROR: $(ICON) not found!" && exit 1)
\tcreate-pkg --titleid $(TITLE_ID) --title "$(APP_TITLE)" --icon $(ICON) $(TARGET) $(PKG_OUTPUT)

clean:
\trm -f $(OBJS) $(TARGET) $(PKG_OUTPUT)
