#!/bin/bash
# create multiresolution windows icon
ICON_SRC=../../src/qt/res/icons/cryptotarget100M.png
ICON_DST=../../src/qt/res/icons/cryptotarget100M.ico
convert ${ICON_SRC} -resize 16x16 cryptotarget100M-16.png
convert ${ICON_SRC} -resize 32x32 cryptotarget100M-32.png
convert ${ICON_SRC} -resize 48x48 cryptotarget100M-48.png
convert cryptotarget100M-16.png cryptotarget100M-32.png cryptotarget100M-48.png ${ICON_DST}

