import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';

import Grid from '@material-ui/core/Grid';


import ModelGrid from './ModelGrid';
import OptimizationObjectsTable from './OptimizationObjectsTable';

const styles = {
  root: {
    margin: 20,
    padding: 20,
    minWidth: 800,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    margin: 20,
  },
  rightIcon: {
    marginLeft: 10,
  },
}

class AddOptimizationObjects extends React.Component {
  _optimizationObjectPrototype = {
    id: null,
    position: {
      lay: {
        min: null,
        max: null
      },
      row: {
        min: null,
        max: null
      },
      col: {
        min: null,
        max: null
      }
    },
  }
  constructor(props) {
    super(props);
    
    this.state = {
      optimizationObjects: []
    };
  }

  handleAddObject() {
    this.setState({
      optimizationObjects : this.state.optimizationObjects.concat([this._optimizationObjectPrototype])
    });
  };
  
  render() {

    const { classes } = this.props;
    const { optimizationObjects } = this.state;
    return (
      <Paper className={classes.root}>

          <Grid container spacing={24}>
            <Grid item xs>
              <OptimizationObjectsTable 
                optimizationObjects = {optimizationObjects}
              />
              <Button color="primary" className={classes.button} onClick = {this.handleAddObject.bind(this)}>
                Add wel
              </Button>
            </Grid>
            
            <Grid item xs>
              {/* <ModelGrid
                modelData = {modelData}
                width = {500}
                height = {500}
              /> */}
            </Grid>
          </Grid>
            
      </Paper>
    )
  }
};
  

export default withStyles(styles)(AddOptimizationObjects);

