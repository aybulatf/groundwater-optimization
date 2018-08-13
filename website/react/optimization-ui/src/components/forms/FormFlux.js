import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import { ValidatorForm, TextValidator} from 'react-material-ui-form-validator';

import ObjectFlux from '../prototypes/ObjectFlux';


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
    padding: 5,
    width: 70
  },
  inputText: {
    fontSize: 12
  },
  formFlux: {
    width: '100%',
    marginTop: 20,
    overflowX: 'auto',
  }
};

class FormFlux extends React.Component {
  constructor(props) {
    super(props);
    this.editedObject = props.editedObject;
    this.objectFlux = new ObjectFlux(props.nper)
    if (this.editedObject.flux != null) {
      this.objectFlux.flux = this.editedObject.flux;
    }
    this.state = this.objectFlux.flux;
  }
  handleSubmit() {
    this.editedObject.flux = this.state;
    this.props.handleEditObject(null, null)
  }

  handleInputChange = (period, minmax) => event => {
    const value = parseFloat(event.target.value);
    this.setState((prevState) => {
      switch(minmax) {
        case "min":
          prevState[period]["min"] = value;
          if (value > prevState[period]["max"]){
            prevState[period]["max"] = value;
          }
          break;
        case "max":
          prevState[period]["max"] = value;
          if (value < prevState[period]["min"]){
            prevState[period]["min"] = value;
          }
          break;
      };
      return prevState;
    });
  };
  
  render() {
    const { classes } = this.props;
    var tableRows = [];

    for (let period in this.state) {
      tableRows.push(
        <TableRow>
          <TableCell className={classes.tableCell}>
            {period}
          </TableCell>
          <TableCell className={classes.tableCell}>
            <TextValidator
              id={"fluxMin" + period.toString()}
              name={"fluxMin" + period.toString()}
              className={classes.textField}
              value={this.state[period].min}
              type="number"
              onChange={this.handleInputChange(period, "min")}
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
          <TableCell className={classes.tableCell}>
            <TextValidator
              id={"fluxMax" + period.toString()}
              name={"fluxMax" + period.toString()}
              className={classes.textField}
              value={this.state[period].max}
              type="number"
              onChange={this.handleInputChange(period, "max")}
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
          
        </TableRow>
      );
    };
    return (
      <div>
        <Typography variant="title" gutterBottom>
          Define flux variables
        </Typography>
        <ValidatorForm
          ref="fluxForm"
          onSubmit={this.handleSubmit.bind(this)}
          onError={errors => console.log(errors)}
        >
          <Paper className={classes.formFlux}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  <TableCell className={classes.tableCell}>Stress period</TableCell>
                  <TableCell className={classes.tableCell}>Flux from </TableCell>
                  <TableCell className={classes.tableCell}>Flux to</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tableRows}
              </TableBody>
            </Table>
          </Paper>
          <Button color="primary" variant="contained" className={classes.saveButton} type="submit">
              Save
            </Button>
        </ValidatorForm>
      </div>
    )
  }
}

export default withStyles(styles)(FormFlux);