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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11ll111l_opy_, bstack1ll1l11l11_opy_
class bstack1l1l11l11l_opy_:
  working_dir = os.getcwd()
  bstack1ll11l111l_opy_ = False
  config = {}
  binary_path = bstack1111_opy_ (u"ࠫࠬᑣ")
  bstack1lllll11111_opy_ = bstack1111_opy_ (u"ࠬ࠭ᑤ")
  bstack1l111ll1ll_opy_ = False
  bstack1llllllllll_opy_ = None
  bstack1111111ll1_opy_ = {}
  bstack1llllll1111_opy_ = 300
  bstack1lllll111l1_opy_ = False
  logger = None
  bstack1lllll1llll_opy_ = False
  bstack111111111l_opy_ = bstack1111_opy_ (u"࠭ࠧᑥ")
  bstack111111ll1l_opy_ = {
    bstack1111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᑦ") : 1,
    bstack1111_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩᑧ") : 2,
    bstack1111_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᑨ") : 3,
    bstack1111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᑩ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111l11l1_opy_(self):
    bstack11111111ll_opy_ = bstack1111_opy_ (u"ࠫࠬᑪ")
    bstack1lllll11l1l_opy_ = sys.platform
    bstack1lllll111ll_opy_ = bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᑫ")
    if re.match(bstack1111_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨᑬ"), bstack1lllll11l1l_opy_) != None:
      bstack11111111ll_opy_ = bstack11l111lll1_opy_ + bstack1111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣᑭ")
      self.bstack111111111l_opy_ = bstack1111_opy_ (u"ࠨ࡯ࡤࡧࠬᑮ")
    elif re.match(bstack1111_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢᑯ"), bstack1lllll11l1l_opy_) != None:
      bstack11111111ll_opy_ = bstack11l111lll1_opy_ + bstack1111_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦᑰ")
      bstack1lllll111ll_opy_ = bstack1111_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢᑱ")
      self.bstack111111111l_opy_ = bstack1111_opy_ (u"ࠬࡽࡩ࡯ࠩᑲ")
    else:
      bstack11111111ll_opy_ = bstack11l111lll1_opy_ + bstack1111_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤᑳ")
      self.bstack111111111l_opy_ = bstack1111_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᑴ")
    return bstack11111111ll_opy_, bstack1lllll111ll_opy_
  def bstack1llllll111l_opy_(self):
    try:
      bstack1lllll1l1ll_opy_ = [os.path.join(expanduser(bstack1111_opy_ (u"ࠣࢀࠥᑵ")), bstack1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᑶ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lllll1l1ll_opy_:
        if(self.bstack1lllllll11l_opy_(path)):
          return path
      raise bstack1111_opy_ (u"࡙ࠥࡳࡧ࡬ࡣࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᑷ")
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨᑸ").format(e))
  def bstack1lllllll11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lllll1ll11_opy_(self, bstack11111111ll_opy_, bstack1lllll111ll_opy_):
    try:
      bstack1lllll11l11_opy_ = self.bstack1llllll111l_opy_()
      bstack1lllll11ll1_opy_ = os.path.join(bstack1lllll11l11_opy_, bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨᑹ"))
      bstack111111l11l_opy_ = os.path.join(bstack1lllll11l11_opy_, bstack1lllll111ll_opy_)
      if os.path.exists(bstack111111l11l_opy_):
        self.logger.info(bstack1111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᑺ").format(bstack111111l11l_opy_))
        return bstack111111l11l_opy_
      if os.path.exists(bstack1lllll11ll1_opy_):
        self.logger.info(bstack1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧᑻ").format(bstack1lllll11ll1_opy_))
        return self.bstack111111lll1_opy_(bstack1lllll11ll1_opy_, bstack1lllll111ll_opy_)
      self.logger.info(bstack1111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨᑼ").format(bstack11111111ll_opy_))
      response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"ࠩࡊࡉ࡙࠭ᑽ"), bstack11111111ll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lllll11ll1_opy_, bstack1111_opy_ (u"ࠪࡻࡧ࠭ᑾ")) as file:
          file.write(response.content)
        self.logger.info(bstack1111_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤᑿ").format(bstack1lllll11ll1_opy_))
        return self.bstack111111lll1_opy_(bstack1lllll11ll1_opy_, bstack1lllll111ll_opy_)
      else:
        raise(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣᒀ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᒁ").format(e))
  def bstack1lllll1l111_opy_(self, bstack11111111ll_opy_, bstack1lllll111ll_opy_):
    try:
      retry = 2
      bstack111111l11l_opy_ = None
      bstack111111l1l1_opy_ = False
      while retry > 0:
        bstack111111l11l_opy_ = self.bstack1lllll1ll11_opy_(bstack11111111ll_opy_, bstack1lllll111ll_opy_)
        bstack111111l1l1_opy_ = self.bstack1lllllll111_opy_(bstack11111111ll_opy_, bstack1lllll111ll_opy_, bstack111111l11l_opy_)
        if bstack111111l1l1_opy_:
          break
        retry -= 1
      return bstack111111l11l_opy_, bstack111111l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᒂ").format(e))
    return bstack111111l11l_opy_, False
  def bstack1lllllll111_opy_(self, bstack11111111ll_opy_, bstack1lllll111ll_opy_, bstack111111l11l_opy_, bstack1111111111_opy_ = 0):
    if bstack1111111111_opy_ > 1:
      return False
    if bstack111111l11l_opy_ == None or os.path.exists(bstack111111l11l_opy_) == False:
      self.logger.warn(bstack1111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᒃ"))
      return False
    bstack111111l1ll_opy_ = bstack1111_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢᒄ")
    command = bstack1111_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩᒅ").format(bstack111111l11l_opy_)
    bstack11111l11ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111111l1ll_opy_, bstack11111l11ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥᒆ"))
      return False
  def bstack111111lll1_opy_(self, bstack1lllll11ll1_opy_, bstack1lllll111ll_opy_):
    try:
      working_dir = os.path.dirname(bstack1lllll11ll1_opy_)
      shutil.unpack_archive(bstack1lllll11ll1_opy_, working_dir)
      bstack111111l11l_opy_ = os.path.join(working_dir, bstack1lllll111ll_opy_)
      os.chmod(bstack111111l11l_opy_, 0o755)
      return bstack111111l11l_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᒇ"))
  def bstack1111111lll_opy_(self):
    try:
      percy = str(self.config.get(bstack1111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᒈ"), bstack1111_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨᒉ"))).lower()
      if percy != bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨᒊ"):
        return False
      self.bstack1l111ll1ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᒋ").format(e))
  def bstack1llllll11ll_opy_(self):
    try:
      bstack1llllll11ll_opy_ = str(self.config.get(bstack1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᒌ"), bstack1111_opy_ (u"ࠦࡦࡻࡴࡰࠤᒍ"))).lower()
      return bstack1llllll11ll_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᒎ").format(e))
  def init(self, bstack1ll11l111l_opy_, config, logger):
    self.bstack1ll11l111l_opy_ = bstack1ll11l111l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111111lll_opy_():
      return
    self.bstack1111111ll1_opy_ = config.get(bstack1111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᒏ"), {})
    self.bstack1111111l1l_opy_ = config.get(bstack1111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᒐ"), bstack1111_opy_ (u"ࠣࡣࡸࡸࡴࠨᒑ"))
    try:
      bstack11111111ll_opy_, bstack1lllll111ll_opy_ = self.bstack11111l11l1_opy_()
      bstack111111l11l_opy_, bstack111111l1l1_opy_ = self.bstack1lllll1l111_opy_(bstack11111111ll_opy_, bstack1lllll111ll_opy_)
      if bstack111111l1l1_opy_:
        self.binary_path = bstack111111l11l_opy_
        thread = Thread(target=self.bstack111111ll11_opy_)
        thread.start()
      else:
        self.bstack1lllll1llll_opy_ = True
        self.logger.error(bstack1111_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᒒ").format(bstack111111l11l_opy_))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᒓ").format(e))
  def bstack11111l111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1111_opy_ (u"ࠫࡱࡵࡧࠨᒔ"), bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᒕ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1111_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᒖ").format(logfile))
      self.bstack1lllll11111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᒗ").format(e))
  def bstack111111ll11_opy_(self):
    bstack1lllll11lll_opy_ = self.bstack1llllll11l1_opy_()
    if bstack1lllll11lll_opy_ == None:
      self.bstack1lllll1llll_opy_ = True
      self.logger.error(bstack1111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᒘ"))
      return False
    command_args = [bstack1111_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᒙ") if self.bstack1ll11l111l_opy_ else bstack1111_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᒚ")]
    bstack1llllll1ll1_opy_ = self.bstack1llllllll1l_opy_()
    if bstack1llllll1ll1_opy_ != None:
      command_args.append(bstack1111_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᒛ").format(bstack1llllll1ll1_opy_))
    env = os.environ.copy()
    env[bstack1111_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᒜ")] = bstack1lllll11lll_opy_
    bstack1llllll1lll_opy_ = [self.binary_path]
    self.bstack11111l111l_opy_()
    self.bstack1llllllllll_opy_ = self.bstack111111l111_opy_(bstack1llllll1lll_opy_ + command_args, env)
    self.logger.debug(bstack1111_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᒝ"))
    bstack1111111111_opy_ = 0
    while self.bstack1llllllllll_opy_.poll() == None:
      bstack1lllll1ll1l_opy_ = self.bstack1llllll1l1l_opy_()
      if bstack1lllll1ll1l_opy_:
        self.logger.debug(bstack1111_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᒞ"))
        self.bstack1lllll111l1_opy_ = True
        return True
      bstack1111111111_opy_ += 1
      self.logger.debug(bstack1111_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᒟ").format(bstack1111111111_opy_))
      time.sleep(2)
    self.logger.error(bstack1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᒠ").format(bstack1111111111_opy_))
    self.bstack1lllll1llll_opy_ = True
    return False
  def bstack1llllll1l1l_opy_(self, bstack1111111111_opy_ = 0):
    try:
      if bstack1111111111_opy_ > 10:
        return False
      bstack11111l1111_opy_ = os.environ.get(bstack1111_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᒡ"), bstack1111_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᒢ"))
      bstack1lllll1lll1_opy_ = bstack11111l1111_opy_ + bstack11l11l111l_opy_
      response = requests.get(bstack1lllll1lll1_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1llllll11l1_opy_(self):
    bstack11111111l1_opy_ = bstack1111_opy_ (u"ࠬࡧࡰࡱࠩᒣ") if self.bstack1ll11l111l_opy_ else bstack1111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᒤ")
    bstack111l1l1lll_opy_ = bstack1111_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠨᒥ").format(self.config[bstack1111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᒦ")], bstack11111111l1_opy_)
    uri = bstack1l11ll111l_opy_(bstack111l1l1lll_opy_)
    try:
      response = bstack1ll1l11l11_opy_(bstack1111_opy_ (u"ࠩࡊࡉ࡙࠭ᒧ"), uri, {}, {bstack1111_opy_ (u"ࠪࡥࡺࡺࡨࠨᒨ"): (self.config[bstack1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᒩ")], self.config[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᒪ")])})
      if response.status_code == 200:
        bstack111111llll_opy_ = response.json()
        if bstack1111_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᒫ") in bstack111111llll_opy_:
          return bstack111111llll_opy_[bstack1111_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᒬ")]
        else:
          raise bstack1111_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨᒭ").format(bstack111111llll_opy_)
      else:
        raise bstack1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᒮ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᒯ").format(e))
  def bstack1llllllll1l_opy_(self):
    bstack1llllllll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᒰ"))
    try:
      if bstack1111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᒱ") not in self.bstack1111111ll1_opy_:
        self.bstack1111111ll1_opy_[bstack1111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᒲ")] = 2
      with open(bstack1llllllll11_opy_, bstack1111_opy_ (u"ࠧࡸࠩᒳ")) as fp:
        json.dump(self.bstack1111111ll1_opy_, fp)
      return bstack1llllllll11_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᒴ").format(e))
  def bstack111111l111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111111111l_opy_ == bstack1111_opy_ (u"ࠩࡺ࡭ࡳ࠭ᒵ"):
        bstack1lllllll1l1_opy_ = [bstack1111_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫᒶ"), bstack1111_opy_ (u"ࠫ࠴ࡩࠧᒷ")]
        cmd = bstack1lllllll1l1_opy_ + cmd
      cmd = bstack1111_opy_ (u"ࠬࠦࠧᒸ").join(cmd)
      self.logger.debug(bstack1111_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥᒹ").format(cmd))
      with open(self.bstack1lllll11111_opy_, bstack1111_opy_ (u"ࠢࡢࠤᒺ")) as bstack1lllll1l11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lllll1l11l_opy_, text=True, stderr=bstack1lllll1l11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lllll1llll_opy_ = True
      self.logger.error(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᒻ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lllll111l1_opy_:
        self.logger.info(bstack1111_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥᒼ"))
        cmd = [self.binary_path, bstack1111_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨᒽ")]
        self.bstack111111l111_opy_(cmd)
        self.bstack1lllll111l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᒾ").format(cmd, e))
  def bstack11l1111l1_opy_(self):
    if not self.bstack1l111ll1ll_opy_:
      return
    try:
      bstack1111111l11_opy_ = 0
      while not self.bstack1lllll111l1_opy_ and bstack1111111l11_opy_ < self.bstack1llllll1111_opy_:
        if self.bstack1lllll1llll_opy_:
          self.logger.info(bstack1111_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᒿ"))
          return
        time.sleep(1)
        bstack1111111l11_opy_ += 1
      os.environ[bstack1111_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᓀ")] = str(self.bstack1lllllllll1_opy_())
      self.logger.info(bstack1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᓁ"))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᓂ").format(e))
  def bstack1lllllllll1_opy_(self):
    if self.bstack1ll11l111l_opy_:
      return
    try:
      bstack1lllll1111l_opy_ = [platform[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᓃ")].lower() for platform in self.config.get(bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᓄ"), [])]
      bstack1llllll1l11_opy_ = sys.maxsize
      bstack1lllll1l1l1_opy_ = bstack1111_opy_ (u"ࠫࠬᓅ")
      for browser in bstack1lllll1111l_opy_:
        if browser in self.bstack111111ll1l_opy_:
          bstack1lllllll1ll_opy_ = self.bstack111111ll1l_opy_[browser]
        if bstack1lllllll1ll_opy_ < bstack1llllll1l11_opy_:
          bstack1llllll1l11_opy_ = bstack1lllllll1ll_opy_
          bstack1lllll1l1l1_opy_ = browser
      return bstack1lllll1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᓆ").format(e))