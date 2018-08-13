class ObjectFlux {
  constructor(nper) {
    this.flux = {};
    for (let period of [...Array(nper).keys()]) {
      this.flux[period] = { min: 0, max: 0 };
    }
  }
};

export default ObjectFlux;