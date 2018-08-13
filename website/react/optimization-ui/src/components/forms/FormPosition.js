import React from 'react'
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import { ValidatorForm, TextValidator} from 'react-material-ui-form-validator';
import Modal from '@material-ui/core/Modal';

import ObjectPosition from '../prototypes/ObjectPosition';

import ModelGrid from '../ModelGrid';


const styles = {
  button: {
    margin: 10
  },
  saveButton: {
    marginTop: 10,
  },
  textField: {
    margin: 10,
    padding: 5,
    width: 100
  },
  subheading: {
    margin: 10
  },
  formPosition: {
    width: '100%',
    marginTop: 20,
    overflowX: 'auto',
  },
  modelGrid: {
    margin: 10
  },
  gridModal:{
    backgroundColor: '#EFF3F6',
    top: "10%",
    left:"30%",
    position: "absolute",
    width: 600,
    height: 650
  }
};

class FormPosition extends React.Component {
  constructor(props) {
    super(props);
    this.modelData = props.modelData;
    this.nlay=props.modelData.data.mf.DIS.nlay;
    this.nrow=props.modelData.data.mf.DIS.nrow;
    this.ncol=props.modelData.data.mf.DIS.ncol;
    this.editedObject = props.editedObject;
    this.objectPosition = new ObjectPosition(this.nlay, this.nrow, this.ncol)
    if (this.editedObject.position != null) {
      this.objectPosition.position = this.editedObject.position;
    }
    this.modelGrid = React.createRef();
    this.state = {};
    this.state.position = this.objectPosition.position;
    this.state.showGrid = false;
  }

  handleSubmit() {
    this.editedObject.position = this.state.position;
    this.props.handleEditObject(null, null)
  }

  handleInputChange = (param, minmax) => event => {
    var value = parseInt(event.target.value);
    if (value < 0) {value=0;}
    if (param == "lay" && value>this.nlay-1) {value=this.nlay-1;}
    if (param === "row" && value>this.nrow-1) {value=this.nrow-1;}
    if (param === "col" && value>this.ncol-1) {value=this.ncol-1;}
    
    this.setState((prevState) => {
      switch(minmax) {
        case "min":
          prevState.position[param]["min"] = value;
          if (value > prevState.position[param]["max"]){
            prevState.position[param]["max"] = value;
          }
          break;
        case "max":
          prevState.position[param]["max"] = value;
          if (value < prevState.position[param]["min"]){
            prevState.position[param]["min"] = value;
          }
          break;
      };
      return prevState;
    });
  }
  getSelectedRows(){
    if (this.objectPosition.position === null) {
      return null;
    } else {
      var selectedRows = [];
      for (let i=this.objectPosition.position.row.min; i<=this.objectPosition.position.row.max; i++) {
        selectedRows.push(i)
      }
      return selectedRows;
    }
  };

  getSelectedCols(){
    if (this.objectPosition.position === null) {
      return null;
    } else {
      var selectedCols = [];
      for (let i=this.objectPosition.position.col.min; i<=this.objectPosition.position.col.max; i++) {
        selectedCols.push(i)
      }
      return selectedCols;
    }
  };

  showGrid() {
    this.setState({
      showGrid: true
    })
  };

  closeGrid() {
    this.setState({
      showGrid: false
    })
  };

