import os
import sys
import json
import numpy as np
import flopy

"""
Create test data including Modflow, Mt3dms models and optimization problem
"""

nlay, nrow, ncol = 1, 90, 90
nper = 10
perlen = [30]*int(nper)
nstp = [1]*int(nper)

ibound = np.ones((nlay,nrow,ncol), dtype=np.int)

botm = -50.
top = 0.
hk = 2.5
ss = 0.0002
sy = 0.1


half_of_grid = np.hstack((
    np.ones(2)*1000,
    np.ones(1)*300,
    np.ones(42)*5
    ))

delr = np.hstack((half_of_grid, np.flipud(half_of_grid)))
delc = np.hstack((half_of_grid, np.flipud(half_of_grid)))
model_ws = './createModel_output'
mf_modelname = 'mf'
mt_modelname = 'mt'

oc_spd = {}

mf = flopy.modflow.Modflow(mf_modelname, model_ws=model_ws, exe_name='mf2005')
dis = flopy.modflow.ModflowDis(mf, nlay=nlay, nrow=nrow, ncol=ncol, nstp=nstp,
                               perlen=perlen, nper=nper, botm=botm, top=top,
                               steady=False, delr=delr, delc=delc)
bas = flopy.modflow.ModflowBas(mf, ibound=ibound, strt=top)
lpf = flopy.modflow.ModflowLpf(mf, hk=hk, vka=hk, ss=ss, sy=sy)
oc = flopy.modflow.ModflowOc(mf)
pcg = flopy.modflow.ModflowPcg(mf)
lmt = flopy.modflow.ModflowLmt(mf, output_file_name='mt3d_link.ftl',
                               output_file_format='unformatted', output_file_header='extended')

itype = flopy.mt3d.Mt3dSsm.itype_dict()

ssm_data = {}
chd_data = {}
wel_data = {}
for j in range(nper):
    chd_data[j] = []
    ssm_data[j] = []
    wel_data[j] = []

for i in range(nrow):
    for j in range(nper):
        chd_data[j].append((0, i, 0, -7.5, -7.5))
        chd_data[j].append((0, i, ncol-1, 7.5, 7.5))
        ssm_data[j].append((0, i, 0, 1.9, itype['CHD']))
        ssm_data[j].append((0, i, ncol-1, 1.9, itype['CHD']))

chd = flopy.modflow.ModflowChd(mf, stress_period_data=chd_data)

wel_data[0].append((0,45,45, -100))
wel_data[1].append((0,45,45, -100))
wel_data[2].append((0,45,45, -100))
wel_data[3].append((0,45,45, -100))
wel_data[4].append((0,45,45, -100))
wel_data[5].append((0,45,45, -100))
wel_data[6].append((0,45,45, -100))
wel_data[7].append((0,45,45, -100))
wel_data[8].append((0,45,45, -100))
wel_data[9].append((0,45,45, -100))


wel = flopy.modflow.ModflowWel(mf, stress_period_data=wel_data)

for i in range(nper):
    ssm_data[i].append((0, 45, 45, 0, itype['WEL']))

mt = flopy.mt3d.Mt3dms(modflowmodel=mf, modelname=mt_modelname, model_ws=model_ws,
                       ftlfilename='mt3d_link.ftl', exe_name='mt3dusgs')

btn = flopy.mt3d.Mt3dBtn(mt, sconc=1.9, ncomp=1, mcomp=1, dt0=30, nprs=-1)
adv = flopy.mt3d.Mt3dAdv(mt, mixelm=0)
dsp = flopy.mt3d.Mt3dDsp(mt, al=5., trpt=0.1, dmcoef=1e-9)
ssm = flopy.mt3d.Mt3dSsm(mt, stress_period_data=ssm_data)
gcg = flopy.mt3d.Mt3dGcg(mt, iter1=100)


mf.write_input()
mf.run_model()
mt.write_input()
mt.run_model()

# Make json

