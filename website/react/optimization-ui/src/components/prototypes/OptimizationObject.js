

class OptimizationObject {
    type = "wel";
    constructor (_id, nlay, nrow, ncol, nper) {
        this.positionAdded = false;
        this.fluxAdded = false;
        this.concentrationAdded = false;
        this.id = _id;
        this.name = null
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
        },
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
                case key === "layMin":
                    this.lay.min = data[key];
                    break;
                case key === "layMax":
                    this.lay.max = data[key];
                    break;
                case key === "rowMin":
                    this.row.min = data[key];
                    break;
                case key === "lrowMax":
                    this.row.max = data[key];
                    break;
                case key === "colMin":
                    this.col.min = data[key];
                    break;
                case key === "colMax":
                    this.col.max = data[key];
                    break;
            }
        }
    }
};

export default OptimizationObject;
