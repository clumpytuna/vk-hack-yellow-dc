import axios from 'axios';

export const baseURL = '/api';
axios.defaults.baseURL = baseURL;
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';

export async function postForm(url, data: string) {
  const formData = new FormData();
  for (const [key, value] of Object.entries(data)) {
    formData.append(key, value);
  }
  return await axios.post(url, formData);
}
