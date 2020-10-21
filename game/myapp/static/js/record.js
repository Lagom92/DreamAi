let mic;

function setup() {
  createCanvas(710, 200);

  // 오디오 입력 생성하기
  mic = new p5.AudioIn();

  // 오디오 입력 시작하기
  // 그 기본값은 .connect()(즉, 컴퓨터 스피커에 연결)되지 "않은" 상태입니다.
  mic.start();
}

function draw() {
  background(200);

  // 전체 볼륨(0과 1.0 사이) 받아오기
  let vol = mic.getLevel();
  console.log(vol)
  fill(127);
  stroke(0);

  // 마이크 소리의 볼륨에 따라 떠있는 높이가 변하는 타원 그리기
  let h = map(vol, 0, 1, height, 0);
  ellipse(width / 2, h - 25, 50, 50);
}