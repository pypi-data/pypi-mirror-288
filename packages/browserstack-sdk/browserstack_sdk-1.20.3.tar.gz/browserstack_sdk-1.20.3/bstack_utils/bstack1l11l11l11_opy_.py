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
class bstack111ll1l1_opy_:
    def __init__(self, handler):
        self._1lll1l1llll_opy_ = None
        self.handler = handler
        self._1lll1l1ll1l_opy_ = self.bstack1lll1l1lll1_opy_()
        self.patch()
    def patch(self):
        self._1lll1l1llll_opy_ = self._1lll1l1ll1l_opy_.execute
        self._1lll1l1ll1l_opy_.execute = self.bstack1lll1l1ll11_opy_()
    def bstack1lll1l1ll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᔡ"), driver_command, None, this, args)
            response = self._1lll1l1llll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1111_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᔢ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1l1ll1l_opy_.execute = self._1lll1l1llll_opy_
    @staticmethod
    def bstack1lll1l1lll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver