import axios from 'axios'

export const HTTP = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

export const sendMessages = (url, data) => 
  HTTP.post('api/sendMessage', JSON.stringify(data), {
      headers: {
        "Content-Type": "application/json"
      }
    }).then(res => {
      return res.data
    }).catch(err => {
      console.log(err);
      return null;
    });