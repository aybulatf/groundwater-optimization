import React from 'react'
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';

const styles = {
  button: {
    margin: 10
  },
  saveButton: {
    marginTop: 10,
  },
  textField: {
    margin: 10,
    padding: 5,
    width: 100
  },
  subheading: {
    margin: 10
  },
  formPosition: {
    width: '100%',
    marginTop: 20,
    overflowX: 'auto',
  }
};

class FormPosition extends React.Component {
  constructor(props) {
    super(props);
    this.optimizationObject = props.optimizationObject;

    this.state = {
      layerMin: this.optimizationObject.position.lay.min,
      layerMax: this.optimizationObject.position.lay.max,
      rowMin: this.optimizationObject.position.row.min,
      rowMax: this.optimizationObject.position.row.max,
      colMin: this.optimizationObject.position.col.min,
      colMax: this.optimizationObject.position.col.max
    };
  }
  handleSubmit() {
    this.optimizationObject.setPosition(this.state);
    this.optimizationObject.positionAdded = true;
    this.props.handleEditObject(null, null)

  }
  handleInputChange = param => event => {
    this.setState({
      [param]: event.target.value
    });
  }
  render() {
    const { classes } = this.props;
    return (
      <div>

        <Typography variant="title" gutterBottom>
          Edit position variables
        </Typography>

        <Paper className={classes.formPosition}>
          <Typography className={classes.subheading} variant="subheading" gutterBottom>
          
            Set layer range
          </Typography>
          <br/>
          <TextField
            id="layerMin"
            label="Layer from:"
            value={this.state.layerMin}
            onChange={this.handleInputChange("layerMin")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />
          <TextField
            id="layerMax"
            label="Layer to:"
            value={this.state.layerMax}
            onChange={this.handleInputChange("layerMax")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />

        </Paper>
        <Paper className={classes.formPosition}>
          <Typography className={classes.subheading} variant="subheading" gutterBottom>
            Set row/column range
          </Typography>
          <br/>
          <TextField
            id="rowMin"
            label="Row from:"
            value={this.state.rowMin}
            onChange={this.handleInputChange("rowMin")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />
          <TextField
            id="rowMax"
            label="Row to:"
            value={this.state.rowMax}
            onChange={this.handleInputChange("rowMax")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />
          <br/>
          <TextField
            id="colMin"
            label="Column from:"
            value={this.state.colMin}
            onChange={this.handleInputChange("colMin")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />
          <TextField
            id="colMax"
            label="Column to:"
            value={this.state.colMax}
            onChange={this.handleInputChange("colMax")}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />

          <Button color="primary" variant="outlined" className={classes.button}
            onClick={this.handleSubmit.bind(this)}>
            Set with map
          </Button>

        </Paper>
 
        <Button color="primary" variant="contained" className={classes.saveButton}
          onClick={this.handleSubmit.bind(this)}>
          Save
        </Button>

      </div>
    )
  }
}

export default withStyles(styles)(FormPosition);