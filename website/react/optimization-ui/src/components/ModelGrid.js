import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import * as d3 from 'd3'
import Grid from '@material-ui/core/Grid';
import { TextField } from '../../node_modules/@material-ui/core';
import MenuItem from '@material-ui/core/MenuItem';


const styles = {
  plot: {
    border: "2px solid blue"
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
  switch(parameter) {
    case "ibound":
      switch(value) {
        case 0: return "white";
        case 1: return "blue";
      };
    default:
      switch(value) {
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
  return {data: data, modelWidth: modelWidth, modelHeight: modelHeight};
}


class ModelGrid extends React.Component {
  _allSPDPackages = ['CHD', 'WEL', 'GHB', 'SSM', 'RCH'];
  _basPackageName = 'BAS';
  _lmtPackageName = 'LMT';

  constructor(props) {
    super(props);
    this.gridData = getGrid(props.modelData.data.mf.DIS.delr, props.modelData.data.mf.DIS.delc);
    this.scaleFactor = Math.min(props.width/this.gridData.modelWidth, props.height/this.gridData.modelHeight);
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
      zoomTransform: null
    }
  }

  scaleGridData(value) {
    return value * this.scaleFactor;
  }

  getGridValues(parameter, layer) {
    switch(parameter) {
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
        console.log('Unknown package '+parameter.toString())
    }
  }
  componentDidMount() {
    
    this.canvas = d3.select(this.refs.canvas).call(d3.zoom().scaleExtent([-3, 15]).on("zoom", this.zoomed.bind(this)));
    this.ctx = this.canvas.node().getContext("2d");
    
    this.ctx.beginPath();
    for (const d of this.gridData.data) {
      this.ctx.rect(
        this.scaleGridData(d[0]), this.scaleGridData(d[1]), this.scaleGridData(d[2]), this.scaleGridData(d[3]))
    }
    this.ctx.lineWidth = 1;
    this.ctx.stroke();
  }
    

  componentDidUpdate() {
    var gridValues = null;
    this.ctx.save();
    this.ctx.clearRect(0, 0, this.props.width, this.props.height);
      
    if (this.state.zoomTransform){
      this.ctx.translate(this.state.zoomTransform.x, this.state.zoomTransform.y);
      this.ctx.scale(this.state.zoomTransform.k, this.state.zoomTransform.k);
    }
    if (this.state.gridColorParameter !== null && this.state.gridColorLayer !== null){
      gridValues = this.getGridValues(this.state.gridColorParameter, this.state.gridColorLayer)
    }
    console.log(gridValues)
    
    if (gridValues) {
      for (let d of this.gridData.data) {
        this.ctx.fillStyle = getGridColor(this.state.gridColorParameter, gridValues[d[4]][d[5]]);
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

    var gridColorParameters = [{value: 'ibound', label: 'ibound'}]
    for (let _package of this.spdPackages){
      gridColorParameters.push({value: _package, label: _package})
    }

    var gridColorLayers = [];
    for (const layer of [...Array(this.props.nlay).keys()]) {
      gridColorLayers.push({
        value: layer,
        label: layer.toString()
      })
    }

    return (
      <Grid container>
        <Grid item xs={12}>
          <TextField
            id="selectParameter"
            select
            helperText = "Chose parameter"
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
            helperText = "Chose layer"
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

          {/* <Button onClick={this.setGridColorParameter.bind(this)}>
            Color
          </Button> */}
          </Grid>
        <Grid item xs={12}>
          <canvas ref="canvas" className={classes.plot} width={width} height={height} />
        </Grid>
      </Grid>
    )
  }
};

export default withStyles(styles)(ModelGrid);
