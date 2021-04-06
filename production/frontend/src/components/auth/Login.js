import React, { Component } from "react";
// import PropTypes from "prop-types";
import { reduxForm, Field, propTypes } from "redux-form";
import { Link } from "react-router-dom";
import { required } from "redux-form-validators"

import { renderField, renderError} from "../../utils/renderUtils";
import { loginUser } from "../../actions/authActions";
import axios from "axios";
import "../../styles/loginStyle.css";

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
        axios.get("https://rats-osu2021.herokuapp.com/oauth2/url").then( (response) => { this.setState({oauth2_url: response.data.url}) });
    };
    render() {
        const { handleSubmit, error } = this.props;

        // html
        return (
            <div>
                <form
                    id="loginId"
                    className="col col-sm-4 card p-2"
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

                    <fieldset className="col col-sm-4 card p-2">
                        { renderError(error) }
                        <button type="submit">Login with RATS account</button>
                        <br></br>
                        <a className="button" href={this.state.oauth2_url}>Login with Google OAuth2</a>
                    </fieldset>
                    <br></br>
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
