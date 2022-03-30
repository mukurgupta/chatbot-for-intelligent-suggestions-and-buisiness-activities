import React from 'react';
import Chat from './Components/Chat';
import Sidebar from './Components/Sidebar';
import { Container, Row, Card, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default class App extends React.Component {
	state = {
		loginPage: false,
		name: 'Eva',
		subtitle: 'Ever eVolving Autonomous Bot',
		url: 'http://127.0.0.1:8000'
	}

	setBot = (name) => {
		if (name === 'Business') {
			this.setState({
				loginPage: true,
				name: "BusinessBot",
				subtitle: "Building the future",
				url: "http://127.0.0.1:8000"
			});
		} else {
			this.setState({loginPage: true});
		}
	}

	render() {
	  return (
	    <Container fluid>
	    	{
	    		(this.state.loginPage) ?
			    		<Row>
					    	<Sidebar name={this.state.name} subtitle={this.state.subtitle}/>
					      	<Chat name={this.state.name} url={this.state.url} />
				      	</Row>
			      : <Row>
			      		<Card className="text-center my-auto mx-5" style={{ left: '24em', top: '13em', width: '18rem' }}>
			      			<Card.Body>
								    <Card.Title>Eva</Card.Title>
								    <Card.Text>
								      Ever eVolving Autonomous Bot
								    </Card.Text>
								    <Button onClick={() => this.setBot('Eva')}>Enter</Button>
								  </Card.Body>
			      		</Card>
			      		<Card className="text-center my-auto mx-5" style={{ left: '24em', top: '13em', width: '18rem' }}>
			      			<Card.Body>
								    <Card.Title>BusinessBot</Card.Title>
								    <Card.Text>
								      Building the future
								    </Card.Text>
								    <Button onClick={() => this.setBot('Business')}>Enter</Button>
								  </Card.Body>
			      		</Card>
				      </Row>
			    }
	    </Container>
	  );
	}
}