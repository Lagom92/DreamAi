let mic;
let x1, y1, x2, y2, x3;
let pg;

 function setup(){
    let cnv = createCanvas(600, 100);
    cnv.mousePressed(userStartAudio);
    textAlign(CENTER);
    x1 = width/3
    y1 = height*0
    x2 = width/3
    y2 = height-20
    x3 = width/4
    pg = createGraphics(400, 250);
    mic = new p5.AudioIn();
    mic.start();
}

function draw(){
    background(0);
    fill(255);
    text('tap to start', 60, 20);


    // 윗 장애물
    //150, 75, 0 => 갈색
    fill(255);
    rect(x1, y1, 300, 20);

    // 아랫 장애물
    fill(255);
    rect(x2, y2, 300, 20);

    //첫번째 발판
    fill(255);
    rect(550 , 66, 60, 10);

    //두번째 발판
    fill(255);
    rect(550 , 33, 60, 10);


    //세번째 발판
    fill(255);
    rect(550 , 0, 100, 10);

    
    micLevel = mic.getLevel();
    let y3 = height - micLevel * height;
    y4 = y3 - 30;
    rect(x3, y4, 10, 10);

    if (y4 < 25) {
        y4.position(x3, 25);
    }

    

}

// mic.js에서 신호를 주면 record.js에서 녹음을 시작할 수 있나?