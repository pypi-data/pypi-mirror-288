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
import re
from bstack_utils.bstack1lllll11l_opy_ import bstack1lll1lllll1_opy_
def bstack1llll111lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓮ")):
        return bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᓯ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓰ")):
        return bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᓱ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓲ")):
        return bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᓳ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᓴ")):
        return bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᓵ")
def bstack1llll111111_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᓶ"), fixture_name))
def bstack1llll11111l_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᓷ"), fixture_name))
def bstack1lll1llllll_opy_(fixture_name):
    return bool(re.match(bstack1111_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᓸ"), fixture_name))
def bstack1llll11l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack1111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓹ")):
        return bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᓺ"), bstack1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᓻ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓼ")):
        return bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᓽ"), bstack1111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᓾ")
    elif fixture_name.startswith(bstack1111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓿ")):
        return bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᔀ"), bstack1111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᔁ")
    elif fixture_name.startswith(bstack1111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᔂ")):
        return bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᔃ"), bstack1111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᔄ")
    return None, None
def bstack1llll1111ll_opy_(hook_name):
    if hook_name in [bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᔅ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᔆ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll11l111_opy_(hook_name):
    if hook_name in [bstack1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᔇ"), bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᔈ")]:
        return bstack1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᔉ")
    elif hook_name in [bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᔊ"), bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᔋ")]:
        return bstack1111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᔌ")
    elif hook_name in [bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᔍ"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᔎ")]:
        return bstack1111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᔏ")
    elif hook_name in [bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᔐ"), bstack1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᔑ")]:
        return bstack1111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᔒ")
    return hook_name
def bstack1llll1111l1_opy_(node, scenario):
    if hasattr(node, bstack1111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᔓ")):
        parts = node.nodeid.rsplit(bstack1111_opy_ (u"ࠨ࡛ࠣᔔ"))
        params = parts[-1]
        return bstack1111_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᔕ").format(scenario.name, params)
    return scenario.name
def bstack1lll1llll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1111_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᔖ")):
            examples = list(node.callspec.params[bstack1111_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᔗ")].values())
        return examples
    except:
        return []
def bstack1llll111ll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll111l1l_opy_(report):
    try:
        status = bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᔘ")
        if report.passed or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᔙ"))):
            status = bstack1111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᔚ")
        elif report.skipped:
            status = bstack1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᔛ")
        bstack1lll1lllll1_opy_(status)
    except:
        pass
def bstack1l11l111l1_opy_(status):
    try:
        bstack1llll111l11_opy_ = bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᔜ")
        if status == bstack1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᔝ"):
            bstack1llll111l11_opy_ = bstack1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᔞ")
        elif status == bstack1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᔟ"):
            bstack1llll111l11_opy_ = bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᔠ")
        bstack1lll1lllll1_opy_(bstack1llll111l11_opy_)
    except:
        pass
def bstack1lll1llll1l_opy_(item=None, report=None, summary=None, extra=None):
    return