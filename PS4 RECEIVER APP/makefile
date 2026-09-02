name: Build Bisan Remote Receiver

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

jobs:
  build-pkg:
    name: Build PS4 PKG
    runs-on: ubuntu-latest

    container:
      image: openorbisofficial/toolchain:latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Show toolchain information
        run: |
          echo "OO_PS4_TOOLCHAIN=$OO_PS4_TOOLCHAIN"
          echo "PATH=$PATH"
          clang --version || true
          find "$OO_PS4_TOOLCHAIN" -maxdepth 3 -type f \
            ( -name "create-pkg" -o -name "create-fself" ) \
            -print || true

      - name: Show project files
        run: |
          ls -la
          ls -la PS4_RECEIVER_APP
          test -f PS4_RECEIVER_APP/main.c
          test -f PS4_RECEIVER_APP/Makefile
          test -f PS4_RECEIVER_APP/icon0.png

      - name: Build PS4 application and PKG
        working-directory: PS4_RECEIVER_APP
        run: |
          make clean
          make

      - name: Show generated PKG
        run: |
          find PS4_RECEIVER_APP -type f ( -iname "*.pkg" -o -iname "*.elf" ) -print

      - name: Upload PKG artifact
        uses: actions/upload-artifact@v4
        with:
          name: Bisan-Remote-Receiver-PKG
          path: PS4_RECEIVER_APP/*.pkg
          if-no-files-found: error
