import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography'
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const styles = {
  overviewTable: {
    width: '100%',
    marginTop: 10,
    marginBottom: 10,
    overflowX: 'auto',
  },
  table: {
    width: 400
  }
};

const ModelOverviewTable = props => {
  const { classes } = props;
    return(
      <div>
        <Typography variant="headline" gutterBottom>
          Model overview
        </Typography>
        <Paper className={classes.addModelObjects}>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <TableCell>Parameter</TableCell>
                <TableCell>Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Modflow packages</TableCell>
                <TableCell>{props.mfPackages.toString()}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>MT3D packages</TableCell>
                <TableCell>{props.mfPackages.toString()}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Number of layers</TableCell>
                <TableCell>{props.nlay}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Number of columns</TableCell>
                <TableCell>{props.ncol}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Number of rows</TableCell>
                <TableCell>{props.nrow}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Number of stress-periods</TableCell>
                <TableCell>{props.nper}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </Paper>
      </div>
    )
};

export default withStyles(styles)(ModelOverviewTable);

  


