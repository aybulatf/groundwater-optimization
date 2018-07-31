import flopy.mt3d as mt


class RctAdapter:
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
        return mt.Mt3dRct(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "isothm": 0,
            "ireact": 0,
            "igetsc": 1,
            "rhob": None,
            "prsity2": None,
            "srconc": None,
            "sp1": None,
            "sp2": None,
            "rc1": None,
            "rc2": None,
            "extension": 'rct',
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "isothm": package.isothm,
            "ireact": package.ireact,
            "igetsc": package.igetsc,
            "rhob": package.rhob,
            "prsity2": package.prsity2,
            "srconc": package.srconc,
            "sp1": package.sp1,
            "sp2": package.sp2,
            "rc1": package.rc1,
            "rc2": package.rc2,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames
        }
        return content
