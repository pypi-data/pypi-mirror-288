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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11llll_opy_, bstack1l11lll1l1_opy_, update, bstack1lllll1l11_opy_,
                                       bstack11llllll_opy_, bstack1l11l1ll11_opy_, bstack1l11111ll_opy_, bstack1l1111l11_opy_,
                                       bstack1l11ll111_opy_, bstack1ll11ll111_opy_, bstack1ll1111111_opy_, bstack1lll11llll_opy_,
                                       bstack1ll1lllll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11ll11l1_opy_)
from browserstack_sdk.bstack1l111ll1_opy_ import bstack111l11l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1lll1ll1l1_opy_
from bstack_utils.capture import bstack1l111111ll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1l11llll1_opy_, bstack111l1ll1l_opy_, bstack1l11l111l_opy_, \
    bstack1ll1l1lll_opy_
from bstack_utils.helper import bstack11l111ll1_opy_, bstack1111lll11l_opy_, bstack11lll11l1l_opy_, bstack1l1lll111l_opy_, bstack111ll1llll_opy_, bstack1ll1ll1l11_opy_, \
    bstack111llll111_opy_, \
    bstack111l1l1ll1_opy_, bstack11ll11111_opy_, bstack1l1l111ll1_opy_, bstack11l1111ll1_opy_, bstack1l1llllll1_opy_, Notset, \
    bstack111l1l11l_opy_, bstack111ll111ll_opy_, bstack111l1111l1_opy_, Result, bstack111l1l1l11_opy_, bstack111l1lllll_opy_, bstack1l111l1l1l_opy_, \
    bstack1111l1l11_opy_, bstack1l1l11lll1_opy_, bstack1lll1111l_opy_, bstack111l11l1l1_opy_
from bstack_utils.bstack1111l1l111_opy_ import bstack1111ll11l1_opy_
from bstack_utils.messages import bstack1l1l1ll11l_opy_, bstack1l111l11_opy_, bstack1111llll_opy_, bstack1ll11l11l_opy_, bstack1l1l1lll1_opy_, \
    bstack111l11ll1_opy_, bstack1l1l11lll_opy_, bstack11ll1l1l1_opy_, bstack1l111111l_opy_, bstack1lll1l1l1_opy_, \
    bstack1ll1ll11l_opy_, bstack1l1ll1lll_opy_
from bstack_utils.proxy import bstack1lll11l1ll_opy_, bstack1111l1ll1_opy_
from bstack_utils.bstack1l11111l_opy_ import bstack1lll1llll1l_opy_, bstack1llll1111ll_opy_, bstack1llll11l111_opy_, bstack1llll11111l_opy_, \
    bstack1lll1llllll_opy_, bstack1llll1111l1_opy_, bstack1llll111ll1_opy_, bstack1l11l111l1_opy_, bstack1llll111l1l_opy_
from bstack_utils.bstack1l11l11l11_opy_ import bstack111ll1l1_opy_
from bstack_utils.bstack1lllll11l_opy_ import bstack111l1l11_opy_, bstack1lllll1ll_opy_, bstack11ll111l_opy_, \
    bstack1l111lll11_opy_, bstack1l111l1ll_opy_
