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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11l11l1l1l_opy_, bstack11l1111ll_opy_, bstack1111l11l1_opy_, bstack1ll111l1_opy_,
                                    bstack11l111llll_opy_, bstack11l11ll111_opy_, bstack11l111l1ll_opy_, bstack11l11ll11l_opy_)
from bstack_utils.messages import bstack11l1ll1l_opy_, bstack111l11ll1_opy_
from bstack_utils.proxy import bstack111l1ll1_opy_, bstack1lll11l1ll_opy_
bstack1lll111l1l_opy_ = Config.bstack11lll1111_opy_()
logger = logging.getLogger(__name__)
def bstack11l1ll11ll_opy_(config):
    return config[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬሁ")]
def bstack11l1ll111l_opy_(config):
    return config[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧሂ")]
def bstack1l1l111l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111l1l111l_opy_(obj):
    values = []
    bstack11l111l111_opy_ = re.compile(bstack1111_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤሃ"), re.I)
    for key in obj.keys():
        if bstack11l111l111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l11ll11_opy_(config):
    tags = []
    tags.extend(bstack111l1l111l_opy_(os.environ))
    tags.extend(bstack111l1l111l_opy_(config))
    return tags
def bstack111l1l1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111llllll1_opy_(bstack111lll1111_opy_):
    if not bstack111lll1111_opy_:
        return bstack1111_opy_ (u"࠭ࠧሄ")
    return bstack1111_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣህ").format(bstack111lll1111_opy_.name, bstack111lll1111_opy_.email)
def bstack11l1llll11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l1ll1l1_opy_ = repo.common_dir
        info = {
            bstack1111_opy_ (u"ࠣࡵ࡫ࡥࠧሆ"): repo.head.commit.hexsha,
            bstack1111_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧሇ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥለ"): repo.active_branch.name,
            bstack1111_opy_ (u"ࠦࡹࡧࡧࠣሉ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣሊ"): bstack111llllll1_opy_(repo.head.commit.committer),
            bstack1111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢላ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢሌ"): bstack111llllll1_opy_(repo.head.commit.author),
            bstack1111_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨል"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥሎ"): repo.head.commit.message,
            bstack1111_opy_ (u"ࠥࡶࡴࡵࡴࠣሏ"): repo.git.rev_parse(bstack1111_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨሐ")),
            bstack1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨሑ"): bstack111l1ll1l1_opy_,
            bstack1111_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤሒ"): subprocess.check_output([bstack1111_opy_ (u"ࠢࡨ࡫ࡷࠦሓ"), bstack1111_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦሔ"), bstack1111_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧሕ")]).strip().decode(
                bstack1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩሖ")),
            bstack1111_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨሗ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢመ"): repo.git.rev_list(
                bstack1111_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨሙ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111lll1lll_opy_ = []
        for remote in remotes:
            bstack111ll1ll11_opy_ = {
                bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧሚ"): remote.name,
                bstack1111_opy_ (u"ࠣࡷࡵࡰࠧማ"): remote.url,
            }
            bstack111lll1lll_opy_.append(bstack111ll1ll11_opy_)
        bstack111ll1l1ll_opy_ = {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሜ"): bstack1111_opy_ (u"ࠥ࡫࡮ࡺࠢም"),
            **info,
            bstack1111_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧሞ"): bstack111lll1lll_opy_
        }
        bstack111ll1l1ll_opy_ = bstack11l11111l1_opy_(bstack111ll1l1ll_opy_)
        return bstack111ll1l1ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣሟ").format(err))
        return {}
def bstack11l11111l1_opy_(bstack111ll1l1ll_opy_):
    bstack11l111l11l_opy_ = bstack1111lllll1_opy_(bstack111ll1l1ll_opy_)
    if bstack11l111l11l_opy_ and bstack11l111l11l_opy_ > bstack11l111llll_opy_:
        bstack111l1lll1l_opy_ = bstack11l111l11l_opy_ - bstack11l111llll_opy_
        bstack111llll1l1_opy_ = bstack111l111ll1_opy_(bstack111ll1l1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢሠ")], bstack111l1lll1l_opy_)
        bstack111ll1l1ll_opy_[bstack1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣሡ")] = bstack111llll1l1_opy_
        logger.info(bstack1111_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥሢ")
                    .format(bstack1111lllll1_opy_(bstack111ll1l1ll_opy_) / 1024))
    return bstack111ll1l1ll_opy_
def bstack1111lllll1_opy_(bstack1ll111lll_opy_):
    try:
        if bstack1ll111lll_opy_:
            bstack111ll1lll1_opy_ = json.dumps(bstack1ll111lll_opy_)
            bstack11l1111111_opy_ = sys.getsizeof(bstack111ll1lll1_opy_)
            return bstack11l1111111_opy_
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤሣ").format(e))
    return -1
def bstack111l111ll1_opy_(field, bstack11l1111l11_opy_):
    try:
        bstack111l11l11l_opy_ = len(bytes(bstack11l11ll111_opy_, bstack1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩሤ")))
        bstack111l111lll_opy_ = bytes(field, bstack1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪሥ"))
        bstack111lll1l11_opy_ = len(bstack111l111lll_opy_)
        bstack111l111l11_opy_ = ceil(bstack111lll1l11_opy_ - bstack11l1111l11_opy_ - bstack111l11l11l_opy_)
        if bstack111l111l11_opy_ > 0:
            bstack111lllll11_opy_ = bstack111l111lll_opy_[:bstack111l111l11_opy_].decode(bstack1111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫሦ"), errors=bstack1111_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭ሧ")) + bstack11l11ll111_opy_
            return bstack111lllll11_opy_
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧረ").format(e))
    return field
def bstack1l1l1l11l_opy_():
    env = os.environ
    if (bstack1111_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨሩ") in env and len(env[bstack1111_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢሪ")]) > 0) or (
            bstack1111_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤራ") in env and len(env[bstack1111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥሬ")]) > 0):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥር"): bstack1111_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢሮ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሯ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦሰ")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሱ"): env.get(bstack1111_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧሲ")),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሳ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሴ"))
        }
    if env.get(bstack1111_opy_ (u"ࠨࡃࡊࠤስ")) == bstack1111_opy_ (u"ࠢࡵࡴࡸࡩࠧሶ") and bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥሷ"))):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሸ"): bstack1111_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧሹ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሺ"): env.get(bstack1111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣሻ")),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሼ"): env.get(bstack1111_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦሽ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሾ"): env.get(bstack1111_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧሿ"))
        }
    if env.get(bstack1111_opy_ (u"ࠥࡇࡎࠨቀ")) == bstack1111_opy_ (u"ࠦࡹࡸࡵࡦࠤቁ") and bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧቂ"))):
        return {
            bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቃ"): bstack1111_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥቄ"),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቅ"): env.get(bstack1111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤቆ")),
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧቇ"): env.get(bstack1111_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨቈ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ቉"): env.get(bstack1111_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧቊ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡋࠥቋ")) == bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨቌ") and env.get(bstack1111_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥቍ")) == bstack1111_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ቎"):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ቏"): bstack1111_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢቐ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቑ"): None,
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤቒ"): None,
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቓ"): None
        }
    if env.get(bstack1111_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧቔ")) and env.get(bstack1111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨቕ")):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቖ"): bstack1111_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ቗"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቘ"): env.get(bstack1111_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ቙")),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቚ"): None,
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣቛ"): env.get(bstack1111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧቜ"))
        }
    if env.get(bstack1111_opy_ (u"ࠦࡈࡏࠢቝ")) == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥ቞") and bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ቟"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧበ"): bstack1111_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢቡ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቢ"): env.get(bstack1111_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨባ")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቤ"): None,
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦብ"): env.get(bstack1111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦቦ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡋࠥቧ")) == bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨቨ") and bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧቩ"))):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣቪ"): bstack1111_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢቫ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣቬ"): env.get(bstack1111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧቭ")),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤቮ"): env.get(bstack1111_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨቯ")),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣተ"): env.get(bstack1111_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨቱ"))
        }
    if env.get(bstack1111_opy_ (u"ࠦࡈࡏࠢቲ")) == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥታ") and bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤቴ"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧት"): bstack1111_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣቶ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቷ"): env.get(bstack1111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢቸ")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቹ"): env.get(bstack1111_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥቺ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቻ"): env.get(bstack1111_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥቼ"))
        }
    if env.get(bstack1111_opy_ (u"ࠣࡅࡌࠦች")) == bstack1111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢቾ") and bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨቿ"))):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኀ"): bstack1111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣኁ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኂ"): env.get(bstack1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨኃ")),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኄ"): env.get(bstack1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦኅ")) or env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨኆ")),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥኇ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢኈ"))
        }
    if bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ኉"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧኊ"): bstack1111_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣኋ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧኌ"): bstack1111_opy_ (u"ࠥࡿࢂࢁࡽࠣኍ").format(env.get(bstack1111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ኎")), env.get(bstack1111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬ኏"))),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣነ"): env.get(bstack1111_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨኑ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኒ"): env.get(bstack1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤና"))
        }
    if bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧኔ"))):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤን"): bstack1111_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢኖ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኗ"): bstack1111_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨኘ").format(env.get(bstack1111_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧኙ")), env.get(bstack1111_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪኚ")), env.get(bstack1111_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫኛ")), env.get(bstack1111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨኜ"))),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢኝ"): env.get(bstack1111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥኞ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨኟ"): env.get(bstack1111_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤአ"))
        }
    if env.get(bstack1111_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥኡ")) and env.get(bstack1111_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧኢ")):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኣ"): bstack1111_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢኤ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤእ"): bstack1111_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥኦ").format(env.get(bstack1111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫኧ")), env.get(bstack1111_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧከ")), env.get(bstack1111_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪኩ"))),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨኪ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧካ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኬ"): env.get(bstack1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢክ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨኮ")), env.get(bstack1111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣኯ")), env.get(bstack1111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢኰ"))]):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ኱"): bstack1111_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧኲ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኳ"): env.get(bstack1111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨኴ")),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኵ"): env.get(bstack1111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ኶")),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ኷"): env.get(bstack1111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤኸ"))
        }
    if env.get(bstack1111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥኹ")):
        return {
            bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦኺ"): bstack1111_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢኻ"),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦኼ"): env.get(bstack1111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦኽ")),
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧኾ"): env.get(bstack1111_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ኿")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦዀ"): env.get(bstack1111_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ዁"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣዂ")) or env.get(bstack1111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥዃ")):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢዄ"): bstack1111_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦዅ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ዆"): env.get(bstack1111_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ዇")),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣወ"): bstack1111_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢዉ") if env.get(bstack1111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥዊ")) else None,
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣዋ"): env.get(bstack1111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣዌ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤው")), env.get(bstack1111_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨዎ")), env.get(bstack1111_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨዏ"))]):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዐ"): bstack1111_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢዑ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧዒ"): None,
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧዓ"): env.get(bstack1111_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣዔ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦዕ"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣዖ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ዗")):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨዘ"): bstack1111_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧዙ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዚ"): env.get(bstack1111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥዛ")),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢዜ"): bstack1111_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢዝ").format(env.get(bstack1111_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪዞ"))) if env.get(bstack1111_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦዟ")) else None,
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣዠ"): env.get(bstack1111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧዡ"))
        }
    if bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧዢ"))):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥዣ"): bstack1111_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢዤ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥዥ"): env.get(bstack1111_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧዦ")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦዧ"): env.get(bstack1111_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨየ")),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥዩ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢዪ"))
        }
    if bstack1lll1111l_opy_(env.get(bstack1111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢያ"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዬ"): bstack1111_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤይ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧዮ"): bstack1111_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦዯ").format(env.get(bstack1111_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨደ")), env.get(bstack1111_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩዱ")), env.get(bstack1111_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ዲ"))),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤዳ"): env.get(bstack1111_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥዴ")),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣድ"): env.get(bstack1111_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥዶ"))
        }
    if env.get(bstack1111_opy_ (u"ࠦࡈࡏࠢዷ")) == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥዸ") and env.get(bstack1111_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨዹ")) == bstack1111_opy_ (u"ࠢ࠲ࠤዺ"):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨዻ"): bstack1111_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤዼ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዽ"): bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢዾ").format(env.get(bstack1111_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩዿ"))),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጀ"): None,
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨጁ"): None,
        }
    if env.get(bstack1111_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦጂ")):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጃ"): bstack1111_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧጄ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጅ"): None,
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢጆ"): env.get(bstack1111_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢጇ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨገ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢጉ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧጊ")), env.get(bstack1111_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥጋ")), env.get(bstack1111_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤጌ")), env.get(bstack1111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨግ"))]):
        return {
            bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጎ"): bstack1111_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥጏ"),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጐ"): None,
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ጑"): env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦጒ")) or None,
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጓ"): env.get(bstack1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢጔ"), 0)
        }
    if env.get(bstack1111_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦጕ")):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ጖"): bstack1111_opy_ (u"ࠣࡉࡲࡇࡉࠨ጗"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧጘ"): None,
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጙ"): env.get(bstack1111_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤጚ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦጛ"): env.get(bstack1111_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧጜ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧጝ")):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨጞ"): bstack1111_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧጟ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጠ"): env.get(bstack1111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥጡ")),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢጢ"): env.get(bstack1111_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤጣ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨጤ"): env.get(bstack1111_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨጥ"))
        }
    return {bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣጦ"): None}
def get_host_info():
    return {
        bstack1111_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧጧ"): platform.node(),
        bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨጨ"): platform.system(),
        bstack1111_opy_ (u"ࠧࡺࡹࡱࡧࠥጩ"): platform.machine(),
        bstack1111_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢጪ"): platform.version(),
        bstack1111_opy_ (u"ࠢࡢࡴࡦ࡬ࠧጫ"): platform.architecture()[0]
    }
def bstack1l1lll111l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111ll11l1l_opy_():
    if bstack1lll111l1l_opy_.get_property(bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩጬ")):
        return bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨጭ")
    return bstack1111_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩጮ")
def bstack111lllllll_opy_(driver):
    info = {
        bstack1111_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪጯ"): driver.capabilities,
        bstack1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩጰ"): driver.session_id,
        bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧጱ"): driver.capabilities.get(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬጲ"), None),
        bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪጳ"): driver.capabilities.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪጴ"), None),
        bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬጵ"): driver.capabilities.get(bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪጶ"), None),
    }
    if bstack111ll11l1l_opy_() == bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫጷ"):
        info[bstack1111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧጸ")] = bstack1111_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ጹ") if bstack1ll11l111l_opy_() else bstack1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪጺ")
    return info
