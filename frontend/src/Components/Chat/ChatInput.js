import React from 'react'
import { bindActionCreators } from "redux";
import { connect } from 'react-redux'
import { sendMessages } from '../../config/apiConfig'
import { sendNewMsg } from '../../Actions'

class ChatInput extends React.Component {
	state = {
		msg: '',
	};

	componentDidMount() {
		const initMsg = "Hi there! I am " + this.props.name + ". What can i do for you?";
		this.props.sendNewMsg({message: initMsg, to: 0, pop: 0});
	}

	handleChange = (e) => {
		this.setState({ msg: e.target.value });
	}

	process_reply = (reply) => {
		if (reply.msg != null) {
			if (reply.data != null) {
				this.props.sendNewMsg({message: reply.msg, to: 0, pop: 0});
				this.props.sendNewMsg({message: reply.data, to: 0, pop: 1});
				if (reply.msg2) setTimeout(() => {this.props.sendNewMsg({message: reply.msg2, to: 0, pop: 0});}, 1000);
			}
			else {
				this.props.sendNewMsg({message: reply.msg, to: 0, pop: 0});
			}
		} else {
			if ("msg2" in reply) this.props.sendNewMsg({message: reply.msg2, to: 0, pop: 0});
			setTimeout(() => {this.props.sendNewMsg({message: reply.data, to: 0, pop: 1});}, 500);
		}
	}

	handleSubmit = async (e) => {
		e.preventDefault()
		if (!this.state.msg)
			return;
		this.props.sendNewMsg({message: this.state.msg, to: 1, pop: 0});
		this.setState({ msg: ''});
		const reply = await sendMessages(this.props.url, {id: 1, message: this.state.msg, to: 1});
		console.log(reply);
		this.process_reply(reply);
		if ("category" in reply) {
			const reply2 = await sendMessages(this.props.url, {id: 1, message: reply.category+'_schedule', to: 1});
			console.log(reply2);
			this.process_reply(reply2);
		}
	}

	render() {
		return (
			<form onSubmit={this.handleSubmit} className="chat-input">
				<input type="text"
					onChange={this.handleChange}
					value={this.state.msg}
					placeholder="Write a message..."
					required />
				<input type="submit"
					value="Send" />
			</form>
		)
	}
}

const mapStateToProps = (state) => {
    return {
    }
}

function matchDispatchToProps(dispatch) {
    return bindActionCreators({
    	sendNewMsg: sendNewMsg
    }, dispatch)
}

export default connect(mapStateToProps,matchDispatchToProps)(ChatInput)