#!/bin/bash
# usage: ./render.sh <config> <music_offset_seconds>
set -e
c=$1; off=${2:-10}
d=$(node record.js $c dur)
node record.js $c sfx out/$c.sfx.json
node record.js $c frames 0 $d out/$c.raw.mp4
SFX_FILE=out/$c.sfx.json MUSIC_OFFSET=$off MIX_WAV=out/$c.wav python3 mix.py out/$c.raw.mp4 out/$c.mix.mp4 musique.mp3 >/dev/null
ffmpeg -y -v error -i out/$c.mix.mp4 -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p -crf 19 -preset slow -g 60 -sc_threshold 0 -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/demo-$c.mp4
rm -f out/$c.raw.mp4 out/$c.mix.mp4 out/$c.wav
echo "OK $c $d"
