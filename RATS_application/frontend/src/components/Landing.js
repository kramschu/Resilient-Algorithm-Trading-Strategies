import React from "react";
import '../styles/landingStyle.css';

const Landing = () => (
    <div className="lp">
    <section className="content__top">
        <div className="content__top__item "></div>
        <div className="content__top__item "></div>
        <div className="content__top__item "></div>
        <div className="content__top__item "></div>
        <div className="content__top__item "></div>
    </section>
    <div className="content">
      <section className="main__text">
        <h1>RATS</h1>
        <h2>
            <div className="header_text">
                <span> Resilient</span>
                <span> Algorithmic</span>
                <span> Trading</span>
                <span> Strategies</span>
            </div>
        </h2>
      </section>
      <section className="shape__holder">
        <div className="shape__circle">
          <div className="circle">
            <div className="circle-half">
            </div>
            <div className="circle-half">
            </div>
          </div>
        </div>
        <div className="squiggle__cont">
          <div className="shape__squiggle">
            <div className="squiggle"></div>
            <div className="squiggle squiggle2">
            </div>
          </div>
          <div className="shape__squiggle">
            <div className="squiggle"></div>
            <div className="squiggle squiggle2">
            </div>
          </div>
          <div className="shape__squiggle">
            <div className="squiggle"></div>
            <div className="squiggle squiggle2">
            </div>
          </div>
          <div className="shape__squiggle">
            <div className="squiggle"></div>
            <div className="squiggle squiggle2">
            </div>
          </div>
        </div>
      </section>
    </div>
    <section className="content__bottom">
      <div className="content__btm__item "></div>
      <div className="content__btm__item "></div>
      <div className="content__btm__item "></div>
      <div className="content__btm__item "></div>
      <div className="content__btm__item "></div>
    </section>
  </div>
);

export default Landing;
