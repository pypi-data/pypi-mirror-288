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
import requests
import logging
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll11111l_opy_ as bstack11l1l1ll11_opy_
from bstack_utils.bstack11ll1l11_opy_ import bstack11ll1l11_opy_
from bstack_utils.helper import bstack1ll1ll1l11_opy_, bstack11lll11l1l_opy_, bstack111ll111_opy_, bstack11l1ll11ll_opy_, bstack11l1ll111l_opy_, bstack1l1l1l11l_opy_, get_host_info, bstack11l1llll11_opy_, bstack1ll1l11l11_opy_, bstack1l111l1l1l_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l111l1l1l_opy_(class_method=False)
def _11l1ll11l1_opy_(driver, bstack1l1llll1l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1111_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬ๦"): caps.get(bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ๧"), None),
        bstack1111_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ๨"): bstack1l1llll1l1_opy_.get(bstack1111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ๩"), None),
        bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ๪"): caps.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ๫"), None),
        bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๬"): caps.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ๭"), None)
    }
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ๮") + str(error))
  return response
def bstack1l1ll111_opy_(config):
  return config.get(bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭๯"), False) or any([p.get(bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ๰"), False) == True for p in config.get(bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๱"), [])])
def bstack1ll1lll111_opy_(config, bstack1l1ll1l11_opy_):
  try:
    if not bstack111ll111_opy_(config):
      return False
    bstack11l1ll1l1l_opy_ = config.get(bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ๲"), False)
    if int(bstack1l1ll1l11_opy_) < len(config.get(bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๳"), [])) and config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๴")][bstack1l1ll1l11_opy_]:
      bstack11l1l11lll_opy_ = config[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๵")][bstack1l1ll1l11_opy_].get(bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭๶"), None)
    else:
      bstack11l1l11lll_opy_ = config.get(bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ๷"), None)
    if bstack11l1l11lll_opy_ != None:
      bstack11l1ll1l1l_opy_ = bstack11l1l11lll_opy_
    bstack11l1lll1l1_opy_ = os.getenv(bstack1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭๸")) is not None and len(os.getenv(bstack1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ๹"))) > 0 and os.getenv(bstack1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ๺")) != bstack1111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ๻")
    return bstack11l1ll1l1l_opy_ and bstack11l1lll1l1_opy_
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ๼") + str(error))
  return False