  render() {
    const { classes } = this.props;
    return (
      <div>

        <Typography variant="title" gutterBottom>
          Edit position variables
        </Typography>
        <ValidatorForm
          ref="positionForm"
          onSubmit={this.handleSubmit.bind(this)}
          onError={errors => console.log(errors)}
        >
        <Paper className={classes.formPosition}>
          <Typography className={classes.subheading} variant="subheading" gutterBottom>
            Set layer range
          </Typography>
          <br/>
          
            <TextValidator
              id="layerMin"
              name="layerMin"
              label="Layer from:"
              value={this.state.position.lay.min}
              onChange={this.handleInputChange("lay", "min")}
              type="number"
              className={classes.textField}
              InputLabelProps={{
                shrink: true,
              }}
              margin="normal"
              validators={[
                `minNumber:${this.objectPosition.minLay}`, `maxNumber:${this.objectPosition.maxLay}`, 
                'required', 'matchRegexp:^[0-9]+$'
              ]}
              errorMessages={[
                'value < than min layer', 'value > than max layer',
                'number is required', 'only integer number is valid input'
              ]}
            />
            <TextValidator
              id="layerMax"
              name="layerMax"
              label="Layer to:"
              value={this.state.position.lay.max}
              onChange={this.handleInputChange("lay", "max")}
              type="number"
              className={classes.textField}
              InputLabelProps={{
                shrink: true,
              }}
              margin="normal"
              validators={[
                `minNumber:${this.objectPosition.minLay}`, `maxNumber:${this.objectPosition.maxLay}`, 
                'required', 'matchRegexp:^[0-9]+$'
              ]}
              errorMessages={[
                'value < than min layer', 'value > than max layer',
                'number is required', 'only integer number is valid input'
              ]}
            />
            

        </Paper>
        <Paper className={classes.formPosition}>
          <Typography className={classes.subheading} variant="subheading" gutterBottom>
            Set row/column range
          </Typography>
          <br/>
          <TextValidator
            id="rowMin"
            name="rowMin"
            label="Row from:"
            value={this.state.position.row.min}
            onChange={this.handleInputChange("row", "min")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
            validators={[
              `minNumber:${this.objectPosition.minRow}`, `maxNumber:${this.objectPosition.maxRow}`, 
              'required', 'matchRegexp:^[0-9]+$'
            ]}
            errorMessages={[
              'value < than min row', 'value > than max row',
              'number is required', 'only integer number is valid input'
            ]}
          />
          <TextValidator
            id="rowMax"
            name="rowMax"
            label="Row to:"
            value={this.state.position.row.max}
            onChange={this.handleInputChange("row", "max")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
            validators={[
              `minNumber:${this.objectPosition.minRow}`, `maxNumber:${this.objectPosition.maxRow}`, 
              'required', 'matchRegexp:^[0-9]+$'
            ]}
            errorMessages={[
              'value < than min row', 'value > than max row',
              'number is required', 'only integer number is valid input'
            ]}
          />
          <br/>
          <TextValidator
            id="colMin"
            name="colMin"
            label="Column from:"
            value={this.state.position.col.min}
            onChange={this.handleInputChange("col", "min")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
            validators={[
              `minNumber:${this.objectPosition.minCol}`, `maxNumber:${this.objectPosition.maxCol}`, 
              'required', 'matchRegexp:^[0-9]+$'
            ]}
            errorMessages={[
              'value < than min column', 'value > than max column',
              'number is required', 'only integer number is valid input'
            ]}
          />
          <TextValidator
            id="colMax"
            name="colMax"
            label="Column to:"
            value={this.state.position.col.max}
            onChange={this.handleInputChange("col", "max")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
            validators={[
              `minNumber:${this.objectPosition.minCol}`, `maxNumber:${this.objectPosition.maxCol}`, 
              'required', 'matchRegexp:^[0-9]+$'
            ]}
            errorMessages={[
              'value < than min column', 'value > than max column',
              'number is required', 'only integer number is valid input'
            ]}
          />
          {this.state.showGrid === false ? (

            <Button color="primary" variant="outlined" className={classes.button}
              onClick={this.showGrid.bind(this)}>
              Show on grid
            </Button>
          ):(
            <div className={classes.modelGrid}>
              <Typography variant="subheading" gutterBottom>
                Change row/column ranges to see updates on map
              </Typography>
              <ModelGrid
                modelData={this.modelData}
                width = {560}
                height = {400}
                selectedRows = {this.getSelectedRows()}
                selectedCols = {this.getSelectedCols()}
              />
              <Button color="primary" variant="outlined" className={classes.button}
                onClick={this.closeGrid.bind(this)}>
                Close grid
              </Button>
            </div>
            
            )
          }

        </Paper>
        <Button color="primary" variant="contained" className={classes.saveButton} type="submit">
          Save
        </Button>
      </ValidatorForm>

      {/* {this.state.showGrid === true && (
        <Modal
          open={this.state.showGrid}
          onClose={this.closeGrid.bind(this)}
        >
        <div className={classes.gridModal}>
          <ModelGrid
            modelData={this.modelData}
            width = {580}
            height = {500}
          />
        </div>
        </Modal>
        )
      } */}

      </div>
    )
  }
}

export default withStyles(styles)(FormPosition);