import React, { Component} from "react";
import axios from "axios";
import Plot from 'react-plotly.js';
import "../../styles/dashboardStyle.css";
import Tabs from "./Tabs";
import ReactTable from "react-table-6";
import AlgorithmUpload from "./algorithmUpload";
import "react-table-6/react-table.css"
import 'font-awesome/css/font-awesome.min.css';

class Dashboard extends Component {
  constructor(props) {
      super(props);
      this.state = {
        error: null,
        loading: false,
        items: [],
        currentAlg: "",
        disabled: true,
        pastFiles: [],
        stratResults: [],
        benchmarkResults: [],
        annualReturnsPng: "",
        assetAllPng: "",
        cumuReturnsPng: "", 
        drawDownPng: "",
        monthlyReturnsPng: "",
        rptPng: "",
        currentEdit: "",
        algorithms: ['Algorithms Loading'],
        total_trades: "",
        win_rate: "",
        loss_rate: "",
        average_win: "",
        average_loss: "",
        profit: "",
        compounding_annual_return: "",
        drawdown: "",
      };    
    }
  componentDidMount() {
    this.getPastRuns();
    this.getAlgorithms();
    document.getElementsByClassName('tab-list')[1].style.opacity = '0.4';
    document.getElementsByClassName('tab-list')[1].style.pointerEvents = 'none';
  }
  getPastRuns() {
    const accessToken = localStorage.getItem("token");
    const headers = {'Authorization': `Bearer ${accessToken}`};
    axios.get("https://rats-osu2021.herokuapp.com//api/quant_connect/algorithm_manager/get_past_runs/", { 'headers': headers })
    .then((response) => {
      let tempFiles = response.data.past_runs.map(data => {
        return {'filename': data}
      });
      this.setState({pastFiles: tempFiles});
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  getAlgorithms() {
    const accessToken = localStorage.getItem("token");
    const headers = {'Authorization': `Bearer ${accessToken}`};
    axios.get("https://rats-osu2021.herokuapp.com//api/quant_connect/algorithm_manager/get_algorithms/", { 'headers': headers })
    .then((response) => {
        console.log(response.data.algorithms);
        this.setState({algorithms: response.data.algorithms})
    //   this.setState({algorithms: response.data.algorithms});
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  getData(option) {
    document.getElementsByClassName('hiding-div')[0].style.display = 'block';
    document.getElementsByClassName('tab-list')[1].style.opacity = '0.4';
    document.getElementsByClassName('tab-list')[1].style.pointerEvents = 'none';
    this.setState(prevState => ({
      loading: !prevState.loading
    }));
    const body = {
      "file_name": option,
    };
    const accessToken = localStorage.getItem("token");
    fetch("https://rats-osu2021.herokuapp.com//api/quant_connect/algorithm_manager/get_past_data/", { 
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      }, 
      method: 'POST', 
      body: JSON.stringify(body) 
      })
      .then(response => response.json())
      .then((data) => {
        document.getElementsByClassName('tab-list')[1].style.opacity = '1.0';
        document.getElementsByClassName('tab-list')[1].style.pointerEvents = 'all';
        document.getElementsByClassName('hiding-div')[0].style.display = 'none';
        const static_dir = '/static/' + data.orig_filepath;
        this.setState({total_trades: data.total_trades});
        this.setState({win_rate: data.win_rate});
        this.setState({loss_rate: data.loss_rate});
        this.setState({average_win: data.average_win});
        this.setState({average_loss: data.average_loss});
        this.setState({profit: data.profit});
        this.setState({compounding_annual_return: data.compounding_annual_return});
        this.setState({drawdown: data.drawdown});
        this.setState({drawDownPng: static_dir + '/drawdowns.png'});
        this.setState({annualReturnsPng: static_dir + '/annual-returns.png'});
        this.setState({assetAllPng: static_dir + '/asset-allocation-backtest.png'});
        this.setState({cumuReturnsPng: static_dir + '/cumulative-return.png'});
        this.setState({monthlyReturnsPng: static_dir + '/monthly-returns.png'});
        this.setState({rptPng: static_dir + '/returns-per-trade.png'});
        const stratResults = [];
        stratResults.push(data.strat_chart);
        this.setState({stratResults: stratResults});
        const benchmarkResults = [];
        benchmarkResults.push(data.benchmark_chart);
        this.setState({benchmarkResults: benchmarkResults});
        this.setState(prevState => ({
          loading: !prevState.loading
        }));
      });
  }
  submitAlgorithm() {
    document.getElementsByClassName('hiding-div')[0].style.display = 'block';
    document.getElementsByClassName('tab-list')[1].style.opacity = '0.4';
    document.getElementsByClassName('tab-list')[1].style.pointerEvents = 'none';
    this.setState(prevState => ({
      loading: !prevState.loading
    }));
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
      "startdate": startdate,
      "enddate": enddate,
    };
    const accessToken = localStorage.getItem("token");
    fetch("https://rats-osu2021.herokuapp.com//api/quant_connect/algorithm_manager/set_algorithm/", { 
      headers: {
        'Access-Control-Allow-Origin':'*',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      }, 
      method: 'POST', 
      body: JSON.stringify(body) 
      })
      .then(response => response.json())
      .then((data) => {
        this.setState(prevState => ({
          loading: !prevState.loading
        }));        
        this.getPastRuns();
        this.getData(data.backtest_id);
      });
  }
  hideNameChangePopup() {
    document.getElementById('change-name-popup').style.display = 'none';
    document.getElementById('change-name-popup').style.display = 'not-allowed';
  }
  editFileName(filename) {
    document.getElementById('change-name-popup').style.display = 'block';
    this.setState({currentEdit: filename});
  }
  renameFile() {
    const newName = document.getElementById("name-change-input").value;
    const body = {
      new_name: newName,
      filename: this.state.currentEdit
    }
    const accessToken = localStorage.getItem("token");
    fetch("https://rats-osu2021.herokuapp.com//api/quant_connect/file_manager/edit_filename/", { 
    headers: {
      'Access-Control-Allow-Origin':'*',
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    method: 'POST',
    body: JSON.stringify(body) 
    })
    .then((response) => {
      this.setState({currentEdit: ""});
      document.getElementById('change-name-popup').style.display = 'none';
      this.getPastRuns();
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  deleteBackTest(filename) {
    const accessToken = localStorage.getItem("token");
    fetch("https://rats-osu2021.herokuapp.com//api/quant_connect/file_manager/delete_file/", { 
    headers: {
      'Access-Control-Allow-Origin':'*',
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    method: 'POST',
    body: JSON.stringify({filename: filename}),
    })
    .then((response) => {
      this.getPastRuns();
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  render() {
    return (
    <div className="lp">
    <div className="App">
        </div>
        <div className="algorithm-start-content">
          <Tabs>
            <div label="Run Algorithm" className="run-algs-content">
              <form id="run-algos-form" ref={el => (this.form = el)}>
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
              <div label="Upload an Algorithm" className="upload-algorithm">
                <AlgorithmUpload />
              </div>
            </div>
            <div label="Past Runs" className="past-run-content">
            <div className="past-run-content">
              <div id="change-name-popup">
                <br></br>
                <span> New Backtest Name: </span>
                <div onClick={() => this.hideNameChangePopup()} className="close"></div>
                <input id="name-change-input"></input>
                <button onClick={() => this.renameFile()}>Change Name</button>
              </div>
            <ReactTable
              data={this.state.pastFiles}
              columns={[
                {
                  Header: "Previously Ran Backtests",
                  columns: [
                    {
                      Header: "File Name",
                      id: "filename",
                      accessor: "filename",
                    },
                    {
                      Header: "Show Backtest Data",
                      Cell: row => (<div onClick={() => this.getData(row['row']['filename'])}><i className="fa fa-signal"></i></div>)
                    },
                    {
                      Header: "Delete Backtest",
                      Cell: row => (<div onClick={() => this.deleteBackTest(row['row']['filename'])}><i className="fa fa-trash"></i></div>)
                    },
                    {
                      Header: "Rename Backtest",
                      Cell: row => (<div onClick={() => this.editFileName(row['row']['filename'])}><i className="fa fa-edit"></i></div>)
                    },
                  ]
                },
              ]}
              defaultPageSize={5}
              className="-striped -highlight"
            />
            <br />

          </div>
            </div>
          </Tabs>
          </div>
          <div className="algorithm-results-content">
          <Tabs>
            <div label="Summary" className="results-text">
              <div className="table-title" id="key-stats-header">
                <h3>Key Statistics</h3>
              </div>
              <table style={{ width: 90 + '%' }} id="key-stats-table">
                <thead>
                  <tr>
                      <th>Statistic</th>
                      <th>Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                      <td> Win Rate:</td>
                      <td>{this.state.win_rate}</td>
                  </tr>
                  <tr>
                      <td> Profit: </td>
                      <td>{this.state.profit}</td>
                  </tr>
                  <tr>
                      <td> Loss Rate: </td>
                      <td>{this.state.loss_rate}</td>
                  </tr>
                  <tr>
                      <td> Total Trades: </td>
                      <td>{this.state.total_trades}</td>
                  </tr>
                  <tr>
                      <td> Average Win: </td>
                      <td>{this.state.average_win}</td>
                  </tr>
                  <tr>
                      <td>Compounding Annual Return: </td>
                      <td>{this.state.compounding_annual_return}</td>
                  </tr>
                  <tr>
                      <td> Average Loss: </td>
                      <td>{this.state.average_loss}</td>
                  </tr>
                  <tr>
                      <td> Drawdown: </td>
                      <td>{this.state.drawdown}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div label="Report" className="img-div">
              <div >
                <span className="imageCaption">Drawdown</span>
                <img src={this.state.drawDownPng} 
              style={{width: 90 + '%'}}
              /></div>
              <div>
                <span className="imageCaption">Cumulative Returns</span>
                <img src={this.state.cumuReturnsPng}
              style={{width: 90 + '%'}}
              /></div>
              <div className="doubleImages"> 
                <div className="imageCaption2">
                  Monthly Returns
                </div>
                <div className="imageCaption3">
                  Annual Returns
                </div>
                <img src={this.state.monthlyReturnsPng}  
                style={{display: "inline-block"}}></img>
                <img src={this.state.annualReturnsPng}
                style={{display: "inline-block"}}></img>
              </div>
              <div className="doubleImages"> 
              <div className="imageCaption2">
                  Returns per Trade
                </div>
                <div className="imageCaption3">
                  Asset Allocation
                </div>
                <img src={this.state.rptPng}  
                style={{display: "inline-block"}}></img>
                <img src={this.state.assetAllPng}
                style={{display: "inline-block"}}></img>
              </div>
              </div>
            <div label="Interactive Charts">            
              <div className="interactive-plots" id="inter_plots">
                <div id="strat-chart">
                <Plot
                    data={this.state.stratResults}
                    layout={
                    {
                    title: 'Strategy',
                    xaxis: {
                      title: '',
                      showgrid: false,
                      zeroline: false
                    },
                    yaxis: {
                      title: '',
                      showline: false
                    } 
                  }
                }
                  />
                </div>
                <div id="benchmark-chart"></div>
                <Plot
                    data={this.state.benchmarkResults}
                    layout={ 
                      {
                        title: 'Benchmark',
                        xaxis: {
                          title: '',
                          showgrid: false,
                          zeroline: false
                        },
                        yaxis: {
                          title: '',
                          showline: false
                        } 
                      }
                     }
                  />
              </div>
            </div>
          </Tabs>
          <div className="hiding-div">
          <div className="spinner" style={{display: this.state.loading ? 'block' : 'none' }}></div>
          </div>
      </div>
      </div>
    );
  }
}

export default Dashboard;