def bstack1l111llll_opy_(bstack11l1lll111_opy_, test_tags):
  bstack11l1lll111_opy_ = os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ๽"))
  if bstack11l1lll111_opy_ is None:
    return True
  bstack11l1lll111_opy_ = json.loads(bstack11l1lll111_opy_)
  try:
    include_tags = bstack11l1lll111_opy_[bstack1111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ๾")] if bstack1111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭๿") in bstack11l1lll111_opy_ and isinstance(bstack11l1lll111_opy_[bstack1111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ຀")], list) else []
    exclude_tags = bstack11l1lll111_opy_[bstack1111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨກ")] if bstack1111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩຂ") in bstack11l1lll111_opy_ and isinstance(bstack11l1lll111_opy_[bstack1111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ຃")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨຄ") + str(error))
  return False
def bstack1l1lll1lll_opy_(config, bstack11l1ll1ll1_opy_, bstack11l1l1lll1_opy_, bstack11l1l1l1ll_opy_):
  bstack11l1l1llll_opy_ = bstack11l1ll11ll_opy_(config)
  bstack11l1lllll1_opy_ = bstack11l1ll111l_opy_(config)
  if bstack11l1l1llll_opy_ is None or bstack11l1lllll1_opy_ is None:
    logger.error(bstack1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ຅"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩຆ"), bstack1111_opy_ (u"ࠩࡾࢁࠬງ")))
    data = {
        bstack1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨຈ"): config[bstack1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩຉ")],
        bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨຊ"): config.get(bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ຋"), os.path.basename(os.getcwd())),
        bstack1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪຌ"): bstack1ll1ll1l11_opy_(),
        bstack1111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ຍ"): config.get(bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬຎ"), bstack1111_opy_ (u"ࠪࠫຏ")),
        bstack1111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫຐ"): {
            bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬຑ"): bstack11l1ll1ll1_opy_,
            bstack1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩຒ"): bstack11l1l1lll1_opy_,
            bstack1111_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫຓ"): __version__,
            bstack1111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪດ"): bstack1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩຕ"),
            bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪຖ"): bstack1111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ທ"),
            bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬຘ"): bstack11l1l1l1ll_opy_
        },
        bstack1111_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨນ"): settings,
        bstack1111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨບ"): bstack11l1llll11_opy_(),
        bstack1111_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨປ"): bstack1l1l1l11l_opy_(),
        bstack1111_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫຜ"): get_host_info(),
        bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬຝ"): bstack111ll111_opy_(config)
    }
    headers = {
        bstack1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪພ"): bstack1111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨຟ"),
    }
    config = {
        bstack1111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫຠ"): (bstack11l1l1llll_opy_, bstack11l1lllll1_opy_),
        bstack1111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨມ"): headers
    }
    response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ຢ"), bstack11l1l1ll11_opy_ + bstack1111_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩຣ"), data, config)
    bstack11l1l1l111_opy_ = response.json()
    if bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ຤")]:
      parsed = json.loads(os.getenv(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬລ"), bstack1111_opy_ (u"ࠬࢁࡽࠨ຦")))
      parsed[bstack1111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧວ")] = bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠧࡥࡣࡷࡥࠬຨ")][bstack1111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩຩ")]
      os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪສ")] = json.dumps(parsed)
      bstack11ll1l11_opy_.bstack11l1l1ll1l_opy_(bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠪࡨࡦࡺࡡࠨຫ")][bstack1111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬຬ")])
      bstack11ll1l11_opy_.bstack11l1ll1lll_opy_(bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠬࡪࡡࡵࡣࠪອ")][bstack1111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨຮ")])
      bstack11ll1l11_opy_.store()
      return bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠧࡥࡣࡷࡥࠬຯ")][bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ະ")], bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠩࡧࡥࡹࡧࠧັ")][bstack1111_opy_ (u"ࠪ࡭ࡩ࠭າ")]
    else:
      logger.error(bstack1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬຳ") + bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ິ")])
      if bstack11l1l1l111_opy_[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧີ")] == bstack1111_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩຶ"):
        for bstack11l1llllll_opy_ in bstack11l1l1l111_opy_[bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨື")]:
          logger.error(bstack11l1llllll_opy_[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧຸࠪ")])
      return None, None
  except Exception as error:
    logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ູࠣࠦ") +  str(error))
    return None, None
def bstack1ll11llll_opy_():
  if os.getenv(bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕ຺ࠩ")) is None:
    return {
        bstack1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬົ"): bstack1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬຼ"),
        bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຽ"): bstack1111_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧ຾")
    }
  data = {bstack1111_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪ຿"): bstack1ll1ll1l11_opy_()}
  headers = {
      bstack1111_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪເ"): bstack1111_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬແ") + os.getenv(bstack1111_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥໂ")),
      bstack1111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬໃ"): bstack1111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪໄ")
  }
  response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"ࠨࡒࡘࡘࠬ໅"), bstack11l1l1ll11_opy_ + bstack1111_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫໆ"), data, { bstack1111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ໇"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤ່ࠧ") + bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"ࠬࡠ້ࠧ"))
      return {bstack1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ໊࠭"): bstack1111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ໋"), bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໌"): bstack1111_opy_ (u"ࠩࠪໍ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨ໎") + str(error))
    return {
        bstack1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ໏"): bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ໐"),
        bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໑"): str(error)
    }
