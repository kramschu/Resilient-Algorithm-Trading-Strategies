import React, { Component } from "react";
import axios from "axios";
import "../../styles/dashboardStyle.css";

class Dashboard extends Component {
  constructor(props) {
      super(props);
      this.state = {
        error: null,
        isLoaded: false,
        items: [],
        pastFiles: [],
        algResults: "",
        algorithms: [
          "AddRiskManagementAlgorithm",
          "AddOptionContractExpiresRegressionAlgorithm",
          "BasicSetAccountCurrencyAlgorithm",
          "BasicTemplateForexAlgorithm",
          "BasicTemplateAlgorithm",
          "BasicTemplateFrameworkAlgorithm",
          "BasicTemplateFuturesAlgorithm",
          "BasicTemplateOptionsAlgorithm",
          "BrokerageModelAlgorithm", 
          "BubbleAlgorithm",
          "ConfidenceWeightedFrameworkAlgorithm",
          "ConstituentsQC500GeneratorAlgorithm",
          "CustomBenchmarkAlgorithm",
          "CustomDataBitcoinAlgorithm",
          "CustomDataNIFTYAlgorithm",
          "DailyAlgorithm",
          "DataConsolidationAlgorithm",
          "MACDTrendAlgorithm",
          "MomentumLeverage",
          "OptionChainProviderAlgorithm",
          "RollingWindowAlgorithm",
          "ScheduledEventsAlgorithm"
        ]
      };
  }
  componentDidMount() {
    axios.get("http://127.0.0.1:8000/api/quant_connect/algorithm_manager/get_past_runs/")
    .then((response) => {
      this.setState({pastFiles: response.data.past_runs});
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  submitAlgorithm() {
    // const method = "POST";
    const formStart = document.getElementById("startdate").value;
    const startdate = [];
    startdate[0] = formStart.slice(5, 7);
    startdate[1] = formStart.slice(8, 10);
    startdate[2] = formStart.slice(0, 4);
    const formEnd = document.getElementById("enddate").value;
    const enddate = [];
    enddate[0] = formEnd.slice(5, 7);
    enddate[1] = formEnd.slice(8, 10);
    enddate[2] = formEnd.slice(0, 4);
    const body = {
      "algorithm": document.getElementById("alg-name").value,
      "cash": document.getElementById("cashAmount").value,
      "buytol": document.getElementById("buytol").value,
      "selltol": document.getElementById("selltol").value,
      "startdate": startdate,
      "enddate": enddate,
    };
    fetch("http://127.0.0.1:8000/api/quant_connect/algorithm_manager/set_algorithm/", { 
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type': 'application/json',
      }, 
      method: 'POST', 
      body: JSON.stringify(body) 
      })
      .then(response => response.json())
      .then((data) => {
        const tempResults = [];
        tempResults.push(JSON.stringify(data));
        this.setState({algResults: tempResults});
      });
      console.log(this.state.algResults);
  }
  render() {
    return (
      <div className="lp">
        <div className="run-algs-content">
          <div>
            <span className="run-algs-header">Run Algorithm</span>
          </div>
          <form ref={el => (this.form = el)}>
            <label htmlFor="alg-name">Algorithm</label><br></br>
            <select id="alg-name" placeholder="Algorithm">
            {this.state.algorithms.map(option => (
              <option key={option} value={option}>
                {option}
              </option>
              ))}
            </select>
            <div>
              <label htmlFor="cashAmount">Cash Amount</label><br></br> 
                <input id="cashAmount" placeholder="Cash Amount" className="basic-slide" type="number">
                </input>
            </div>
            <div>
              <label htmlFor="buytol">Buy Tolerance</label><br></br> 
                <input id="buytol" placeholder="Buy Tolerance" type="number">
                </input>
            </div>
            <div>
              <label htmlFor="selltol">Sell Tolerance</label><br></br> 
                <input id="selltol" placeholder="Sell Tolerance" type="number">
                </input>
            </div>
            <div>
              <label htmlFor="startdate">Start Date</label><br></br> 
                <input id="startdate" placeholder="Start Date" type="date">
                </input>
            </div>
            <div>
              <label htmlFor="enddate">End Date</label><br></br> 
                <input id="enddate" placeholder="End Date" type="date">
                </input>
            </div>
            <div>
              <span>
                <button onClick={() => this.submitAlgorithm()} id="submit-alg" type="button" >Run Algorithm</button>
              </span>
            </div> 
          </form>
        </div>
        <div className="past-run-content">
        <div>
            <span className="past-runs-header">Past Runs</span>
        </div>
        <ul id="file-name">
              {this.state.pastFiles.map(option => (
                <li className="file-list" key={option} value={option}>
                  {option}
                </li>
                ))}
        </ul>
        </div>
        <div className="algorithm-results-content">
          <div className="alg-results-header">Algorithm Results</div>
          <div className="results-text"> {this.state.algResults}
        </div>
      </div>
      </div>
    );
  }
}
export default Dashboard;
