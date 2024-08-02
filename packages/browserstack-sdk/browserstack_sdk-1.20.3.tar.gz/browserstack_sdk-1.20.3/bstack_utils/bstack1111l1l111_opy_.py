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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1111l1l_opy_
from browserstack_sdk.bstack1l111ll1_opy_ import bstack111l11l1_opy_
def _1111l1ll1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111ll11l1_opy_:
    def __init__(self, handler):
        self._1111ll11ll_opy_ = {}
        self._1111l1l11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack111l11l1_opy_.version()
        if bstack11l1111l1l_opy_(pytest_version, bstack1111_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥᏉ")) >= 0:
            self._1111ll11ll_opy_[bstack1111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᏊ")] = Module._register_setup_function_fixture
            self._1111ll11ll_opy_[bstack1111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏋ")] = Module._register_setup_module_fixture
            self._1111ll11ll_opy_[bstack1111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏌ")] = Class._register_setup_class_fixture
            self._1111ll11ll_opy_[bstack1111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᏍ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏎ"))
            Module._register_setup_module_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏏ"))
            Class._register_setup_class_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏐ"))
            Class._register_setup_method_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮡ"))
        else:
            self._1111ll11ll_opy_[bstack1111_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᏒ")] = Module._inject_setup_function_fixture
            self._1111ll11ll_opy_[bstack1111_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᏓ")] = Module._inject_setup_module_fixture
            self._1111ll11ll_opy_[bstack1111_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᏔ")] = Class._inject_setup_class_fixture
            self._1111ll11ll_opy_[bstack1111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᏕ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꮦ"))
            Module._inject_setup_module_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏗ"))
            Class._inject_setup_class_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏘ"))
            Class._inject_setup_method_fixture = self.bstack1111l1lll1_opy_(bstack1111_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᏙ"))
    def bstack1111l11lll_opy_(self, bstack1111l1ll11_opy_, hook_type):
        meth = getattr(bstack1111l1ll11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111l1l11l_opy_[hook_type] = meth
            setattr(bstack1111l1ll11_opy_, hook_type, self.bstack1111ll1l11_opy_(hook_type))
    def bstack1111l1llll_opy_(self, instance, bstack1111l1l1l1_opy_):
        if bstack1111l1l1l1_opy_ == bstack1111_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᏚ"):
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᏛ"))
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᏜ"))
        if bstack1111l1l1l1_opy_ == bstack1111_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᏝ"):
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥᏞ"))
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢᏟ"))
        if bstack1111l1l1l1_opy_ == bstack1111_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᏠ"):
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧᏡ"))
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤᏢ"))
        if bstack1111l1l1l1_opy_ == bstack1111_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᏣ"):
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤᏤ"))
            self.bstack1111l11lll_opy_(instance.obj, bstack1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨᏥ"))
    @staticmethod
    def bstack1111ll1111_opy_(hook_type, func, args):
        if hook_type in [bstack1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᏦ"), bstack1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᏧ")]:
            _1111l1ll1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111ll1l11_opy_(self, hook_type):
        def bstack1111l1l1ll_opy_(arg=None):
            self.handler(hook_type, bstack1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᏨ"))
            result = None
            exception = None
            try:
                self.bstack1111ll1111_opy_(hook_type, self._1111l1l11l_opy_[hook_type], (arg,))
                result = Result(result=bstack1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᏩ"))
            except Exception as e:
                result = Result(result=bstack1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏪ"), exception=e)
                self.handler(hook_type, bstack1111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᏫ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᏬ"), result)
        def bstack1111ll1l1l_opy_(this, arg=None):
            self.handler(hook_type, bstack1111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᏭ"))
            result = None
            exception = None
            try:
                self.bstack1111ll1111_opy_(hook_type, self._1111l1l11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ꮾ"))
            except Exception as e:
                result = Result(result=bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᏯ"), exception=e)
                self.handler(hook_type, bstack1111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᏰ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᏱ"), result)
        if hook_type in [bstack1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᏲ"), bstack1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ᏻ")]:
            return bstack1111ll1l1l_opy_
        return bstack1111l1l1ll_opy_
    def bstack1111l1lll1_opy_(self, bstack1111l1l1l1_opy_):
        def bstack1111ll111l_opy_(this, *args, **kwargs):
            self.bstack1111l1llll_opy_(this, bstack1111l1l1l1_opy_)
            self._1111ll11ll_opy_[bstack1111l1l1l1_opy_](this, *args, **kwargs)
        return bstack1111ll111l_opy_