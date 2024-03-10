const API_URL = 'http://146.148.26.219:8000/search?query=';
//const API_URL = 'http://0.0.0.1:8000/search?query=';
const BASE_URL = "https://upload.wikimedia.org/wikipedia/commons/";

export default {
  search(searchTerm) {
    const url = `${API_URL}${searchTerm}`;
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
};