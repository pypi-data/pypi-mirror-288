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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111l1111_opy_ import RobotHandler
from bstack_utils.capture import bstack1l111111ll_opy_
from bstack_utils.bstack11llll1ll1_opy_ import bstack1l1111lll1_opy_, bstack1l11111ll1_opy_, bstack11ll1lll1l_opy_
from bstack_utils.bstack1l1l111l11_opy_ import bstack11l1ll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l111ll1_opy_, bstack1ll1ll1l11_opy_, Result, \
    bstack1l111l1l1l_opy_, bstack11lll11l1l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ൵"): [],
        bstack1111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ൶"): [],
        bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ൷"): []
    }
    bstack11lll1l11l_opy_ = []
    bstack11ll1l1lll_opy_ = []
    @staticmethod
    def bstack1l11111111_opy_(log):
        if not (log[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ൸")] and log[bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൹")].strip()):
            return
        active = bstack11l1ll1ll_opy_.bstack1l1111111l_opy_()
        log = {
            bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬൺ"): log[bstack1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ൻ")],
            bstack1111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫർ"): bstack11lll11l1l_opy_().isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫൽ"),
            bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫൾ"): log[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൿ")],
        }
        if active:
            if active[bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪ඀")] == bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫඁ"):
                log[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧං")] = active[bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨඃ")]
            elif active[bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ඄")] == bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨඅ"):
                log[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫආ")] = active[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬඇ")]
        bstack11l1ll1ll_opy_.bstack1ll11ll1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l1111l1l1_opy_ = None
        self._11lll1l111_opy_ = None
        self._1l1111llll_opy_ = OrderedDict()
        self.bstack1l111l11ll_opy_ = bstack1l111111ll_opy_(self.bstack1l11111111_opy_)
    @bstack1l111l1l1l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11ll1lll11_opy_()
        if not self._1l1111llll_opy_.get(attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩඈ")), None):
            self._1l1111llll_opy_[attrs.get(bstack1111_opy_ (u"ࠧࡪࡦࠪඉ"))] = {}
        bstack11lll11111_opy_ = bstack11ll1lll1l_opy_(
                bstack1l111l11l1_opy_=attrs.get(bstack1111_opy_ (u"ࠨ࡫ࡧࠫඊ")),
                name=name,
                bstack1l111l111l_opy_=bstack1ll1ll1l11_opy_(),
                file_path=os.path.relpath(attrs[bstack1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩඋ")], start=os.getcwd()) if attrs.get(bstack1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪඌ")) != bstack1111_opy_ (u"ࠫࠬඍ") else bstack1111_opy_ (u"ࠬ࠭ඎ"),
                framework=bstack1111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬඏ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1111_opy_ (u"ࠧࡪࡦࠪඐ"), None)
        self._1l1111llll_opy_[attrs.get(bstack1111_opy_ (u"ࠨ࡫ࡧࠫඑ"))][bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬඒ")] = bstack11lll11111_opy_
    @bstack1l111l1l1l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11ll1ll1ll_opy_()
        self._11llll1l1l_opy_(messages)
        for bstack1l111l1lll_opy_ in self.bstack11lll1l11l_opy_:
            bstack1l111l1lll_opy_[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬඓ")][bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪඔ")].extend(self.store[bstack1111_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫඕ")])
            bstack11l1ll1ll_opy_.bstack11ll1ll1l1_opy_(bstack1l111l1lll_opy_)
        self.bstack11lll1l11l_opy_ = []
        self.store[bstack1111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬඖ")] = []
    @bstack1l111l1l1l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l111l11ll_opy_.start()
        if not self._1l1111llll_opy_.get(attrs.get(bstack1111_opy_ (u"ࠧࡪࡦࠪ඗")), None):
            self._1l1111llll_opy_[attrs.get(bstack1111_opy_ (u"ࠨ࡫ࡧࠫ඘"))] = {}
        driver = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ඙"), None)
        bstack11llll1ll1_opy_ = bstack11ll1lll1l_opy_(
            bstack1l111l11l1_opy_=attrs.get(bstack1111_opy_ (u"ࠪ࡭ࡩ࠭ක")),
            name=name,
            bstack1l111l111l_opy_=bstack1ll1ll1l11_opy_(),
            file_path=os.path.relpath(attrs[bstack1111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫඛ")], start=os.getcwd()),
            scope=RobotHandler.bstack11lll111l1_opy_(attrs.get(bstack1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬග"), None)),
            framework=bstack1111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬඝ"),
            tags=attrs[bstack1111_opy_ (u"ࠧࡵࡣࡪࡷࠬඞ")],
            hooks=self.store[bstack1111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧඟ")],
            bstack11lll111ll_opy_=bstack11l1ll1ll_opy_.bstack11lll1ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1111_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦච").format(bstack1111_opy_ (u"ࠥࠤࠧඡ").join(attrs[bstack1111_opy_ (u"ࠫࡹࡧࡧࡴࠩජ")]), name) if attrs[bstack1111_opy_ (u"ࠬࡺࡡࡨࡵࠪඣ")] else name
        )
        self._1l1111llll_opy_[attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩඤ"))][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඥ")] = bstack11llll1ll1_opy_
        threading.current_thread().current_test_uuid = bstack11llll1ll1_opy_.bstack1l111l1l11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1111_opy_ (u"ࠨ࡫ࡧࠫඦ"), None)
        self.bstack11llll11l1_opy_(bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪට"), bstack11llll1ll1_opy_)
    @bstack1l111l1l1l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l111l11ll_opy_.reset()
        bstack11llllll1l_opy_ = bstack11lll1ll11_opy_.get(attrs.get(bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪඨ")), bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬඩ"))
        self._1l1111llll_opy_[attrs.get(bstack1111_opy_ (u"ࠬ࡯ࡤࠨඪ"))][bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩණ")].stop(time=bstack1ll1ll1l11_opy_(), duration=int(attrs.get(bstack1111_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬඬ"), bstack1111_opy_ (u"ࠨ࠲ࠪත"))), result=Result(result=bstack11llllll1l_opy_, exception=attrs.get(bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪථ")), bstack11lll11ll1_opy_=[attrs.get(bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫද"))]))
        self.bstack11llll11l1_opy_(bstack1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ධ"), self._1l1111llll_opy_[attrs.get(bstack1111_opy_ (u"ࠬ࡯ࡤࠨන"))][bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ඲")], True)
        self.store[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫඳ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l111l1l1l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11ll1lll11_opy_()
        current_test_id = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪප"), None)
        bstack11llllllll_opy_ = current_test_id if bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫඵ"), None) else bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭බ"), None)
        if attrs.get(bstack1111_opy_ (u"ࠫࡹࡿࡰࡦࠩභ"), bstack1111_opy_ (u"ࠬ࠭ම")).lower() in [bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬඹ"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩය")]:
            hook_type = bstack11llllll11_opy_(attrs.get(bstack1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ර")), bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭඼"), None))
            hook_name = bstack1111_opy_ (u"ࠪࡿࢂ࠭ල").format(attrs.get(bstack1111_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ඾"), bstack1111_opy_ (u"ࠬ࠭඿")))
            if hook_type in [bstack1111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪව"), bstack1111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪශ")]:
                hook_name = bstack1111_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩෂ").format(bstack11ll1lllll_opy_.get(hook_type), attrs.get(bstack1111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩස"), bstack1111_opy_ (u"ࠪࠫහ")))
            bstack11lll1lll1_opy_ = bstack1l11111ll1_opy_(
                bstack1l111l11l1_opy_=bstack11llllllll_opy_ + bstack1111_opy_ (u"ࠫ࠲࠭ළ") + attrs.get(bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪෆ"), bstack1111_opy_ (u"࠭ࠧ෇")).lower(),
                name=hook_name,
                bstack1l111l111l_opy_=bstack1ll1ll1l11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ෈")), start=os.getcwd()),
                framework=bstack1111_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ෉"),
                tags=attrs[bstack1111_opy_ (u"ࠩࡷࡥ࡬ࡹ්ࠧ")],
                scope=RobotHandler.bstack11lll111l1_opy_(attrs.get(bstack1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ෋"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11lll1lll1_opy_.bstack1l111l1l11_opy_()
            threading.current_thread().current_hook_id = bstack11llllllll_opy_ + bstack1111_opy_ (u"ࠫ࠲࠭෌") + attrs.get(bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪ෍"), bstack1111_opy_ (u"࠭ࠧ෎")).lower()
            self.store[bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫා")] = [bstack11lll1lll1_opy_.bstack1l111l1l11_opy_()]
            if bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬැ"), None):
                self.store[bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ෑ")].append(bstack11lll1lll1_opy_.bstack1l111l1l11_opy_())
            else:
                self.store[bstack1111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩි")].append(bstack11lll1lll1_opy_.bstack1l111l1l11_opy_())
            if bstack11llllllll_opy_:
                self._1l1111llll_opy_[bstack11llllllll_opy_ + bstack1111_opy_ (u"ࠫ࠲࠭ී") + attrs.get(bstack1111_opy_ (u"ࠬࡺࡹࡱࡧࠪු"), bstack1111_opy_ (u"࠭ࠧ෕")).lower()] = { bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪූ"): bstack11lll1lll1_opy_ }
            bstack11l1ll1ll_opy_.bstack11llll11l1_opy_(bstack1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ෗"), bstack11lll1lll1_opy_)
        else:
            bstack11lllll111_opy_ = {
                bstack1111_opy_ (u"ࠩ࡬ࡨࠬෘ"): uuid4().__str__(),
                bstack1111_opy_ (u"ࠪࡸࡪࡾࡴࠨෙ"): bstack1111_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪේ").format(attrs.get(bstack1111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬෛ")), attrs.get(bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫො"), bstack1111_opy_ (u"ࠧࠨෝ"))) if attrs.get(bstack1111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ෞ"), []) else attrs.get(bstack1111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩෟ")),
                bstack1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ෠"): attrs.get(bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩ෡"), []),
                bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ෢"): bstack1ll1ll1l11_opy_(),
                bstack1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭෣"): bstack1111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ෤"),
                bstack1111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭෥"): attrs.get(bstack1111_opy_ (u"ࠩࡧࡳࡨ࠭෦"), bstack1111_opy_ (u"ࠪࠫ෧"))
            }
            if attrs.get(bstack1111_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ෨"), bstack1111_opy_ (u"ࠬ࠭෩")) != bstack1111_opy_ (u"࠭ࠧ෪"):
                bstack11lllll111_opy_[bstack1111_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ෫")] = attrs.get(bstack1111_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ෬"))
            if not self.bstack11ll1l1lll_opy_:
                self._1l1111llll_opy_[self._11llll1l11_opy_()][bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ෭")].add_step(bstack11lllll111_opy_)
                threading.current_thread().current_step_uuid = bstack11lllll111_opy_[bstack1111_opy_ (u"ࠪ࡭ࡩ࠭෮")]
            self.bstack11ll1l1lll_opy_.append(bstack11lllll111_opy_)
    @bstack1l111l1l1l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11ll1ll1ll_opy_()
        self._11llll1l1l_opy_(messages)
        current_test_id = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭෯"), None)
        bstack11llllllll_opy_ = current_test_id if current_test_id else bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ෰"), None)
        bstack1l1111l11l_opy_ = bstack11lll1ll11_opy_.get(attrs.get(bstack1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෱")), bstack1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨෲ"))
        bstack11lllll1ll_opy_ = attrs.get(bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩෳ"))
        if bstack1l1111l11l_opy_ != bstack1111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ෴") and not attrs.get(bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෵")) and self._1l1111l1l1_opy_:
            bstack11lllll1ll_opy_ = self._1l1111l1l1_opy_
        bstack11lll1111l_opy_ = Result(result=bstack1l1111l11l_opy_, exception=bstack11lllll1ll_opy_, bstack11lll11ll1_opy_=[bstack11lllll1ll_opy_])
        if attrs.get(bstack1111_opy_ (u"ࠫࡹࡿࡰࡦࠩ෶"), bstack1111_opy_ (u"ࠬ࠭෷")).lower() in [bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ෸"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ෹")]:
            bstack11llllllll_opy_ = current_test_id if current_test_id else bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ෺"), None)
            if bstack11llllllll_opy_:
                bstack11lllllll1_opy_ = bstack11llllllll_opy_ + bstack1111_opy_ (u"ࠤ࠰ࠦ෻") + attrs.get(bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ෼"), bstack1111_opy_ (u"ࠫࠬ෽")).lower()
                self._1l1111llll_opy_[bstack11lllllll1_opy_][bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ෾")].stop(time=bstack1ll1ll1l11_opy_(), duration=int(attrs.get(bstack1111_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ෿"), bstack1111_opy_ (u"ࠧ࠱ࠩ฀"))), result=bstack11lll1111l_opy_)
                bstack11l1ll1ll_opy_.bstack11llll11l1_opy_(bstack1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪก"), self._1l1111llll_opy_[bstack11lllllll1_opy_][bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬข")])
        else:
            bstack11llllllll_opy_ = current_test_id if current_test_id else bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬฃ"), None)
            if bstack11llllllll_opy_ and len(self.bstack11ll1l1lll_opy_) == 1:
                current_step_uuid = bstack11l111ll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨค"), None)
                self._1l1111llll_opy_[bstack11llllllll_opy_][bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨฅ")].bstack1l1111l111_opy_(current_step_uuid, duration=int(attrs.get(bstack1111_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫฆ"), bstack1111_opy_ (u"ࠧ࠱ࠩง"))), result=bstack11lll1111l_opy_)
            else:
                self.bstack1l11111l11_opy_(attrs)
            self.bstack11ll1l1lll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1111_opy_ (u"ࠨࡪࡷࡱࡱ࠭จ"), bstack1111_opy_ (u"ࠩࡱࡳࠬฉ")) == bstack1111_opy_ (u"ࠪࡽࡪࡹࠧช"):
                return
            self.messages.push(message)
            bstack11lll1l1ll_opy_ = []
            if bstack11l1ll1ll_opy_.bstack1l1111111l_opy_():
                bstack11lll1l1ll_opy_.append({
                    bstack1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧซ"): bstack1ll1ll1l11_opy_(),
                    bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ฌ"): message.get(bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧญ")),
                    bstack1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ฎ"): message.get(bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧฏ")),
                    **bstack11l1ll1ll_opy_.bstack1l1111111l_opy_()
                })
                if len(bstack11lll1l1ll_opy_) > 0:
                    bstack11l1ll1ll_opy_.bstack1ll11ll1_opy_(bstack11lll1l1ll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack11l1ll1ll_opy_.bstack11lllll11l_opy_()
    def bstack1l11111l11_opy_(self, bstack11ll1llll1_opy_):
        if not bstack11l1ll1ll_opy_.bstack1l1111111l_opy_():
            return
        kwname = bstack1111_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨฐ").format(bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪฑ")), bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠫࡦࡸࡧࡴࠩฒ"), bstack1111_opy_ (u"ࠬ࠭ณ"))) if bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"࠭ࡡࡳࡩࡶࠫด"), []) else bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧต"))
        error_message = bstack1111_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢถ").format(kwname, bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩท")), str(bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫธ"))))
        bstack11lll1llll_opy_ = bstack1111_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥน").format(kwname, bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬบ")))
        bstack11llll1111_opy_ = error_message if bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧป")) else bstack11lll1llll_opy_
        bstack11ll1ll11l_opy_ = {
            bstack1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪผ"): self.bstack11ll1l1lll_opy_[-1].get(bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬฝ"), bstack1ll1ll1l11_opy_()),
            bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪพ"): bstack11llll1111_opy_,
            bstack1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩฟ"): bstack1111_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪภ") if bstack11ll1llll1_opy_.get(bstack1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬม")) == bstack1111_opy_ (u"࠭ࡆࡂࡋࡏࠫย") else bstack1111_opy_ (u"ࠧࡊࡐࡉࡓࠬร"),
            **bstack11l1ll1ll_opy_.bstack1l1111111l_opy_()
        }
        bstack11l1ll1ll_opy_.bstack1ll11ll1_opy_([bstack11ll1ll11l_opy_])
    def _11llll1l11_opy_(self):
        for bstack1l111l11l1_opy_ in reversed(self._1l1111llll_opy_):
            bstack1l11111l1l_opy_ = bstack1l111l11l1_opy_
            data = self._1l1111llll_opy_[bstack1l111l11l1_opy_][bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫฤ")]
            if isinstance(data, bstack1l11111ll1_opy_):
                if not bstack1111_opy_ (u"ࠩࡈࡅࡈࡎࠧล") in data.bstack11lll11lll_opy_():
                    return bstack1l11111l1l_opy_
            else:
                return bstack1l11111l1l_opy_
    def _11llll1l1l_opy_(self, messages):
        try:
            bstack1l1111ll1l_opy_ = BuiltIn().get_variable_value(bstack1111_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤฦ")) in (bstack11lll11l11_opy_.DEBUG, bstack11lll11l11_opy_.TRACE)
            for message, bstack11llll111l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬว"))
                level = message.get(bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫศ"))
                if level == bstack11lll11l11_opy_.FAIL:
                    self._1l1111l1l1_opy_ = name or self._1l1111l1l1_opy_
                    self._11lll1l111_opy_ = bstack11llll111l_opy_.get(bstack1111_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢษ")) if bstack1l1111ll1l_opy_ and bstack11llll111l_opy_ else self._11lll1l111_opy_
        except:
            pass
    @classmethod
    def bstack11llll11l1_opy_(self, event: str, bstack1l1111l1ll_opy_: bstack1l1111lll1_opy_, bstack11lllll1l1_opy_=False):
        if event == bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩส"):
            bstack1l1111l1ll_opy_.set(hooks=self.store[bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬห")])
        if event == bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪฬ"):
            event = bstack1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬอ")
        if bstack11lllll1l1_opy_:
            bstack11lll1l1l1_opy_ = {
                bstack1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨฮ"): event,
                bstack1l1111l1ll_opy_.bstack1l111111l1_opy_(): bstack1l1111l1ll_opy_.bstack1l11111lll_opy_(event)
            }
            self.bstack11lll1l11l_opy_.append(bstack11lll1l1l1_opy_)
        else:
            bstack11l1ll1ll_opy_.bstack11llll11l1_opy_(event, bstack1l1111l1ll_opy_)
class Messages:
    def __init__(self):
        self._11llll11ll_opy_ = []
    def bstack11ll1lll11_opy_(self):
        self._11llll11ll_opy_.append([])
    def bstack11ll1ll1ll_opy_(self):
        return self._11llll11ll_opy_.pop() if self._11llll11ll_opy_ else list()
    def push(self, message):
        self._11llll11ll_opy_[-1].append(message) if self._11llll11ll_opy_ else self._11llll11ll_opy_.append([message])
class bstack11lll11l11_opy_:
    FAIL = bstack1111_opy_ (u"ࠬࡌࡁࡊࡎࠪฯ")
    ERROR = bstack1111_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬะ")
    WARNING = bstack1111_opy_ (u"ࠧࡘࡃࡕࡒࠬั")
    bstack11llll1lll_opy_ = bstack1111_opy_ (u"ࠨࡋࡑࡊࡔ࠭า")
    DEBUG = bstack1111_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨำ")
    TRACE = bstack1111_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩิ")
    bstack1l1111ll11_opy_ = [FAIL, ERROR]
def bstack1l111l1ll1_opy_(bstack11ll1ll111_opy_):
    if not bstack11ll1ll111_opy_:
        return None
    if bstack11ll1ll111_opy_.get(bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧี"), None):
        return getattr(bstack11ll1ll111_opy_[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨึ")], bstack1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫื"), None)
    return bstack11ll1ll111_opy_.get(bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨุࠬ"), None)
def bstack11llllll11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶูࠧ"), bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱฺࠫ")]:
        return
    if hook_type.lower() == bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ฻"):
        if current_test_uuid is None:
            return bstack1111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ฼")
        else:
            return bstack1111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ฽")
    elif hook_type.lower() == bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ฾"):
        if current_test_uuid is None:
            return bstack1111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ฿")
        else:
            return bstack1111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬเ")