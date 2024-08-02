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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1l1l1l_opy_, bstack11ll11l11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1l1l1l_opy_ = bstack11ll1l1l1l_opy_
        self.bstack11ll11l11l_opy_ = bstack11ll11l11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11lll111l1_opy_(bstack11ll1111ll_opy_):
        bstack11ll111l1l_opy_ = []
        if bstack11ll1111ll_opy_:
            tokens = str(os.path.basename(bstack11ll1111ll_opy_)).split(bstack1111_opy_ (u"ࠨ࡟ࠣ๡"))
            camelcase_name = bstack1111_opy_ (u"ࠢࠡࠤ๢").join(t.title() for t in tokens)
            suite_name, bstack11ll111ll1_opy_ = os.path.splitext(camelcase_name)
            bstack11ll111l1l_opy_.append(suite_name)
        return bstack11ll111l1l_opy_
    @staticmethod
    def bstack11ll111l11_opy_(typename):
        if bstack1111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ๣") in typename:
            return bstack1111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ๤")
        return bstack1111_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ๥")