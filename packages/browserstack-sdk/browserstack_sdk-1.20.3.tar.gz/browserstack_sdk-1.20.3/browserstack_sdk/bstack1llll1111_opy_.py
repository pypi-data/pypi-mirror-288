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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1111l1ll_opy_ = {}
        bstack1l111ll11l_opy_ = os.environ.get(bstack1111_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬൎ"), bstack1111_opy_ (u"ࠬ࠭൏"))
        if not bstack1l111ll11l_opy_:
            return bstack1111l1ll_opy_
        try:
            bstack1l111ll111_opy_ = json.loads(bstack1l111ll11l_opy_)
            if bstack1111_opy_ (u"ࠨ࡯ࡴࠤ൐") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠢࡰࡵࠥ൑")] = bstack1l111ll111_opy_[bstack1111_opy_ (u"ࠣࡱࡶࠦ൒")]
            if bstack1111_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ൓") in bstack1l111ll111_opy_ or bstack1111_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨൔ") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢൕ")] = bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤൖ"), bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤൗ")))
            if bstack1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ൘") in bstack1l111ll111_opy_ or bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ൙") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ൚")] = bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦ൛"), bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ൜")))
            if bstack1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ൝") in bstack1l111ll111_opy_ or bstack1111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ൞") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣൟ")] = bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥൠ"), bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥൡ")))
            if bstack1111_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥൢ") in bstack1l111ll111_opy_ or bstack1111_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣൣ") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ൤")] = bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨ൥"), bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦ൦")))
            if bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ൧") in bstack1l111ll111_opy_ or bstack1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ൨") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ൩")] = bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ൪"), bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ൫")))
            if bstack1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ൬") in bstack1l111ll111_opy_ or bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ൭") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ൮")] = bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ൯"), bstack1l111ll111_opy_.get(bstack1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ൰")))
            if bstack1111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ൱") in bstack1l111ll111_opy_:
                bstack1111l1ll_opy_[bstack1111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ൲")] = bstack1l111ll111_opy_[bstack1111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ൳")]
        except Exception as error:
            logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨ൴") +  str(error))
        return bstack1111l1ll_opy_