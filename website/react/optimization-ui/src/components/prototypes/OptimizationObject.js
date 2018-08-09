

class OptimizationObject {
    type = "wel";
    constructor (_id, nlay, nrow, ncol, nper) {
        this.positionAdded = false;
        this.fluxAdded = false;
        this.concentrationAdded = false;
        this.id = _id;

        this.position = {
            lay: {
                min: 0,
                max: 0
            },
            row: {
                min: 0,
                max: 0
            },
            col: {
                min: 0,
                max: 0
            }
        };
        this.flux = {};
        this.concentration = {};
        for (let period of [...Array(nper).keys()]){
            this.flux[period] = {min: 0, max: 0};
            this.concentration[period] = {component1:{min: 0, max: 0}}
            
        }
    }
    setPosition(data){
        
        for (let key in data) {
            switch(key){
                case "layerMin":
                    this.position.lay.min = data[key];
                    break;
                case "layerMax":
                    this.position.lay.max = data[key];
                    break;
                case "rowMin":
                    this.position.row.min = data[key];
                    break;
                case "rowMax":
                    this.position.row.max = data[key];
                    break;
                case "colMin":
                    this.position.col.min = data[key];
                    break;
                case "colMax":
                    this.position.col.max = data[key];
                    break;
            }
        }
    }
};

export default OptimizationObject;
