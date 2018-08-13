

class OptimizationObject {
  type = "wel";
  constructor(_id) {
    this.id = _id;
    this.position = null;
    this.flux = null;
    this.concentration = null;
  }
};

export default OptimizationObject;
