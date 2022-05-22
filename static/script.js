function ShowCam() {
  Webcam.set({
    width: 320,
    height: 240,
    image_format: "jpeg",
    jpeg_quality: 100,
  });
  Webcam.attach("#my_camera");
}
window.onload = ShowCam;

function snap() {
  Webcam.snap(function (data_uri) {
    // display results in page
    document.getElementById("results").innerHTML =
      '<img id="image" src="' + data_uri + '"/>';
  });
}

async function upload() {
  console.log("Uploading...");
  var image = document.getElementById("image").src;
  var form = document.getElementById("myForm");
  var formData = new FormData(form);
  formData.append("file", image);
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/signup");
  xmlhttp.send(formData);
  xmlhttp.onload = () => {
    data = JSON.parse(xmlhttp.responseText);
    window.location.href = `http://127.0.0.1:5000/success/${data.name}`;
  };
}
