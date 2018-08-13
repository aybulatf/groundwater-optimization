import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';

const styles = {
  objectsTable: {
    width: '100%',
    marginTop: 20,
    marginBottom: 10,
    overflowX: 'auto',
  },
  table: {
    // width: 400,
  },
  button: {
    fontSize: 10,
  },
  // tableCell: {
  //   paddingLeft: "auto",
  //   paddingRigh: "auto",
  // }
};

const OptimizationObjectsTable = (props) => {

    const { classes } = props;
    var tableRows = [];

    
    for (let _object of props.optimizationObjects) {
      tableRows.push(
        <TableRow>
        <TableCell className={classes.tableCell}>
          {_object.id}
        </TableCell>
        <TableCell className={classes.tableCell}>
          {_object.position != null ? (
            <Button color="primary" size="small" variant="text" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "position")}>
              Edit position variables
            </Button>
          ):(
            <Button color="secondary" size="small" variant="text" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "position")}>
              Add position variables
            </Button>
          )}
        </TableCell>
        <TableCell className={classes.tableCell}>
          {_object.flux != null ? (
            <Button color="primary" size="small" variant="text" className={classes.button} 
            onClick = {props.handleEditObject.bind(this, _object.id, "flux")}>
            Edit flux variables
          </Button>
          ):(
            <Button color="secondary" size="small" variant="text" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "flux")}>
              Add flux variables
            </Button>
          )}
        </TableCell>
        <TableCell className={classes.tableCell}>
          {_object.concentration != null ? (
            <Button color="primary" size="small" variant="text" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "concentration")}>
              Edit concentration variables
            </Button>
          ):(
            <Button color="secondary" size="small" variant="text" className={classes.button} 
              onClick = {props.handleEditObject.bind(this, _object.id, "concentration")}>
              Add concentration variables
            </Button>
          )}
        </TableCell>
        
      </TableRow>
      )
    };
      return(      
      <Paper className={classes.objectsTable}>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <TableCell padding={"dense"} className={classes.tableCell}>ID</TableCell>
              <TableCell padding={"dense"} className={classes.tableCell}>Position </TableCell>
              <TableCell padding={"dense"} className={classes.tableCell}>Flux</TableCell>
              <TableCell padding={"dense"} className={classes.tableCell}>Concentration</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tableRows}
          </TableBody>
        </Table>
      </Paper>
      )


};

export default withStyles(styles)(OptimizationObjectsTable);

  