from bstack_utils.bstack11llll1ll1_opy_ import bstack11ll1lll1l_opy_
from bstack_utils.bstack1l1l111l11_opy_ import bstack11l1ll1ll_opy_
import bstack_utils.bstack1l11l1l1ll_opy_ as bstack1ll11lll11_opy_
from bstack_utils.bstack11ll1l11_opy_ import bstack11ll1l11_opy_
bstack1lll11lll_opy_ = None
bstack11l11lll1_opy_ = None
bstack1l1l1ll111_opy_ = None
bstack1l1lllll1_opy_ = None
bstack1ll11l1l11_opy_ = None
bstack1l1111111_opy_ = None
bstack11l1l1lll_opy_ = None
bstack111lll1l_opy_ = None
bstack1llllllll_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1l1lll1l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1l11lllll1_opy_ = None
bstack1l1l11ll1_opy_ = bstack1111_opy_ (u"ࠫࠬᙾ")
CONFIG = {}
bstack11l11l1l_opy_ = False
bstack1l1ll11l11_opy_ = bstack1111_opy_ (u"ࠬ࠭ᙿ")
bstack1l1l1ll1ll_opy_ = bstack1111_opy_ (u"࠭ࠧ ")
bstack1ll1ll1l1l_opy_ = False
bstack1lll11lll1_opy_ = []
bstack1l1lll1ll1_opy_ = bstack1l11llll1_opy_
bstack1ll1llll11l_opy_ = bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᚁ")
bstack1ll1lllllll_opy_ = False
bstack1l1ll11l1l_opy_ = {}
bstack11111111l_opy_ = False
logger = bstack1lll1ll1l1_opy_.get_logger(__name__, bstack1l1lll1ll1_opy_)
store = {
    bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᚂ"): []
}
bstack1ll1ll1lll1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1111llll_opy_ = {}
current_test_uuid = None
def bstack1lll11l1l_opy_(page, bstack11ll1llll_opy_):
    try:
        page.evaluate(bstack1111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᚃ"),
                      bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧᚄ") + json.dumps(
                          bstack11ll1llll_opy_) + bstack1111_opy_ (u"ࠦࢂࢃࠢᚅ"))
    except Exception as e:
        print(bstack1111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥᚆ"), e)
def bstack1111l1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1111_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᚇ"), bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬᚈ") + json.dumps(
            message) + bstack1111_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫᚉ") + json.dumps(level) + bstack1111_opy_ (u"ࠩࢀࢁࠬᚊ"))
    except Exception as e:
        print(bstack1111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨᚋ"), e)
def pytest_configure(config):
    bstack1lll111l1l_opy_ = Config.bstack11lll1111_opy_()
    config.args = bstack11l1ll1ll_opy_.bstack1lll111l1ll_opy_(config.args)
    bstack1lll111l1l_opy_.bstack1ll1l11l_opy_(bstack1lll1111l_opy_(config.getoption(bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᚌ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll1ll1l1l1_opy_ = item.config.getoption(bstack1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᚍ"))
    plugins = item.config.getoption(bstack1111_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢᚎ"))
    report = outcome.get_result()
    bstack1ll1lll1ll1_opy_(item, call, report)
    if bstack1111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧᚏ") not in plugins or bstack1l1llllll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤᚐ"), None)
    page = getattr(item, bstack1111_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣᚑ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll1llllll1_opy_(item, report, summary, bstack1ll1ll1l1l1_opy_)
    if (page is not None):
        bstack1ll1lll1111_opy_(item, report, summary, bstack1ll1ll1l1l1_opy_)
def bstack1ll1llllll1_opy_(item, report, summary, bstack1ll1ll1l1l1_opy_):
    if report.when == bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚒ") and report.skipped:
        bstack1llll111l1l_opy_(report)
    if report.when in [bstack1111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᚓ"), bstack1111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᚔ")]:
        return
    if not bstack111ll1llll_opy_():
        return
    try:
        if (str(bstack1ll1ll1l1l1_opy_).lower() != bstack1111_opy_ (u"࠭ࡴࡳࡷࡨࠫᚕ")):
            item._driver.execute_script(
                bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬᚖ") + json.dumps(
                    report.nodeid) + bstack1111_opy_ (u"ࠨࡿࢀࠫᚗ"))
        os.environ[bstack1111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᚘ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1111_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥᚙ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᚚ")))
    bstack11ll1lll1_opy_ = bstack1111_opy_ (u"ࠧࠨ᚛")
    bstack1llll111l1l_opy_(report)
    if not passed:
        try:
            bstack11ll1lll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ᚜").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll1lll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ᚝")))
        bstack11ll1lll1_opy_ = bstack1111_opy_ (u"ࠣࠤ᚞")
        if not passed:
            try:
                bstack11ll1lll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ᚟").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll1lll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᚠ")
                    + json.dumps(bstack1111_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧᚡ"))
                    + bstack1111_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᚢ")
                )
            else:
                item._driver.execute_script(
                    bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᚣ")
                    + json.dumps(str(bstack11ll1lll1_opy_))
                    + bstack1111_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᚤ")
                )
        except Exception as e:
            summary.append(bstack1111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨᚥ").format(e))
def bstack1ll1ll1llll_opy_(test_name, error_message):
    try:
        bstack1ll1ll11111_opy_ = []
        bstack1l1ll1l11_opy_ = os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᚦ"), bstack1111_opy_ (u"ࠪ࠴ࠬᚧ"))
        bstack1ll1l1ll1l_opy_ = {bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᚨ"): test_name, bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᚩ"): error_message, bstack1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᚪ"): bstack1l1ll1l11_opy_}
        bstack1ll1ll11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᚫ"))
        if os.path.exists(bstack1ll1ll11lll_opy_):
            with open(bstack1ll1ll11lll_opy_) as f:
                bstack1ll1ll11111_opy_ = json.load(f)
        bstack1ll1ll11111_opy_.append(bstack1ll1l1ll1l_opy_)
        with open(bstack1ll1ll11lll_opy_, bstack1111_opy_ (u"ࠨࡹࠪᚬ")) as f:
            json.dump(bstack1ll1ll11111_opy_, f)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧᚭ") + str(e))
def bstack1ll1lll1111_opy_(item, report, summary, bstack1ll1ll1l1l1_opy_):
    if report.when in [bstack1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᚮ"), bstack1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᚯ")]:
        return
    if (str(bstack1ll1ll1l1l1_opy_).lower() != bstack1111_opy_ (u"ࠬࡺࡲࡶࡧࠪᚰ")):
        bstack1lll11l1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᚱ")))
    bstack11ll1lll1_opy_ = bstack1111_opy_ (u"ࠢࠣᚲ")
    bstack1llll111l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11ll1lll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᚳ").format(e)
                )
        try:
            if passed:
                bstack1l111l1ll_opy_(getattr(item, bstack1111_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᚴ"), None), bstack1111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᚵ"))
            else:
                error_message = bstack1111_opy_ (u"ࠫࠬᚶ")
                if bstack11ll1lll1_opy_:
                    bstack1111l1l1_opy_(item._page, str(bstack11ll1lll1_opy_), bstack1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᚷ"))
                    bstack1l111l1ll_opy_(getattr(item, bstack1111_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᚸ"), None), bstack1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᚹ"), str(bstack11ll1lll1_opy_))
                    error_message = str(bstack11ll1lll1_opy_)
                else:
                    bstack1l111l1ll_opy_(getattr(item, bstack1111_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᚺ"), None), bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᚻ"))
                bstack1ll1ll1llll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1111_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢᚼ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1111_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᚽ"), default=bstack1111_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᚾ"), help=bstack1111_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᚿ"))
    parser.addoption(bstack1111_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᛀ"), default=bstack1111_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᛁ"), help=bstack1111_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᛂ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧᛃ"), action=bstack1111_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥᛄ"), default=bstack1111_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧᛅ"),
                         help=bstack1111_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧᛆ"))
def bstack1l11111111_opy_(log):
    if not (log[bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛇ")] and log[bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᛈ")].strip()):
        return
    active = bstack1l1111111l_opy_()
    log = {
        bstack1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᛉ"): log[bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᛊ")],
        bstack1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᛋ"): bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"ࠬࡠࠧᛌ"),
        bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᛍ"): log[bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛎ")],
    }
    if active:
        if active[bstack1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᛏ")] == bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᛐ"):
            log[bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛑ")] = active[bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᛒ")]
        elif active[bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪᛓ")] == bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࠫᛔ"):
            log[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᛕ")] = active[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛖ")]
    bstack11l1ll1ll_opy_.bstack1ll11ll1_opy_([log])
def bstack1l1111111l_opy_():
    if len(store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᛗ")]) > 0 and store[bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᛘ")][-1]:
        return {
            bstack1111_opy_ (u"ࠫࡹࡿࡰࡦࠩᛙ"): bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᛚ"),
            bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᛛ"): store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᛜ")][-1]
        }
    if store.get(bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᛝ"), None):
        return {
            bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᛞ"): bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨᛟ"),
            bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᛠ"): store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᛡ")]
        }
    return None
