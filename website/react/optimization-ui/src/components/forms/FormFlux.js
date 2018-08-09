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
    this.optimizationObject = props.optimizationObject;

    this.state = this.optimizationObject.flux;
  }
  handleSubmit() {
    this.optimizationObject.flux = this.state;
    this.optimizationObject.fluxAdded = true;
    this.props.handleEditObject(null, null)
  }

  handleInputChange = (period, minmax) => event => {
    event.persist();
    this.setState((prevState) => {
      prevState[period][minmax] = event.target.value;
      return prevState;
    });
  };
  
  render() {
    const { classes } = this.props;
    var tableRows = [];

    for (let period in this.state) {
      console.log("fluxMin" + period.toString())
      tableRows.push(
        <TableRow>
          <TableCell className={classes.tableCell}>
            {period}
          </TableCell>
          <TableCell className={classes.tableCell}>
            <TextField
              id={"fluxMin" + period.toString()}
              className={classes.textField}
              value={this.state[period].min}
              type="number"
              onChange={this.handleInputChange(period, "min")}
              InputProps={{
                classes: {
                  input: classes.inputText,
                },
              }}
            />
          </TableCell>
          <TableCell className={classes.tableCell}>
            <TextField
              id={"fluxMax" + period.toString()}
              className={classes.textField}
              value={this.state[period].max}
              type="number"
              onChange={this.handleInputChange(period, "max")}
              InputProps={{
                classes: {
                  input: classes.inputText,
                },
              }}
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
        <Button color="primary" variant="contained" className={classes.saveButton}
          onClick={this.handleSubmit.bind(this)}>
          Save
        </Button>
      </div>
    )
  }
}

export default withStyles(styles)(FormFlux);