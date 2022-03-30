import React from 'react'
import Messages from './Messages'
import ChatInput from './ChatInput'
import { Col } from 'react-bootstrap'
import '../../styles/chat.css'

export default class Sidebar extends React.Component {
	render() {
		return (
			<Col xs={10} className="content-box">
				<div className="chat-to">
					<span style={{color: 'grey'}}>To: </span>
					<b>{this.props.name}</b>
				</div>
				<div className="chat-container">
					<Messages />
					<ChatInput name={this.props.name} url={this.props.url}/>
				</div>
			</Col>
		);
	}
}