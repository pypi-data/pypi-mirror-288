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
from browserstack_sdk.bstack1l111ll1_opy_ import bstack111l11l1_opy_
from browserstack_sdk.bstack1l111l1111_opy_ import RobotHandler
def bstack1111ll1ll_opy_(framework):
    if framework.lower() == bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᇽ"):
        return bstack111l11l1_opy_.version()
    elif framework.lower() == bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ᇾ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨᇿ"):
        import behave
        return behave.__version__
    else:
        return bstack1111_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪሀ")