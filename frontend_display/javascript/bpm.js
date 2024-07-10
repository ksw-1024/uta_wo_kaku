// 音を鳴らすための初期設定
const audioContext = new AudioContext();
let tempo = 150;
let isPlaying = false;
let intervalId;

const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');

const audio = document.getElementById('bgm');
const count = document.getElementById("count");

audio.volume = 0.2
count.volume = 0.2

audio.src = "/frontend_display/audio/bgm.mp3";
count.src = "/frontend_display/audio/metro.wav";

var bgm = new Howl({
    src: ["/frontend_display/audio/bgm.mp3"]
});

var count2 = new Howl({
    src: ["/frontend_display/audio/metro.wav"]
});

startButton.addEventListener('click', () => {
    play();
});

stopButton.addEventListener('click', () => {
    isPlaying = false;

    bgm.pause();
    audio.currentTime = 0;
});

function play() {
    bgm.play();

    isPlaying = true;
    setTimeout(beep, (60 / tempo) * 1000);

    console.log((60 / tempo) * 1000)
}

function beep() {
    let d = new Date();
    let startTime = d.getTime();
    count2.play();

    let d2 = new Date();
    console.log(((60 / tempo) * 1000) - (d2.getTime() - startTime));
    setTimeout(beep, ((60 / tempo) * 1000) - (d2.getTime() - startTime));
}