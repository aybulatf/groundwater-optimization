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

const OptimizationObjectsTable = (props) => {

    const { classes } = props;
    var tableRows = [];

    
    for (let _object of props.optimizationObjects) {
      tableRows.push(
        <TableRow>
        <TableCell className={classes.tableCell}>
          <TextField
          
              className={classes.textField}
              value={_object.id}
              // onChange={this.handleChange('name')}
              margin="normal"
            />
        </TableCell>
        <TableCell className={classes.tableCell}>
          {_object.positionAdded ? (
            <Button color="secondary" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "position")}>
              Edit position variables
            </Button>
          ):(
            <Button color="primary" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "position")}>
              Add position variables
            </Button>
          )}
        </TableCell>
        <TableCell className={classes.tableCell}>
          {_object.fluxAdded ? (
            <Button color="primary" className={classes.button} 
            onClick = {props.handleEditObject.bind(this, _object.id, "flux")}>
            Edit flux variables
          </Button>
          ):(
            <Button color="primary" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "flux")}>
              Add flux variables
            </Button>
          )}
        </TableCell>
        <TableCell className={classes.tableCell}>
          {_object.concentrationAdded ? (
            <Button color="secondary" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "concentration")}>
              Edit concentration variables
            </Button>
          ):(
            <Button color="primary" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "concentration")}>
              Add concentration variables
            </Button>
          )}
        </TableCell>
        
      </TableRow>
      )
    };
      return(
        <div>
          <Typography variant="headline" gutterBottom>
            Optimization objects
          </Typography>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <TableCell className={classes.tableCell}>Name</TableCell>
                <TableCell className={classes.tableCell}>Position </TableCell>
                <TableCell className={classes.tableCell}>Flux</TableCell>
                <TableCell className={classes.tableCell}>Concentration</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
             {tableRows}
            </TableBody>
          </Table>
        </div>
      )


};

export default withStyles(styles)(OptimizationObjectsTable);

  


