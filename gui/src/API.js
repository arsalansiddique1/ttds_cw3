const API_URL = 'http://146.148.26.219:8000/';
//const API_URL = 'http://127.0.0.1:8000/';

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
            url: item.filename,
            filename: item.filename,
            title: item.title,
            caption: item.caption,
            date: item.date,
            license: item.license,
            size: item.size,
            width: item.width,
            height: item.height
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
            url: item.filename,
            filename: item.filename,
            title: item.title,
            caption: item.caption,
            date: item.date,
            license: item.license,
            size: item.size,
            width: item.width,
            height: item.height
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
