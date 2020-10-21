var song;
var amp;
var button;
let mic;

var volhistory = [];

// function toggleSong() {
//   if (song.isPlaying()) {
//     song.pause();
//   } else {
//     song.play();
//   }
// }

// function preload() {
//   song = loadSound('../static/sound/The-Avengers-Theme-Song.mp3');
// }

function setup() {
  createCanvas(200, 200);
  // button = createButton('toggle');
  // button.mousePressed(toggleSong);
  // song.play();
  // amp = new p5.Amplitude();
  mic = new p5.AudioIn();
  mic.start();
}

function draw() {
  background(0);
  let vol = mic.getLevel();
  // var vol = amp.getLevel();
  console.log(vol)
  volhistory.push(vol);
  stroke(255);
  noFill();
  push();
  var currentY = map(vol, 0, 1, height, 0);
  translate(0, height / 2 - currentY);
  beginShape();
  for (var i = 0; i < volhistory.length; i++) {
    var y = map(volhistory[i], 0, 1, height, 0);
    vertex(i, y);
  }
  endShape();
  pop();
  if (volhistory.length > width - 50) {
    volhistory.splice(0, 1);
  }

  stroke(255, 0, 0);
  line(volhistory.length, 0, volhistory.length, height);
  // ellipse(100, 100, 200, vol * 200);
}