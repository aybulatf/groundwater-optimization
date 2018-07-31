import flopy.mt3d as mt


class AdvAdapter:
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
        return mt.Mt3dAdv(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "mixelm": 3,
            "percel": 0.75,
            "mxpart": 800000,
            "nadvfd": 1,
            "itrack": 3,
            "wd": 0.5,
            "dceps": 1e-05,
            "nplane": 2,
            "npl": 10,
            "nph": 40,
            "npmin": 5,
            "npmax": 80,
            "nlsink": 0,
            "npsink": 15,
            "dchmoc": 0.0001,
            "extension": 'adv',
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "mixelm": package.mixelm,
            "percel": package.percel,
            "mxpart": package.mxpart,
            "nadvfd": package.nadvfd,
            "itrack": package.itrack,  # None
            "wd": package.wd,  # None
            "dceps": package.dceps,  # None
            "nplane": package.nplane,  # None
            "npl": package.npl,  # None
            "nph": package.nph,  # None
            "npmin": package.npmin,  # None
            "npmax": package.npmax,  # None
            "nlsink": package.nlsink,  # None
            "npsink": package.npsink,  # None
            "dchmoc": package.dchmoc,  # None
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0],
            # "filenames": package.filenames
        }
        return content
