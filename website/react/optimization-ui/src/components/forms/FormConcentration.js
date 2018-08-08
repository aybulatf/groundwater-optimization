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


const styles = {
    table: {
      width: 400
    },
    textField: {
      marginLeft: 0,
      marginRight: 0,
      width: 50 ,
    },
    tableCell :{
      margin: 0,
      padding: 0
    }
};

class FormConcentration extends React.Component {
  constructor(props) {
    super(props);
    this.optimizationObject = props.optimizationObject;

    this.state = this.optimizationObject.concentration;
  }
  handleSubmit() {
    this.optimizationObject.setConcentration(this.state);
    this.optimizationObject.concentrationAdded = true;
    console.log(this.optimizationObject)
    this.props.handleEditObject(null, null)
  }
  handleMinChange(event) {
    const target = event.target;
    const value = target.value;
    const period = target.period;
    const component = target.component;

    this.setState((prevState) => {
      return prevState[period][component].min = value
    });
  }

  handleMaxChange(event) {
    const target = event.target;
    const value = target.value;
    const period = target.period;
    const component = target.component;

    this.setState((prevState) => {
      return prevState[period][component].max = value
    });
  }

  handleAddComponent() {
    this.setState((prevState) => {
      for (let period in prevState) {
        prevState[period]["component" + prevState[period].length.toString()] = prevState[period]["component1"]
      }
      return prevState
    });
  }
  render() {
    const { classes } = this.props;
    var tableRows = [];
      for (let period in this.state) {
        var row = <TableCell className={classes.tableCell}>
                    {period}
                  </TableCell>;
        var headerRow = <TableCell className={classes.tableCell}>Stress period</TableCell>
        
        for (let component in this.state[period]) {
          headerRow.push(
            <TableCell className={classes.tableCell}>
              Component {component}, concentration from
            </TableCell>
          );
          headerRow.push(
            <TableCell className={classes.tableCell}>
              Component {component}, concentration to
            </TableCell>
          );
          row.push(
            <TableCell className={classes.tableCell}>
              <TextField
                className={classes.textField}
                value={this.state[period][component].min}
                period={period}
                component={component}
                onChange={this.handleMinChange("period", "component")}
              />
            </TableCell>
          );
          row.push(
            <TableCell className={classes.tableCell}>
              <TextField
                className={classes.textField}
                value={this.state[period][component].max}
                period={period}
                component={component}
                onChange={this.handleMinChange("period", "component")}
              />
            </TableCell>
          );
        }
        tableRows.push(<TableRow>{row}</TableRow>);
      }
    return (
      <div>
        <Typography variant="headline" gutterBottom>
          Define flux variables
                </Typography>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              {headerRow}
            </TableRow>
          </TableHead>
          <TableBody>
            {tableRows}
          </TableBody>
        </Table>
        <Button color="primary" className={classes.button} onClick={this.handleSubmit.bind(this)}>
          Save
        </Button>
        <Button color="primary" className={classes.button} onClick={this.handleAddComponent.bind(this)}>
          Add component
        </Button>
      </div>
    )
  }
}

export default FormConcentration;