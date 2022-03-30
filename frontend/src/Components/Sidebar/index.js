import React from "react";
import { Nav, Col } from "react-bootstrap";
import '../../styles/sidebar.css'
import logo from '../../maverick_logo.png'

export default class Sidebar extends React.Component {
  render() {
    return (
      <Col xs ={2} id="sidebar-wrapper">
        <Nav className="col-md-12 d-none d-md-block bg-light sidebar">
          <div className="sidebar-sticky"></div>
          <Nav.Item className="nav-name">
            <b><h3>{this.props.name}</h3></b>
            <span style={{color: 'grey'}}>{this.props.subtitle}</span>
          </Nav.Item>
          <Nav.Item className="nav-footer">
            <img src={logo} alt="Maverick"/><br/>
            IIT Kharagpur<br />
            Team:<b> MonsterTrio</b>
          </Nav.Item>
        </Nav>
      </Col>
    );
  }
};