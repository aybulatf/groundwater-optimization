import flopy.modflow as mf


class LpfAdapter:
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

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowLpf(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "laytyp": 0,
            "layavg": 0,
            "chani": 1.0,
            "layvka": 0,
            "laywet": 0,
            "ipakcb": 53,
            "hdry": -1e+30,
            "iwdflg": 0,
            "wetfct": 0.1,
            "iwetit": 1,
            "ihdwet": 0,
            "hk": 1.0,
            "hani": 1.0,
            "vka": 1.0,
            "ss": 1e-5,
            "sy": 0.15,
            "vkcb": 0.0,
            "wetdry": -0.01,
            "storagecoefficient": False,
            "constantcv": False,
            "thickstrt": False,
            "nocvcorrection": False,
            "novfc": False,
            "extension": 'lpf',
            "unitnumber": 15
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "laytyp": package.laytyp.array.tolist(),
            "layavg": package.layavg.array.tolist(),
            "chani": package.chani.array.tolist(),
            "layvka": package.layvka.array.tolist(),
            "laywet": package.laywet.array.tolist(),
            "ipakcb": package.ipakcb,
            "hdry": package.hdry,
            # "iwdflg": package.iwdflg,
            "wetfct": package.wetfct,  # None
            "iwetit": package.iwetit,  # None
            "ihdwet": package.ihdwet,  # None
            "hk": package.hk.array.tolist(),
            "hani": package.hani.array.tolist(),
            "vka": package.vka.array.tolist(),
            "ss": package.ss.array.tolist(),
            "sy": package.sy.array.tolist(),
            "vkcb": package.vkcb.array.tolist(),
            "wetdry": package.wetdry.array.tolist(),
            # "storagecoefficient": package.storagecoefficient,
            # "constantcv": package.constantcv,
            # "thickstrt": package.thickstrt,
            # "nocvcorrection": package.nocvcorrection,
            # "novfc": package.novfc,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
