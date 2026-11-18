#!/bin/bash
# Rebuild the Devoxx4Kids MicroBlocks firmware and the bomb image file system for the
# M5Stack Core2 v1.3. Needs git, Python 3 with platformio and esptool, and internet access.
# Usage: firmware/build.sh            (from the workshop folder)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BASE=f4767a3
WORK="${WORK:-$(mktemp -d)}"

git clone --quiet --branch dev https://codeberg.org/MicroBlocks/smallvm.git "$WORK/smallvm"
cd "$WORK/smallvm"
git checkout --quiet "$BASE"
git apply "$HERE/microblocks-core2-v1.3.patch"
cp "$HERE/d4kLogo.h" vm/   # the start-up logo, included by the patched tftPrims.cpp

rm -rf data
mkdir data
cp "$HERE"/images/*.data data/

pio run -e m5core2
pio run -e m5core2 -t buildfs

B=.pio/build/m5core2
BOOT_APP0="$(find "${PLATFORMIO_CORE_DIR:-$HOME/.platformio}/packages" -name boot_app0.bin | head -1)"
esptool --chip esp32 merge-bin --flash-size 16MB -o "$HERE/microblocks-core2-v1.3.bin" \
  0x1000 "$B/bootloader.bin" 0x8000 "$B/partitions.bin" 0xe000 "$BOOT_APP0" 0x10000 "$B/firmware.bin"
cp "$B/littlefs.bin" "$HERE/bomb-images.bin"

cd "$HERE"
shasum -a 256 microblocks-core2-v1.3.bin bomb-images.bin
