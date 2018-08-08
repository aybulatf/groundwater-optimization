import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';

import Grid from '@material-ui/core/Grid';


import ModelGrid from './ModelGrid';
import OptimizationObjectsTable from './OptimizationObjectsTable';
import OptimizationObject from './prototypes/OptimizationObject'
import FormPosition from './forms/FormPosition'
import FormFlux from './forms/FormFlux'
import FormConcentration from './forms/FormConcentration'

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
      console.log(newObject)
      return {optimizationObjects: prevState.optimizationObjects.concat([newObject])};
    });
  };

  handleEditObject(index, parameter) {
    console.log(index)
    console.log(parameter)
    this.setState({
      editedObjectIndex: index,
      editedParameter: parameter
    });
  };

  render() {

    const { classes } = this.props;
    const { optimizationObjects, editedObjectIndex, editedParameter } = this.state;
    console.log(editedParameter)
    console.log(editedObjectIndex)
    return (
      <Paper className={classes.root}>
        <Grid>
          <Grid item xs={6}>
            <OptimizationObjectsTable
              optimizationObjects={optimizationObjects}
              handleEditObject={this.handleEditObject.bind(this)}
            />
            <Button color="primary" className={classes.button} onClick={this.handleAddObject.bind(this)}>
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
            {/* {function () {
              
              switch (editedParameter) {
                
                case "position":
                return(
                  <FormPosition
                    optimizationObject={optimizationObjects[editedObjectIndex]}
                    handleEditObject={this.handleEditObject.bind(this)}
                  />)
                  break;
                case "flux":
                  <FormFlux
                    optimizationObject={optimizationObjects[editedObjectIndex]}
                    handleEditObject={this.handleEditObject.bind(this)}
                  />
                  break;
                case "concentration":
                  <FormConcentration
                    optimizationObject={optimizationObjects[editedObjectIndex]}
                    handleEditObject={this.handleEditObject.bind(this)}
                  />
                  break;

                default:
                  break;
              }
            }
            } */}
          </Grid>
        </Grid>

      </Paper>
    )
  }
};


export default withStyles(styles)(AddOptimizationObjects);

