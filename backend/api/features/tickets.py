import requests
import pandas as pd
import json

class ticket_func:
	def __init__(self, token, orgId):
		self.baseurl = "https://desk.zoho.in/api/v1"
		self.orgid = orgId
		self.token = token
		
		self.headers = {'orgId': self.orgid, 'Authorization': 'Zoho-oauthtoken '+self.token}

	def create_ticket(self, customerId, title):
		title = title.replace('"', '')
		response = requests.get(self.baseurl + '/departments', headers=self.headers)
		deptId = pd.DataFrame(json.loads(response.text)['data'])['id'][0]
		data = {'subject': title, 'departmentId': deptId, 'contactId': customerId}
		response = requests.post(self.baseurl+'/tickets', json = data, headers = self.headers)
		msg = 'Ticket created successfully' if response.status_code == 200 else 'Some error while processing.'
		output = {'msg': msg, 'data': None}
		return output
	
	def show_tickets(self):
		response = requests.get(self.baseurl+'/tickets', headers = self.headers)
		return {'msg': None, 'data': pd.DataFrame(json.loads(response.text)['data'])[['id', 'ticketNumber', 'subject', 'status', 'createdTime']]}

	def close_ticket(self, ticketId):
		data = {'ids': [ticketId]}
		response = requests.post(self.baseurl+'/closeTickets', json=data, headers=self.headers)
		msg = 'Ticket Closed' if response.status_code == 200 else 'Some error while processing.'
		return {'msg': msg, 'data': None}

	def show_customers(self):
		response = requests.get(self.baseurl + '/contacts', headers=self.headers)
		return {'msg': None, 'data': pd.DataFrame(json.loads(response.text)['data'])[['id', 'firstName', 'lastName', 'email', 'type']]}

	def show_departments(self):
		response = requests.get(self.baseurl + '/departments', headers=self.headers)
		return {'msg': None, 'data': pd.DataFrame(json.loads(response.text)['data'])[['id', 'name', 'description']]}