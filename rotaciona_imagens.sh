#!/bin/bash
find /home/jfreitas/C1-imagens/ -name "*.jpg" | while IFS= read -r file; do
  convert "$file" -rotate 180 "$file"
done