class ObjectPosition {

    constructor (nlay, nrow, ncol) {
        this.minLay = 0;
        this.minRow = 0;
        this.minCol = 0;
        this.maxLay = nlay-1;
        this.maxRow = nrow-1;
        this.maxCol = ncol-1;

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
    };
};

export default ObjectPosition;