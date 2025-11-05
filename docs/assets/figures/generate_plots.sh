uv run sniff protocol-1d --n 5 --save protocol-1d.png
uv run sniff protocol-2d --n 20 --noise-strength 1 --noise-model white --save protocol-2d.png
uv run sniff formation --n 20  --noise-strength 1 --noise-model white --save formation.png
uv run sniff circle --link 0.5 --n 20 --alpha 0.1 --noise-strength 1 --save circle.png
