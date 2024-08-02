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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1l11l1l1ll_opy_ as bstack1ll11lll11_opy_
from browserstack_sdk.bstack1llll11l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l1lll1_opy_
class bstack111l11l1_opy_:
    def __init__(self, args, logger, bstack11ll1l1l1l_opy_, bstack11ll11l11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1l1l1l_opy_ = bstack11ll1l1l1l_opy_
        self.bstack11ll11l11l_opy_ = bstack11ll11l11l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111lll1l1_opy_ = []
        self.bstack11ll11l1l1_opy_ = None
        self.bstack1l1l11111l_opy_ = []
        self.bstack11ll11ll1l_opy_ = self.bstack11ll1l1l_opy_()
        self.bstack11l1l1l1l_opy_ = -1
    def bstack1l11llll11_opy_(self, bstack11ll1l111l_opy_):
        self.parse_args()
        self.bstack11ll111lll_opy_()
        self.bstack11ll1l1l11_opy_(bstack11ll1l111l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll11lll1_opy_():
        import importlib
        if getattr(importlib, bstack1111_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧแ"), False):
            bstack11ll1l1ll1_opy_ = importlib.find_loader(bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬโ"))
        else:
            bstack11ll1l1ll1_opy_ = importlib.util.find_spec(bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ใ"))
    def bstack11ll11ll11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l1l1l1l_opy_ = -1
        if self.bstack11ll11l11l_opy_ and bstack1111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬไ") in self.bstack11ll1l1l1l_opy_:
            self.bstack11l1l1l1l_opy_ = int(self.bstack11ll1l1l1l_opy_[bstack1111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ๅ")])
        try:
            bstack11ll11l1ll_opy_ = [bstack1111_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩๆ"), bstack1111_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ็"), bstack1111_opy_ (u"ࠩ࠰ࡴ่ࠬ")]
            if self.bstack11l1l1l1l_opy_ >= 0:
                bstack11ll11l1ll_opy_.extend([bstack1111_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶ้ࠫ"), bstack1111_opy_ (u"ࠫ࠲ࡴ๊ࠧ")])
            for arg in bstack11ll11l1ll_opy_:
                self.bstack11ll11ll11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll111lll_opy_(self):
        bstack11ll11l1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11ll11l1l1_opy_ = bstack11ll11l1l1_opy_
        return bstack11ll11l1l1_opy_
    def bstack1ll1l11111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll11lll1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l1lll1_opy_)
    def bstack11ll1l1l11_opy_(self, bstack11ll1l111l_opy_):
        bstack1lll111l1l_opy_ = Config.bstack11lll1111_opy_()
        if bstack11ll1l111l_opy_:
            self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦ๋ࠩ"))
            self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"࠭ࡔࡳࡷࡨࠫ์"))
        if bstack1lll111l1l_opy_.bstack11ll11llll_opy_():
            self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ํ"))
            self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠨࡖࡵࡹࡪ࠭๎"))
        self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠩ࠰ࡴࠬ๏"))
        self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ๐"))
        self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭๑"))
        self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ๒"))
        if self.bstack11l1l1l1l_opy_ > 1:
            self.bstack11ll11l1l1_opy_.append(bstack1111_opy_ (u"࠭࠭࡯ࠩ๓"))
            self.bstack11ll11l1l1_opy_.append(str(self.bstack11l1l1l1l_opy_))
    def bstack11ll1l11l1_opy_(self):
        bstack1l1l11111l_opy_ = []
        for spec in self.bstack111lll1l1_opy_:
            bstack1lll1l1111_opy_ = [spec]
            bstack1lll1l1111_opy_ += self.bstack11ll11l1l1_opy_
            bstack1l1l11111l_opy_.append(bstack1lll1l1111_opy_)
        self.bstack1l1l11111l_opy_ = bstack1l1l11111l_opy_
        return bstack1l1l11111l_opy_
    def bstack11ll1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll11ll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll11ll1l_opy_ = False
        return self.bstack11ll11ll1l_opy_
    def bstack1l111l11l_opy_(self, bstack11ll1l1111_opy_, bstack1l11llll11_opy_):
        bstack1l11llll11_opy_[bstack1111_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ๔")] = self.bstack11ll1l1l1l_opy_
        multiprocessing.set_start_method(bstack1111_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ๕"))
        bstack1ll11lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1l111ll_opy_ = manager.list()
        if bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๖") in self.bstack11ll1l1l1l_opy_:
            for index, platform in enumerate(self.bstack11ll1l1l1l_opy_[bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๗")]):
                bstack1ll11lll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11ll1l1111_opy_,
                                                            args=(self.bstack11ll11l1l1_opy_, bstack1l11llll11_opy_, bstack1l1l111ll_opy_)))
            bstack11ll11l111_opy_ = len(self.bstack11ll1l1l1l_opy_[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๘")])
        else:
            bstack1ll11lll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11ll1l1111_opy_,
                                                        args=(self.bstack11ll11l1l1_opy_, bstack1l11llll11_opy_, bstack1l1l111ll_opy_)))
            bstack11ll11l111_opy_ = 1
        i = 0
        for t in bstack1ll11lll_opy_:
            os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ๙")] = str(i)
            if bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ๚") in self.bstack11ll1l1l1l_opy_:
                os.environ[bstack1111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ๛")] = json.dumps(self.bstack11ll1l1l1l_opy_[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๜")][i % bstack11ll11l111_opy_])
            i += 1
            t.start()
        for t in bstack1ll11lll_opy_:
            t.join()
        return list(bstack1l1l111ll_opy_)
    @staticmethod
    def bstack1l1l1111l1_opy_(driver, bstack1l1llll1l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭๝"), None)
        if item and getattr(item, bstack1111_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬ๞"), None) and not getattr(item, bstack1111_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭๟"), False):
            logger.info(
                bstack1111_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦ๠"))
            bstack11ll1l11ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll11lll11_opy_.bstack11ll1l1ll_opy_(driver, bstack11ll1l11ll_opy_, item.name, item.module.__name__, item.path, bstack1l1llll1l1_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)