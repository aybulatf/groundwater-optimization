import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import { ValidatorForm, TextValidator} from 'react-material-ui-form-validator';

import ObjectConcentration from '../prototypes/ObjectConcentration';


const styles = {
  table: {
  },
  button: {
    margin: 10
  },
  saveButton: {
    marginTop: 10,
  },
  textField: {
    marginRight: 10,
    width: 70
  },
  inputText: {
    fontSize: 12
  },
  formConcentration: {
    width: '100%',
    marginTop: 20,
    overflowX: 'auto',
  }
};

class FormConcentration extends React.Component {
  constructor(props) {
    super(props);
    this.editedObject = props.editedObject;
    this.objectConcentration = new ObjectConcentration(props.nper)
    if (this.editedObject.concentration != null) {
      this.objectConcentration.concentration = this.editedObject.concentration;
    }
    this.state = this.objectConcentration.concentration;

  }
  handleSubmit() {
    this.editedObject.concentration = this.state;
    this.props.handleEditObject(null, null)
  }

  handleInputChange = (period, component, minmax) => event => {
    const value = parseFloat(event.target.value);
    this.setState((prevState) => {
      switch(minmax) {
        case "min":
          prevState[period][component]["min"] = value;
          if (value > prevState[period][component]["max"]){
            prevState[period][component]["max"] = value;
          }
          break;
        case "max":
          prevState[period][component]["max"] = value;
          if (value < prevState[period][component]["min"]){
            prevState[period][component]["min"] = value;
          }
          break;
      };
      return prevState;
    });
  };

  handleAddComponent() {
    this.setState((prevState) => {
      const newComponentName = "component"+(Object.keys(prevState[0]).length+1).toString();
      
      for (let period in prevState) {
        prevState[period][newComponentName] = {min: 0, max: 0}
      }
      return prevState
    });
  }

  render() {
    const { classes } = this.props;
    var tableRows = [];

      for (let period in this.state) {
        var bodyRowCells = [
          <TableCell className={classes.tableCell}>
            {period}
          </TableCell>
        ];
        var headerRowCells = [
          <TableCell className={classes.tableCell}>
            Stress period
          </TableCell>
        ];
        
        for (let component in this.state[period]) {
          headerRowCells.push(
            <TableCell className={classes.tableCell}>
              {component}, concentration from
            </TableCell>
          );
          headerRowCells.push(
            <TableCell className={classes.tableCell}>
              {component}, concentration to
            </TableCell>
          );
          bodyRowCells.push(
            <TableCell className={classes.tableCell}>
              <TextValidator
                id={"concMin" + component + period.toString()}
                name={"concMin" + component + period.toString()}
                className={classes.textField}
                value={this.state[period][component].min}
                type="number"
                onChange={this.handleInputChange(period, component, "min")}
                InputProps={{
                  classes: {
                    input: classes.inputText,
                  },
                }}
                validators={[
                  'required'
                ]}
                errorMessages={[
                  'number is required'
                ]}
              />
            </TableCell>
          );
          bodyRowCells.push(
            <TableCell className={classes.tableCell}>
              <TextValidator
                id={"concMax" + component + period.toString()}
                name={"concMin" + component + period.toString()}
                className={classes.textField}
                value={this.state[period][component].max}
                type="number"
                onChange={this.handleInputChange(period, component, "max")}
                InputProps={{
                  classes: {
                    input: classes.inputText,
                  },
                }}
                validators={[
                  'required'
                ]}
                errorMessages={[
                  'number is required'
                ]}
              />
            </TableCell>
          );
        }
        tableRows.push(<TableRow>{bodyRowCells}</TableRow>);
      }
    return (
      <div>
        <Typography variant="title" gutterBottom>
          Define flux variables
        </Typography>
        <ValidatorForm
          ref="concentrationForm"
          onSubmit={this.handleSubmit.bind(this)}
          onError={errors => console.log(errors)}
        >
          <Paper className={classes.formConcentration}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  {headerRowCells}
                </TableRow>
              </TableHead>
              <TableBody>
                {tableRows}
              </TableBody>
            </Table>
            <Button color="primary" variant="outlined" className={classes.button}
              onClick={this.handleAddComponent.bind(this)}>
              Add component
            </Button>
          </Paper>
          <Button color="primary" variant="contained" className={classes.saveButton} type="submit">
            Save
          </Button>
        </ValidatorForm>

        
      </div>
    )
  }
}

export default withStyles(styles)(FormConcentration);