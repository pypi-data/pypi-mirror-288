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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l11l11l1_opy_, bstack11l111l1ll_opy_
import tempfile
import json
bstack11111lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧᏴ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1111_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᏵ"),
      datefmt=bstack1111_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ᏶"),
      stream=sys.stdout
    )
  return logger
def bstack11111lll1l_opy_():
  global bstack11111lll11_opy_
  if os.path.exists(bstack11111lll11_opy_):
    os.remove(bstack11111lll11_opy_)
def bstack111111111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1lll1ll1_opy_(config, log_level):
  bstack11111ll11l_opy_ = log_level
  if bstack1111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᏷") in config and config[bstack1111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᏸ")] in bstack11l11l11l1_opy_:
    bstack11111ll11l_opy_ = bstack11l11l11l1_opy_[config[bstack1111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᏹ")]]
  if config.get(bstack1111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᏺ"), False):
    logging.getLogger().setLevel(bstack11111ll11l_opy_)
    return bstack11111ll11l_opy_
  global bstack11111lll11_opy_
  bstack111111111_opy_()
  bstack11111ll1l1_opy_ = logging.Formatter(
    fmt=bstack1111_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᏻ"),
    datefmt=bstack1111_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨᏼ")
  )
  bstack1111l11ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11111lll11_opy_)
  file_handler.setFormatter(bstack11111ll1l1_opy_)
  bstack1111l11ll1_opy_.setFormatter(bstack11111ll1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111l11ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩᏽ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111l11ll1_opy_.setLevel(bstack11111ll11l_opy_)
  logging.getLogger().addHandler(bstack1111l11ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11111ll11l_opy_
def bstack11111ll1ll_opy_(config):
  try:
    bstack1111l1111l_opy_ = set(bstack11l111l1ll_opy_)
    bstack1111l11l11_opy_ = bstack1111_opy_ (u"ࠨࠩ᏾")
    with open(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ᏿")) as bstack1111l111ll_opy_:
      bstack1111l11l1l_opy_ = bstack1111l111ll_opy_.read()
      bstack1111l11l11_opy_ = re.sub(bstack1111_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫ᐀"), bstack1111_opy_ (u"ࠫࠬᐁ"), bstack1111l11l1l_opy_, flags=re.M)
      bstack1111l11l11_opy_ = re.sub(
        bstack1111_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨᐂ") + bstack1111_opy_ (u"࠭ࡼࠨᐃ").join(bstack1111l1111l_opy_) + bstack1111_opy_ (u"ࠧࠪ࠰࠭ࠨࠬᐄ"),
        bstack1111_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᐅ"),
        bstack1111l11l11_opy_, flags=re.M | re.I
      )
    def bstack11111llll1_opy_(dic):
      bstack1111l111l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111l1111l_opy_:
          bstack1111l111l1_opy_[key] = bstack1111_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᐆ")
        else:
          if isinstance(value, dict):
            bstack1111l111l1_opy_[key] = bstack11111llll1_opy_(value)
          else:
            bstack1111l111l1_opy_[key] = value
      return bstack1111l111l1_opy_
    bstack1111l111l1_opy_ = bstack11111llll1_opy_(config)
    return {
      bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᐇ"): bstack1111l11l11_opy_,
      bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᐈ"): json.dumps(bstack1111l111l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll11ll1_opy_(config):
  global bstack11111lll11_opy_
  try:
    if config.get(bstack1111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᐉ"), False):
      return
    uuid = os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᐊ"))
    if not uuid or uuid == bstack1111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᐋ"):
      return
    bstack11111lllll_opy_ = [bstack1111_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫᐌ"), bstack1111_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪᐍ"), bstack1111_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫᐎ"), bstack11111lll11_opy_]
    bstack111111111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪᐏ") + uuid + bstack1111_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ᐐ"))
    with tarfile.open(output_file, bstack1111_opy_ (u"ࠨࡷ࠻ࡩࡽࠦᐑ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11111lllll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11111ll1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111l11111_opy_ = data.encode()
        tarinfo.size = len(bstack1111l11111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111l11111_opy_))
    bstack1l1l11l111_opy_ = MultipartEncoder(
      fields= {
        bstack1111_opy_ (u"ࠧࡥࡣࡷࡥࠬᐒ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1111_opy_ (u"ࠨࡴࡥࠫᐓ")), bstack1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧᐔ")),
        bstack1111_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᐕ"): uuid
      }
    )
    response = requests.post(
      bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨᐖ"),
      data=bstack1l1l11l111_opy_,
      headers={bstack1111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᐗ"): bstack1l1l11l111_opy_.content_type},
      auth=(config[bstack1111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᐘ")], config[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᐙ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧᐚ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨᐛ") + str(e))
  finally:
    try:
      bstack11111lll1l_opy_()
    except:
      pass