bstack1l111l11ll_opy_ = bstack1l111111ll_opy_(bstack1l11111111_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll1lllllll_opy_
        item._1ll1lll11ll_opy_ = True
        bstack11l1lll1_opy_ = bstack1ll11lll11_opy_.bstack1l111llll_opy_(CONFIG, bstack111l1l1ll1_opy_(item.own_markers))
        item._a11y_test_case = bstack11l1lll1_opy_
        if bstack1ll1lllllll_opy_:
            driver = getattr(item, bstack1111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᛢ"), None)
            item._a11y_started = bstack1ll11lll11_opy_.bstack1ll11ll1l1_opy_(driver, bstack11l1lll1_opy_)
        if not bstack11l1ll1ll_opy_.on() or bstack1ll1llll11l_opy_ != bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᛣ"):
            return
        global current_test_uuid, bstack1l111l11ll_opy_
        bstack1l111l11ll_opy_.start()
        bstack11ll1ll111_opy_ = {
            bstack1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᛤ"): uuid4().__str__(),
            bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᛥ"): bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"ࠪ࡞ࠬᛦ")
        }
        current_test_uuid = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩᛧ")]
        store[bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᛨ")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛩ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1111llll_opy_[item.nodeid] = {**_1l1111llll_opy_[item.nodeid], **bstack11ll1ll111_opy_}
        bstack1ll1llll1l1_opy_(item, _1l1111llll_opy_[item.nodeid], bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᛪ"))
    except Exception as err:
        print(bstack1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ᛫"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll1ll1lll1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1111ll1_opy_():
        atexit.register(bstack1ll1ll1ll_opy_)
        if not bstack1ll1ll1lll1_opy_:
            try:
                bstack1ll1ll11l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l11l1l1_opy_():
                    bstack1ll1ll11l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1ll11l1l_opy_:
                    signal.signal(s, bstack1ll1l1lllll_opy_)
                bstack1ll1ll1lll1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ᛬") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll1llll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᛭")
    try:
        if not bstack11l1ll1ll_opy_.on():
            return
        bstack1l111l11ll_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll1ll111_opy_ = {
            bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩᛮ"): uuid,
            bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᛯ"): bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"࡚࠭ࠨᛰ"),
            bstack1111_opy_ (u"ࠧࡵࡻࡳࡩࠬᛱ"): bstack1111_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᛲ"),
            bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᛳ"): bstack1111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᛴ"),
            bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᛵ"): bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᛶ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᛷ")] = item
        store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᛸ")] = [uuid]
        if not _1l1111llll_opy_.get(item.nodeid, None):
            _1l1111llll_opy_[item.nodeid] = {bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᛹"): [], bstack1111_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ᛺"): []}
        _1l1111llll_opy_[item.nodeid][bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᛻")].append(bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩ᛼")])
        _1l1111llll_opy_[item.nodeid + bstack1111_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ᛽")] = bstack11ll1ll111_opy_
        bstack1ll1ll1l11l_opy_(item, bstack11ll1ll111_opy_, bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ᛾"))
    except Exception as err:
        print(bstack1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ᛿"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1ll11l1l_opy_
        if CONFIG.get(bstack1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᜀ"), False):
            if CONFIG.get(bstack1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᜁ"), bstack1111_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᜂ")) == bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᜃ"):
                bstack1ll1l1lll1l_opy_ = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᜄ"), None)
                bstack1lll1ll111_opy_ = bstack1ll1l1lll1l_opy_ + bstack1111_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᜅ")
                driver = getattr(item, bstack1111_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᜆ"), None)
                PercySDK.screenshot(driver, bstack1lll1ll111_opy_)
        if getattr(item, bstack1111_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᜇ"), False):
            bstack111l11l1_opy_.bstack1l1l1111l1_opy_(getattr(item, bstack1111_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᜈ"), None), bstack1l1ll11l1l_opy_, logger, item)
        if not bstack11l1ll1ll_opy_.on():
            return
        bstack11ll1ll111_opy_ = {
            bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᜉ"): uuid4().__str__(),
            bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᜊ"): bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"ࠬࡠࠧᜋ"),
            bstack1111_opy_ (u"࠭ࡴࡺࡲࡨࠫᜌ"): bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᜍ"),
            bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᜎ"): bstack1111_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᜏ"),
            bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᜐ"): bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᜑ")
        }
        _1l1111llll_opy_[item.nodeid + bstack1111_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᜒ")] = bstack11ll1ll111_opy_
        bstack1ll1ll1l11l_opy_(item, bstack11ll1ll111_opy_, bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᜓ"))
    except Exception as err:
        print(bstack1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ᜔࠭"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack11l1ll1ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llll11111l_opy_(fixturedef.argname):
        store[bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳ᜕ࠧ")] = request.node
    elif bstack1lll1llllll_opy_(fixturedef.argname):
        store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ᜖")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ᜗"): fixturedef.argname,
            bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᜘"): bstack111llll111_opy_(outcome),
            bstack1111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ᜙"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᜚")]
        if not _1l1111llll_opy_.get(current_test_item.nodeid, None):
            _1l1111llll_opy_[current_test_item.nodeid] = {bstack1111_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ᜛"): []}
        _1l1111llll_opy_[current_test_item.nodeid][bstack1111_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ᜜")].append(fixture)
    except Exception as err:
        logger.debug(bstack1111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ᜝"), str(err))
if bstack1l1llllll1_opy_() and bstack11l1ll1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1111llll_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭᜞")].bstack1lll11l1l1l_opy_(id(step))
        except Exception as err:
            print(bstack1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩᜟ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1111llll_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᜠ")].bstack1l1111l111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᜡ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11llll1ll1_opy_: bstack11ll1lll1l_opy_ = _1l1111llll_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᜢ")]
            bstack11llll1ll1_opy_.bstack1l1111l111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᜣ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1llll11l_opy_
        try:
            if not bstack11l1ll1ll_opy_.on() or bstack1ll1llll11l_opy_ != bstack1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᜤ"):
                return
            global bstack1l111l11ll_opy_
            bstack1l111l11ll_opy_.start()
            driver = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᜥ"), None)
            if not _1l1111llll_opy_.get(request.node.nodeid, None):
                _1l1111llll_opy_[request.node.nodeid] = {}
            bstack11llll1ll1_opy_ = bstack11ll1lll1l_opy_.bstack1lll1l11ll1_opy_(
                scenario, feature, request.node,
                name=bstack1llll1111l1_opy_(request.node, scenario),
                bstack1l111l111l_opy_=bstack1ll1ll1l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1111_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᜦ"),
                tags=bstack1llll111ll1_opy_(feature, scenario),
                bstack11lll111ll_opy_=bstack11l1ll1ll_opy_.bstack11lll1ll1l_opy_(driver) if driver and driver.session_id else {}
            )
            _1l1111llll_opy_[request.node.nodeid][bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᜧ")] = bstack11llll1ll1_opy_
            bstack1ll1ll1l1ll_opy_(bstack11llll1ll1_opy_.uuid)
            bstack11l1ll1ll_opy_.bstack11llll11l1_opy_(bstack1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᜨ"), bstack11llll1ll1_opy_)
        except Exception as err:
            print(bstack1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩᜩ"), str(err))
def bstack1ll1ll1ll11_opy_(bstack1ll1ll111ll_opy_):
    if bstack1ll1ll111ll_opy_ in store[bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᜪ")]:
        store[bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᜫ")].remove(bstack1ll1ll111ll_opy_)
def bstack1ll1ll1l1ll_opy_(bstack1ll1lll1lll_opy_):
    store[bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᜬ")] = bstack1ll1lll1lll_opy_
    threading.current_thread().current_test_uuid = bstack1ll1lll1lll_opy_
@bstack11l1ll1ll_opy_.bstack1lll11l1l11_opy_
def bstack1ll1lll1ll1_opy_(item, call, report):
    global bstack1ll1llll11l_opy_
    bstack11lll1ll1_opy_ = bstack1ll1ll1l11_opy_()
    if hasattr(report, bstack1111_opy_ (u"ࠫࡸࡺ࡯ࡱࠩᜭ")):
        bstack11lll1ll1_opy_ = bstack111l1l1l11_opy_(report.stop)
    elif hasattr(report, bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᜮ")):
        bstack11lll1ll1_opy_ = bstack111l1l1l11_opy_(report.start)
    try:
        if getattr(report, bstack1111_opy_ (u"࠭ࡷࡩࡧࡱࠫᜯ"), bstack1111_opy_ (u"ࠧࠨᜰ")) == bstack1111_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᜱ"):
            bstack1l111l11ll_opy_.reset()
        if getattr(report, bstack1111_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᜲ"), bstack1111_opy_ (u"ࠪࠫᜳ")) == bstack1111_opy_ (u"ࠫࡨࡧ࡬࡭᜴ࠩ"):
            if bstack1ll1llll11l_opy_ == bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᜵"):
                _1l1111llll_opy_[item.nodeid][bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᜶")] = bstack11lll1ll1_opy_
                bstack1ll1llll1l1_opy_(item, _1l1111llll_opy_[item.nodeid], bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ᜷"), report, call)
                store[bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ᜸")] = None
            elif bstack1ll1llll11l_opy_ == bstack1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ᜹"):
                bstack11llll1ll1_opy_ = _1l1111llll_opy_[item.nodeid][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭᜺")]
                bstack11llll1ll1_opy_.set(hooks=_1l1111llll_opy_[item.nodeid].get(bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᜻"), []))
                exception, bstack11lll11ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll11ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1111_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫ᜼"), bstack1111_opy_ (u"࠭ࠧ᜽"))]
                bstack11llll1ll1_opy_.stop(time=bstack11lll1ll1_opy_, result=Result(result=getattr(report, bstack1111_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ᜾"), bstack1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᜿")), exception=exception, bstack11lll11ll1_opy_=bstack11lll11ll1_opy_))
                bstack11l1ll1ll_opy_.bstack11llll11l1_opy_(bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᝀ"), _1l1111llll_opy_[item.nodeid][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᝁ")])
        elif getattr(report, bstack1111_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᝂ"), bstack1111_opy_ (u"ࠬ࠭ᝃ")) in [bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᝄ"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᝅ")]:
            bstack11lllllll1_opy_ = item.nodeid + bstack1111_opy_ (u"ࠨ࠯ࠪᝆ") + getattr(report, bstack1111_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᝇ"), bstack1111_opy_ (u"ࠪࠫᝈ"))
            if getattr(report, bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᝉ"), False):
                hook_type = bstack1111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᝊ") if getattr(report, bstack1111_opy_ (u"࠭ࡷࡩࡧࡱࠫᝋ"), bstack1111_opy_ (u"ࠧࠨᝌ")) == bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᝍ") else bstack1111_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᝎ")
                _1l1111llll_opy_[bstack11lllllll1_opy_] = {
                    bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᝏ"): uuid4().__str__(),
                    bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᝐ"): bstack11lll1ll1_opy_,
                    bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᝑ"): hook_type
                }
            _1l1111llll_opy_[bstack11lllllll1_opy_][bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᝒ")] = bstack11lll1ll1_opy_
            bstack1ll1ll1ll11_opy_(_1l1111llll_opy_[bstack11lllllll1_opy_][bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᝓ")])
            bstack1ll1ll1l11l_opy_(item, _1l1111llll_opy_[bstack11lllllll1_opy_], bstack1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᝔"), report, call)
            if getattr(report, bstack1111_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ᝕"), bstack1111_opy_ (u"ࠪࠫ᝖")) == bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ᝗"):
                if getattr(report, bstack1111_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭᝘"), bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᝙")) == bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᝚"):
                    bstack11ll1ll111_opy_ = {
                        bstack1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᝛"): uuid4().__str__(),
                        bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᝜"): bstack1ll1ll1l11_opy_(),
                        bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᝝"): bstack1ll1ll1l11_opy_()
                    }
                    _1l1111llll_opy_[item.nodeid] = {**_1l1111llll_opy_[item.nodeid], **bstack11ll1ll111_opy_}
                    bstack1ll1llll1l1_opy_(item, _1l1111llll_opy_[item.nodeid], bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ᝞"))
                    bstack1ll1llll1l1_opy_(item, _1l1111llll_opy_[item.nodeid], bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᝟"), report, call)
    except Exception as err:
        print(bstack1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᝠ"), str(err))
def bstack1ll1l1llll1_opy_(test, bstack11ll1ll111_opy_, result=None, call=None, bstack111ll11l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11llll1ll1_opy_ = {
        bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᝡ"): bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᝢ")],
        bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᝣ"): bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨᝤ"),
        bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᝥ"): test.name,
        bstack1111_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᝦ"): {
            bstack1111_opy_ (u"࠭࡬ࡢࡰࡪࠫᝧ"): bstack1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᝨ"),
            bstack1111_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᝩ"): inspect.getsource(test.obj)
        },
        bstack1111_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᝪ"): test.name,
        bstack1111_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᝫ"): test.name,
        bstack1111_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᝬ"): bstack11l1ll1ll_opy_.bstack11lll111l1_opy_(test),
        bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ᝭"): file_path,
        bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᝮ"): file_path,
        bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᝯ"): bstack1111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᝰ"),
        bstack1111_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ᝱"): file_path,
        bstack1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᝲ"): bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᝳ")],
        bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᝴"): bstack1111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭᝵"),
        bstack1111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ᝶"): {
            bstack1111_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ᝷"): test.nodeid
        },
        bstack1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ᝸"): bstack111l1l1ll1_opy_(test.own_markers)
    }
    if bstack111ll11l1_opy_ in [bstack1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ᝹"), bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭᝺")]:
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠬࡳࡥࡵࡣࠪ᝻")] = {
            bstack1111_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ᝼"): bstack11ll1ll111_opy_.get(bstack1111_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ᝽"), [])
        }
    if bstack111ll11l1_opy_ == bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ᝾"):
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᝿")] = bstack1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫក")
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪខ")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫគ")]
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫឃ")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬង")]
    if result:
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨច")] = result.outcome
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪឆ")] = result.duration * 1000
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨជ")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩឈ")]
        if result.failed:
            bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫញ")] = bstack11l1ll1ll_opy_.bstack11ll111l11_opy_(call.excinfo.typename)
            bstack11llll1ll1_opy_[bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧដ")] = bstack11l1ll1ll_opy_.bstack1lll11111ll_opy_(call.excinfo, result)
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ឋ")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧឌ")]
    if outcome:
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩឍ")] = bstack111llll111_opy_(outcome)
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫណ")] = 0
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩត")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪថ")]
        if bstack11llll1ll1_opy_[bstack1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ទ")] == bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧធ"):
            bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧន")] = bstack1111_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪប")  # bstack1ll1ll11ll1_opy_
            bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫផ")] = [{bstack1111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧព"): [bstack1111_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩភ")]}]
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬម")] = bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭យ")]
    return bstack11llll1ll1_opy_
def bstack1ll1lllll1l_opy_(test, bstack11lll1lll1_opy_, bstack111ll11l1_opy_, result, call, outcome, bstack1ll1lll11l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫរ")]
    hook_name = bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬល")]
    hook_data = {
        bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨវ"): bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩឝ")],
        bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪឞ"): bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫស"),
        bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬហ"): bstack1111_opy_ (u"ࠨࡽࢀࠫឡ").format(bstack1llll1111ll_opy_(hook_name)),
        bstack1111_opy_ (u"ࠩࡥࡳࡩࡿࠧអ"): {
            bstack1111_opy_ (u"ࠪࡰࡦࡴࡧࠨឣ"): bstack1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫឤ"),
            bstack1111_opy_ (u"ࠬࡩ࡯ࡥࡧࠪឥ"): None
        },
        bstack1111_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬឦ"): test.name,
        bstack1111_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧឧ"): bstack11l1ll1ll_opy_.bstack11lll111l1_opy_(test, hook_name),
        bstack1111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫឨ"): file_path,
        bstack1111_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫឩ"): file_path,
        bstack1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪឪ"): bstack1111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬឫ"),
        bstack1111_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪឬ"): file_path,
        bstack1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪឭ"): bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫឮ")],
        bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫឯ"): bstack1111_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫឰ") if bstack1ll1llll11l_opy_ == bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧឱ") else bstack1111_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫឲ"),
        bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨឳ"): hook_type
    }
    bstack1ll1lll111l_opy_ = bstack1l111l1ll1_opy_(_1l1111llll_opy_.get(test.nodeid, None))
    if bstack1ll1lll111l_opy_:
        hook_data[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ឴")] = bstack1ll1lll111l_opy_
    if result:
        hook_data[bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ឵")] = result.outcome
        hook_data[bstack1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩា")] = result.duration * 1000
        hook_data[bstack1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧិ")] = bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨី")]
        if result.failed:
            hook_data[bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪឹ")] = bstack11l1ll1ll_opy_.bstack11ll111l11_opy_(call.excinfo.typename)
            hook_data[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ឺ")] = bstack11l1ll1ll_opy_.bstack1lll11111ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ុ")] = bstack111llll111_opy_(outcome)
        hook_data[bstack1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨូ")] = 100
        hook_data[bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ួ")] = bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧើ")]
        if hook_data[bstack1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪឿ")] == bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫៀ"):
            hook_data[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫេ")] = bstack1111_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧែ")  # bstack1ll1ll11ll1_opy_
            hook_data[bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨៃ")] = [{bstack1111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫោ"): [bstack1111_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ៅ")]}]
    if bstack1ll1lll11l1_opy_:
        hook_data[bstack1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪំ")] = bstack1ll1lll11l1_opy_.result
        hook_data[bstack1111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬះ")] = bstack111ll111ll_opy_(bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩៈ")], bstack11lll1lll1_opy_[bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ៉")])
        hook_data[bstack1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ៊")] = bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭់")]
        if hook_data[bstack1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ៌")] == bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ៍"):
            hook_data[bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ៎")] = bstack11l1ll1ll_opy_.bstack11ll111l11_opy_(bstack1ll1lll11l1_opy_.exception_type)
            hook_data[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭៏")] = [{bstack1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ័"): bstack111l1111l1_opy_(bstack1ll1lll11l1_opy_.exception)}]
    return hook_data
def bstack1ll1llll1l1_opy_(test, bstack11ll1ll111_opy_, bstack111ll11l1_opy_, result=None, call=None, outcome=None):
    bstack11llll1ll1_opy_ = bstack1ll1l1llll1_opy_(test, bstack11ll1ll111_opy_, result, call, bstack111ll11l1_opy_, outcome)
    driver = getattr(test, bstack1111_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ៑"), None)
    if bstack111ll11l1_opy_ == bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥ្ࠩ") and driver:
        bstack11llll1ll1_opy_[bstack1111_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ៓")] = bstack11l1ll1ll_opy_.bstack11lll1ll1l_opy_(driver)
    if bstack111ll11l1_opy_ == bstack1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ។"):
        bstack111ll11l1_opy_ = bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭៕")
    bstack11lll1l1l1_opy_ = {
        bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ៖"): bstack111ll11l1_opy_,
        bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨៗ"): bstack11llll1ll1_opy_
    }
    bstack11l1ll1ll_opy_.bstack11ll1ll1l1_opy_(bstack11lll1l1l1_opy_)
def bstack1ll1ll1l11l_opy_(test, bstack11ll1ll111_opy_, bstack111ll11l1_opy_, result=None, call=None, outcome=None, bstack1ll1lll11l1_opy_=None):
    hook_data = bstack1ll1lllll1l_opy_(test, bstack11ll1ll111_opy_, bstack111ll11l1_opy_, result, call, outcome, bstack1ll1lll11l1_opy_)
    bstack11lll1l1l1_opy_ = {
        bstack1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ៘"): bstack111ll11l1_opy_,
        bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ៙"): hook_data
    }
    bstack11l1ll1ll_opy_.bstack11ll1ll1l1_opy_(bstack11lll1l1l1_opy_)
def bstack1l111l1ll1_opy_(bstack11ll1ll111_opy_):
    if not bstack11ll1ll111_opy_:
        return None
    if bstack11ll1ll111_opy_.get(bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ៚"), None):
        return getattr(bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭៛")], bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩៜ"), None)
    return bstack11ll1ll111_opy_.get(bstack1111_opy_ (u"ࠬࡻࡵࡪࡦࠪ៝"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack11l1ll1ll_opy_.on():
            return
        places = [bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ៞"), bstack1111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ៟"), bstack1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ០")]
        bstack11lll1l1ll_opy_ = []
        for bstack1ll1lll1l11_opy_ in places:
            records = caplog.get_records(bstack1ll1lll1l11_opy_)
            bstack1ll1ll111l1_opy_ = bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ១") if bstack1ll1lll1l11_opy_ == bstack1111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ២") else bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៣")
            bstack1ll1ll1l111_opy_ = request.node.nodeid + (bstack1111_opy_ (u"ࠬ࠭៤") if bstack1ll1lll1l11_opy_ == bstack1111_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ៥") else bstack1111_opy_ (u"ࠧ࠮ࠩ៦") + bstack1ll1lll1l11_opy_)
            bstack1ll1lll1lll_opy_ = bstack1l111l1ll1_opy_(_1l1111llll_opy_.get(bstack1ll1ll1l111_opy_, None))
            if not bstack1ll1lll1lll_opy_:
                continue
            for record in records:
                if bstack111l1lllll_opy_(record.message):
                    continue
                bstack11lll1l1ll_opy_.append({
                    bstack1111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ៧"): bstack1111lll11l_opy_(record.created).isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫ៨"),
                    bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៩"): record.levelname,
                    bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ៪"): record.message,
                    bstack1ll1ll111l1_opy_: bstack1ll1lll1lll_opy_
                })
        if len(bstack11lll1l1ll_opy_) > 0:
            bstack11l1ll1ll_opy_.bstack1ll11ll1_opy_(bstack11lll1l1ll_opy_)
    except Exception as err:
        print(bstack1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ៫"), str(err))
def bstack11ll1l11l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11111111l_opy_
    bstack1l1l1l11l1_opy_ = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ៬"), None) and bstack11l111ll1_opy_(
            threading.current_thread(), bstack1111_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭៭"), None)
    bstack1ll1l1111_opy_ = getattr(driver, bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ៮"), None) != None and getattr(driver, bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ៯"), None) == True
    if sequence == bstack1111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ៰") and driver != None:
      if not bstack11111111l_opy_ and bstack111ll1llll_opy_() and bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៱") in CONFIG and CONFIG[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ៲")] == True and bstack11ll1l11_opy_.bstack1ll111l1l_opy_(driver_command) and (bstack1ll1l1111_opy_ or bstack1l1l1l11l1_opy_) and not bstack1l11ll11l1_opy_(args):
        try:
          bstack11111111l_opy_ = True
          logger.debug(bstack1111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ៳").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ៴").format(str(err)))
        bstack11111111l_opy_ = False
    if sequence == bstack1111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ៵"):
        if driver_command == bstack1111_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭៶"):
            bstack11l1ll1ll_opy_.bstack11ll11l11_opy_({
                bstack1111_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ៷"): response[bstack1111_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ៸")],
                bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ៹"): store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ៺")]
            })
