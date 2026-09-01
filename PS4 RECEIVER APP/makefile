# إعدادات OpenOrbis SDK لبناء PKG البلايستيشن
TITLE_ID    := ODAI00001
APP_TITLE   := PS4 Remote Receiver
BOOSTER     := 1
ICON        := icon0.png

# المترجم والأدوات
CC          := clang
CFLAGS      := -O2 -Wall
LDFLAGS     := -lkernel -lSceNet

SRCS        := main.c
OBJS        := $(SRCS:.c=.o)
TARGET      := $(TITLE_ID).elf

all: $(TARGET) pkg

$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

pkg:
	create-pkg --titleid $(TITLE_ID) --title "$(APP_TITLE)" --icon $(ICON) $(TARGET) app.pkg

clean:
	rm -f $(OBJS) $(TARGET) app.pkg
