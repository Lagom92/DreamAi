// var song;
// var amp;
// var button;
// let mic;

// var volhistory = [];

// // function toggleSong() {
// //   if (song.isPlaying()) {
// //     song.pause();
// //   } else {
// //     song.play();
// //   }
// // }

// // function preload() {
// //   song = loadSound('../static/sound/The-Avengers-Theme-Song.mp3');
// // }

// function setup() {
//   createCanvas(200, 200);
//   // button = createButton('toggle');
//   // button.mousePressed(toggleSong);
//   // song.play();
//   // amp = new p5.Amplitude();
//   mic = new p5.AudioIn();
//   mic.start();
// }

// function draw() {
//   background(0);
//   let vol = mic.getLevel();
//   // var vol = amp.getLevel();
//   console.log(vol)
//   volhistory.push(vol);
//   stroke(255);
//   noFill();
//   push();
//   var currentY = map(vol, 0, 1, height, 0);
//   translate(0, height / 2 - currentY);
//   beginShape();
//   for (var i = 0; i < volhistory.length; i++) {
//     var y = map(volhistory[i], 0, 1, height, 0);
//     vertex(i, y);
//   }
//   endShape();
//   pop();
//   if (volhistory.length > width - 50) {
//     volhistory.splice(0, 1);
//   }

//   stroke(255, 0, 0);
//   line(volhistory.length, 0, volhistory.length, height);
//   // ellipse(100, 100, 200, vol * 200);
// }

// ----------------------------------------------------------------------
// FUNCTION NAME
// setup()
// canvasPressed()
// draw()

// http://localhost:8000/record/

let mic, recorder, soundFile;
let state = 0;

function setup() {
  let cnv = createCanvas(100, 100);
  cnv.position(0, 200, 'fixed');
  cnv.mousePressed(canvasPressed);
  background(220);
  textAlign(CENTER, CENTER);

  // create an audio in
  mic = new p5.AudioIn();

  // prompts user to enable their browser mic
  mic.start();

  // create a sound recorder
  recorder = new p5.SoundRecorder();

  // connect the mic to the recorder
  recorder.setInput(mic);

  // this sound file will be used to
  // playback & save the recording
  soundFile = new p5.SoundFile();

  text('tap to record', width/2, height/2);
}

function canvasPressed() {
  // ensure audio is enabled
  userStartAudio();

  // make sure user enabled the mic
  if (state === 0 && mic.enabled) {

    // record to our p5.SoundFile
    recorder.record(soundFile);

    background(255,0,0);
    text('Recording!', width/2, height/2);
    state++;
  }
  else if (state === 1) {
    background(0,255,0);

    // stop recorder and
    // send result to soundFile
    recorder.stop();

    text('Done! Tap to play and download', width/2, height/2, width - 20);
    state++;
  }

  else if (state === 2) {
    soundFile.play(); // play the result!
    save(soundFile, 'mySound.wav');
    state++;
  }
}