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

class FormFlux extends React.Component {
    constructor(props) {
        super(props);
        this.optimizationObject = props.optimizationObject;
        
        this.state = this.optimizationObject.flux;
    }
    handleSubmit(){
        this.optimizationObject.setFlux(this.state);
        this.optimizationObject.fluxAdded = true;
        console.log(this.optimizationObject)
        this.props.handleEditObject(null, null)
    }
    handleMinChange(event) {
        const target = event.target;
        const value = target.value;
        const period = target.name;

        this.setState((prevState) => {
            return prevState[period].min = value
        });
    }

    handleMaxChange(event) {
            const target = event.target;
            const value = target.value;
            const period = target.name;
    
            this.setState((prevState) => {
                return prevState[period].max = value
            });
      }
    render() {
        const { classes } = this.props;
        const tableRows = this.state.map((period) =>
            <TableRow>
                <TableCell className={classes.tableCell}>
                    {period}
                </TableCell>
                <TableCell className={classes.tableCell}>
                    <TextField
                        className={classes.textField}
                        value={this.state[period].min}
                        name={period}
                        onChange={this.handleMinChange("name")}
                    />
                </TableCell>
                <TableCell className={classes.tableCell}>
                    <TextField
                        className={classes.textField}
                        value={this.state[period].max}
                        name={period}
                        onChange={this.handleMaxChange("name")}
                    />
                </TableCell>
            </TableRow>
        );
        return (
            <div>
                <Typography variant="headline" gutterBottom>
                    Define flux variables
                </Typography>
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
                <Button color="primary" className={classes.button} onClick = {this.handleSubmit.bind(this)}>
                    Save
                </Button>
            </div>
        )
    }
}

export default withStyles(styles)(FormFlux);