def bstack1ll11l111l_opy_():
    if bstack1lll111l1l_opy_.get_property(bstack1111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨጻ")):
        return True
    if bstack1lll1111l_opy_(os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫጼ"), None)):
        return True
    return False
def bstack1ll1l11l11_opy_(bstack111ll11lll_opy_, url, data, config):
    headers = config.get(bstack1111_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬጽ"), None)
    proxies = bstack111l1ll1_opy_(config, url)
    auth = config.get(bstack1111_opy_ (u"ࠬࡧࡵࡵࡪࠪጾ"), None)
    response = requests.request(
            bstack111ll11lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll11l1ll1_opy_(bstack1ll111l1ll_opy_, size):
    bstack11llll1l1_opy_ = []
    while len(bstack1ll111l1ll_opy_) > size:
        bstack1l11ll1lll_opy_ = bstack1ll111l1ll_opy_[:size]
        bstack11llll1l1_opy_.append(bstack1l11ll1lll_opy_)
        bstack1ll111l1ll_opy_ = bstack1ll111l1ll_opy_[size:]
    bstack11llll1l1_opy_.append(bstack1ll111l1ll_opy_)
    return bstack11llll1l1_opy_
def bstack111ll11111_opy_(message, bstack111ll111l1_opy_=False):
    os.write(1, bytes(message, bstack1111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬጿ")))
    os.write(1, bytes(bstack1111_opy_ (u"ࠧ࡝ࡰࠪፀ"), bstack1111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧፁ")))
    if bstack111ll111l1_opy_:
        with open(bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨፂ") + os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩፃ")] + bstack1111_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩፄ"), bstack1111_opy_ (u"ࠬࡧࠧፅ")) as f:
            f.write(message + bstack1111_opy_ (u"࠭࡜࡯ࠩፆ"))
def bstack111ll1llll_opy_():
    return os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪፇ")].lower() == bstack1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ፈ")
def bstack1l11ll111l_opy_(bstack111l1l1lll_opy_):
    return bstack1111_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨፉ").format(bstack11l11l1l1l_opy_, bstack111l1l1lll_opy_)
def bstack1ll1ll1l11_opy_():
    return bstack11lll11l1l_opy_().replace(tzinfo=None).isoformat() + bstack1111_opy_ (u"ࠪ࡞ࠬፊ")
def bstack111ll111ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111_opy_ (u"ࠫ࡟࠭ፋ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111_opy_ (u"ࠬࡠࠧፌ")))).total_seconds() * 1000
def bstack111l1l1l11_opy_(timestamp):
    return bstack1111lll11l_opy_(timestamp).isoformat() + bstack1111_opy_ (u"࡚࠭ࠨፍ")
def bstack111llll1ll_opy_(bstack1111llll1l_opy_):
    date_format = bstack1111_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬፎ")
    bstack1111lll1ll_opy_ = datetime.datetime.strptime(bstack1111llll1l_opy_, date_format)
    return bstack1111lll1ll_opy_.isoformat() + bstack1111_opy_ (u"ࠨ࡜ࠪፏ")
def bstack111llll111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩፐ")
    else:
        return bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪፑ")
def bstack1lll1111l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111_opy_ (u"ࠫࡹࡸࡵࡦࠩፒ")
def bstack111l1l1l1l_opy_(val):
    return val.__str__().lower() == bstack1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫፓ")
def bstack1l111l1l1l_opy_(bstack111l1lll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l1lll11_opy_ as e:
                print(bstack1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨፔ").format(func.__name__, bstack111l1lll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111lll111_opy_(bstack111l11ll1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l11ll1l_opy_(cls, *args, **kwargs)
            except bstack111l1lll11_opy_ as e:
                print(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢፕ").format(bstack111l11ll1l_opy_.__name__, bstack111l1lll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111lll111_opy_
    else:
        return decorator
def bstack111ll111_opy_(bstack11ll1l1l1l_opy_):
    if bstack1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬፖ") in bstack11ll1l1l1l_opy_ and bstack111l1l1l1l_opy_(bstack11ll1l1l1l_opy_[bstack1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ፗ")]):
        return False
    if bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬፘ") in bstack11ll1l1l1l_opy_ and bstack111l1l1l1l_opy_(bstack11ll1l1l1l_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ፙ")]):
        return False
    return True
def bstack1l1llllll1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1l111ll1_opy_(hub_url):
    if bstack11ll11111_opy_() <= version.parse(bstack1111_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬፚ")):
        if hub_url != bstack1111_opy_ (u"࠭ࠧ፛"):
            return bstack1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ፜") + hub_url + bstack1111_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ፝")
        return bstack1111l11l1_opy_
    if hub_url != bstack1111_opy_ (u"ࠩࠪ፞"):
        return bstack1111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ፟") + hub_url + bstack1111_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ፠")
    return bstack1ll111l1_opy_
def bstack11l1111ll1_opy_():
    return isinstance(os.getenv(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ፡")), str)
def bstack1111111l_opy_(url):
    return urlparse(url).hostname
def bstack11lll1l11_opy_(hostname):
    for bstack111l1lll1_opy_ in bstack11l1111ll_opy_:
        regex = re.compile(bstack111l1lll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111ll1l1l1_opy_(bstack111lll111l_opy_, file_name, logger):
    bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"࠭ࡾࠨ።")), bstack111lll111l_opy_)
    try:
        if not os.path.exists(bstack11l11111l_opy_):
            os.makedirs(bstack11l11111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠧࡿࠩ፣")), bstack111lll111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111_opy_ (u"ࠨࡹࠪ፤")):
                pass
            with open(file_path, bstack1111_opy_ (u"ࠤࡺ࠯ࠧ፥")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1ll1l_opy_.format(str(e)))
def bstack111ll1ll1l_opy_(file_name, key, value, logger):
    file_path = bstack111ll1l1l1_opy_(bstack1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ፦"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1l1ll_opy_ = json.load(open(file_path, bstack1111_opy_ (u"ࠫࡷࡨࠧ፧")))
        else:
            bstack1ll1l1ll_opy_ = {}
        bstack1ll1l1ll_opy_[key] = value
        with open(file_path, bstack1111_opy_ (u"ࠧࡽࠫࠣ፨")) as outfile:
            json.dump(bstack1ll1l1ll_opy_, outfile)
def bstack1ll11l11l1_opy_(file_name, logger):
    file_path = bstack111ll1l1l1_opy_(bstack1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭፩"), file_name, logger)
    bstack1ll1l1ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111_opy_ (u"ࠧࡳࠩ፪")) as bstack1lll11l11l_opy_:
            bstack1ll1l1ll_opy_ = json.load(bstack1lll11l11l_opy_)
    return bstack1ll1l1ll_opy_
def bstack11ll1ll1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ፫") + file_path + bstack1111_opy_ (u"ࠩࠣࠫ፬") + str(e))
def bstack11ll11111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ፭")
def bstack111l1l11l_opy_(config):
    if bstack1111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ፮") in config:
        del (config[bstack1111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ፯")])
        return False
    if bstack11ll11111_opy_() < version.parse(bstack1111_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ፰")):
        return False
    if bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭፱")):
        return True
    if bstack1111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ፲") in config and config[bstack1111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ፳")] is False:
        return False
    else:
        return True
def bstack1l1l111l1l_opy_(args_list, bstack111l1l11l1_opy_):
    index = -1
    for value in bstack111l1l11l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lll11ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lll11ll1_opy_ = bstack11lll11ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ፴"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ፵"), exception=exception)
    def bstack11ll111l11_opy_(self):
        if self.result != bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ፶"):
            return None
        if bstack1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ፷") in self.exception_type:
            return bstack1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ፸")
        return bstack1111_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ፹")
    def bstack111l1111ll_opy_(self):
        if self.result != bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ፺"):
            return None
        if self.bstack11lll11ll1_opy_:
            return self.bstack11lll11ll1_opy_
        return bstack111l1111l1_opy_(self.exception)
def bstack111l1111l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1lllll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l111ll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111lll1_opy_(config, logger):
    try:
        import playwright
        bstack111ll1111l_opy_ = playwright.__file__
        bstack111l1l11ll_opy_ = os.path.split(bstack111ll1111l_opy_)
        bstack111l111l1l_opy_ = bstack111l1l11ll_opy_[0] + bstack1111_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭፻")
        os.environ[bstack1111_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ፼")] = bstack1lll11l1ll_opy_(config)
        with open(bstack111l111l1l_opy_, bstack1111_opy_ (u"ࠬࡸࠧ፽")) as f:
            bstack1llll1l111_opy_ = f.read()
            bstack111ll1l111_opy_ = bstack1111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ፾")
            bstack111lllll1l_opy_ = bstack1llll1l111_opy_.find(bstack111ll1l111_opy_)
            if bstack111lllll1l_opy_ == -1:
              process = subprocess.Popen(bstack1111_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ፿"), shell=True, cwd=bstack111l1l11ll_opy_[0])
              process.wait()
              bstack11l111l1l1_opy_ = bstack1111_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᎀ")
              bstack111lll1l1l_opy_ = bstack1111_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᎁ")
              bstack111l1l1111_opy_ = bstack1llll1l111_opy_.replace(bstack11l111l1l1_opy_, bstack111lll1l1l_opy_)
              with open(bstack111l111l1l_opy_, bstack1111_opy_ (u"ࠪࡻࠬᎂ")) as f:
                f.write(bstack111l1l1111_opy_)
    except Exception as e:
        logger.error(bstack111l11ll1_opy_.format(str(e)))
def bstack1ll1l11ll_opy_():
  try:
    bstack111lll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᎃ"))
    bstack111l1llll1_opy_ = []
    if os.path.exists(bstack111lll11ll_opy_):
      with open(bstack111lll11ll_opy_) as f:
        bstack111l1llll1_opy_ = json.load(f)
      os.remove(bstack111lll11ll_opy_)
    return bstack111l1llll1_opy_
  except:
    pass
  return []
def bstack1111l1l11_opy_(bstack11111ll1_opy_):
  try:
    bstack111l1llll1_opy_ = []
    bstack111lll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᎄ"))
    if os.path.exists(bstack111lll11ll_opy_):
      with open(bstack111lll11ll_opy_) as f:
        bstack111l1llll1_opy_ = json.load(f)
    bstack111l1llll1_opy_.append(bstack11111ll1_opy_)
    with open(bstack111lll11ll_opy_, bstack1111_opy_ (u"࠭ࡷࠨᎅ")) as f:
        json.dump(bstack111l1llll1_opy_, f)
  except:
    pass
def bstack1l1l11lll1_opy_(logger, bstack111l11lll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᎆ"), bstack1111_opy_ (u"ࠨࠩᎇ"))
    if test_name == bstack1111_opy_ (u"ࠩࠪᎈ"):
        test_name = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᎉ"), bstack1111_opy_ (u"ࠫࠬᎊ"))
    bstack111l1ll111_opy_ = bstack1111_opy_ (u"ࠬ࠲ࠠࠨᎋ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l11lll1_opy_:
        bstack1l1ll1l11_opy_ = os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᎌ"), bstack1111_opy_ (u"ࠧ࠱ࠩᎍ"))
        bstack1ll1l1ll1l_opy_ = {bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᎎ"): test_name, bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᎏ"): bstack111l1ll111_opy_, bstack1111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ᎐"): bstack1l1ll1l11_opy_}
        bstack111l1ll11l_opy_ = []
        bstack111l1ll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ᎑"))
        if os.path.exists(bstack111l1ll1ll_opy_):
            with open(bstack111l1ll1ll_opy_) as f:
                bstack111l1ll11l_opy_ = json.load(f)
        bstack111l1ll11l_opy_.append(bstack1ll1l1ll1l_opy_)
        with open(bstack111l1ll1ll_opy_, bstack1111_opy_ (u"ࠬࡽࠧ᎒")) as f:
            json.dump(bstack111l1ll11l_opy_, f)
    else:
        bstack1ll1l1ll1l_opy_ = {bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᎓"): test_name, bstack1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᎔"): bstack111l1ll111_opy_, bstack1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᎕"): str(multiprocessing.current_process().name)}
        if bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭᎖") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1l1ll1l_opy_)
  except Exception as e:
      logger.warn(bstack1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᎗").format(e))
def bstack1111ll1l1_opy_(error_message, test_name, index, logger):
  try:
    bstack111lll1ll1_opy_ = []
    bstack1ll1l1ll1l_opy_ = {bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᎘"): test_name, bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᎙"): error_message, bstack1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᎚"): index}
    bstack1111llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᎛"))
    if os.path.exists(bstack1111llllll_opy_):
        with open(bstack1111llllll_opy_) as f:
            bstack111lll1ll1_opy_ = json.load(f)
    bstack111lll1ll1_opy_.append(bstack1ll1l1ll1l_opy_)
    with open(bstack1111llllll_opy_, bstack1111_opy_ (u"ࠨࡹࠪ᎜")) as f:
        json.dump(bstack111lll1ll1_opy_, f)
  except Exception as e:
    logger.warn(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᎝").format(e))
def bstack1ll1111l11_opy_(bstack1l1lllll11_opy_, name, logger):
  try:
    bstack1ll1l1ll1l_opy_ = {bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ᎞"): name, bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᎟"): bstack1l1lllll11_opy_, bstack1111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᎠ"): str(threading.current_thread()._name)}
    return bstack1ll1l1ll1l_opy_
  except Exception as e:
    logger.warn(bstack1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᎡ").format(e))
  return
def bstack111l11l1l1_opy_():
    return platform.system() == bstack1111_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨᎢ")
def bstack1ll1l1l11_opy_(bstack111ll1l11l_opy_, config, logger):
    bstack1111ll1lll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111ll1l11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢᎣ").format(e))
    return bstack1111ll1lll_opy_
def bstack11l1111l1l_opy_(bstack111l111111_opy_, bstack111l11l111_opy_):
    bstack111llll11l_opy_ = version.parse(bstack111l111111_opy_)
    bstack111l11l1ll_opy_ = version.parse(bstack111l11l111_opy_)
    if bstack111llll11l_opy_ > bstack111l11l1ll_opy_:
        return 1
    elif bstack111llll11l_opy_ < bstack111l11l1ll_opy_:
        return -1
    else:
        return 0
def bstack11lll11l1l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111lll11l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111lll11l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111ll1l11_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1111_opy_ (u"ࠩࡪࡩࡹ࠭Ꭴ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l1ll1l_opy_ = caps.get(bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᎥ"))
    bstack1111llll11_opy_ = True
    if bstack111l1l1l1l_opy_(caps.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᎦ"))) or bstack111l1l1l1l_opy_(caps.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᎧ"))):
        bstack1111llll11_opy_ = False
    if bstack111l1l11l_opy_({bstack1111_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᎨ"): bstack1111llll11_opy_}):
        bstack1l1l1ll1l_opy_ = bstack1l1l1ll1l_opy_ or {}
        bstack1l1l1ll1l_opy_[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᎩ")] = bstack111lll11l1_opy_(framework)
        bstack1l1l1ll1l_opy_[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᎪ")] = bstack111ll1llll_opy_()
        if getattr(options, bstack1111_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᎫ"), None):
            options.set_capability(bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᎬ"), bstack1l1l1ll1l_opy_)
        else:
            options[bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᎭ")] = bstack1l1l1ll1l_opy_
    else:
        if getattr(options, bstack1111_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭Ꭾ"), None):
            options.set_capability(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᎯ"), bstack111lll11l1_opy_(framework))
            options.set_capability(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᎰ"), bstack111ll1llll_opy_())
        else:
            options[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᎱ")] = bstack111lll11l1_opy_(framework)
            options[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᎲ")] = bstack111ll1llll_opy_()
    return options
def bstack111ll11l11_opy_(bstack111l11111l_opy_, framework):
    if bstack111l11111l_opy_ and len(bstack111l11111l_opy_.split(bstack1111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᎳ"))) > 1:
        ws_url = bstack111l11111l_opy_.split(bstack1111_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᎴ"))[0]
        if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᎵ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111ll1ll1_opy_ = json.loads(urllib.parse.unquote(bstack111l11111l_opy_.split(bstack1111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᎶ"))[1]))
            bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_ or {}
            bstack1111ll1ll1_opy_[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᎷ")] = str(framework) + str(__version__)
            bstack1111ll1ll1_opy_[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᎸ")] = bstack111ll1llll_opy_()
            bstack111l11111l_opy_ = bstack111l11111l_opy_.split(bstack1111_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᎹ"))[0] + bstack1111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᎺ") + urllib.parse.quote(json.dumps(bstack1111ll1ll1_opy_))
    return bstack111l11111l_opy_
def bstack1l11ll1l11_opy_():
    global bstack11l11l1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l11l1l1_opy_ = BrowserType.connect
    return bstack11l11l1l1_opy_
def bstack1ll1111l1l_opy_(framework_name):
    global bstack1l1l11ll1_opy_
    bstack1l1l11ll1_opy_ = framework_name
    return framework_name
def bstack1llllllll1_opy_(self, *args, **kwargs):
    global bstack11l11l1l1_opy_
    try:
        global bstack1l1l11ll1_opy_
        if bstack1111_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᎻ") in kwargs:
            kwargs[bstack1111_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᎼ")] = bstack111ll11l11_opy_(
                kwargs.get(bstack1111_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᎽ"), None),
                bstack1l1l11ll1_opy_
            )
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢᎾ").format(str(e)))
    return bstack11l11l1l1_opy_(self, *args, **kwargs)
def bstack111ll11ll1_opy_(bstack11l11111ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111l1ll1_opy_(bstack11l11111ll_opy_, bstack1111_opy_ (u"ࠣࠤᎿ"))
        if proxies and proxies.get(bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᏀ")):
            parsed_url = urlparse(proxies.get(bstack1111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᏁ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᏂ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᏃ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᏄ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᏅ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lllll11l1_opy_(bstack11l11111ll_opy_):
    bstack111l11llll_opy_ = {
        bstack11l11ll11l_opy_[bstack11l111111l_opy_]: bstack11l11111ll_opy_[bstack11l111111l_opy_]
        for bstack11l111111l_opy_ in bstack11l11111ll_opy_
        if bstack11l111111l_opy_ in bstack11l11ll11l_opy_
    }
    bstack111l11llll_opy_[bstack1111_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᏆ")] = bstack111ll11ll1_opy_(bstack11l11111ll_opy_, bstack1lll111l1l_opy_.get_property(bstack1111_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᏇ")))
    bstack1111lll1l1_opy_ = [element.lower() for element in bstack11l111l1ll_opy_]
    bstack11l1111lll_opy_(bstack111l11llll_opy_, bstack1111lll1l1_opy_)
    return bstack111l11llll_opy_
def bstack11l1111lll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1111_opy_ (u"ࠥ࠮࠯࠰ࠪࠣᏈ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1111lll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1111lll_opy_(item, keys)