import React, { Component } from "react";
// import PropTypes from "prop-types";
import { reduxForm, Field, propTypes } from "redux-form";
import { Link } from "react-router-dom";
import { required } from "redux-form-validators"

import { renderField, renderError} from "../../utils/renderUtils";
import { loginUser } from "../../actions/authActions";
import axios from "axios";
import "../../styles/loginStyleOAuth2.css";

axios.defaults.withCredentials = true;
class LoginOAuth2 extends Component {

    static propTypes = {
        ...propTypes
    };

    constructor(props) {
        super(props);
        this.state = {
            email: '',
            firstname: '',
            lastname: '',
        };
    };

    componentDidMount() {
        axios.get("https://rats-osu2021.herokuapp.com/cred/user")
             .then( (response) => { this.setState({
                        email: response.data.username,
                        firstname: response.data.firstname,
                        lastname: response.data.lastname,
                    }); 
                    this.props.change('email', response.data.email);
                    this.props.change('password', response.data.firstname);
                    this.props.change('oauth2', true);
                }
             );
    };

    render() {
        const { handleSubmit, error } = this.props;

        // html
        return (
            <div className="oauth2-mainpage">
                <div className="greeting">
                    <h1>Welcome back to the RATS pack</h1> 
                    <h1 className="oauth2-name">{this.state.firstname} {this.state.lastname}</h1>
                    <h2>Please click the button below to confirm login</h2>
                </div>
                <form
                    className="oauth2-form"
                    onSubmit={handleSubmit}
                >                
                    <fieldset >
                        { renderError(error) }
                        <button action="submit"><h3>Confirm Gmail Login to RATS</h3></button>
                        <br></br>
                    </fieldset>
                    <br></br>
                </form>
            </div>
        )
    }
}

export default reduxForm({
    form: "loginoauth2",
    onSubmit: loginUser
})(LoginOAuth2);
