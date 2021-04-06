import React, {Component} from "react";
import Header from "./Header";
import MainContent from "./MainContent";
import '../styles/appStyle.css';


export default class App extends Component {
    
    constructor(props) {
        super(props);
    };

    render() {
        return (
            <div className="container"
            >
                <Header />
                <MainContent />
            </div>
        );
    }
}