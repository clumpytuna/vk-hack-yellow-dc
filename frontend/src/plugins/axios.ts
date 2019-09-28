import axios from 'axios';

axios.defaults.baseURL = 'http://demo134.bravo.vkhackathon.com';
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

export async function postForm(url, data) {
  const formData = new FormData();
  for (const [key, value] of Object.entries(data)) {
    formData.append(key, value);
  }
  return await axios.post(url, formData);
}
