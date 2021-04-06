import React, { Component } from "react";
import axios from "axios";
import "../../styles/algorithmUploadStyle.css";

axios.defaults.withCredentials = true;


class AlgorithmUpload extends Component {
  constructor(props) {
    super(props);

    this.state = {
      file: null,
    };

    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleFileChange = this.handleFileChange.bind(this);
  };

    handleSubmit (e) {
        e.preventDefault();
        console.log(this.state.file.name)
        let form_data = new FormData();
        form_data.append('file', this.state.file, this.state.file.name);
        // form_data.append('name', this.state.file.name);

        let url = 'https://rats-osu2021.herokuapp.com/api/quant_connect/algorithm_manager/upload_algorithm';
        axios.post(url, form_data, {
        headers: {
            'content-type': 'multipart/form-data'
        }
        })
            .then(res => {
            console.log(res.data);
            })
            .catch(err => console.log(err));
        this.uploadInput.value='';

  };

  handleFileChange = (e) => {
    this.setState({
      file: e.target.files[0]
    });
  };
  render() {
    return (
        <div className="algorithm-upload-content">
            <div>
                <span className="algorithm-upload-header">Upload Algorithm</span>
            </div>
            <form className="algorithm-upload-form" onSubmit={this.handleSubmit}>
                <div>
                    <input ref={(ref) => { this.uploadInput = ref; }} type="file" accept=".py" 
                     onChange={this.handleFileChange} required/>
                </div>
                <button className="algorithm-upload-button" type="submit">Upload</button>
            </form>
        </div>

    );
  }
}

export default AlgorithmUpload;
