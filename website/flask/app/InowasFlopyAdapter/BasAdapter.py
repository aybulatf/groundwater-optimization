import flopy.modflow as mf


class BasAdapter:
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
        return mf.ModflowBas(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ibound": 1,
            "strt": 1.0,
            "ifrefm": True,
            "ixsec": False,
            "ichflg": False,
            "stoper": None,
            "hnoflo": -999.99,
            "extension": 'bas',
            "unitnumber": 13
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "ibound": package.ibound.array.tolist(),
            "strt": package.strt.array.tolist(),
            "ifrefm": package.ifrefm,
            "ixsec": package.ixsec,
            "ichflg": package.ichflg,
            "stoper": package.stoper,
            "hnoflo": package.hnoflo,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
