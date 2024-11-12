Dropzone.autoDiscover = false;

function init() {
  let dz = new Dropzone("#dropzone", {
    url: "/",
    maxFiles: 1,
    addRemoveLinks: true,
    dictDefaultMessage: "celebrity",
    autoProcessQueue: false,
  });

  dz.on("addedfile", function () {
    if (dz.files[1] != null) {
      dz.removeFile(dz.files[0]);
    }
  });

  dz.on("complete", function (file) {
    let imageData = file.dataURL;

    var url = "http://127.0.0.1:5000/classify_image";

    $.post(
      url,
      {
        image_data: file.dataURL,
      },
      function (data, status) {
        console.log(data);
        $("#resultHolder").html("");
        $("#resultHolder").append("<h4>Please wait...</h4>");
        // alert(data);
        if (!data || data.length == 0) {
          $("#resultHolder").hide();
          $("#divClassTable").hide();
          $("#error").show();
          return;
        }
        $("#resultHolder").show();
        htm = "";
        for (let i = 0; i < data.length; ++i) {
          // alert(
          //   data[i].cid +
          //     " " +
          //     data[i].celeb +
          //     " " +
          //     data[i].score +
          //     " " +
          //     data[i].proba
          // );
          // $("#resultHolder").append($("#c" + data[i].cid));

          $("#error").hide();
          htm +=
            "<div ><img src='faces/" +
            data[i].celeb +
            ".png' style='border-radius:80px;width:80px;padding:5px'><b>" +
            data[i].celeb +
            "</b><span style='color:green'><i> " +
            data[i].score +
            "% match</i></span></div>";
        }
        $("#resultHolder").html("");
        $("#resultHolder").append(htm);
        /*if (match) {
          $("#error").hide();
          $("#resultHolder").show();
          $("#divClassTable").show();
          $("#resultHolder").html($(`[data-player="${match.class}"`).html());
          let classDictionary = match.class_dictionary;
          for (let personName in classDictionary) {
            let index = classDictionary[personName];
            let proabilityScore = match.class_probability[index];
            let elementName = "#score_" + personName;
            $(elementName).html(proabilityScore);
          }
        }*/

        // dz.removeFile(file);
      }
    );
  });

  $("#submitBtn").on("click", function (e) {
    $("#resultHolder").show();

    $("#resultHolder").html("<h4>Please wait...</h4>");
    dz.processQueue();
  });
}

$(document).ready(function () {
  console.log("ready!");
  $("#error").hide();
  $("#resultHolder").hide();
  $("#divClassTable").hide();

  init();

  console.log("document loaded");
   var url = "http://127.0.0.1:5000/get_celeb_names"; // Use this if you are NOT using nginx which is first 7 tutorials
  //var url = "/api/get_celeb_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  $.get(url, function (data, status) {
    console.log("got response for get_celeb_names request");
    if (data) {
      var celebs = data.location;
      // alert(celebs);
      var uiLocations = document.getElementById("uiCelebList");

      // $("#uiCelebs").empty();
      html = "";
      for (var i in celebs) {
        // var opt = new Option(celebs[i]);
        // $("#uiLocations").append(opt);
        html +=
          "<div class='col-2 celeb' id=c" +
          i +
          "><img src='faces/" +
          celebs[i] +
          ".png' class='celeb_img'" +
          "/>" +
          celebs[i] +
          "</div>";
      }
      $("#uiCelebList").html(html);
    }
  });
});
