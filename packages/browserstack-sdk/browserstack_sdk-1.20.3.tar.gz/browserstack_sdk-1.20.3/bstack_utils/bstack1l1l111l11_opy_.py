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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11l1llll11_opy_, bstack1l1l1l11l_opy_, get_host_info, bstack11l1ll11ll_opy_, bstack11l1ll111l_opy_, bstack111l11ll11_opy_, bstack11lll11l1l_opy_, \
    bstack111lllllll_opy_, bstack111ll11l1l_opy_, bstack1ll1l11l11_opy_, bstack111ll11111_opy_, bstack1lll1111l_opy_, bstack1l111l1l1l_opy_, bstack1l1l111l_opy_, bstack1ll1ll1l11_opy_
from bstack_utils.bstack1lll1ll1l1l_opy_ import bstack1lll1ll1lll_opy_
from bstack_utils.bstack11llll1ll1_opy_ import bstack1l1111lll1_opy_
import bstack_utils.bstack1l11l1l1ll_opy_ as bstack1ll11lll11_opy_
from bstack_utils.constants import bstack11l11l1l11_opy_
bstack1lll111llll_opy_ = [
    bstack1111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᖕ"), bstack1111_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᖖ"), bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᖗ"), bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᖘ"),
    bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᖙ"), bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᖚ"), bstack1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᖛ")
]
bstack1lll111111l_opy_ = bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᖜ")
logger = logging.getLogger(__name__)
class bstack11l1ll1ll_opy_:
    bstack1lll1ll1l1l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lll1111l11_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll111lll1_opy_()
        bstack11l1l1llll_opy_ = bstack11l1ll11ll_opy_(bs_config)
        bstack11l1lllll1_opy_ = bstack11l1ll111l_opy_(bs_config)
        bstack1l11111l1_opy_ = False
        bstack11l11llll_opy_ = False
        if bstack1111_opy_ (u"ࠪࡥࡵࡶࠧᖝ") in bs_config:
            bstack1l11111l1_opy_ = True
        else:
            bstack11l11llll_opy_ = True
        bstack1l1l1lll1l_opy_ = {
            bstack1111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᖞ"): cls.bstack1l11ll11l_opy_(bstack1lll1111l11_opy_.get(bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᖟ"), bstack1111_opy_ (u"࠭ࠧᖠ"))),
            bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᖡ"): bstack1ll11lll11_opy_.bstack1l1ll111_opy_(bs_config),
            bstack1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᖢ"): bs_config.get(bstack1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᖣ"), False),
            bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᖤ"): bstack11l11llll_opy_,
            bstack1111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᖥ"): bstack1l11111l1_opy_
        }
        data = {
            bstack1111_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᖦ"): bstack1111_opy_ (u"࠭ࡪࡴࡱࡱࠫᖧ"),
            bstack1111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᖨ"): bs_config.get(bstack1111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᖩ"), bstack1111_opy_ (u"ࠩࠪᖪ")),
            bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨᖫ"): bs_config.get(bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᖬ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᖭ"): bs_config.get(bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᖮ")),
            bstack1111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᖯ"): bs_config.get(bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᖰ"), bstack1111_opy_ (u"ࠩࠪᖱ")),
            bstack1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᖲ"): datetime.datetime.now().isoformat(),
            bstack1111_opy_ (u"ࠫࡹࡧࡧࡴࠩᖳ"): bstack111l11ll11_opy_(bs_config),
            bstack1111_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᖴ"): get_host_info(),
            bstack1111_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᖵ"): bstack1l1l1l11l_opy_(),
            bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᖶ"): os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᖷ")),
            bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᖸ"): os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᖹ"), False),
            bstack1111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᖺ"): bstack11l1llll11_opy_(),
            bstack1111_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪᖻ"): bstack1l1l1lll1l_opy_,
            bstack1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᖼ"): {
                bstack1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᖽ"): bstack1lll1111l11_opy_.get(bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᖾ"), bstack1111_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᖿ")),
                bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗀ"): bstack1lll1111l11_opy_.get(bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᗁ")),
                bstack1111_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᗂ"): bstack1lll1111l11_opy_.get(bstack1111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᗃ"))
            }
        }
        config = {
            bstack1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᗄ"): (bstack11l1l1llll_opy_, bstack11l1lllll1_opy_),
            bstack1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᗅ"): cls.default_headers()
        }
        response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᗆ"), cls.request_url(bstack1111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪᗇ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᗈ")] = bstack1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᗉ")
            os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᗊ")] = bstack1111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᗋ")
            os.environ[bstack1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᗌ")] = bstack1111_opy_ (u"ࠩࡱࡹࡱࡲࠧᗍ")
            os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᗎ")] = bstack1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᗏ")
            os.environ[bstack1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᗐ")] = bstack1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᗑ")
            bstack1lll111ll1l_opy_ = response.json()
            if bstack1lll111ll1l_opy_ and bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗒ")]:
                error_message = bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗓ")]
                if bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᗔ")] == bstack1111_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡌࡒ࡛ࡇࡌࡊࡆࡢࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࠨᗕ"):
                    logger.error(error_message)
                elif bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᗖ")] == bstack1111_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠫᗗ"):
                    logger.info(error_message)
                elif bstack1lll111ll1l_opy_[bstack1111_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᗘ")] == bstack1111_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡓࡅࡍࡢࡈࡊࡖࡒࡆࡅࡄࡘࡊࡊࠧᗙ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1111_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᗚ"))
            return [None, None, None]
        bstack1lll111ll1l_opy_ = response.json()
        os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᗛ")] = bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᗜ")]
        if cls.bstack1l11ll11l_opy_(bstack1lll1111l11_opy_.get(bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᗝ"), bstack1111_opy_ (u"ࠬ࠭ᗞ"))) is True:
            logger.debug(bstack1111_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᗟ"))
            os.environ[bstack1111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᗠ")] = bstack1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᗡ")
            if bstack1lll111ll1l_opy_.get(bstack1111_opy_ (u"ࠩ࡭ࡻࡹ࠭ᗢ")):
                os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᗣ")] = bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠫ࡯ࡽࡴࠨᗤ")]
                os.environ[bstack1111_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᗥ")] = json.dumps({
                    bstack1111_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᗦ"): bstack11l1l1llll_opy_,
                    bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᗧ"): bstack11l1lllll1_opy_
                })
            if bstack1lll111ll1l_opy_.get(bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᗨ")):
                os.environ[bstack1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᗩ")] = bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᗪ")]
            if bstack1lll111ll1l_opy_.get(bstack1111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᗫ")):
                os.environ[bstack1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᗬ")] = str(bstack1lll111ll1l_opy_[bstack1111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᗭ")])
        return [bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠧ࡫ࡹࡷࠫᗮ")], bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᗯ")], bstack1lll111ll1l_opy_[bstack1111_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᗰ")]]
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def stop(cls, bstack1lll11l11ll_opy_ = None):
        if not cls.on():
            return
        if os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᗱ")] == bstack1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᗲ") or os.environ[bstack1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᗳ")] == bstack1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᗴ"):
            print(bstack1111_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᗵ"))
            return {
                bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᗶ"): bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᗷ"),
                bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗸ"): bstack1111_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᗹ")
            }
        else:
            cls.bstack1lll1ll1l1l_opy_.shutdown()
            data = {
                bstack1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗺ"): bstack1ll1ll1l11_opy_()
            }
            if not bstack1lll11l11ll_opy_ is None:
                data[bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪᗻ")] = [{
                    bstack1111_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᗼ"): bstack1111_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ᗽ"),
                    bstack1111_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩᗾ"): bstack1lll11l11ll_opy_
                }]
            config = {
                bstack1111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᗿ"): cls.default_headers()
            }
            bstack111l1l1lll_opy_ = bstack1111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬᘀ").format(os.environ[bstack1111_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᘁ")])
            bstack1lll1111ll1_opy_ = cls.request_url(bstack111l1l1lll_opy_)
            response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"࠭ࡐࡖࡖࠪᘂ"), bstack1lll1111ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1111_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨᘃ"))
    @classmethod
    def bstack11lllll11l_opy_(cls):
        if cls.bstack1lll1ll1l1l_opy_ is None:
            return
        cls.bstack1lll1ll1l1l_opy_.shutdown()
    @classmethod
    def bstack11111l11l_opy_(cls):
        if cls.on():
            print(
                bstack1111_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫᘄ").format(os.environ[bstack1111_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣᘅ")]))
    @classmethod
    def bstack1lll111lll1_opy_(cls):
        if cls.bstack1lll1ll1l1l_opy_ is not None:
            return
        cls.bstack1lll1ll1l1l_opy_ = bstack1lll1ll1lll_opy_(cls.bstack1lll111l111_opy_)
        cls.bstack1lll1ll1l1l_opy_.start()
    @classmethod
    def bstack11ll1ll1l1_opy_(cls, bstack1l1111l1ll_opy_, bstack1lll111ll11_opy_=bstack1111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᘆ")):
        if not cls.on():
            return
        bstack111ll11l1_opy_ = bstack1l1111l1ll_opy_[bstack1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᘇ")]
        bstack1lll11l11l1_opy_ = {
            bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᘈ"): bstack1111_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡺࡡࡳࡶࡢ࡙ࡵࡲ࡯ࡢࡦࠪᘉ"),
            bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᘊ"): bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡥࡅ࡯ࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᘋ"),
            bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᘌ"): bstack1111_opy_ (u"ࠪࡘࡪࡹࡴࡠࡕ࡮࡭ࡵࡶࡥࡥࡡࡘࡴࡱࡵࡡࡥࠩᘍ"),
            bstack1111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᘎ"): bstack1111_opy_ (u"ࠬࡒ࡯ࡨࡡࡘࡴࡱࡵࡡࡥࠩᘏ"),
            bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᘐ"): bstack1111_opy_ (u"ࠧࡉࡱࡲ࡯ࡤ࡙ࡴࡢࡴࡷࡣ࡚ࡶ࡬ࡰࡣࡧࠫᘑ"),
            bstack1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᘒ"): bstack1111_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡆࡰࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᘓ"),
            bstack1111_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᘔ"): bstack1111_opy_ (u"ࠫࡈࡈࡔࡠࡗࡳࡰࡴࡧࡤࠨᘕ")
        }.get(bstack111ll11l1_opy_)
        if bstack1lll111ll11_opy_ == bstack1111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᘖ"):
            cls.bstack1lll111lll1_opy_()
            cls.bstack1lll1ll1l1l_opy_.add(bstack1l1111l1ll_opy_)
        elif bstack1lll111ll11_opy_ == bstack1111_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᘗ"):
            cls.bstack1lll111l111_opy_([bstack1l1111l1ll_opy_], bstack1lll111ll11_opy_)
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1lll111l111_opy_(cls, bstack1l1111l1ll_opy_, bstack1lll111ll11_opy_=bstack1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᘘ")):
        config = {
            bstack1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᘙ"): cls.default_headers()
        }
        response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᘚ"), cls.request_url(bstack1lll111ll11_opy_), bstack1l1111l1ll_opy_, config)
        bstack11l1l1l111_opy_ = response.json()
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1ll11ll1_opy_(cls, bstack11lll1l1ll_opy_):
        bstack1lll11l111l_opy_ = []
        for log in bstack11lll1l1ll_opy_:
            bstack1lll111l11l_opy_ = {
                bstack1111_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᘛ"): bstack1111_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭ᘜ"),
                bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᘝ"): log[bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘞ")],
                bstack1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᘟ"): log[bstack1111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᘠ")],
                bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩᘡ"): {},
                bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘢ"): log[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘣ")],
            }
            if bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘤ") in log:
                bstack1lll111l11l_opy_[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘥ")] = log[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘦ")]
            elif bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘧ") in log:
                bstack1lll111l11l_opy_[bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘨ")] = log[bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘩ")]
            bstack1lll11l111l_opy_.append(bstack1lll111l11l_opy_)
        cls.bstack11ll1ll1l1_opy_({
            bstack1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᘪ"): bstack1111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᘫ"),
            bstack1111_opy_ (u"࠭࡬ࡰࡩࡶࠫᘬ"): bstack1lll11l111l_opy_
        })
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1lll111l1l1_opy_(cls, steps):
        bstack1lll1111l1l_opy_ = []
        for step in steps:
            bstack1lll11111l1_opy_ = {
                bstack1111_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᘭ"): bstack1111_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫᘮ"),
                bstack1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᘯ"): step[bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᘰ")],
                bstack1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᘱ"): step[bstack1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᘲ")],
                bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘳ"): step[bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘴ")],
                bstack1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᘵ"): step[bstack1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᘶ")]
            }
            if bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘷ") in step:
                bstack1lll11111l1_opy_[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘸ")] = step[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘹ")]
            elif bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘺ") in step:
                bstack1lll11111l1_opy_[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘻ")] = step[bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘼ")]
            bstack1lll1111l1l_opy_.append(bstack1lll11111l1_opy_)
        cls.bstack11ll1ll1l1_opy_({
            bstack1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᘽ"): bstack1111_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᘾ"),
            bstack1111_opy_ (u"ࠫࡱࡵࡧࡴࠩᘿ"): bstack1lll1111l1l_opy_
        })
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack11ll11l11_opy_(cls, screenshot):
        cls.bstack11ll1ll1l1_opy_({
            bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᙀ"): bstack1111_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᙁ"),
            bstack1111_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᙂ"): [{
                bstack1111_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᙃ"): bstack1111_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫᙄ"),
                bstack1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᙅ"): bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"ࠫ࡟࠭ᙆ"),
                bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙇ"): screenshot[bstack1111_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᙈ")],
                bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᙉ"): screenshot[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᙊ")]
            }]
        }, bstack1lll111ll11_opy_=bstack1111_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᙋ"))
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1ll11111l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1ll1l1_opy_({
            bstack1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᙌ"): bstack1111_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᙍ"),
            bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᙎ"): {
                bstack1111_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᙏ"): cls.current_test_uuid(),
                bstack1111_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨᙐ"): cls.bstack11lll1ll1l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᙑ"), None) is None or os.environ[bstack1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᙒ")] == bstack1111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᙓ"):
            return False
        return True
    @classmethod
    def bstack1l11ll11l_opy_(cls, framework=bstack1111_opy_ (u"ࠦࠧᙔ")):
        if framework not in bstack11l11l1l11_opy_:
            return False
        bstack1lll1111lll_opy_ = not bstack1l1l111l_opy_()
        return bstack1lll1111l_opy_(cls.bs_config.get(bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᙕ"), bstack1lll1111lll_opy_))
    @staticmethod
    def request_url(url):
        return bstack1111_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᙖ").format(bstack1lll111111l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᙗ"): bstack1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᙘ"),
            bstack1111_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᙙ"): bstack1111_opy_ (u"ࠪࡸࡷࡻࡥࠨᙚ")
        }
        if os.environ.get(bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᙛ"), None):
            headers[bstack1111_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᙜ")] = bstack1111_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᙝ").format(os.environ[bstack1111_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠣᙞ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᙟ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᙠ"), None)
    @staticmethod
    def bstack1l1111111l_opy_():
        if getattr(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᙡ"), None):
            return {
                bstack1111_opy_ (u"ࠫࡹࡿࡰࡦࠩᙢ"): bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࠪᙣ"),
                bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᙤ"): getattr(threading.current_thread(), bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᙥ"), None)
            }
        if getattr(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᙦ"), None):
            return {
                bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᙧ"): bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᙨ"),
                bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙩ"): getattr(threading.current_thread(), bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᙪ"), None)
            }
        return None
    @staticmethod
    def bstack11lll1ll1l_opy_(driver):
        return {
            bstack111ll11l1l_opy_(): bstack111lllllll_opy_(driver)
        }
    @staticmethod
    def bstack1lll11111ll_opy_(exception_info, report):
        return [{bstack1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᙫ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll111l11_opy_(typename):
        if bstack1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᙬ") in typename:
            return bstack1111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ᙭")
        return bstack1111_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥ᙮")
    @staticmethod
    def bstack1lll11l1l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11lll111l1_opy_(test, hook_name=None):
        bstack1lll11l1111_opy_ = test.parent
        if hook_name in [bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᙯ"), bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᙰ"), bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᙱ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᙲ")]:
            bstack1lll11l1111_opy_ = test
        scope = []
        while bstack1lll11l1111_opy_ is not None:
            scope.append(bstack1lll11l1111_opy_.name)
            bstack1lll11l1111_opy_ = bstack1lll11l1111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1111111_opy_(hook_type):
        if hook_type == bstack1111_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᙳ"):
            return bstack1111_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᙴ")
        elif hook_type == bstack1111_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᙵ"):
            return bstack1111_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᙶ")
    @staticmethod
    def bstack1lll111l1ll_opy_(bstack111lll1l1_opy_):
        try:
            if not bstack11l1ll1ll_opy_.on():
                return bstack111lll1l1_opy_
            if os.environ.get(bstack1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᙷ"), None) == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥᙸ"):
                tests = os.environ.get(bstack1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥᙹ"), None)
                if tests is None or tests == bstack1111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᙺ"):
                    return bstack111lll1l1_opy_
                bstack111lll1l1_opy_ = tests.split(bstack1111_opy_ (u"ࠨ࠮ࠪᙻ"))
                return bstack111lll1l1_opy_
        except Exception as exc:
            print(bstack1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥᙼ"), str(exc))
        return bstack111lll1l1_opy_
    @classmethod
    def bstack11llll11l1_opy_(cls, event: str, bstack1l1111l1ll_opy_: bstack1l1111lll1_opy_):
        bstack11lll1l1l1_opy_ = {
            bstack1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᙽ"): event,
            bstack1l1111l1ll_opy_.bstack1l111111l1_opy_(): bstack1l1111l1ll_opy_.bstack1l11111lll_opy_(event)
        }
        bstack11l1ll1ll_opy_.bstack11ll1ll1l1_opy_(bstack11lll1l1l1_opy_)