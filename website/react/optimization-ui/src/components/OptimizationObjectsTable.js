import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography'
import TextField from '@material-ui/core/TextField';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const styles = {
  table: {
    width: 400
  },
  textField: {
    marginLeft: 0,
    marginRight: 0,
    width: 50,
  },
};

const OptimizationObjectsTable = props => {
  const { classes } = props;
  const { optimizationObjects } = props;
  const tableRows = optimizationObjects.map((_object) =>
    <TableRow>
      <TableCell>
        <TextField
            id="name"
            className={classes.textField}
            value={_object.id}
            // onChange={this.handleChange('name')}
            margin="normal"
          />
      </TableCell>
      <TableCell>
      <TextField
          id="layMin"
          value={_object.position.lay.min}
          // onChange={this.handleChange('age')}
          type="number"
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
      </TableCell>
      <TableCell>
      <TextField
          id="layMax"
          value={_object.position.lay.max}
          // onChange={this.handleChange('age')}
          type="number"
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
      </TableCell>
      <TableCell>
      <TextField
          id="rowMin"
          value={_object.position.row.min}
          // onChange={this.handleChange('age')}
          type="number"
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
      </TableCell>
      <TableCell>
      <TextField
          id="rowMax"
          value={_object.position.row.max}
          // onChange={this.handleChange('age')}
          type="number"
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
      </TableCell>
      <TableCell>
      <TextField
          id="colMin"
          value={_object.position.col.min}
          // onChange={this.handleChange('age')}
          type="number"
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
      </TableCell>
      <TableCell>
      <TextField
          id="colMax"
          value={_object.position.col.ma}
          // onChange={this.handleChange('age')}
          type="number"
          className={classes.textField}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
      </TableCell>
    </TableRow>
  );

    return(
      <div>
        <Typography variant="headline" gutterBottom>
          Optimization objects
        </Typography>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Layer from</TableCell>
              <TableCell>layer to</TableCell>
              <TableCell>Row from</TableCell>
              <TableCell>Row to</TableCell>
              <TableCell>Column from</TableCell>
              <TableCell>Column to</TableCell>
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

  


