import numpy as np
import flopy.mt3d as mt


class BtnAdapter:
    _data = None

    def __init__(self, data):
        self._data = data

    def validate(self):
        # should be implemented
        # for key in content:
        #   do something
        #   return some hints
        pass

    def is_valid(self):
        # should be implemented
        # for key in content:
        #   do something
        #   return true or false
        return True

    def merge(self):
        default = self.default()
        for key in self._data:
            default[key] = self._data[key]
        return default

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dBtn(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "MFStyleArr": False,
            "DRYCell": False,
            "Legacy99Stor": False,
            "FTLPrint": False,
            "NoWetDryPrint": False,
            "OmitDryBud": False,
            "AltWTSorb": False,
            "nlay": None,
            "nrow": None,
            "ncol": None,
            "nper": None,
            "ncomp": 1,
            "mcomp": 1,
            "tunit": 'D',
            "lunit": 'M',
            "munit": 'KG',
            "laycon": None,
            "delr": None,
            "delc": None,
            "htop": None,
            "dz": None,
            "prsity": 0.3,
            "icbund": 1,
            "sconc": 0.0,
            "cinact": 1e+30,
            "thkmin": 0.01,
            "ifmtcn": 0,
            "ifmtnp": 0,
            "ifmtrf": 0,
            "ifmtdp": 0,
            "savucn": True,
            "nprs": 0,
            "timprs": None,
            "obs": None,
            "nprobs": 1,
            "chkmas": True,
            "nprmas": 1,
            "perlen": None,
            "nstp": None,
            "tsmult": None,
            "ssflag": None,
            "dt0": 0,
            "mxstrn": 50000,
            "ttsmult": 1.0,
            "ttsmax": 0,
            "species_names": None,
            "extension": 'btn',
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "MFStyleArr": package.MFStyleArr,
            "DRYCell": package.DRYCell,
            "Legacy99Stor": package.Legacy99Stor,
            "FTLPrint": package.FTLPrint,
            "NoWetDryPrint": package.NoWetDryPrint,
            "OmitDryBud": package.OmitDryBud,
            "AltWTSorb": package.AltWTSorb,
            "nlay": package.nlay,
            "nrow": package.nrow,
            "ncol": package.ncol,
            "nper": package.nper,
            "ncomp": package.ncomp,
            "mcomp": package.mcomp,
            "tunit": package.tunit,
            "lunit": package.lunit,
            "munit": package.munit,
            "laycon": package.laycon.array.tolist(),
            "delr": np.reshape(package.delr.array, (len(package.delr.array),)).tolist(),
            "delc": np.reshape(package.delc.array, (len(package.delc.array),)).tolist(),
            "htop": package.htop.array.tolist(),
            "dz": package.dz.array.tolist(),
            "prsity": package.prsity.array.tolist(),
            "icbund": package.icbund.array.tolist(),
            "sconc": [i.array.tolist() for i in package.sconc],
            "cinact": package.cinact,
            "thkmin": package.thkmin,
            "ifmtcn": package.ifmtcn,
            "ifmtnp": package.ifmtnp,
            "ifmtrf": package.ifmtrf,
            "ifmtdp": package.ifmtdp,
            "savucn": package.savucn,
            "nprs": package.nprs,
            "timprs": package.timprs,  # None
            "obs": package.obs,  # None
            "nprobs": package.nprobs,
            "chkmas": package.chkmas,
            "nprmas": package.nprmas,
            "perlen": package.perlen.array.tolist(),
            "nstp": package.nstp.array.tolist(),
            "tsmult": package.tsmult.array.tolist(),
            # "ssflag": package.ssflag,
            "dt0": package.dt0.array.tolist(),
            "mxstrn": package.mxstrn.array.tolist(),
            "ttsmult": package.ttsmult.array.tolist(),
            "ttsmax": package.ttsmax.array.tolist(),
            "species_names": package.species_names if package.species_names else None,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0],
            # "filenames": package.filenames
        }
        return content
