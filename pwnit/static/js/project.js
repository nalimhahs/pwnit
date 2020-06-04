/* Project specific Javascript goes here. */


function addToLibrary(data) {
    // const axios = require("axios").default;

  if (confirm("Are you sure?")) {
        data.csrfmiddlewaretoken = '{{ csrf_token }}'
        console.log(data)
        let request = new XMLHttpRequest();
        request.open("POST", '/movies/api/add', true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send(data)
    // fetch('/movies/api/add', {
    //     method: 'POST',
    //     body: JSON.stringify(data)
    // })
    // axios
    //   .post("/movies/api/add", {
    //     firstName: "Fred",
    //     lastName: "Flintstone",
    //   })
    //   .then(function (response) {
    //     console.log(response);
    //   })
    //   .catch(function (error) {
    //     console.log(error);
    //   });
  }
}
