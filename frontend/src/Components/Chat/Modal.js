import React, { Component, Fragment } from 'react';
import { Modal, Table, Button } from 'react-bootstrap'

export default class TableModal extends Component {

	state = {
		showTable: false
	}

	toggleTable = (i) => {
		this.setState({showTable: !this.state.showTable});
	}

	render() {
		const data = this.props.data[0];
		return (
			<Fragment>
				<div className="msg-body modal-link" onClick={this.toggleTable}>
					<u>Click Here</u>
				</div>
				<Modal size="lg" show={this.state.showTable} onHide={this.toggleTable}>
	        <Modal.Body>
	        	<Table bordered hover>
	        		<thead>
		        		<tr>
			        		{
			        			this.props.headers.map((name) => {
			        				return (
			        					<th key={name}>{(name === 'url') ? 'Article' : name}</th>
		        					);
			        			})
			        		}
		        		</tr>
	        		</thead>
	        		<tbody>
	        			{
	        				[...Array(this.props.n)].map((e, i) => {
	        					return (
	        						<tr key={i}>
	        							{
	        								this.props.headers.map((name) => {
	        									if (name === 'url') {
	        										return (
        												<td key={name + i}>
        													<a href={data[name][i]} target="_blank">
		        												<Button variant="info">View</Button>
	        												</a>
        												</td>
        											);
	        									}
	        									else {
	        										return (
		        										<td key={name + i}>
		        											{data[name][i]}
		        										</td>
		      										);
	        									}
	        								})
	        							}
	        						</tr>
	      						);
	        				})
	        			}
	        		</tbody>
	        	</Table>
	        </Modal.Body>
				</Modal>
			</Fragment>
		);
	}
}