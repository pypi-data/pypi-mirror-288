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
from uuid import uuid4
from bstack_utils.helper import bstack1ll1ll1l11_opy_, bstack111ll111ll_opy_
from bstack_utils.bstack1l11111l_opy_ import bstack1lll1llll11_opy_
class bstack1l1111lll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l111l_opy_=None, framework=None, tags=[], scope=[], bstack1lll1l111l1_opy_=None, bstack1lll1l11l1l_opy_=True, bstack1lll11lllll_opy_=None, bstack111ll11l1_opy_=None, result=None, duration=None, bstack1l111l11l1_opy_=None, meta={}):
        self.bstack1l111l11l1_opy_ = bstack1l111l11l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1l11l1l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l111l_opy_ = bstack1l111l111l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1l111l1_opy_ = bstack1lll1l111l1_opy_
        self.bstack1lll11lllll_opy_ = bstack1lll11lllll_opy_
        self.bstack111ll11l1_opy_ = bstack111ll11l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111l1l11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lll11ll1ll_opy_(self):
        bstack1lll11l1lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᕗ"): bstack1lll11l1lll_opy_,
            bstack1111_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᕘ"): bstack1lll11l1lll_opy_,
            bstack1111_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᕙ"): bstack1lll11l1lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1111_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᕚ") + key)
            setattr(self, key, val)
    def bstack1lll1l111ll_opy_(self):
        return {
            bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᕛ"): self.name,
            bstack1111_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᕜ"): {
                bstack1111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᕝ"): bstack1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᕞ"),
                bstack1111_opy_ (u"ࠫࡨࡵࡤࡦࠩᕟ"): self.code
            },
            bstack1111_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᕠ"): self.scope,
            bstack1111_opy_ (u"࠭ࡴࡢࡩࡶࠫᕡ"): self.tags,
            bstack1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᕢ"): self.framework,
            bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᕣ"): self.bstack1l111l111l_opy_
        }
    def bstack1lll11ll11l_opy_(self):
        return {
         bstack1111_opy_ (u"ࠩࡰࡩࡹࡧࠧᕤ"): self.meta
        }
    def bstack1lll11ll1l1_opy_(self):
        return {
            bstack1111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᕥ"): {
                bstack1111_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᕦ"): self.bstack1lll1l111l1_opy_
            }
        }
    def bstack1lll1l11lll_opy_(self, bstack1lll11lll1l_opy_, details):
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠬ࡯ࡤࠨᕧ")] == bstack1lll11lll1l_opy_, self.meta[bstack1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᕨ")]), None)
        step.update(details)
    def bstack1lll11l1l1l_opy_(self, bstack1lll11lll1l_opy_):
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠧࡪࡦࠪᕩ")] == bstack1lll11lll1l_opy_, self.meta[bstack1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᕪ")]), None)
        step.update({
            bstack1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᕫ"): bstack1ll1ll1l11_opy_()
        })
    def bstack1l1111l111_opy_(self, bstack1lll11lll1l_opy_, result, duration=None):
        bstack1lll11lllll_opy_ = bstack1ll1ll1l11_opy_()
        if bstack1lll11lll1l_opy_ is not None and self.meta.get(bstack1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᕬ")):
            step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠫ࡮ࡪࠧᕭ")] == bstack1lll11lll1l_opy_, self.meta[bstack1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᕮ")]), None)
            step.update({
                bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᕯ"): bstack1lll11lllll_opy_,
                bstack1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᕰ"): duration if duration else bstack111ll111ll_opy_(step[bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᕱ")], bstack1lll11lllll_opy_),
                bstack1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᕲ"): result.result,
                bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᕳ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1l1111l_opy_):
        if self.meta.get(bstack1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᕴ")):
            self.meta[bstack1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᕵ")].append(bstack1lll1l1111l_opy_)
        else:
            self.meta[bstack1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᕶ")] = [ bstack1lll1l1111l_opy_ ]
    def bstack1lll11ll111_opy_(self):
        return {
            bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕷ"): self.bstack1l111l1l11_opy_(),
            **self.bstack1lll1l111ll_opy_(),
            **self.bstack1lll11ll1ll_opy_(),
            **self.bstack1lll11ll11l_opy_()
        }
    def bstack1lll1l11111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᕸ"): self.bstack1lll11lllll_opy_,
            bstack1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᕹ"): self.duration,
            bstack1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᕺ"): self.result.result
        }
        if data[bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᕻ")] == bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᕼ"):
            data[bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᕽ")] = self.result.bstack11ll111l11_opy_()
            data[bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᕾ")] = [{bstack1111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᕿ"): self.result.bstack111l1111ll_opy_()}]
        return data
    def bstack1lll11lll11_opy_(self):
        return {
            bstack1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖀ"): self.bstack1l111l1l11_opy_(),
            **self.bstack1lll1l111ll_opy_(),
            **self.bstack1lll11ll1ll_opy_(),
            **self.bstack1lll1l11111_opy_(),
            **self.bstack1lll11ll11l_opy_()
        }
    def bstack1l11111lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1111_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᖁ") in event:
            return self.bstack1lll11ll111_opy_()
        elif bstack1111_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᖂ") in event:
            return self.bstack1lll11lll11_opy_()
    def bstack1l111111l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1lll11lllll_opy_ = time if time else bstack1ll1ll1l11_opy_()
        self.duration = duration if duration else bstack111ll111ll_opy_(self.bstack1l111l111l_opy_, self.bstack1lll11lllll_opy_)
        if result:
            self.result = result
class bstack11ll1lll1l_opy_(bstack1l1111lll1_opy_):
    def __init__(self, hooks=[], bstack11lll111ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11lll111ll_opy_ = bstack11lll111ll_opy_
        super().__init__(*args, **kwargs, bstack111ll11l1_opy_=bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࠪᖃ"))
    @classmethod
    def bstack1lll1l11ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111_opy_ (u"࠭ࡩࡥࠩᖄ"): id(step),
                bstack1111_opy_ (u"ࠧࡵࡧࡻࡸࠬᖅ"): step.name,
                bstack1111_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᖆ"): step.keyword,
            })
        return bstack11ll1lll1l_opy_(
            **kwargs,
            meta={
                bstack1111_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᖇ"): {
                    bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨᖈ"): feature.name,
                    bstack1111_opy_ (u"ࠫࡵࡧࡴࡩࠩᖉ"): feature.filename,
                    bstack1111_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᖊ"): feature.description
                },
                bstack1111_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᖋ"): {
                    bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᖌ"): scenario.name
                },
                bstack1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᖍ"): steps,
                bstack1111_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᖎ"): bstack1lll1llll11_opy_(test)
            }
        )
    def bstack1lll11llll1_opy_(self):
        return {
            bstack1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᖏ"): self.hooks
        }
    def bstack1lll11l1ll1_opy_(self):
        if self.bstack11lll111ll_opy_:
            return {
                bstack1111_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᖐ"): self.bstack11lll111ll_opy_
            }
        return {}
    def bstack1lll11lll11_opy_(self):
        return {
            **super().bstack1lll11lll11_opy_(),
            **self.bstack1lll11llll1_opy_()
        }
    def bstack1lll11ll111_opy_(self):
        return {
            **super().bstack1lll11ll111_opy_(),
            **self.bstack1lll11l1ll1_opy_()
        }
    def bstack1l111111l1_opy_(self):
        return bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᖑ")
class bstack1l11111ll1_opy_(bstack1l1111lll1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack111ll11l1_opy_=bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᖒ"))
    def bstack11lll11lll_opy_(self):
        return self.hook_type
    def bstack1lll1l11l11_opy_(self):
        return {
            bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᖓ"): self.hook_type
        }
    def bstack1lll11lll11_opy_(self):
        return {
            **super().bstack1lll11lll11_opy_(),
            **self.bstack1lll1l11l11_opy_()
        }
    def bstack1lll11ll111_opy_(self):
        return {
            **super().bstack1lll11ll111_opy_(),
            **self.bstack1lll1l11l11_opy_()
        }
    def bstack1l111111l1_opy_(self):
        return bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᖔ")