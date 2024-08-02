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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11111l1l1l_opy_
bstack1lll111l1l_opy_ = Config.bstack11lll1111_opy_()
def bstack1llll11l1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llll1l1111_opy_(bstack1llll11lll1_opy_, bstack1llll11llll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llll11lll1_opy_):
        with open(bstack1llll11lll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llll11l1l1_opy_(bstack1llll11lll1_opy_):
        pac = get_pac(url=bstack1llll11lll1_opy_)
    else:
        raise Exception(bstack1111_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᓈ").format(bstack1llll11lll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1111_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᓉ"), 80))
        bstack1llll11ll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll11ll1l_opy_ = bstack1111_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᓊ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll11llll_opy_, bstack1llll11ll1l_opy_)
    return proxy_url
def bstack1l1l11llll_opy_(config):
    return bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᓋ") in config or bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᓌ") in config
def bstack1lll11l1ll_opy_(config):
    if not bstack1l1l11llll_opy_(config):
        return
    if config.get(bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᓍ")):
        return config.get(bstack1111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᓎ"))
    if config.get(bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᓏ")):
        return config.get(bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᓐ"))
def bstack111l1ll1_opy_(config, bstack1llll11llll_opy_):
    proxy = bstack1lll11l1ll_opy_(config)
    proxies = {}
    if config.get(bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᓑ")) or config.get(bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᓒ")):
        if proxy.endswith(bstack1111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᓓ")):
            proxies = bstack1111l1ll1_opy_(proxy, bstack1llll11llll_opy_)
        else:
            proxies = {
                bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᓔ"): proxy
            }
    bstack1lll111l1l_opy_.bstack1l1lll1111_opy_(bstack1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᓕ"), proxies)
    return proxies
def bstack1111l1ll1_opy_(bstack1llll11lll1_opy_, bstack1llll11llll_opy_):
    proxies = {}
    global bstack1llll11ll11_opy_
    if bstack1111_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪᓖ") in globals():
        return bstack1llll11ll11_opy_
    try:
        proxy = bstack1llll1l1111_opy_(bstack1llll11lll1_opy_, bstack1llll11llll_opy_)
        if bstack1111_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣᓗ") in proxy:
            proxies = {}
        elif bstack1111_opy_ (u"ࠤࡋࡘ࡙ࡖࠢᓘ") in proxy or bstack1111_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤᓙ") in proxy or bstack1111_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥᓚ") in proxy:
            bstack1llll11l1ll_opy_ = proxy.split(bstack1111_opy_ (u"ࠧࠦࠢᓛ"))
            if bstack1111_opy_ (u"ࠨ࠺࠰࠱ࠥᓜ") in bstack1111_opy_ (u"ࠢࠣᓝ").join(bstack1llll11l1ll_opy_[1:]):
                proxies = {
                    bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᓞ"): bstack1111_opy_ (u"ࠤࠥᓟ").join(bstack1llll11l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᓠ"): str(bstack1llll11l1ll_opy_[0]).lower() + bstack1111_opy_ (u"ࠦ࠿࠵࠯ࠣᓡ") + bstack1111_opy_ (u"ࠧࠨᓢ").join(bstack1llll11l1ll_opy_[1:])
                }
        elif bstack1111_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᓣ") in proxy:
            bstack1llll11l1ll_opy_ = proxy.split(bstack1111_opy_ (u"ࠢࠡࠤᓤ"))
            if bstack1111_opy_ (u"ࠣ࠼࠲࠳ࠧᓥ") in bstack1111_opy_ (u"ࠤࠥᓦ").join(bstack1llll11l1ll_opy_[1:]):
                proxies = {
                    bstack1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᓧ"): bstack1111_opy_ (u"ࠦࠧᓨ").join(bstack1llll11l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᓩ"): bstack1111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᓪ") + bstack1111_opy_ (u"ࠢࠣᓫ").join(bstack1llll11l1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᓬ"): proxy
            }
    except Exception as e:
        print(bstack1111_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᓭ"), bstack11111l1l1l_opy_.format(bstack1llll11lll1_opy_, str(e)))
    bstack1llll11ll11_opy_ = proxies
    return proxies