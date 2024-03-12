const API_URL = 'http://146.148.26.219:8000/search?query=';
//const API_URL = 'http://127.0.0.1:8000/';
const BASE_URL = "https://upload.wikimedia.org/wikipedia/commons/";

export default {
  search(searchTerm) {
    const url = `${API_URL}search?query=${searchTerm}`;
    return fetch(url)
      .then(response => response.json())
      .then(result => {
        const data = result.results.map(item => ({
          id: item.id,
          url: BASE_URL + item.filename,
          title: item.title,
          caption: item.caption
        }));
        console.log(result)
        console.log(data)
        return data;
      });
  },
  boolean_search(searchTerm) {
    // Implement your boolean search logic here
    // For example:
    const url = `${API_URL}boolean_search?query=${searchTerm}`;
    return fetch(url)
      .then(response => response.json())
      .then(result => {
        const data = result.results.map(item => ({
          id: item.id,
          url: BASE_URL + item.filename,
          title: item.title,
          caption: item.caption
        }));
        console.log(result)
        console.log(data)
        return data;
      });
  }
};