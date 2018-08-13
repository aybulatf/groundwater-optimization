import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import * as d3 from 'd3'
import Typography from '@material-ui/core/Typography'
import { TextField } from '../../node_modules/@material-ui/core';
import MenuItem from '@material-ui/core/MenuItem';


const styles = {
  modelGrid: {
    width: '100%',
    // width: 580,
    marginTop: 10,
    marginBottom: 10,
    overflowX: 'auto',
  },
  textField: {
    marginLeft: 20,
    marginRight: 20,
    width: 200,
  },
  menu: {
    width: 200,
  }
};


const getGridColor = (parameter, value) => {
  switch (parameter) {
    case "ibound":
      switch (value) {
        case 0: return "white";
        case 1: return "blue";
      };
    case "selection":
      switch (value) {
        case 0: return "white";
        case 1: return "red";
      };
    default:
      switch (value) {
        case 0: return "white";
        case 1: return "blue";
      };
  };
}

const getGrid = (delr, delc) => {
  var data = new Array();
  var xpos = 0;
  var ypos = 0;
  var modelWidth = 0;
  var modelHeight = 0;

  for (let width of delc) {
    modelWidth += width;
  }
  for (let height of delr) {
    modelHeight += height;
  }

  for (let [rowIndex, height] of delr.entries()) {
    for (let [colIndex, width] of delc.entries()) {
      data.push([
        xpos,
        ypos,
        width,
        height,
        rowIndex,
        colIndex
      ])
      xpos += width;
    }
    xpos = 0;
    ypos += height;
  }
  return { data: data, modelWidth: modelWidth, modelHeight: modelHeight };
}


class ModelGrid extends React.Component {
  _allSPDPackages = ['CHD', 'WEL', 'GHB', 'SSM', 'RCH'];
  _basPackageName = 'BAS';
  _lmtPackageName = 'LMT';

  constructor(props) {
    super(props);
    this.delr = props.modelData.data.mf.DIS.delr;
    this.delc = props.modelData.data.mf.DIS.delc;
    this.gridData = getGrid(this.delr, this.delc);
    this.scaleFactor = Math.min(props.width / this.gridData.modelWidth, props.height / this.gridData.modelHeight);
    this.maxZoom = 15;
    this.minZoom = -3;
    this.spdPackages = [];
    this.nrow = props.modelData.data.mf.DIS.nrow;
    this.ncol = props.modelData.data.mf.DIS.ncol;

    for (let _package of props.modelData.data.mf.packages.concat(props.modelData.data.mt.packages)) {
      if (this._allSPDPackages.indexOf(_package) >= 0) {
        this.spdPackages.push(_package)
      }
      if (_package == 'BAS6') {
        this._basPackageName = 'BAS6';
      }
      if (_package == 'LMT6') {
        this._lmtPackageName = 'LMT6';
      }
    }

    this.state = {
      gridColorParameter: null,
      gridColorLayer: null,
      zoomTransform: null,
      selectedRows: props.selectedRows,
      selectedCols: props.selectedCols,
    }
  }

  setSelectedCells(selectedRows, selectedCols) {
    this.setState({
      selectedRows: selectedRows,
      selectedCols: selectedCols
    })
  }

  scaleGridData(value) {
    return value * this.scaleFactor;
  }

