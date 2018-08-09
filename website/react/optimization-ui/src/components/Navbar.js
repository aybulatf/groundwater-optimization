import React from 'react'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import { withStyles } from '@material-ui/core/styles';

const styles = {
  navbar: {
    // backgroundColor: "#4C4C4C"
  }
};

const NavBar = (props) => {
  const { classes } = props;
  return (
      <AppBar className={classes.navbar} position="static">
        <Toolbar>
          <Typography variant="title" color="inherit">
            Groundwater optimization
          </Typography>
        </Toolbar>
      </AppBar>
  )
}

export default withStyles(styles)(NavBar);