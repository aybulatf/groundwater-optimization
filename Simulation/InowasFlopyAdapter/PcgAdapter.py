import flopy.modflow as mf


class PcgAdapter:
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
        return mf.ModflowPcg(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "mxiter": 50,
            "iter1": 30,
            "npcond": 1,
            "hclose": 1E-5,
            "rclose": 1E-5,
            "relax": 1.0,
            "nbpol": 0,
            "iprpcg": 0,
            "mutpcg": 3,
            "damp": 1.0,
            "dampt": 1.0,
            "ihcofadd": 0,
            "extension": 'pcg',
            "unitnumber": 27
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "mxiter": package.mxiter,
            "iter1": package.iter1,
            "npcond": package.npcond,
            "hclose": package.hclose,
            "rclose": package.rclose,
            "relax": package.relax,
            "nbpol": package.nbpol,
            "iprpcg": package.iprpcg,
            "mutpcg": package.mutpcg,
            "damp": package.damp,
            "dampt": package.dampt,
            "ihcofadd": package.ihcofadd,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
