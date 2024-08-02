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
import sys
class bstack1l111111ll_opy_:
    def __init__(self, handler):
        self._11l11lll11_opy_ = sys.stdout.write
        self._11l11lllll_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l11llll1_opy_
        sys.stdout.error = self.bstack11l11lll1l_opy_
    def bstack11l11llll1_opy_(self, _str):
        self._11l11lll11_opy_(_str)
        if self.handler:
            self.handler({bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༤"): bstack1111_opy_ (u"࠭ࡉࡏࡈࡒࠫ༥"), bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༦"): _str})
    def bstack11l11lll1l_opy_(self, _str):
        self._11l11lllll_opy_(_str)
        if self.handler:
            self.handler({bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༧"): bstack1111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ༨"), bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༩"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l11lll11_opy_
        sys.stderr.write = self._11l11lllll_opy_