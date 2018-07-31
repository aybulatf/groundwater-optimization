import React from 'react';
import './App.css';
import NavBar from './components/Navbar'
import MainWindow from './components/MainWindow'

class App extends React.Component {

  constructor(props) {
    super(props);
    this.optimizationData = {
      uploadedModel: null,
      optimizationObjects: null,
      optimizationObjectives: null,
      optimizationConstraints: null,
      progressLog: null,
      optimizationResults: null
    };
  }

  setData(category, data) {
    this.optimizationData.category = data;
  }

  render() {
    return (
      <div>
        <NavBar />
        <MainWindow setData={this.setData} />
      </div>
    );
  }

}

export default App;
