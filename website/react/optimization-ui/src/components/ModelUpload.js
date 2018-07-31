import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography'
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';

const styles = {
  root: {
    margin: 20,
    padding: 20,
    minWidth: 800
  },
  input: {
    display: 'none',
  },
}

class ModelUpload extends React.Component {
  constructor(props) {
    super(props);

    this.maxModelSize = 10;
    this.validFileExtensions = ["nam", "dis", "bas", "wel", "chd", "ghb", "riv"]

    this.state = {

    };

    // this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUpload(event) {
    let formData = new FormData();
    let totalModelSize = 0;
    try {
      for(let file of event.target.files) {
        let extension = file.name.split(".")[1]
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
    for(var pair of formData.entries()) {
      console.log(pair[0]+ ', '+ pair[1]); 
   }
    fetch('http://localhost:5000/model-upload', {
      method: 'POST',
      body: formData,
    }).then((response) => {
      response.json().then((body) => {
      console.log(body.message)
      });
    });  
  };
  
  render() {
    const { classes } = this.props;
    return (
      <Paper className={classes.root}>
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
          </Button>
        </label>
      </Paper>
    )
  }
};
  

export default withStyles(styles)(ModelUpload);

