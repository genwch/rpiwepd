_BLACK = 0
_WHITE = 255
_GRAY = 128

_S_FONT = 15
_M_FONT = 25
_L_FONT = 40

_FONTPATH = "./static/font/"


class img_cls():
    def __init__(self, name: str, w_h: tuple, fill: int = _WHITE):
        from PIL import Image, ImageDraw
        self._BACK = fill
        self._img = Image.new("1", (w_h[0], w_h[1]), fill)
        self._draw = ImageDraw.Draw(self._img)
        self._w_h = w_h
        self._name = name
        self._obj = []

    def add_text(self, text: str, x_y: tuple = (0, 0), size: int = _M_FONT, fill: int = _BLACK) -> (((int, int), (int, int)), bool):
        exists = []
        (x_y, w_h) = self.__cal_xy(text=text, size=size) if x_y == (0, 0) else x_y
        for k, o in enumerate(self._obj):
            if o.get("x_y") == x_y:
                if o.get("text") == text:
                    return ((x_y, (None, None)), True)
                else:
                    exists.append(self._obj.pop(k))
                    break
        for e in exists:
            self.__draw_text(text=e.get("text"), x_y=e.get(
                "x_y"), size=e.get("size"), fill=self._BACK, append_obj=False)
        (x_y, (w, h)) = self.__draw_text(
            text=text, x_y=x_y, size=size, fill=fill)
        return ((x_y, (w, h)), False)

    def __get_font(self, size):
        from PIL import ImageFont
        return ImageFont.truetype(f"{_FONTPATH}unifont-13.0.06.ttf", size)

    def __cal_xy(self, text: str, size: int = _M_FONT):
        font = self.__get_font(size)
        draw = self._draw
        (w, h) = draw.textsize(text, font=font)
        if w % 2 == 1:
            w += 1
        if h % 2 == 1:
            h += 1
        (ow, oh) = self._w_h
        x_y = (int((ow-w)//2), int((oh-h)//2))
        return (x_y, (w, h))

    def __tuple_add(self, x_y: tuple, offset: int = 0) -> list:
        rtn = []
        for o in range(offset+1):
            rtn.append((x_y[0]+o, x_y[1]))
            rtn.append((x_y[0], x_y[1]+o))
        return list(set(rtn))

    def __draw_text(self, text: str, x_y: tuple = (0, 0), size: int = _M_FONT, fill: int = _BLACK, append_obj=True) -> ((int, int), (int, int)):
        draw = self._draw
        offset = 1
        font = self.__get_font(size)
        (x_y, (w, h)) = self.__cal_xy(text, size)
        for p in self.__tuple_add(x_y, offset):
            draw.text(p, text, font=font, fill=fill)
        if append_obj:
            self._obj.append(
                {"text": text, "x_y": x_y, "size": size, "fill": fill})
        return (x_y, (w+offset, h+offset))

    def img(self):
        return self._img

    def w_h(self):
        return self._w_h

    def rotate(img):
        return img.rotate(180, expand=True)


class screen_cls():
    def __init__(self):
        self.new()

    def new(self):
        self._obj = []

    def add(self, *args, **kwargs):
        default = {"name": None, "obj": None, "x_y": (0, 0), "w_h": (0, 0)}
        for a in args:
            kwargs.update(a)
        img = img_cls(name=kwargs.get("name"), w_h=kwargs.get(
            "w_h", default.get("w_h")), fill=kwargs.get("fill", None))
        kwargs.update({"obj": img})
        obj = {k: kwargs.get(k, v) for k, v in default.items()}
        self._obj.append(obj)

    def get(self) -> list:
        return self._obj


def set_screen(w_h: tuple, bg_img) -> list:
    (epd_w, epd_h) = w_h
    srns = []
    srn = screen_cls()
    sec_margin = 35
    w = (epd_w-sec_margin)//2
    srn.add(name="clk_sec", x_y=(w, 0), w_h=(sec_margin, epd_h), fill=_WHITE)
    srn.add(name="clk_hr", x_y=(0, 0), w_h=(w, epd_h), fill=_WHITE)
    srn.add(name="clk_min", x_y=(w+sec_margin, 0), w_h=(w, epd_h), fill=_WHITE)
    srns.append({"name": "clock", "srn": srn,
                 "img": bg_img, "idel": 5, "switch": 25})
    del srn
    srn = screen_cls()
    srn.add(name="cal_date", x_y=(0, 0), w_h=(epd_w, epd_h//2), fill=_WHITE)
    srn.add(name="cal_info", x_y=(0, epd_h//2),
            w_h=(epd_w, epd_h//2), fill=_BLACK)
    srns.append({"name": "calendar", "srn": srn,
                 "img": bg_img, "idel": 5, "switch": 35})
    return srns


def main():
    import lib.epd as epdlib
    from PIL import Image
    import time
    from datetime import datetime
    epd = epdlib.EPD()
    epd_w = epd.height
    epd_h = epd.width

    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    epd.init(epd.FULL_UPDATE)
    bg = img_cls(name="bg", w_h=(epd_w, epd_h))
    bg_img = bg.img()
    epd.displayPartBaseImage(epd.getbuffer(bg_img))

    epd.init(epd.PART_UPDATE)
    srns = set_screen((epd_w, epd_h), bg_img)
    start = datetime.now()
    target = 50
    img = bg_img.copy()
    idx = len(srns)-1
    # idx=0
    init = True
    while True:
        now = datetime.now()
        switch = srns[idx].get("switch", 0)
        # if init:
        #     second=35
        # else:
        second = int(now.strftime("%S"))
        if (second >= switch and second < switch+srns[idx].get("idel", 0.5)*4) or init:
            # print(f"swap-second: {second}, idx: {idx}")
            idx = 0 if idx+1 >= len(srns) else idx+1
            srn = srns[idx].get("srn")
            # img=srns[idx].get("img", bg_img).copy()
            img = bg_img.copy()
            if init:
                idel = 0.1
            else:
                idel = srns[idx].get("idel", 0.5)
            swap = True
            init = False
        refresh = False
        for s in srn.get():
            rtn = True
            o = s.get("obj")
            (ox, oy) = s.get("x_y")
            (ow, oh) = s.get("w_h")
            if s.get("name") == "clk_hr":
                (((x, y), (w, h)), rtn) = o.add_text(
                    text=now.strftime("%H"), size=110, fill=_BLACK)
            elif s.get("name") == "clk_min":
                (((x, y), (w, h)), rtn) = o.add_text(
                    text=now.strftime("%M"), size=110, fill=_BLACK)
            elif s.get("name") == "clk_sec":
                text = ":"
                # if second % 2==1:
                #     text=" "
                (((x, y), (w, h)), rtn) = o.add_text(
                    text=text, x_y=(-10, 12), size=110, fill=_BLACK)
                # print(f"text: {text}, rtn: {rtn}")
            elif s.get("name") == "cal_date":
                (((x, y), (w, h)), rtn) = o.add_text(
                    text=now.strftime("%d%b%y"), size=60, fill=_BLACK)
            elif s.get("name") == "cal_info":
                (((x, y), (w, h)), rtn) = o.add_text(
                    text=now.strftime("%A"), size=60, fill=_WHITE)
            if rtn and not(swap):
                continue
            refresh = True
            oimg = o.img().copy()
            img.paste(oimg, (ox, oy, ox+ow, oy+oh))
        if refresh:
            swap = False
            # print(f"refresh - {second}")
            epd.displayPartial(epd.getbuffer(img_cls.rotate(img)))
        time.sleep(idel)
    epd.sleep()


if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        print("Waiting for exit...")
        import lib.epd as epdlib
        try:
            epd = epdlib.EPD()
            epd.init(epd.FULL_UPDATE)
            epd.Clear(0xFF)
            epd.sleep()
        except:
            print("Clear fail")
            pass
        sys.exit()
