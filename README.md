---
title: DSFS-33 Back
emoji: 📉
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
license: apache-2.0
short_description: 'dsfs-33-backend API'
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## Docker
docker build -t dsfs-33-back .

docker run -it -v "$(pwd):/home/user/app" -p 4000:7860 --env-file .env -e PORT=7860  dsfs-33-back
