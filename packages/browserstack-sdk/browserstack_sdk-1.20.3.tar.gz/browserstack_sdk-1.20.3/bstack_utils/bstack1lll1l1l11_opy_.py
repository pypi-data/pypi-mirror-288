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
from collections import deque
from bstack_utils.constants import *
class bstack11lllll1l_opy_:
    def __init__(self):
        self._1llll1ll1l1_opy_ = deque()
        self._1llll1l1ll1_opy_ = {}
        self._1llll1lll1l_opy_ = False
    def bstack1llll1l11l1_opy_(self, test_name, bstack1llll1lllll_opy_):
        bstack1llll1l111l_opy_ = self._1llll1l1ll1_opy_.get(test_name, {})
        return bstack1llll1l111l_opy_.get(bstack1llll1lllll_opy_, 0)
    def bstack1llll1l1lll_opy_(self, test_name, bstack1llll1lllll_opy_):
        bstack1llll1ll11l_opy_ = self.bstack1llll1l11l1_opy_(test_name, bstack1llll1lllll_opy_)
        self.bstack1llll1l1l1l_opy_(test_name, bstack1llll1lllll_opy_)
        return bstack1llll1ll11l_opy_
    def bstack1llll1l1l1l_opy_(self, test_name, bstack1llll1lllll_opy_):
        if test_name not in self._1llll1l1ll1_opy_:
            self._1llll1l1ll1_opy_[test_name] = {}
        bstack1llll1l111l_opy_ = self._1llll1l1ll1_opy_[test_name]
        bstack1llll1ll11l_opy_ = bstack1llll1l111l_opy_.get(bstack1llll1lllll_opy_, 0)
        bstack1llll1l111l_opy_[bstack1llll1lllll_opy_] = bstack1llll1ll11l_opy_ + 1
    def bstack1ll111ll1l_opy_(self, bstack1llll1l1l11_opy_, bstack1llll1l11ll_opy_):
        bstack1llll1llll1_opy_ = self.bstack1llll1l1lll_opy_(bstack1llll1l1l11_opy_, bstack1llll1l11ll_opy_)
        bstack1llll1lll11_opy_ = bstack11l11l1111_opy_[bstack1llll1l11ll_opy_]
        bstack1llll1ll111_opy_ = bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣᓇ").format(bstack1llll1l1l11_opy_, bstack1llll1lll11_opy_, bstack1llll1llll1_opy_)
        self._1llll1ll1l1_opy_.append(bstack1llll1ll111_opy_)
    def bstack1l1ll111l_opy_(self):
        return len(self._1llll1ll1l1_opy_) == 0
    def bstack1lll1ll11_opy_(self):
        bstack1llll1ll1ll_opy_ = self._1llll1ll1l1_opy_.popleft()
        return bstack1llll1ll1ll_opy_
    def capturing(self):
        return self._1llll1lll1l_opy_
    def bstack1lll11ll_opy_(self):
        self._1llll1lll1l_opy_ = True
    def bstack1ll1ll11ll_opy_(self):
        self._1llll1lll1l_opy_ = False