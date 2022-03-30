import requests
import pandas as pd
import json
import os 

class expense_management:
    def __init__(self, token, orgId):
        self.url = 'https://books.zoho.in/api/v3'
        self.orgid = orgId
        self.token = token
        self.headers = {'Authorization':'Zoho-oauthtoken '+self.token}
    
    def create_expense(self,account_id,date,amount):
        data = {'account_id':account_id,'date': date,'amount':amount}
        response = requests.post(self.url+'/expenses?organization_id='+self.orgid,json=data,headers=self.headers)
        output = {'msg':json.loads(response.text)['message'],'data':None}
        return output
    
    def update_expense(self,expense_id,account_id,date,amount):
        data = {'account_id':account_id,'date': date,'amount':amount}
        response = requests.put(self.url+'/expenses/'+str(expense_id)+'?organization_id='+self.orgid,json=data,headers=self.headers)
        output = {'msg':json.loads(response.text)['message'],'data':None}
        return output
        
    def get_expense(self,expense_id):
        response = requests.get(self.url+'/expenses/'+str(expense_id)+'?organization_id='+self.orgid,headers=self.headers)
        expense_json = json.loads(response.text)['expense'] 
        data = pd.DataFrame([[expense_json['account_name'],str(expense_json['total']),expense_json['date']]],columns=['Expense Type','Amount','Date of Expense'])
        output = {'msg':None,'data':data}
        return output
    
    def list_expenses(self):
        response = requests.get(self.url+'/expenses/?organization_id='+self.orgid,headers=self.headers)
        expense_list = []
        for instance in json.loads(response.text)['expenses']:
            expense_list.append([str(instance['expense_id']), str(instance['customer_id']), instance['account_name'],str(instance['total']),instance['date']])
        data = pd.DataFrame(expense_list,columns=['Id', 'Customer Id', 'Expense Type','Amount','Date of Expense'])
        output = {'msg':None,'data':data}
        return output
    
    def list_accounts(self):
        data = {'filter_by': 'AccountType.Expense'}
        response = requests.get(self.url+'/chartofaccounts/?organization_id='+self.orgid, json=data, headers=self.headers)
        account_list = []
        for instance in json.loads(response.text)['chartofaccounts']:
            account_list.append([instance['account_id'],str(instance['account_name']), instance['account_type']])
        data = pd.DataFrame(account_list,columns=['account_id','account_name', 'Account Type'])
        output = {'msg':None,'data':data}
        return output
    
    def delete_expense(self,expense_id):
        response = requests.delete(self.url+'/expenses/'+str(expense_id)+'?organization_id='+self.orgid,headers=self.headers)
        msg = 'Expense Deleted' if response.status_code == 200 else 'Some error while processing.'
        output = {'msg': msg,'data':None}
        return output
    
    def list_expense_history(self,expense_id):
        response = requests.get(self.url+'/expenses/'+str(expense_id)+'/comments?organization_id='+self.orgid,headers=self.headers)
        comments = [] 
        for comment in json.loads(response.text)['comments']:
            comments.append([comment['comment_id'],comment['description'],comment['date_description']])
        data = pd.DataFrame(comments,columns=['Comment_Id','Description','Date'])
        output = {'msg':None ,'data':data}
        return output
    
    #Helper Function
    def get_account_id(self,account_name):
        data = {'filter_by': 'AccountType.Expense'}
        response = requests.get(self.url+'/chartofaccounts/?organization_id='+self.orgid, json=data, headers=self.headers)
        account_list = {}
        for instance in json.loads(response.text)['chartofaccounts']:
            account_list[instance['account_name'].lower()] = instance['account_id']
        return account_list[account_name.lower()]
