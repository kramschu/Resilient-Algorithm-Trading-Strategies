import React, { Component } from "react";
// import PropTypes from "prop-types";
import { reduxForm, Field, propTypes } from "redux-form";
import { Link } from "react-router-dom";
import { required } from "redux-form-validators"

import { renderField, renderError} from "../../utils/renderUtils";
import { loginUser } from "../../actions/authActions";
import axios from "axios";

axios.defaults.withCredentials = true;

class Login extends Component {

    static propTypes = {
        ...propTypes
    };

    constructor(props) {
        super(props);
        this.state = {
            oauth2_url: '',
        };
    };
    
    componentDidMount() {
        axios.get("http://127.0.0.1:8000/oauth2/url").then( (response) => { this.setState({oauth2_url: response.data.url}) });
    };


    render() {
        const { handleSubmit, error } = this.props;

        return (
            <div className="row justify-content-center">
                <div className="col col-sm-4 card mt-5 p-2">
                    <a href={this.state.oauth2_url}><button>Click here for Google OAuth2</button></a>
                </div>
                <form
                    className="col col-sm-4 card mt-5 p-2"
                    onSubmit={handleSubmit}
                >
                    <h4 className="text-md-center">Please Log In</h4>
                    <hr/>

                    <fieldset className="form-group">
                        <Field name="email" label="Email" component={renderField}
                               type="text" validate={[required({message: "This field is required."})]}
                        />
                    </fieldset>


                    <fieldset className="form-group">
                        <Field name="password" label="Password" component={renderField}
                               type="password"  validate={[required({message: "This field is required."})]}
                        />
                    </fieldset>

                    <fieldset className="form-group">
                        { renderError(error) }
                        <button action="submit" className="btn btn-primary">Login</button>
                    </fieldset>

                    <p>Not registered? <Link to="/signup">Signup Here!</Link></p>
                    <Link to="/reset_password">forgot password?</Link>
                </form>
            </div>
        )
    }
}

export default reduxForm({
    form: "login",
    onSubmit: loginUser
})(Login);
