URL = window.URL || window.webkitURL;

var gumStream; 						
var rec; 		
var input; 	

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext 

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    var constraints = { audio: true, video:false }

	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

		audioContext = new AudioContext();

		gumStream = stream;
		
		input = audioContext.createMediaStreamSource(stream);

		rec = new Recorder(input,{numChannels:1})

		rec.record()

	}).catch(function(err) {
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	pauseButton.disabled = true
	});
}

function pauseRecording(){
	if (rec.recording){
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	stopButton.disabled = true;
	recordButton.disabled = false;
	pauseButton.disabled = true;

	pauseButton.innerHTML="Pause";
	
	rec.stop();

	gumStream.getAudioTracks()[0].stop();

	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	var bar = document.createElement('p')

	var filename = new Date().toISOString();

	au.controls = true;
	au.src = url;

	link.href = url;
	link.download = filename+".wav";
	link.innerHTML = "Save";

	li.appendChild(au);
	
	//add the filename to the li
	// li.appendChild(document.createTextNode(filename+".wav "))
	
	li.appendChild(document.createElement("br"));
	
	li.appendChild(link);

	var upload = document.createElement('a');
	upload.href="http://localhost:8000/res";
	upload.innerHTML = "Inference";
	upload.addEventListener("click", function(event){
		  var xhr=new XMLHttpRequest();
		  xhr.onload=function(e) {
		      if(this.readyState === 4) {                                        
				//   console.log("Server returned: ",e.target.responseText);
				console.log('inference audio')
		      }
		  };
		  var fd=new FormData();
		  fd.append("audio_data",blob, filename);
		  xhr.open("POST","http://localhost:8000/pred",false);
		  xhr.send(fd);
	})
	li.appendChild(document.createTextNode (" "))
	li.appendChild(upload)

	recordingsList.appendChild(li);
}