  getGridValues(parameter, layer) {
    switch (parameter) {
      case "ibound":
        const ibound = this.props.modelData.data.mf[this._basPackageName].ibound;
        return ibound[layer];

      case "CHD":
        const chdSPD = this.props.modelData.data.mf.CHD.stress_period_data;
        var chdGrid = Array(this.nrow).fill(Array(this.ncol).fill(0));

        for (let period in chdSPD) {
          for (let record of chdSPD[period]) {
            if (record[0] == layer) {
              chdGrid[record[1]][record[2]] = 1;
            }
          }
        }
        return chdGrid;

      case "WEL":
        const welSPD = this.props.modelData.data.mf.WEL.stress_period_data;
        var welGrid = Array(this.nrow).fill(Array(this.ncol).fill(0))

        for (let period in welSPD) {
          for (let record of welSPD[period]) {
            if (record[0] == layer) {
              welGrid[record[1]][record[2]] = 1;
            }
          }
        }
        return welGrid;

      case "SSM":
        const ssmSPD = this.props.modelData.data.mt.SSM.stress_period_data;
        var ssmGrid = Array(this.nrow).fill(Array(this.ncol).fill(0))

        for (let period in ssmSPD) {
          for (let record of ssmSPD[period]) {
            if (record[0] == layer) {
              ssmGrid[record[1]][record[2]] = 1;
            }
          }
        }
        return ssmGrid;

      case "GHB":
        const ghbSPD = this.props.modelData.data.mf.GHB.stress_period_data;
        var ghbGrid = Array(this.nrow).fill(Array(this.ncol).fill(0))

        for (let period in ghbSPD) {
          for (let record of ghbSPD[period]) {
            if (record[0] == layer) {
              ghbGrid[record[1]][record[2]] = 1;
            }
          }
        }
        return ghbGrid;

      case "RCH":
        const rchSPD = this.props.modelData.data.mf.RCH.stress_period_data;
        var rchGrid = Array(this.nrow).fill(Array(this.ncol).fill(0))

        for (let period in rchSPD) {
          for (let record of rchSPD[period]) {
            if (record[0] == layer) {
              rchGrid[record[1]][record[2]] = 1;
            }
          }
        }
        return rchGrid;

      default:
        console.log('Unknown package ' + parameter.toString())
    }
  }
  getInitialZoomTransform(selectedRows, selectedCols) {
    var selectedRowsLength = 0;
    var selectedColsLength = 0;

    for(let i of selectedRows ){
      selectedRowsLength += this.delr[i];
    };
    for(let i of selectedCols){
      selectedColsLength += this.delc[i];
    };
    const xZoom = (this.gridData.modelWidth/selectedColsLength)/2;
    const yZoom = (this.gridData.modelHeight/selectedRowsLength)/2

    var initZoom = Math.min(xZoom, yZoom);
    if (initZoom > this.maxZoom) {
      initZoom = this.maxZoom;
    };

    var initX = 0;
    var initY = 0;
    for(let i = 0; i<selectedRows[0]; i++ ){
      initY -= this.delr[i];
    };
    for(let i =0; i<selectedCols[0]; i++ ){
      initX -= this.delc[i];
    };

    initX = this.scaleGridData(initX+selectedColsLength/2)*initZoom;
    initY = this.scaleGridData(initY+selectedRowsLength/2)*initZoom;

    return {initZoom, initX, initY};
  }

  makeGridArray(nrow, ncol) {
    var gridArray = [];
    for (let i=0; i<nrow; i++) {
      var row = [];
      for (let j=0; j<ncol; j++) {
        row.push(0);
      }
      gridArray.push(row);
    }
    return gridArray;
  }
  

  getSelectionGrid (gridArray, selectedRows, selectedCols){

    for (let r in selectedRows) {
      if (r<0) {r=0}
      for (let c in selectedCols) {
        if (c<0) {c=0}
        gridArray[selectedRows[r]][selectedCols[c]] = 1;
      }
    }

    return gridArray;
  }

  componentDidMount() {
    var selectionGrid = null;
    var initialZoomTransform = null;
    if (this.state.selectedRows !== null && this.state.selectedCols !== null) {
      initialZoomTransform = this.getInitialZoomTransform(this.state.selectedRows, this.state.selectedCols);
      selectionGrid = this.getSelectionGrid(
        this.makeGridArray(this.nrow, this.ncol),
        this.state.selectedRows, this.state.selectedCols
      );
    }

    var d3zoom = d3.zoom().scaleExtent([this.minZoom, this.maxZoom]).on("zoom", this.zoomed.bind(this));
    if (initialZoomTransform !== null) {
      this.canvas = d3.select(this.refs.canvas)
                      .call(d3zoom)
                      .call(d3zoom.transform, d3.zoomIdentity
                        .translate(initialZoomTransform.initX, initialZoomTransform.initY)
                        .scale(initialZoomTransform.initZoom));
    } else {
      this.canvas = d3.select(this.refs.canvas)
                      .call(d3zoom);
    }
    this.ctx = this.canvas.node().getContext("2d");

    if (selectionGrid) {
      for (let d of this.gridData.data) {
        this.ctx.fillStyle = getGridColor("selection", selectionGrid[d[4]][d[5]]);
        this.ctx.fillRect(
          this.scaleGridData(d[0]), this.scaleGridData(d[1]), this.scaleGridData(d[2]), this.scaleGridData(d[3])
        );
      }
    }

    this.ctx.beginPath();
    for (let d of this.gridData.data) {
      this.ctx.rect(
        this.scaleGridData(d[0]), this.scaleGridData(d[1]), this.scaleGridData(d[2]), this.scaleGridData(d[3]))
    }
    this.ctx.lineWidth = 1;
    this.ctx.stroke();
  }


