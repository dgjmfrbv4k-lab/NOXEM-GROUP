# Vidéo motion design — Déstockage verre plat

`index.html` = version 2 (18 plans courts, rythme rapide). `index-v1.html` = première version (7 scènes).

Animation codée en HTML/JS (`index.html`), rendue image par image avec Chromium
(Playwright) puis assemblée en MP4 avec ffmpeg. 1920×1080, 30 i/s, 60 s.

## Rendre la vidéo

    node record.js frames 0 60 noxem.mp4          # vidéo complète (≈ 2 à 6 min)
    node record.js stills 4.5,21,51.5 .           # quelques images de contrôle

Pour aller plus vite, rendre 4 morceaux en parallèle puis les coller :

    for i in 0 1 2 3; do node record.js frames $((i*15)) $((i*15+15)) part$i.mp4 & done; wait
    printf "file 'part%s.mp4'\n" 0 1 2 3 > list.txt
    ffmpeg -f concat -i list.txt -c copy noxem.mp4

## Voix off ElevenLabs

Texte et minutage dans `voiceover.json` (une phrase par scène). Nécessite la
variable d'environnement `ELEVENLABS_API_KEY` (et `ELEVENLABS_VOICE_ID` pour
changer de voix).

    node voiceover.mjs noxem.mp4 noxem-voix.mp4              # voix seule
    node voiceover.mjs noxem.mp4 noxem-voix.mp4 musique.mp3  # voix + musique baissée sous la voix

## Modifier

Le minutage des scènes est dans `SC` en bas de `index.html` ; chaque scène a sa
fonction dans `R` (temps local en secondes).

## Voix off déjà générée (fichier ElevenLabs) + bruitages

Si la voix off est générée sur le site ElevenLabs (un seul fichier pour tout
le texte), la placer dans `audio/voix.mp3`, puis :

    python3 mix.py noxem.mp4 noxem-voix.mp4              # voix + bruitages
    python3 mix.py noxem.mp4 noxem-voix.mp4 musique.mp3  # + musique baissée sous la voix

Les points de découpe de la voix (`VOICE_CUTS`) sont en haut de `mix.py`. Les
instants des bruitages sont définis dans `index.html` (`SFX`) et exportés avec
`node record.js sfx sfx.json`. Les bruitages sont synthétisés par `mix.py`.
