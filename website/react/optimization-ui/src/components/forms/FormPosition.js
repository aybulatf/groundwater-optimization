import React from 'react'

class FormPosition extends React.Component {
    constructor(props) {
        super(props);
        this.optimizationObject = props.optimizationObject;
        console.log(this.optimizationObject)
        
        this.state = {
            layerMin: this.optimizationObject.position.lay.min,
            layerMax: this.optimizationObject.position.lay.max,
            rowMin: this.optimizationObject.position.row.min,
            rowMax: this.optimizationObject.position.row.max,
            colMin: this.optimizationObject.position.col.min,
            colMax: this.optimizationObject.position.col.max
        };
    }
    handleSubmit(event){
        this.optimizationObject.setPosition(this.state);
        this.optimizationObject.positionAdded = true;
        console.log(this.optimizationObject)
        this.props.handleEditObject(null, null)
        event.preventDefault();
    }
    handleInputChange = name => event => {
        const target = event.target;
        const value = target.value;
        // const name = target.name;
        console.log(name)
        // console.log(target.name1)

        this.setState({
            [name]: value
        });
      }
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Layer from:
                    <input
                        required
                        value = {this.state.layerMin}
                        type="number"
                        onChange={this.handleInputChange("layerMin")} 
                    />
                </label>
                <br />
                <label>
                    Layer to:
                    <input
                        required
                        name="layerMax"
                        value = {this.state.layerMax}
                        type="number"
                        onChange={this.handleInputChange.bind(this)} 
                    />
                </label>
                <label>
                    Row from:
                    <input
                        required
                        name="rowMin"
                        value = {this.state.rowMin}
                        type="number"
                        onChange={this.handleInputChange} 
                    />
                </label>
                <label>
                    Row to:
                    <input
                        required
                        name="rowMax"
                        value = {this.state.rowMax}
                        type="number"
                        onChange={this.handleInputChange} 
                    />
                </label>
                <label>
                    Column from:
                    <input
                        required
                        name="colMin"
                        value = {this.state.colMin}
                        type="number"
                        onChange={this.handleInputChange} 
                    />
                </label>
                <label>
                    Column to:
                    <input
                        required
                        name="colMax"
                        value = {this.state.colMax}
                        type="number"
                        onChange={this.handleInputChange} 
                    />
                </label>
                <input type="submit" value="Save" />
            </form>
        )
    }
}

export default FormPosition;