const API_URL = 'http://127.0.0.1:8000/search?query=';

export default {
  search(searchTerm) {
    const url = `${API_URL}${searchTerm}`;
    return fetch(url)
      .then(response => response.json())
      .then(result => {
        const data = result.results.map(item => ({
          url: item.filenames,
          caption: item.captions
        }));
        return data;
      });
  },
};