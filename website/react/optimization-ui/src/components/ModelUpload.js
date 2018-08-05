import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography'
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';

import ModelGrid from './ModelGrid';
import ModelOverviewTable from './ModelOverviewTable';

const styles = {
  root: {
    margin: 20,
    padding: 20,
    minWidth: 800,
    justifyContent: 'center',
    alignItems: 'center',
  },
  input: {
    display: 'none',
  },
  progress: {},
  table: {
    width: 400
  },
  button: {
    margin: 20,
  },
  rightIcon: {
    marginLeft: 10,
  },
}

class ModelUpload extends React.Component {
  constructor(props) {
    super(props);

    this.maxModelSize = 10;
    this.validFileExtensions = [
      "nam", "dis", "bas", "bas6", "lpf", "pcg", "oc", "wel", "chd", "lmt", "lmt6", "nwt", "rch", "ghb",
      "adv", "btn", "dsp", "gcg", "ssm"
    ]

    this.state = {
      message: null,
      modelData: null,
      modelUploaded: false,
      modelUploadedSuccess: false
    };
  }

  handleUpload(event) {
    let formData = new FormData();
    let totalModelSize = 0;
    try {
      for(let file of event.target.files) {
        let extension = file.name.split(".")[1].toLowerCase()
        if (this.validFileExtensions.indexOf(extension) < 0) {
          throw "Invalid file extension - " + extension;
        }
        totalModelSize += file.size;
        if (totalModelSize > this.maxModelSize*1024*1024) {
          throw "Max model size " + this.maxModelSize+ " mb limmit exceeded";
        }
        formData.append('file[]', file, file.name);
      }
    } catch (error) {
      alert("Error: " + error + ".");
    }

    this.setState(
      {
        waitingForResponse: true
      }
    );

    fetch('http://localhost:80/model-upload', {
      method: 'POST',
      body: formData,
    }).then((response) => {
      response.json().then((body) => {

        let modelUploadedSuccess = false;

        if (body.message.code == 200) {
          modelUploadedSuccess = true;
        }
   
        this.setState(
          {
            message: body.message,
            modelData: body.model_data,
            modelUploaded: true,
            modelUploadedSuccess: modelUploadedSuccess,
            waitingForResponse: false
          }
        );
      });
    });  
  };
  
  render() {

    const { classes } = this.props;
    const { modelData } = this.state;
    return (
      <Paper className={classes.root}>

        {this.state.waitingForResponse ? (
          <div className={classes.progress} >
            <CircularProgress />
          </div>
        ) : (
          <div>
            {this.state.modelUploaded ? (
              <div>
                <Grid container spacing={24}>
                  <Grid item xs>
                    <ModelOverviewTable 
                      mfPackages = {modelData.data.mf.packages}
                      mtPackages = {modelData.data.mt.packages}
                      nlay = {modelData.data.mf.DIS.nlay}
                      nrow = {modelData.data.mf.DIS.nrow}
                      ncol = {modelData.data.mf.DIS.ncol}
                      nper = {modelData.data.mf.DIS.nper}
                    />
                  </Grid>
                  <Grid item xs>
                    <ModelGrid
                      modelData = {modelData}
                      width = {500}
                      height = {500}
                    />
                  </Grid>
                </Grid>
                    
                <input
                  className={classes.input}
                  id="outlined-button-file"
                  multiple
                  type="file"
                  onChange={this.handleUpload.bind(this)}
                />
                <label htmlFor="outlined-button-file">
                  <Button color="primary" variant="outlined" component="span" className={classes.button}>
                    Upload another
                    <CloudUploadIcon className={classes.rightIcon}/>
                  </Button>
                </label>
              </div>
            ) : (
              <div>
                <Typography variant="headline" gutterBottom>
                  Upload MODFLOW and MT3D-USGS model files
                </Typography>
                <Typography variant="subheading" gutterBottom>
                  Valid extensions: { this.validFileExtensions.toString() }
                </Typography>
                <Typography variant="subheading" gutterBottom>
                  Max model size: { this.maxModelSize } MB
                </Typography>
                <input
                  className={classes.input}
                  id="outlined-button-file"
                  multiple
                  type="file"
                  onChange={this.handleUpload.bind(this)}
                />
                <label htmlFor="outlined-button-file">
                  <Button color="primary" variant="outlined" component="span" className={classes.button}>
                    Upload
                    <CloudUploadIcon className={classes.rightIcon}/>
                  </Button>
                </label>
              </div>
            )}
          </div>
        )}
      </Paper>
    )
  }
};
  

export default withStyles(styles)(ModelUpload);

