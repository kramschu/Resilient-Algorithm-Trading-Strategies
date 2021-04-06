import React, { Component } from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import axios from "axios";
import { AuthTypes } from "../constants/actionTypes";

axios.defaults.withCredentials = true;

class Header extends Component {

    static propTypes = {
        authenticated: PropTypes.bool
    };

    constructor(props) {
        super(props);
    };

    componentDidMount() {
        axios.get("http://127.0.0.1:8000/cred/user").then((response) => {
                    console.log(response.data);
                    if (response.data.logged_in == true) {
                        localStorage.username = response.data.username;
                        this.props.dispatch({type: AuthTypes.OAUTH2_LOGIN});
                        console.log(this.props.authenticated);
                    }
                });
    };
    
    renderLinks() {
        if (this.props.authenticated) {
            return (
                [
                    <li className="nav-item" key="profile">
                        <Link className="nav-link" to="/profile">Hi {localStorage.username}</Link>
                    </li>,
                    <li className="nav-item" key="logout">
                        <Link className="nav-link" to="/logout">Logout</Link>
                    </li>,
                    <li className="nav-item" key="dashboard">
                        <Link className="nav-link" to="/dashboard"><b>Dashboard</b></Link>
                    </li>
                ]
            );

        } else {
            return (
                [
                    <li className="nav-item" key="login">
                        <Link className="nav-link" to="/login">Login</Link>
                    </li>,
                    <li className="nav-item" key="signup">
                        <Link className="nav-link" to="/signup">Sign Up</Link>
                    </li>,
                    <li className="nav-item" key="dashboard">
                        <Link className="nav-link" to="/dashboard">Dashboard</Link>
                    </li>
                ]
            );
        }
    }

    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <Link to="/" className="navbar-brand">RATS</Link>
                <ul className="navbar-nav">
                    {this.renderLinks()}
                </ul>
            </nav>
        )
    }
}

function mapStateToProps(state) {
    return {
        authenticated: state.auth.authenticated
    }
}
export default connect(mapStateToProps)(Header);
// export default Header;