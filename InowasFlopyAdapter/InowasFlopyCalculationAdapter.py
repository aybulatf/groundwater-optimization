"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format.

Author: Ralf Junghanns
EMail: ralf.junghanns@gmail.com
"""

from .BasAdapter import BasAdapter
from .ChdAdapter import ChdAdapter
from .DisAdapter import DisAdapter
from .GhbAdapter import GhbAdapter
from .LpfAdapter import LpfAdapter
from .MfAdapter import MfAdapter
from .NwtAdapter import NwtAdapter
from .OcAdapter import OcAdapter
from .PcgAdapter import PcgAdapter
from .RchAdapter import RchAdapter
from .RivAdapter import RivAdapter
from .ReadBudget import ReadBudget
from .ReadDrawdown import ReadDrawdown
from .ReadHead import ReadHead
from .UpwAdapter import UpwAdapter
from .WelAdapter import WelAdapter
from .LmtAdapter import LmtAdapter
from .MtAdapter import MtAdapter
from .AdvAdapter import AdvAdapter
from .BtnAdapter import BtnAdapter
from .DspAdapter import DspAdapter
from .GcgAdapter import GcgAdapter
from .LktAdapter import LktAdapter
from .PhcAdapter import PhcAdapter
from .RctAdapter import RctAdapter
from .SftAdapter import SftAdapter
from .SsmAdapter import SsmAdapter
from .TobAdapter import TobAdapter
from .UztAdapter import UztAdapter


class InowasFlopyCalculationAdapter:
    """The Flopy Class"""

    _version = None
    _uuid = None
    _mf = None
    _mt = None
    _report = ''

    mf_package_order = [
        'mf', 'dis', 'bas', 'bas6',
        'riv', 'wel', 'rch', 'chd', 'ghb',
        'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6'
    ]

    mt_package_order = [
        "mt", "btn", "adv", "dsp", "gcg", "ssm", "lkt",
        "phc", "rct", "sft", "tob", "uzt"
    ]

    def __init__(self, version, data, uuid):
        self._mf_data = data.get("mf")
        self._mt_data = data.get("mt")
        self._version = version
        self._uuid = uuid

        if self._mf_data is not None:
            package_content = self.read_packages(self._mf_data)
            self.create_model(self.mf_package_order, package_content)

            if self._mf_data.get("write_input"):
                self.write_input_model(self._mf)

            if self._mf_data.get("run_model"):
                self._report += self.run_model(self._mf)

            if self._mt_data is not None:
                package_content = self.read_packages(self._mt_data)
                self.create_model(self.mt_package_order, package_content)

                if self._mt_data.get("write_input"):
                    self.write_input_model(self._mt)

                if self._mt_data.get("run_model"):
                    self._report += self.run_model(self._mt)

    @staticmethod
    def read_packages(data):
        package_content = {}
        for package in data["packages"]:
            print('Read Flopy Package: %s' % package)
            package_content[package.lower()] = data[package]
        return package_content

    def create_model(self, package_order, package_content):
        for package in package_order:
            if package in package_content:
                print('Create Flopy Package: %s' % package)
                self.create_package(package, package_content[package])

    @staticmethod
    def write_input_model(model):
        print('Write %s input files' % model)
        model.write_input()

    @staticmethod
    def run_model(model):
        print('Run the %s model' % model)
        print(model.namefile)
        print(model.exe_name)
        success, report = model.run_model(report=True, silent=True)
        return ' \n'.join(str(e) for e in report + [success])

    def check_model(self):
        if self._mf is not None:
            self._mf.check()
        if self._mt is not None:
            self._mt.check()

    def create_package(self, name, content):
        # Modlfow packages
        if name == 'mf':
            self._mf = MfAdapter(content).get_package()
        if name == 'dis':
            DisAdapter(content).get_package(self._mf)
        if name == 'bas' or name == 'bas6':
            BasAdapter(content).get_package(self._mf)
        if name == 'lpf':
            LpfAdapter(content).get_package(self._mf)
        if name == 'upw':
            UpwAdapter(content).get_package(self._mf)
        if name == 'pcg':
            PcgAdapter(content).get_package(self._mf)
        if name == 'nwt':
            NwtAdapter(content).get_package(self._mf)
        if name == 'oc':
            OcAdapter(content).get_package(self._mf)
        if name == 'riv':
            RivAdapter(content).get_package(self._mf)
        if name == 'wel':
            WelAdapter(content).get_package(self._mf)
        if name == 'rch':
            RchAdapter(content).get_package(self._mf)
        if name == 'chd':
            ChdAdapter(content).get_package(self._mf)
        if name == 'ghb':
            GhbAdapter(content).get_package(self._mf)
        if name == 'lmt':
            LmtAdapter(content).get_package(self._mf)

        # MT3D packages
        if name == 'mt':
            self._mt = MtAdapter(content).get_package(self._mf)
        if name == 'adv':
            AdvAdapter(content).get_package(self._mt)
        if name == 'btn':
            BtnAdapter(content).get_package(self._mt)
        if name == 'dsp':
            DspAdapter(content).get_package(self._mt)
        if name == 'gcg':
            GcgAdapter(content).get_package(self._mt)
        if name == 'lkt':
            LktAdapter(content).get_package(self._mt)
        if name == 'phc':
            PhcAdapter(content).get_package(self._mt)
        if name == 'rct':
            RctAdapter(content).get_package(self._mt)
        if name == 'sft':
            SftAdapter(content).get_package(self._mt)
        if name == 'ssm':
            SsmAdapter(content).get_package(self._mt)
        if name == 'tob':
            TobAdapter(content).get_package(self._mt)
        if name == 'uzt':
            UztAdapter(content).get_package(self._mt)

    def response(self):
        key = 'mf'
        if 'MF' in self._mf_data:
            key = 'MF'

        heads = ReadHead(self._mf_data[key]['model_ws'])
        drawdowns = ReadDrawdown(self._mf_data[key]['model_ws'])
        budgets = ReadBudget(self._mf_data[key]['model_ws'])
        response = {}
        response['heads'] = heads.read_times()
        response['drawdowns'] = drawdowns.read_times()
        response['budgets'] = budgets.read_times()
        response['number_of_layers'] = heads.read_number_of_layers()

        return response

    def response_message(self):
        return self._report
