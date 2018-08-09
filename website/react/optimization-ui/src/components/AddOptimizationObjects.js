import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';


import ModelGrid from './ModelGrid';
import OptimizationObjectsTable from './OptimizationObjectsTable';
import OptimizationObject from './prototypes/OptimizationObject'
import FormPosition from './forms/FormPosition'
import FormFlux from './forms/FormFlux'
import FormConcentration from './forms/FormConcentration'

const styles = {
  addModelObjects: {
    // margin: 20,
    padding: 20,
    width: "100%",
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#EFF3F6'
  },
}

class AddOptimizationObjects extends React.Component {
  constructor(props) {
    super(props);
    this.modelData = props.modelData,

      this.state = {
        optimizationObjects: []
      };
    this.editedObject = null;
    this.editedParameter = null;
  }

  handleAddObject() {
    this.setState((prevState, props) => {
      let newObject = new OptimizationObject(
        prevState.optimizationObjects.length,
        this.modelData.data.mf.DIS.nlay,
        this.modelData.data.mf.DIS.nrow,
        this.modelData.data.mf.DIS.ncol,
        this.modelData.data.mf.DIS.nper
      );
      return {optimizationObjects: prevState.optimizationObjects.concat([newObject])};
    });
  };

  handleEditObject(index, parameter) {
    this.setState({
      editedObjectIndex: index,
      editedParameter: parameter
    });
  };

  render() {

    const { classes } = this.props;
    const { optimizationObjects, editedObjectIndex, editedParameter } = this.state;
    console.log(optimizationObjects)
    return (
      <Paper className={classes.addModelObjects}>
        <Grid container spacing={24}>
          <Grid item xs={6}>
            <Typography variant="title" gutterBottom>
              Optimization objects:
            </Typography>
            <OptimizationObjectsTable
              optimizationObjects={optimizationObjects}
              handleEditObject={this.handleEditObject.bind(this)}
            />
            <Button color="primary" variant="outlined" className={classes.button} onClick={this.handleAddObject.bind(this)}>
              Add wel
            </Button>
          </Grid>

          <Grid item xs={6}>
            {editedParameter === "position" && (
               <FormPosition
               optimizationObject={optimizationObjects[editedObjectIndex]}
               handleEditObject={this.handleEditObject.bind(this)}
             />
            )}
            {editedParameter === "flux" && (
               <FormFlux
               optimizationObject={optimizationObjects[editedObjectIndex]}
               handleEditObject={this.handleEditObject.bind(this)}
             />
            )}
            {editedParameter === "concentration" && (
               <FormConcentration
               optimizationObject={optimizationObjects[editedObjectIndex]}
               handleEditObject={this.handleEditObject.bind(this)}
             />
            )}
          </Grid>
        </Grid>

      </Paper>
    )
  }
};


export default withStyles(styles)(AddOptimizationObjects);

