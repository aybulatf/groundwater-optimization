class ObjectConcentration {
    constructor(nper) {
      this.concentration = {};
      for (let period of [...Array(nper).keys()]) {
        this.concentration[period] = {};
        this.concentration[period]["component1"] = { min: 0, max: 0 };
      }
    }
  };
  
  export default ObjectConcentration;