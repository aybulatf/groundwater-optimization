import React from 'react'
// import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography'


import AddOptimizationObjects from './AddOptimizationObjects';
import CreateObjectives from './CreateObjectives';
import CreateConstraints from './CreateConstraints';
import RunOptimization from './RunOptimization';
import ModelUpload from './ModelUpload';

const styles = theme => ({
  root: {
    width: '90%',
    minWidth: '800px',
    marginLeft: "auto",
    marginRight: "auto"
  },
  
  button: {
    marginRight: theme.spacing.unit,
  },
  instructions: {
    marginTop: theme.spacing.unit,
    marginBottom: theme.spacing.unit,
  },
});

function getSteps() {
  return [
    'Upload a model',
    'Create optimization objects',
    'Define objectives',
    'Define constraints',
    'Run optimization'
  ];
}

function getStepContent(step, modelData, setModelData) {
  switch (step) {
    case 0:
      return <ModelUpload modelData={modelData} setModelData={setModelData}/>;
    case 1:
      return <AddOptimizationObjects modelData={modelData}  setModelData={setModelData}/>;
    case 2:
      return <CreateObjectives />;
    case 3:
      return <CreateConstraints />;
    case 4:
      return <RunOptimization />;
    default:
      return 'Unknown step';
  }
}

class MainWindow extends React.Component {
  constructor(props) {
    super(props);
    this.modeData = null;
    this.state = {
      activeStep: 0,
      skipped: new Set()
    };

  }
  setModelData(modelData){
    this.modeData = modelData;
  };
  isStepOptional = step => {
    return step === 3;
  };
  handleNext = () => {
    const { activeStep } = this.state;
    let { skipped } = this.state;
    if (this.isStepSkipped(activeStep)) {
      skipped = new Set(skipped.values());
      skipped.delete(activeStep);
    }
    this.setState({
      activeStep: activeStep + 1,
      skipped
    });
  };

  handleBack = () => {
    const { activeStep } = this.state;
    this.setState({
      activeStep: activeStep - 1,
    });
  };

  handleSkip = () => {
    const { activeStep } = this.state;
    if (!this.isStepOptional(activeStep)) {
      // You probably want to guard against something like this,
      // it should never occur unless someone's actively trying to break something.
      throw new Error("Can only skip the Define constraints step.");
    }
    this.setState(state => {
      const skipped = new Set(state.skipped.values());
      skipped.add(activeStep);
      return {
        activeStep: state.activeStep + 1,
        skipped,
      };
    });
  };

  handleReset = () => {
    this.setState({
      activeStep: 0,
    });
  };

  isStepSkipped(step) {
    return this.state.skipped.has(step);
  }

  render() {
    const { classes } = this.props;
    const steps = getSteps();
    const { activeStep } = this.state;

    return (
      <div className={classes.root}>
        <Stepper activeStep={activeStep}>
          {steps.map((label, index) => {
            const props = {};
            const labelProps = {};
            if (this.isStepOptional(index)) {
              labelProps.optional = <Typography variant="caption">Optional</Typography>;
            }
            if (this.isStepSkipped(index)) {
              props.completed = false;
            }
            return (
              <Step key={label} {...props}>
                <StepLabel {...labelProps}>{label}</StepLabel>
              </Step>
            );
          })}
        </Stepper>
   
        {getStepContent(activeStep, this.modeData, this.setModelData.bind(this))}
                  
        <Button
          disabled={activeStep === 0}
          onClick={this.handleBack}
          className={classes.button}
        >
          Back
                  </Button>
        {this.isStepOptional(activeStep) && (
          <Button
            variant="contained"
            color="primary"
            onClick={this.handleSkip}
            className={classes.button}
          >
            Skip
          </Button>
        )}
        <Button
          variant="contained"
          color="primary"
          onClick={this.handleNext}
          className={classes.button}
        >
          {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
        </Button>
      </div>
    );
  }
}

// MainWindow.propTypes = {
//   classes: PropTypes.object,
// };

export default withStyles(styles)(MainWindow);