def bstack1ll1ll1ll_opy_():
    global bstack1lll11lll1_opy_
    bstack1lll1ll1l1_opy_.bstack111111111_opy_()
    logging.shutdown()
    bstack11l1ll1ll_opy_.bstack11lllll11l_opy_()
    for driver in bstack1lll11lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l1lllll_opy_(*args):
    global bstack1lll11lll1_opy_
    bstack11l1ll1ll_opy_.bstack11lllll11l_opy_()
    for driver in bstack1lll11lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l111lll_opy_(self, *args, **kwargs):
    bstack1l1l1l1ll_opy_ = bstack1lll11lll_opy_(self, *args, **kwargs)
    if not bstack11l1ll1ll_opy_.on():
        return bstack1l1l1l1ll_opy_
    bstack11l1ll1ll_opy_.bstack1ll11111l1_opy_(self)
    return bstack1l1l1l1ll_opy_
def bstack1lllll1l1_opy_(framework_name):
    global bstack1l1l11ll1_opy_
    global bstack111ll1lll_opy_
    bstack1l1l11ll1_opy_ = framework_name
    logger.info(bstack1l1ll1lll_opy_.format(bstack1l1l11ll1_opy_.split(bstack1111_opy_ (u"ࠧ࠮ࠩ៻"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111ll1llll_opy_():
            Service.start = bstack1l11111ll_opy_
            Service.stop = bstack1l1111l11_opy_
            webdriver.Remote.__init__ = bstack1l11l11111_opy_
            webdriver.Remote.get = bstack1l11ll1l1l_opy_
            if not isinstance(os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ៼")), str):
                return
            WebDriver.close = bstack1l11ll111_opy_
            WebDriver.quit = bstack11l11l11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111ll1llll_opy_():
            webdriver.Remote.__init__ = bstack11l111lll_opy_
        bstack111ll1lll_opy_ = True
    except Exception as e:
        pass
    bstack11l111111_opy_()
    if os.environ.get(bstack1111_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ៽")):
        bstack111ll1lll_opy_ = eval(os.environ.get(bstack1111_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ៾")))
    if not bstack111ll1lll_opy_:
        bstack1ll1111111_opy_(bstack1111_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ៿"), bstack1ll1ll11l_opy_)
    if bstack1lll11ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1ll1llllll_opy_
        except Exception as e:
            logger.error(bstack111l11ll1_opy_.format(str(e)))
    if bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᠀") in str(framework_name).lower():
        if not bstack111ll1llll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11llllll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11l1ll11_opy_
            Config.getoption = bstack11lll1lll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll111111l_opy_
        except Exception as e:
            pass
def bstack11l11l11_opy_(self):
    global bstack1l1l11ll1_opy_
    global bstack11l11ll11_opy_
    global bstack11l11lll1_opy_
    try:
        if bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᠁") in bstack1l1l11ll1_opy_ and self.session_id != None and bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ᠂"), bstack1111_opy_ (u"ࠨࠩ᠃")) != bstack1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ᠄"):
            bstack1lll1l1l_opy_ = bstack1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᠅") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᠆")
            bstack1l1l11lll1_opy_(logger, True)
            if self != None:
                bstack1l111lll11_opy_(self, bstack1lll1l1l_opy_, bstack1111_opy_ (u"ࠬ࠲ࠠࠨ᠇").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᠈"), None)
        if item is not None and bstack1ll1lllllll_opy_:
            bstack111l11l1_opy_.bstack1l1l1111l1_opy_(self, bstack1l1ll11l1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1111_opy_ (u"ࠧࠨ᠉")
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ᠊") + str(e))
    bstack11l11lll1_opy_(self)
    self.session_id = None
def bstack1l11l11111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l11ll11_opy_
    global bstack1lll1111l1_opy_
    global bstack1ll1ll1l1l_opy_
    global bstack1l1l11ll1_opy_
    global bstack1lll11lll_opy_
    global bstack1lll11lll1_opy_
    global bstack1l1ll11l11_opy_
    global bstack1l1l1ll1ll_opy_
    global bstack1ll1lllllll_opy_
    global bstack1l1ll11l1l_opy_
    CONFIG[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᠋")] = str(bstack1l1l11ll1_opy_) + str(__version__)
    command_executor = bstack1l1l111ll1_opy_(bstack1l1ll11l11_opy_)
    logger.debug(bstack1ll11l11l_opy_.format(command_executor))
    proxy = bstack1ll1lllll1_opy_(CONFIG, proxy)
    bstack1l1ll1l11_opy_ = 0
    try:
        if bstack1ll1ll1l1l_opy_ is True:
            bstack1l1ll1l11_opy_ = int(os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᠌")))
    except:
        bstack1l1ll1l11_opy_ = 0
    bstack1lll1lll11_opy_ = bstack1l11llll_opy_(CONFIG, bstack1l1ll1l11_opy_)
    logger.debug(bstack11ll1l1l1_opy_.format(str(bstack1lll1lll11_opy_)))
    bstack1l1ll11l1l_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᠍"))[bstack1l1ll1l11_opy_]
    if bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ᠎") in CONFIG and CONFIG[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ᠏")]:
        bstack11ll111l_opy_(bstack1lll1lll11_opy_, bstack1l1l1ll1ll_opy_)
    if bstack1ll11lll11_opy_.bstack1ll1lll111_opy_(CONFIG, bstack1l1ll1l11_opy_) and bstack1ll11lll11_opy_.bstack1l111llll1_opy_(bstack1lll1lll11_opy_, options, desired_capabilities):
        bstack1ll1lllllll_opy_ = True
        bstack1ll11lll11_opy_.set_capabilities(bstack1lll1lll11_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1llll111_opy_ = bstack1l11lll1l1_opy_(desired_capabilities)
        bstack1l1llll111_opy_[bstack1111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ᠐")] = bstack111l1l11l_opy_(CONFIG)
        bstack11l1lll11_opy_ = bstack1l11llll_opy_(bstack1l1llll111_opy_)
        if bstack11l1lll11_opy_:
            bstack1lll1lll11_opy_ = update(bstack11l1lll11_opy_, bstack1lll1lll11_opy_)
        desired_capabilities = None
    if options:
        bstack1ll11ll111_opy_(options, bstack1lll1lll11_opy_)
    if not options:
        options = bstack1lllll1l11_opy_(bstack1lll1lll11_opy_)
    if proxy and bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ᠑")):
        options.proxy(proxy)
    if options and bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ᠒")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11ll11111_opy_() < version.parse(bstack1111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ᠓")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll1lll11_opy_)
    logger.info(bstack1111llll_opy_)
    if bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ᠔")):
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ᠕")):
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭᠖")):
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll11lll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11111ll1_opy_ = bstack1111_opy_ (u"ࠧࠨ᠗")
        if bstack11ll11111_opy_() >= version.parse(bstack1111_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ᠘")):
            bstack11111ll1_opy_ = self.caps.get(bstack1111_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ᠙"))
        else:
            bstack11111ll1_opy_ = self.capabilities.get(bstack1111_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ᠚"))
        if bstack11111ll1_opy_:
            bstack1111l1l11_opy_(bstack11111ll1_opy_)
            if bstack11ll11111_opy_() <= version.parse(bstack1111_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ᠛")):
                self.command_executor._url = bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ᠜") + bstack1l1ll11l11_opy_ + bstack1111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ᠝")
            else:
                self.command_executor._url = bstack1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ᠞") + bstack11111ll1_opy_ + bstack1111_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ᠟")
            logger.debug(bstack1l111l11_opy_.format(bstack11111ll1_opy_))
        else:
            logger.debug(bstack1l1l1ll11l_opy_.format(bstack1111_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥᠠ")))
    except Exception as e:
        logger.debug(bstack1l1l1ll11l_opy_.format(e))
    bstack11l11ll11_opy_ = self.session_id
    if bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᠡ") in bstack1l1l11ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᠢ"), None)
        if item:
            bstack1ll1lll1l1l_opy_ = getattr(item, bstack1111_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪᠣ"), False)
            if not getattr(item, bstack1111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᠤ"), None) and bstack1ll1lll1l1l_opy_:
                setattr(store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᠥ")], bstack1111_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᠦ"), self)
        bstack11l1ll1ll_opy_.bstack1ll11111l1_opy_(self)
    bstack1lll11lll1_opy_.append(self)
    if bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᠧ") in CONFIG and bstack1111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᠨ") in CONFIG[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᠩ")][bstack1l1ll1l11_opy_]:
        bstack1lll1111l1_opy_ = CONFIG[bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᠪ")][bstack1l1ll1l11_opy_][bstack1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᠫ")]
    logger.debug(bstack1lll1l1l1_opy_.format(bstack11l11ll11_opy_))
def bstack1l11ll1l1l_opy_(self, url):
    global bstack1llllllll_opy_
    global CONFIG
    try:
        bstack1lllll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l111111l_opy_.format(str(err)))
    try:
        bstack1llllllll_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11l111_opy_ = str(e)
            if any(err_msg in bstack1l11l111_opy_ for err_msg in bstack1l11l111l_opy_):
                bstack1lllll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l111111l_opy_.format(str(err)))
        raise e
def bstack1lll11l1_opy_(item, when):
    global bstack1ll1ll111_opy_
    try:
        bstack1ll1ll111_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll111111l_opy_(item, call, rep):
    global bstack1l11lllll1_opy_
    global bstack1lll11lll1_opy_
    name = bstack1111_opy_ (u"ࠧࠨᠬ")
    try:
        if rep.when == bstack1111_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᠭ"):
            bstack11l11ll11_opy_ = threading.current_thread().bstackSessionId
            bstack1ll1ll1l1l1_opy_ = item.config.getoption(bstack1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᠮ"))
            try:
                if (str(bstack1ll1ll1l1l1_opy_).lower() != bstack1111_opy_ (u"ࠪࡸࡷࡻࡥࠨᠯ")):
                    name = str(rep.nodeid)
                    bstack1lll11l111_opy_ = bstack111l1l11_opy_(bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᠰ"), name, bstack1111_opy_ (u"ࠬ࠭ᠱ"), bstack1111_opy_ (u"࠭ࠧᠲ"), bstack1111_opy_ (u"ࠧࠨᠳ"), bstack1111_opy_ (u"ࠨࠩᠴ"))
                    os.environ[bstack1111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᠵ")] = name
                    for driver in bstack1lll11lll1_opy_:
                        if bstack11l11ll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11l111_opy_)
            except Exception as e:
                logger.debug(bstack1111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᠶ").format(str(e)))
            try:
                bstack1l11l111l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᠷ"):
                    status = bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᠸ") if rep.outcome.lower() == bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᠹ") else bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᠺ")
                    reason = bstack1111_opy_ (u"ࠨࠩᠻ")
                    if status == bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᠼ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1111_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᠽ") if status == bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᠾ") else bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᠿ")
                    data = name + bstack1111_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨᡀ") if status == bstack1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᡁ") else name + bstack1111_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫᡂ") + reason
                    bstack11l1l111_opy_ = bstack111l1l11_opy_(bstack1111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᡃ"), bstack1111_opy_ (u"ࠪࠫᡄ"), bstack1111_opy_ (u"ࠫࠬᡅ"), bstack1111_opy_ (u"ࠬ࠭ᡆ"), level, data)
                    for driver in bstack1lll11lll1_opy_:
                        if bstack11l11ll11_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1l111_opy_)
            except Exception as e:
                logger.debug(bstack1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᡇ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫᡈ").format(str(e)))
    bstack1l11lllll1_opy_(item, call, rep)
notset = Notset()
def bstack11lll1lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1lll1l_opy_
    if str(name).lower() == bstack1111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᡉ"):
        return bstack1111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᡊ")
    else:
        return bstack1l1lll1l_opy_(self, name, default, skip)
def bstack1ll1llllll_opy_(self):
    global CONFIG
    global bstack11l1l1lll_opy_
    try:
        proxy = bstack1lll11l1ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᡋ")):
                proxies = bstack1111l1ll1_opy_(proxy, bstack1l1l111ll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11lll1_opy_ = proxies.popitem()
                    if bstack1111_opy_ (u"ࠦ࠿࠵࠯ࠣᡌ") in bstack1ll11lll1_opy_:
                        return bstack1ll11lll1_opy_
                    else:
                        return bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᡍ") + bstack1ll11lll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥᡎ").format(str(e)))
    return bstack11l1l1lll_opy_(self)
def bstack1lll11ll1_opy_():
    return (bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᡏ") in CONFIG or bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᡐ") in CONFIG) and bstack1l1lll111l_opy_() and bstack11ll11111_opy_() >= version.parse(
        bstack111l1ll1l_opy_)
def bstack1lll11111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lll1111l1_opy_
    global bstack1ll1ll1l1l_opy_
    global bstack1l1l11ll1_opy_
    CONFIG[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᡑ")] = str(bstack1l1l11ll1_opy_) + str(__version__)
    bstack1l1ll1l11_opy_ = 0
    try:
        if bstack1ll1ll1l1l_opy_ is True:
            bstack1l1ll1l11_opy_ = int(os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᡒ")))
    except:
        bstack1l1ll1l11_opy_ = 0
    CONFIG[bstack1111_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᡓ")] = True
    bstack1lll1lll11_opy_ = bstack1l11llll_opy_(CONFIG, bstack1l1ll1l11_opy_)
    logger.debug(bstack11ll1l1l1_opy_.format(str(bstack1lll1lll11_opy_)))
    if CONFIG.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᡔ")):
        bstack11ll111l_opy_(bstack1lll1lll11_opy_, bstack1l1l1ll1ll_opy_)
    if bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᡕ") in CONFIG and bstack1111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᡖ") in CONFIG[bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᡗ")][bstack1l1ll1l11_opy_]:
        bstack1lll1111l1_opy_ = CONFIG[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᡘ")][bstack1l1ll1l11_opy_][bstack1111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᡙ")]
    import urllib
    import json
    bstack1l11l1lll_opy_ = bstack1111_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ᡚ") + urllib.parse.quote(json.dumps(bstack1lll1lll11_opy_))
    browser = self.connect(bstack1l11l1lll_opy_)
    return browser
def bstack11l111111_opy_():
    global bstack111ll1lll_opy_
    global bstack1l1l11ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1llllllll1_opy_
        if not bstack111ll1llll_opy_():
            global bstack11l11l1l1_opy_
            if not bstack11l11l1l1_opy_:
                from bstack_utils.helper import bstack1l11ll1l11_opy_, bstack1ll1111l1l_opy_
                bstack11l11l1l1_opy_ = bstack1l11ll1l11_opy_()
                bstack1ll1111l1l_opy_(bstack1l1l11ll1_opy_)
            BrowserType.connect = bstack1llllllll1_opy_
            return
        BrowserType.launch = bstack1lll11111_opy_
        bstack111ll1lll_opy_ = True
    except Exception as e:
        pass
def bstack1ll1ll1111l_opy_():
    global CONFIG
    global bstack11l11l1l_opy_
    global bstack1l1ll11l11_opy_
    global bstack1l1l1ll1ll_opy_
    global bstack1ll1ll1l1l_opy_
    global bstack1l1lll1ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫᡛ")))
    bstack11l11l1l_opy_ = eval(os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᡜ")))
    bstack1l1ll11l11_opy_ = os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧᡝ"))
    bstack1lll11llll_opy_(CONFIG, bstack11l11l1l_opy_)
    bstack1l1lll1ll1_opy_ = bstack1lll1ll1l1_opy_.bstack1lll1ll1_opy_(CONFIG, bstack1l1lll1ll1_opy_)
    global bstack1lll11lll_opy_
    global bstack11l11lll1_opy_
    global bstack1l1l1ll111_opy_
    global bstack1l1lllll1_opy_
    global bstack1ll11l1l11_opy_
    global bstack1l1111111_opy_
    global bstack111lll1l_opy_
    global bstack1llllllll_opy_
    global bstack11l1l1lll_opy_
    global bstack1l1lll1l_opy_
    global bstack1ll1ll111_opy_
    global bstack1l11lllll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll11lll_opy_ = webdriver.Remote.__init__
        bstack11l11lll1_opy_ = WebDriver.quit
        bstack111lll1l_opy_ = WebDriver.close
        bstack1llllllll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᡞ") in CONFIG or bstack1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᡟ") in CONFIG) and bstack1l1lll111l_opy_():
        if bstack11ll11111_opy_() < version.parse(bstack111l1ll1l_opy_):
            logger.error(bstack1l1l11lll_opy_.format(bstack11ll11111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11l1l1lll_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack111l11ll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1lll1l_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll1ll111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l1lll1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l11lllll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫᡠ"))
    bstack1l1l1ll1ll_opy_ = CONFIG.get(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᡡ"), {}).get(bstack1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᡢ"))
    bstack1ll1ll1l1l_opy_ = True
    bstack1lllll1l1_opy_(bstack1ll1l1lll_opy_)
if (bstack11l1111ll1_opy_()):
    bstack1ll1ll1111l_opy_()
@bstack1l111l1l1l_opy_(class_method=False)
def bstack1ll1ll11l11_opy_(hook_name, event, bstack1ll1lllll11_opy_=None):
    if hook_name not in [bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᡣ"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᡤ"), bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᡥ"), bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᡦ"), bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᡧ"), bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᡨ"), bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᡩ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᡪ")]:
        return
    node = store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᡫ")]
    if hook_name in [bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᡬ"), bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᡭ")]:
        node = store[bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᡮ")]
    elif hook_name in [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᡯ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᡰ")]:
        node = store[bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᡱ")]
    if event == bstack1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᡲ"):
        hook_type = bstack1llll11l111_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11lll1lll1_opy_ = {
            bstack1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᡳ"): uuid,
            bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᡴ"): bstack1ll1ll1l11_opy_(),
            bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨᡵ"): bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᡶ"),
            bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᡷ"): hook_type,
            bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᡸ"): hook_name
        }
        store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᡹")].append(uuid)
        bstack1ll1llll1ll_opy_ = node.nodeid
        if hook_type == bstack1111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭᡺"):
            if not _1l1111llll_opy_.get(bstack1ll1llll1ll_opy_, None):
                _1l1111llll_opy_[bstack1ll1llll1ll_opy_] = {bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᡻"): []}
            _1l1111llll_opy_[bstack1ll1llll1ll_opy_][bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᡼")].append(bstack11lll1lll1_opy_[bstack1111_opy_ (u"ࠫࡺࡻࡩࡥࠩ᡽")])
        _1l1111llll_opy_[bstack1ll1llll1ll_opy_ + bstack1111_opy_ (u"ࠬ࠳ࠧ᡾") + hook_name] = bstack11lll1lll1_opy_
        bstack1ll1ll1l11l_opy_(node, bstack11lll1lll1_opy_, bstack1111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ᡿"))
    elif event == bstack1111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᢀ"):
        bstack11lllllll1_opy_ = node.nodeid + bstack1111_opy_ (u"ࠨ࠯ࠪᢁ") + hook_name
        _1l1111llll_opy_[bstack11lllllll1_opy_][bstack1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᢂ")] = bstack1ll1ll1l11_opy_()
        bstack1ll1ll1ll11_opy_(_1l1111llll_opy_[bstack11lllllll1_opy_][bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᢃ")])
        bstack1ll1ll1l11l_opy_(node, _1l1111llll_opy_[bstack11lllllll1_opy_], bstack1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᢄ"), bstack1ll1lll11l1_opy_=bstack1ll1lllll11_opy_)
def bstack1ll1ll1ll1l_opy_():
    global bstack1ll1llll11l_opy_
    if bstack1l1llllll1_opy_():
        bstack1ll1llll11l_opy_ = bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᢅ")
    else:
        bstack1ll1llll11l_opy_ = bstack1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᢆ")
@bstack11l1ll1ll_opy_.bstack1lll11l1l11_opy_
def bstack1ll1llll111_opy_():
    bstack1ll1ll1ll1l_opy_()
    if bstack1l1lll111l_opy_():
        bstack111ll1l1_opy_(bstack11ll1l11l_opy_)
    try:
        bstack1111ll11l1_opy_(bstack1ll1ll11l11_opy_)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣᢇ").format(e))
bstack1ll1llll111_opy_()