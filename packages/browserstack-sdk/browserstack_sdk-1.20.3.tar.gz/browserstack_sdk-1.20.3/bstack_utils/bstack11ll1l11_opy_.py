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
class bstack11l1l11l1l_opy_(object):
  bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠬࢄࠧ༏")), bstack1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭༐"))
  bstack11l1l11111_opy_ = os.path.join(bstack11l11111l_opy_, bstack1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧ༑"))
  bstack11l1l11l11_opy_ = None
  perform_scan = None
  bstack111llll11_opy_ = None
  bstack1111l1111_opy_ = None
  bstack11l1lll11l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1111_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪ༒")):
      cls.instance = super(bstack11l1l11l1l_opy_, cls).__new__(cls)
      cls.instance.bstack11l1l111l1_opy_()
    return cls.instance
  def bstack11l1l111l1_opy_(self):
    try:
      with open(self.bstack11l1l11111_opy_, bstack1111_opy_ (u"ࠩࡵࠫ༓")) as bstack1lll11l11l_opy_:
        bstack11l1l111ll_opy_ = bstack1lll11l11l_opy_.read()
        data = json.loads(bstack11l1l111ll_opy_)
        if bstack1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ༔") in data:
          self.bstack11l1ll1lll_opy_(data[bstack1111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭༕")])
        if bstack1111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭༖") in data:
          self.bstack11l1l1ll1l_opy_(data[bstack1111_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ༗")])
    except:
      pass
  def bstack11l1l1ll1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1111_opy_ (u"ࠧࡴࡥࡤࡲ༘ࠬ")]
      self.bstack111llll11_opy_ = scripts[bstack1111_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷ༙ࠬ")]
      self.bstack1111l1111_opy_ = scripts[bstack1111_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭༚")]
      self.bstack11l1lll11l_opy_ = scripts[bstack1111_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨ༛")]
  def bstack11l1ll1lll_opy_(self, bstack11l1l11l11_opy_):
    if bstack11l1l11l11_opy_ != None and len(bstack11l1l11l11_opy_) != 0:
      self.bstack11l1l11l11_opy_ = bstack11l1l11l11_opy_
  def store(self):
    try:
      with open(self.bstack11l1l11111_opy_, bstack1111_opy_ (u"ࠫࡼ࠭༜")) as file:
        json.dump({
          bstack1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ༝"): self.bstack11l1l11l11_opy_,
          bstack1111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ༞"): {
            bstack1111_opy_ (u"ࠢࡴࡥࡤࡲࠧ༟"): self.perform_scan,
            bstack1111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ༠"): self.bstack111llll11_opy_,
            bstack1111_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ༡"): self.bstack1111l1111_opy_,
            bstack1111_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ༢"): self.bstack11l1lll11l_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll111l1l_opy_(self, bstack11l1l1111l_opy_):
    try:
      return any(command.get(bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ༣")) == bstack11l1l1111l_opy_ for command in self.bstack11l1l11l11_opy_)
    except:
      return False
bstack11ll1l11_opy_ = bstack11l1l11l1l_opy_()