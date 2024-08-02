# coding: UTF-8
import sys
bstack11l11l1_opy_ = sys.version_info [0] == 2
bstack1l11111_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1111_opy_ (bstack111l1l_opy_):
    global bstack1l1ll1_opy_
    bstack1ll11l1_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack11111l1_opy_ = bstack111l1l_opy_ [:-1]
    bstack1llll_opy_ = bstack1ll11l1_opy_ % len (bstack11111l1_opy_)
    bstack1ll11l_opy_ = bstack11111l1_opy_ [:bstack1llll_opy_] + bstack11111l1_opy_ [bstack1llll_opy_:]
    if bstack11l11l1_opy_:
        bstack1111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11111_opy_ - (bstack1ll111_opy_ + bstack1ll11l1_opy_) % bstack1111lll_opy_) for bstack1ll111_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1111l_opy_ = str () .join ([chr (ord (char) - bstack1l11111_opy_ - (bstack1ll111_opy_ + bstack1ll11l1_opy_) % bstack1111lll_opy_) for bstack1ll111_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1111l_opy_)
import threading
bstack1lll1ll1l11_opy_ = 1000
bstack1lll1ll111l_opy_ = 5
bstack1lll1lll111_opy_ = 30
bstack1lll1ll1111_opy_ = 2
class bstack1lll1ll1lll_opy_:
    def __init__(self, handler, bstack1lll1ll11l1_opy_=bstack1lll1ll1l11_opy_, bstack1lll1lll1l1_opy_=bstack1lll1ll111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll1ll11l1_opy_ = bstack1lll1ll11l1_opy_
        self.bstack1lll1lll1l1_opy_ = bstack1lll1lll1l1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lll1lll1ll_opy_()
    def bstack1lll1lll1ll_opy_(self):
        self.timer = threading.Timer(self.bstack1lll1lll1l1_opy_, self.bstack1lll1ll1ll1_opy_)
        self.timer.start()
    def bstack1lll1ll11ll_opy_(self):
        self.timer.cancel()
    def bstack1lll1lll11l_opy_(self):
        self.bstack1lll1ll11ll_opy_()
        self.bstack1lll1lll1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll1ll11l1_opy_:
                t = threading.Thread(target=self.bstack1lll1ll1ll1_opy_)
                t.start()
                self.bstack1lll1lll11l_opy_()
    def bstack1lll1ll1ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lll1ll11l1_opy_]
        del self.queue[:self.bstack1lll1ll11l1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lll1ll11ll_opy_()
        while len(self.queue) > 0:
            self.bstack1lll1ll1ll1_opy_()