  componentDidUpdate() {
    var gridValues = null;
    var selectionGrid = null;
    this.ctx.save();
    this.ctx.clearRect(0, 0, this.props.width, this.props.height);

    if (this.state.zoomTransform) {
      this.ctx.translate(this.state.zoomTransform.x, this.state.zoomTransform.y);
      this.ctx.scale(this.state.zoomTransform.k, this.state.zoomTransform.k);
    }

    if (this.state.gridColorParameter !== null && this.state.gridColorLayer !== null) {
      gridValues = this.getGridValues(this.state.gridColorParameter, this.state.gridColorLayer)
    }

    if (this.state.selectedRows !== null && this.state.selectedCols !== null) {
      selectionGrid = this.getSelectionGrid(
        this.makeGridArray(this.nrow, this.ncol),
        this.props.selectedRows, this.props.selectedCols
      );
    }

    if (gridValues) {
      for (let d of this.gridData.data) {
        this.ctx.fillStyle = getGridColor(this.state.gridColorParameter, gridValues[d[4]][d[5]]);
        this.ctx.fillRect(
          this.scaleGridData(d[0]), this.scaleGridData(d[1]), this.scaleGridData(d[2]), this.scaleGridData(d[3])
        );
      }
    }

    if (selectionGrid) {
      for (let d of this.gridData.data) {
        this.ctx.fillStyle = getGridColor("selection", selectionGrid[d[4]][d[5]]);
        this.ctx.fillRect(
          this.scaleGridData(d[0]), this.scaleGridData(d[1]), this.scaleGridData(d[2]), this.scaleGridData(d[3])
        );
      }
    }

    

    

    this.ctx.beginPath();
    for (let d of this.gridData.data) {
      this.ctx.rect(
        this.scaleGridData(d[0]), this.scaleGridData(d[1]), this.scaleGridData(d[2]), this.scaleGridData(d[3])
      );
    }
    this.ctx.restore();
    this.ctx.lineWidth = 1;
    this.ctx.stroke();
  }

  zoomed() {
    this.setState({
      zoomTransform: d3.event.transform
    });
  }

  handleInput = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  render() {
    const { classes } = this.props;
    const { width, height } = this.props;

    var gridColorParameters = [{ value: 'ibound', label: 'ibound' }]
    for (let _package of this.spdPackages) {
      gridColorParameters.push({ value: _package, label: _package })
    }

    var gridColorLayers = [];
    for (const layer of [...Array(this.props.nlay).keys()]) {
      gridColorLayers.push({
        value: layer,
        label: layer.toString()
      })
    }

    return (
      <div>
        <Paper className={classes.modelGrid}>
            <canvas ref="canvas" className={classes.plot} width={width} height={height} />
        </Paper>

        <TextField
          id="selectParameter"
          select
          helperText="Chose parameter"
          value={this.state.gridColorParameter}
          className={classes.textField}
          onChange={this.handleInput('gridColorParameter')}
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          margin="normal"
        >
          {gridColorParameters.map(option => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          id="selectLayer"
          select
          helperText="Chose layer"
          value={this.state.gridColorLayer}
          className={classes.textField}
          onChange={this.handleInput('gridColorLayer')}
          SelectProps={{
            MenuProps: {
              className: classes.menu,
            },
          }}
          margin="normal"
        >
          {gridColorLayers.map(option => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
      </div>
    )
  }
};

export default withStyles(styles)(ModelGrid);
