function getArrival() {
  console.log("getArrival");
  $.ajax({
    //The URL to process the request
      url : "http://127.0.0.1:8080/arrival?",
    //The type of request, also known as the "method" in HTML forms
    //Can be 'GET' or 'POST'
      type : 'GET',
      dataType: 'text',
    //Any post-data/get-data parameters
    //This is optional
      data : {
        'starTime' : document.getElementById("starTimeArrive").value,
        'endTime' : document.getElementById("endTimeArrive").value
      },
    //The response from the server
      success : function(data) {
      //You can use any jQuery/JavaScript here!!!
        if (data == "success") {
          console.log('request sent!');
        }
      },
      statusCode: {
          404: function (response) {
              alert(404);
          },
          405: function (response) {
              alert(405);
          },
          200: function (response) {
              //alert(response);
              arr = new Array();
              arr = response.split("\n");
              for (index = 0; index < arr.length; ++index) {
                document.getElementById("arriveContent").innerHTML += "<p>" + arr[index] + "</p>";
              }
              document.getElementById("downloadArrive").style.display = "block";
          }
      }
    });
}

function getDeparture() {
  console.log("getDeparture");
    $.ajax({
      //The URL to process the request
        url : "http://127.0.0.1:8080/departure?",
      //The type of request, also known as the "method" in HTML forms
      //Can be 'GET' or 'POST'
        type : 'GET',
        dataType: 'text',
      //Any post-data/get-data parameters
      //This is optional
        data : {
          'starTime' : document.getElementById("starTimeDeparture").value,
          'endTime' : document.getElementById("endTimeDeparture").value
        },
      //The response from the server
        success : function(data) {
        //You can use any jQuery/JavaScript here!!!
          if (data == "success") {
            console.log('request sent!');
          }
        },
        statusCode: {
            404: function (response) {
                alert(404);
            },
            405: function (response) {
                alert(405);
            },
            200: function (response) {
                //alert(response);
                arr = new Array();
                arr = response.split("\n");
                for (index = 0; index < arr.length; ++index) {
                  document.getElementById("departureContent").innerHTML += "<p>" + arr[index] + "</p>";
                }
                document.getElementById("downloadDeparture").style.display = "block";
            }
        }
      });
  }
