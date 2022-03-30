import React, { Component, Fragment } from 'react'
import { connect } from 'react-redux'
import TableModal from './Modal'

class Messages extends Component {

	componentDidMount() {
		const div = document.getElementById('messageList');
		div.scrollTop = div.scrollHeight;
	}

	componentDidUpdate() {
		const div = document.getElementById('messageList');
		div.scrollTop = div.scrollHeight;
	}

	render() {
		var dt = new Date();
		var h = dt.getHours(), m = dt.getMinutes();
		m = (m < 10) ? ('0'+m) : m;
		var time = (h > 12) ? (h-12 + ':' + m +' pm') : (h + ':' + m +' am');
		return (
			<Fragment>
				<div className="msg-date">
					<hr className="date-line"/>
					<span className="date">Today, {time}</span>
					<hr className="date-line"/>
				</div>
				<div id="messageList" className="messages">
					{this.props.messages.map((msg, i) => {
						const place = msg.to ? 'right' : 'left';
						let headers=[], n;
						if (msg.message) {
							headers = Object.keys(msg.message);
							n = msg.message[headers[0]].length;
						}
						return (msg.pop) ?
							<div key={i} className={`message ${place}`}>
								<TableModal headers={headers} n={n} data={[msg.message]}/>
							</div>
						: <div key={i} className={`message ${place}`}>
								<div className="msg-body">
									{msg.message}
								</div>
							</div>
					})}
				</div>
			</Fragment>
		)
	}
}

const mapStateToProps = (state) => {
    return {
        messages: state.messages
    }
}

export default connect(mapStateToProps)(Messages)