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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111ll1l1l1_opy_, bstack1111111l_opy_, bstack11l111ll1_opy_, bstack11lll1l11_opy_, \
    bstack111ll1ll1l_opy_
def bstack1ll1ll1ll_opy_(bstack1lll1l1l111_opy_):
    for driver in bstack1lll1l1l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l111lll11_opy_(driver, status, reason=bstack1111_opy_ (u"ࠧࠨᔣ")):
    bstack1lll111l1l_opy_ = Config.bstack11lll1111_opy_()
    if bstack1lll111l1l_opy_.bstack11ll11llll_opy_():
        return
    bstack1lll11l111_opy_ = bstack111l1l11_opy_(bstack1111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᔤ"), bstack1111_opy_ (u"ࠩࠪᔥ"), status, reason, bstack1111_opy_ (u"ࠪࠫᔦ"), bstack1111_opy_ (u"ࠫࠬᔧ"))
    driver.execute_script(bstack1lll11l111_opy_)
def bstack1l111l1ll_opy_(page, status, reason=bstack1111_opy_ (u"ࠬ࠭ᔨ")):
    try:
        if page is None:
            return
        bstack1lll111l1l_opy_ = Config.bstack11lll1111_opy_()
        if bstack1lll111l1l_opy_.bstack11ll11llll_opy_():
            return
        bstack1lll11l111_opy_ = bstack111l1l11_opy_(bstack1111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᔩ"), bstack1111_opy_ (u"ࠧࠨᔪ"), status, reason, bstack1111_opy_ (u"ࠨࠩᔫ"), bstack1111_opy_ (u"ࠩࠪᔬ"))
        page.evaluate(bstack1111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᔭ"), bstack1lll11l111_opy_)
    except Exception as e:
        print(bstack1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᔮ"), e)
def bstack111l1l11_opy_(type, name, status, reason, bstack11llll111_opy_, bstack1ll11ll1l_opy_):
    bstack1l1ll1ll_opy_ = {
        bstack1111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᔯ"): type,
        bstack1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᔰ"): {}
    }
    if type == bstack1111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᔱ"):
        bstack1l1ll1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᔲ")][bstack1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᔳ")] = bstack11llll111_opy_
        bstack1l1ll1ll_opy_[bstack1111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᔴ")][bstack1111_opy_ (u"ࠫࡩࡧࡴࡢࠩᔵ")] = json.dumps(str(bstack1ll11ll1l_opy_))
    if type == bstack1111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᔶ"):
        bstack1l1ll1ll_opy_[bstack1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᔷ")][bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᔸ")] = name
    if type == bstack1111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᔹ"):
        bstack1l1ll1ll_opy_[bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᔺ")][bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᔻ")] = status
        if status == bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᔼ") and str(reason) != bstack1111_opy_ (u"ࠧࠨᔽ"):
            bstack1l1ll1ll_opy_[bstack1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᔾ")][bstack1111_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᔿ")] = json.dumps(str(reason))
    bstack1111llll1_opy_ = bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᕀ").format(json.dumps(bstack1l1ll1ll_opy_))
    return bstack1111llll1_opy_
def bstack1lllll1ll_opy_(url, config, logger, bstack1l1l111l1_opy_=False):
    hostname = bstack1111111l_opy_(url)
    is_private = bstack11lll1l11_opy_(hostname)
    try:
        if is_private or bstack1l1l111l1_opy_:
            file_path = bstack111ll1l1l1_opy_(bstack1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᕁ"), bstack1111_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᕂ"), logger)
            if os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᕃ")) and eval(
                    os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᕄ"))):
                return
            if (bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᕅ") in config and not config[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᕆ")]):
                os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᕇ")] = str(True)
                bstack1lll1l1l1l1_opy_ = {bstack1111_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᕈ"): hostname}
                bstack111ll1ll1l_opy_(bstack1111_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᕉ"), bstack1111_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᕊ"), bstack1lll1l1l1l1_opy_, logger)
    except Exception as e:
        pass
def bstack11ll111l_opy_(caps, bstack1lll1l1l11l_opy_):
    if bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕋ") in caps:
        caps[bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᕌ")][bstack1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᕍ")] = True
        if bstack1lll1l1l11l_opy_:
            caps[bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᕎ")][bstack1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᕏ")] = bstack1lll1l1l11l_opy_
    else:
        caps[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᕐ")] = True
        if bstack1lll1l1l11l_opy_:
            caps[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᕑ")] = bstack1lll1l1l11l_opy_
def bstack1lll1lllll1_opy_(bstack11llllll1l_opy_):
    bstack1lll1l1l1ll_opy_ = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᕒ"), bstack1111_opy_ (u"࠭ࠧᕓ"))
    if bstack1lll1l1l1ll_opy_ == bstack1111_opy_ (u"ࠧࠨᕔ") or bstack1lll1l1l1ll_opy_ == bstack1111_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᕕ"):
        threading.current_thread().testStatus = bstack11llllll1l_opy_
    else:
        if bstack11llllll1l_opy_ == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᕖ"):
            threading.current_thread().testStatus = bstack11llllll1l_opy_