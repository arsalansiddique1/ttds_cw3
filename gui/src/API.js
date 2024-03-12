const API_URL = 'http://146.148.26.219:8000/';
// const API_URL = 'http://127.0.0.1:8000/';
const BASE_URL = "https://upload.wikimedia.org/wikipedia/commons/";

export default {
  search(searchTerm) {
    const url = `${API_URL}search?query=${searchTerm}`;
    console.log(url)
    return fetch(url)
      .then(response => response.json())
      .then(result => {
        if (result && result.results) { // Check if result is not null and has results property
          const data = result.results.map(item => ({
            id: item.id,
            url: BASE_URL + item.filename,
            title: item.title,
            caption: item.caption
          }));
          console.log(result);
          console.log(data);
          return data;
        } else {
          console.log("No data found"); // Handle case when no data is found
          return [];
        }
      })
      .catch(error => {
        console.error('Error:', error); // Log any errors that occur during the fetch
        return []; // Return an empty array in case of error
      });
  },
  boolean_search(searchTerm) {
    const url = `${API_URL}boolean_search?query=${searchTerm}`;
    return fetch(url)
      .then(response => response.json())
      .then(result => {
        if (result && result.results) { // Check if result is not null and has results property
          const data = result.results.map(item => ({
            id: item.id,
            url: BASE_URL + item.filename,
            title: item.title,
            caption: item.caption
          }));
          console.log(result);
          console.log(data);
          return data;
        } else {
          console.log("No data found"); // Handle case when no data is found
          return [];
        }
      })
      .catch(error => {
        console.error('Error:', error); // Log any errors that occur during the fetch
        return []; // Return an empty array in case of error
      });
  }
};
