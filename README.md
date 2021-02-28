# E-Paper Display sample for raspberry pi zero W

Sample for use e-paper (2.13") as clock for raspberry pi zero w on docker

# Usage

```sh
docker run -dit \
  --name=rpiwepd \
  --privileged \
  --device /dev/gpiomem \
  --device /dev/spidev0.0 \
  -e TZ=Asia/Hongkong \
  -v /sys:/sys \
  --restart unless-stopped \
  genwch/rpiwepd
```

Ref:
https://github.com/waveshare/e-Paper