def bstack1l111llll1_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l1ll1111_opy_ = caps.get(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ໒"), {}).get(bstack1111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ໓"), caps.get(bstack1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ໔"), bstack1111_opy_ (u"ࠪࠫ໕")))
    if bstack11l1ll1111_opy_:
      logger.warn(bstack1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ໖"))
      return False
    if options:
      bstack11l1l11ll1_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11l1l11ll1_opy_ = desired_capabilities
    else:
      bstack11l1l11ll1_opy_ = {}
    browser = caps.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ໗"), bstack1111_opy_ (u"࠭ࠧ໘")).lower() or bstack11l1l11ll1_opy_.get(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ໙"), bstack1111_opy_ (u"ࠨࠩ໚")).lower()
    if browser != bstack1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ໛"):
      logger.warn(bstack1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨໜ"))
      return False
    browser_version = caps.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬໝ")) or caps.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧໞ")) or bstack11l1l11ll1_opy_.get(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧໟ")) or bstack11l1l11ll1_opy_.get(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ໠"), {}).get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ໡")) or bstack11l1l11ll1_opy_.get(bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ໢"), {}).get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໣"))
    if browser_version and browser_version != bstack1111_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫ໤") and int(browser_version.split(bstack1111_opy_ (u"ࠬ࠴ࠧ໥"))[0]) <= 94:
      logger.warn(bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠶࠱ࠦ໦"))
      return False
    if not options is None:
      bstack11l1lll1ll_opy_ = bstack11l1l11ll1_opy_.get(bstack1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ໧"), {})
      if bstack1111_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬ໨") in bstack11l1lll1ll_opy_.get(bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ໩"), []):
        logger.warn(bstack1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧ໪"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨ໫") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11ll111111_opy_ = config.get(bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ໬"), {})
    bstack11ll111111_opy_[bstack1111_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩ໭")] = os.getenv(bstack1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ໮"))
    bstack11l1l1l11l_opy_ = json.loads(os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ໯"), bstack1111_opy_ (u"ࠩࡾࢁࠬ໰"))).get(bstack1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ໱"))
    caps[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ໲")] = True
    if bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭໳") in caps:
      caps[bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ໴")][bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ໵")] = bstack11ll111111_opy_
      caps[bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ໶")][bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ໷")][bstack1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ໸")] = bstack11l1l1l11l_opy_
    else:
      caps[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ໹")] = bstack11ll111111_opy_
      caps[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ໺")][bstack1111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ໻")] = bstack11l1l1l11l_opy_
  except Exception as error:
    logger.debug(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣ໼") +  str(error))
def bstack1ll11ll1l1_opy_(driver, bstack11ll1111l1_opy_):
  try:
    setattr(driver, bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ໽"), True)
    session = driver.session_id
    if session:
      bstack11l1llll1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1llll1l_opy_ = False
      bstack11l1llll1l_opy_ = url.scheme in [bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶࠢ໾"), bstack1111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ໿")]
      if bstack11l1llll1l_opy_:
        if bstack11ll1111l1_opy_:
          logger.info(bstack1111_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦༀ"))
      return bstack11ll1111l1_opy_
  except Exception as e:
    logger.error(bstack1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ༁") + str(e))
    return False
def bstack11ll1l1ll_opy_(driver, class_name, name, module_name, path, bstack1l1llll1l1_opy_):
  try:
    bstack11ll1l11ll_opy_ = [class_name] if not class_name is None else []
    bstack11l1ll1l11_opy_ = {
        bstack1111_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ༂"): True,
        bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡉ࡫ࡴࡢ࡫࡯ࡷࠧ༃"): {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨ༄"): name,
            bstack1111_opy_ (u"ࠤࡷࡩࡸࡺࡒࡶࡰࡌࡨࠧ༅"): os.environ.get(bstack1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩ༆")),
            bstack1111_opy_ (u"ࠦ࡫࡯࡬ࡦࡒࡤࡸ࡭ࠨ༇"): str(path),
            bstack1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࡐ࡮ࡹࡴࠣ༈"): [module_name, *bstack11ll1l11ll_opy_, name],
        },
        bstack1111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ༉"): _11l1ll11l1_opy_(driver, bstack1l1llll1l1_opy_)
    }
    logger.debug(bstack1111_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ༊"))
    logger.debug(driver.execute_async_script(bstack11ll1l11_opy_.perform_scan, {bstack1111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ་"): name}))
    logger.debug(driver.execute_async_script(bstack11ll1l11_opy_.bstack11l1lll11l_opy_, bstack11l1ll1l11_opy_))
    logger.info(bstack1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ༌"))
  except Exception as bstack11l1l1l1l1_opy_:
    logger.error(bstack1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ།") + str(path) + bstack1111_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨ༎") + str(bstack11l1l1l1l1_opy_))