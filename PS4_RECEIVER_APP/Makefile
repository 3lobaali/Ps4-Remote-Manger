# ==========================================================
# Bisan Remote Receiver - OpenOrbis Build
# ==========================================================

TITLE_ID := ODAI00001
APP_TITLE := Bisan Remote Receiver
APP_VERSION := 01.00

TARGET := eboot
ELF := $(TARGET).elf
EBOOT := eboot.bin

SRCS := main.c
OBJS := $(SRCS:.c=.o)

CC := clang
CREATE_EBOOT := create-eboot

PS4_TARGET := x86_64-scei-ps4

CFLAGS := -O2 -Wall -target $(PS4_TARGET)

LDFLAGS := -target $(PS4_TARGET)

LIBS := -lSceLibcInternal -lSceNet

all: $(EBOOT)

$(ELF): $(OBJS)
\t$(CC) $(OBJS) $(LDFLAGS) $(LIBS) -o $@

%.o: %.c
\t$(CC) $(CFLAGS) -c $< -o $@

$(EBOOT): $(ELF)
\t$(CREATE_EBOOT) $(ELF) $(EBOOT)

clean:
\trm -f $(OBJS) $(ELF) $(EBOOT) *.pkg