model_input_ga = {
    "author": "Aybulat F",
    "project": "Test model with Mt3d",
    "type": "optimization",
    "version": "3.2.6",
    "model_id": "test_model_id",
    "calculation_id": "test_calculation_id",
    "optimization": {
        "parameters": {
            "method": "GA",
            "ngen": 5,
            "pop_size": 10,
            "mutpb": 0.1,
            "cxpb": 0.9,
            "eta": 20,
            "indpb": 0.2,
            "diversity_flg": True,
            "ncls": 3,
            "maxf": 10,
            "qbound": 0.25
        },
        "objectives": [
            {
                "type": "concentration",
                "conc_file_name": "MT3D001.UCN",
                "summary_method": "max",
                "weight": -1,
                "penalty_value": 999,
                "location": {
                    "type": "bbox",
                    "ts": [0, 9],
                    "lay": [0, 0],
                    "row": [45, 45],
                    "col": [45, 45]
                }
            },
            {
                "type": "head",
                "summary_method": "max",
                "weight": 1,
                "penalty_value": 999,
                "location": {
                    "type": "bbox",
                    "ts": [0, 9],
                    "lay": [0, 0],
                    "row": [45, 45],
                    "col": [45, 45]
                }
            },
            # {
            #     "type": "flux",
            #     "package": "wel",
            #     "summary_method": "mean",
            #     "weight": -1,
            #     "penalty_value": 999,
            #     "location": {
            #         "type": "object",
            #         "objects": [0, 1]
            #     }
            # },
            # {
            #     "type": "input_concentration",
            #     "component": "component1",
            #     "package": "wel",
            #     "summary_method": "mean",
            #     "weight": -1,
            #     "penalty_value": 999,
            #     "location": {
            #         "type": "object",
            #         "objects": [0]
            #     }
            # }

        ],
        "constraints": [
            {
                "type": "concentration",
                "conc_file_name": "MT3D001.UCN",
                "summary_method": "max",
                "operator": "less",
                "value": 2,
                "location": {
                    "type": "bbox",
                    "ts": [0, 9],
                    "lay": [0, 0],
                    "row": [45, 45],
                    "col": [45, 45]
                }
            }
        ],
        "objects": [
            {
                "id": 0,
                "type": "well",
                "position": {
                    "row": {
                        "min": 10,
                        "max": 80,
                    },
                    "col": {
                        "min": 10,
                        "max": 80,
                    },
                    "lay": {
                        "min": 0,
                        "max": 0,
                    }
                },
                "flux": {
                    "0": {
                        "min": 1000,
                        "max": 1000
                    },
                    "1": {
                        "min": 1000,
                        "max": 1000
                    },
                    "2": {
                        "min": 1000,
                        "max": 1000
                    },
                    "3": {
                        "min": 1000,
                        "max": 1000
                    },
                    "4": {
                        "min": 1000,
                        "max": 1000
                    },
                    "5": {
                        "min": 1000,
                        "max": 1000
                    },
                    "6": {
                        "min": 1000,
                        "max": 1000
                    },
                    "7": {
                        "min": 1000,
                        "max": 1000
                    },
                    "8": {
                        "min": 1000,
                        "max": 1000
                    },
                    "9": {
                        "min": 1000,
                        "max": 1000
                    }
                },
                "concentration": {
                    "0": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "1": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "2": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "3": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "4": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "5": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "6": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "7": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "8": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "9": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    }
                }
            },
            {
                "id": 1,
                "type": "well",
                "position": {
                    "row": {
                        "min": 10,
                        "max": 80,
                    },
                    "col": {
                        "min": 10,
                        "max": 80,
                    },
                    "lay": {
                        "min": 0,
                        "max": 0,
                    }
                },
                "flux": {
                    "0": {
                        "min": 1000,
                        "max": 1000
                    },
                    "1": {
                        "min": 1000,
                        "max": 1000
                    },
                    "2": {
                        "min": 1000,
                        "max": 1000
                    },
                    "3": {
                        "min": 1000,
                        "max": 1000
                    },
                    "4": {
                        "min": 1000,
                        "max": 1000
                    },
                    "5": {
                        "min": 1000,
                        "max": 1000
                    },
                    "6": {
                        "min": 1000,
                        "max": 1000
                    },
                    "7": {
                        "min": 1000,
                        "max": 1000
                    },
                    "8": {
                        "min": 1000,
                        "max": 1000
                    },
                    "9": {
                        "min": 1000,
                        "max": 1000
                    }
                },
                "concentration": {
                    "0": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "1": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "2": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "3": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "4": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "5": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "6": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "7": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "8": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    },
                    "9": {
                        "component1": {
                            "min": 1,
                            "max": 1
                        }
                    }
                }
            }
        ]
    },
    "data": {
        "mf": {
            "run_model": True,
            "write_input": True,
            "packages": ["mf", "dis", "lpf", "bas", "chd", "wel", "oc", "pcg", "lmt"],
            "mf": {
                "modelname": mf_modelname,
                "exe_name": "mf2005",
                "model_ws": ".",
                "version": "mf2005"
            },
            "dis": {
                "nlay": nlay,
                "nrow": nrow,
                "ncol": ncol,
                "nper": nper,
                "delr": delr.tolist(),
                "delc": delc.tolist(),
                "top": top,
                "botm": botm,
                "perlen": perlen,
                "nstp": nstp,
                "steady": False
            },
            "lpf": {
                "hk": hk,
                "vka": hk,
                "ss": ss,
                "sy": sy
            },
            "bas": {
                "ibound": ibound.tolist(),
                "strt": top
            },
            "chd": {
                "stress_period_data": {str(k): list(v) for k, v in chd_data.items()}
            },
            "wel": {
                "stress_period_data": {str(k): list(v) for k, v in wel_data.items()}
            },
            "oc": {},
            "pcg": {},
            "lmt": {
                "output_file_name": 'mt3d_link.ftl',
                "output_file_format": 'unformatted',
                "output_file_header": 'extended'
            }
        },
        "mt": {
            "run_model": True,
            "write_input": True,
            "packages": ["mt", "btn", "adv", "dsp", "gcg", "ssm"],
            "mt": {
                "modelname": mt_modelname,
                "exe_name": "mt3dusgs",
                "model_ws": ".",
                "ftlfilename": "mt3d_link.ftl"
            },
            "btn": {
                "sconc": 1.9,
                "ncomp": 1,
                "mcomp": 1,
                "dt0": 30,
                "nprs": -1
            },
            "adv": {
                "mixelm": 0
            },
            "dsp": {
                "al": 5,
                "trpt": 0.1,
                "dmcoef": 1e-9
            },
            "gcg": {
                "iter1": 100
            },
            "ssm": {
                "stress_period_data": {str(k): list(v) for k, v in ssm_data.items()}
            }
        }
    }
}

model_input_simplex = {
    "author": "Aybulat F",
    "project": "Test model with Mt3d",
    "type": "optimization",
    "version": "3.2.6",
    "model_id": "test_model_id",
    "calculation_id": "test_calculation_id",
    "optimization": {
        "parameters": {
            "method": "Simplex",
            "maxf": 30,
            "xtol": 0.0001,
            "ftol": 0.0001
        },
        "objectives": [
            {
                "type": "concentration",
                "conc_file_name": "MT3D001.UCN",
                "summary_method": "max",
                "weight": -1,
                "penalty_value": 999,
                "location": {
                    "type": "bbox",
                    "ts": [0, 0],
                    "lay": [0, 0],
                    "row": [40, 40],
                    "col": [40, 40]
                }
            },
            {
                "type": "head",
                "summary_method": "max",
                "weight": -1,
                "penalty_value": 999,
                "location": {
                    "type": "bbox",
                    "ts": [0, 0],
                    "lay": [0, 0],
                    "row": [40, 40],
                    "col": [40, 40]
                }
            },
            {
                "type": "flux",
                "package": "wel",
                "summary_method": "mean",
                "weight": -1,
                "penalty_value": 999,
                "location": {
                    "type": "object",
                    "objects": [0, 1]
                }
            },
            {
                "type": "input_concentration",
                "component": "component1",
                "package": "wel",
                "summary_method": "mean",
                "weight": -1,
                "penalty_value": 999,
                "location": {
                    "type": "object",
                    "objects": [0]
                }
            }

        ],
        "constraints": [
            {
                "type": "concentration",
                "conc_file_name": "MT3D001.UCN",
                "summary_method": "max",
                "operator": "less",
                "value": 2,
                "location": {
                    "type": "bbox",
                    "ts": [0, 0],
                    "lay": [0, 0],
                    "row": [40, 40],
                    "col": [40, 40]
                }
            }
        ],
        "objects": [
            {
                "id": 0,
                "type": "well",
                "position": {
                    "row": {
                        "min": 10,
                        "max": 80,
                        "initial": 50
                    },
                    "col": {
                        "min": 10,
                        "max": 80,
                        "initial": 50
                    },
                    "lay": {
                        "min": 0,
                        "max": 0,
                    }
                },
                "flux": {
                    "0": {
                        "min": 720,
                        "max": 720
                    }
                },
                "concentration": {
                    "0": {
                        "component1": {
                            "min": 0,
                            "max": 0
                        }
                    }
                }
            },
            {
                "id": 1,
                "type": "well",
                "position": {
                    "row": {
                        "min": 10,
                        "max": 80,
                        "initial": 40
                    },
                    "col": {
                        "min": 10,
                        "max": 80,
                        "initial": 40
                    },
                    "lay": {
                        "min": 0,
                        "max": 0,
                    }
                },
                "flux": {
                    "0": {
                        "min": 720,
                        "max": 720
                    }
                },
                "concentration": {
                    "0": {
                        "component1": {
                            "min": 0,
                            "max": 0
                        }
                    }
                }
            },
            {
                "id": 2,
                "type": "well",
                "position": {
                    "row": {
                        "min": 10,
                        "max": 80,
                        "initial": 60
                    },
                    "col": {
                        "min": 10,
                        "max": 80,
                        "initial": 60
                    },
                    "lay": {
                        "min": 0,
                        "max": 0,
                    }
                },
                "flux": {
                    "0": {
                        "min": 720,
                        "max": 720
                    }
                },
                "concentration": {
                    "0": {
                        "component1": {
                            "min": 0,
                            "max": 0
                        }
                    }
                }
            }
        ]
    },
    "data": {
        "mf": {
            "run_model": True,
            "write_input": True,
            "packages": ["mf", "dis", "lpf", "bas", "chd", "wel", "oc", "pcg", "lmt"],
            "mf": {
                "modelname": mf_modelname,
                "exe_name": "mf2005",
                "model_ws": ".",
                "version": "mf2005"
            },
            "dis": {
                "nlay": nlay,
                "nrow": nrow,
                "ncol": ncol,
                "nper": nper,
                "delr": delr.tolist(),
                "delc": delc.tolist(),
                "top": top,
                "botm": botm,
                "perlen": perlen,
                "nstp": nstp,
                "steady": False
            },
            "lpf": {
                "hk": hk,
                "vka": hk,
                "ss": ss,
                "sy": sy
            },
            "bas": {
                "ibound": ibound.tolist(),
                "strt": top
            },
            "chd": {
                "stress_period_data": {str(k): list(v) for k, v in chd_data.items()}
            },
            "wel": {
                "stress_period_data": {str(k): list(v) for k, v in wel_data.items()}
            },
            "oc": {},
            "pcg": {},
            "lmt": {
                "output_file_name": 'mt3d_link.ftl',
                "output_file_format": 'unformatted',
                "output_file_header": 'extended'
            }
        },
        "mt": {
            "run_model": True,
            "write_input": True,
            "packages": ["mt", "btn", "adv", "dsp", "gcg", "ssm"],
            "mt": {
                "modelname": mt_modelname,
                "exe_name": "mt3dusgs",
                "model_ws": ".",
                "ftlfilename": "mt3d_link.ftl"
            },
            "btn": {
                "sconc": 1.9,
                "ncomp": 1,
                "mcomp": 1,
                "dt0": 30,
                "nprs": -1
            },
            "adv": {
                "mixelm": 0
            },
            "dsp": {
                "al": 5,
                "trpt": 0.1,
                "dmcoef": 1e-9
            },
            "gcg": {
                "iter1": 100
            },
            "ssm": {
                "stress_period_data": {str(k): list(v) for k, v in ssm_data.items()}
            }
        }
    }
}

with open('test_optimization_ga.json', 'w') as f:
     json.dump(model_input_ga, f)
    
with open('test_optimization_simplex.json', 'w') as f:
     json.dump(model_input_simplex, f)
