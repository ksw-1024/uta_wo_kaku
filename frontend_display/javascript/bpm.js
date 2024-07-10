// 音を鳴らすための初期設定
const audioContext = new AudioContext();
let tempo = 150;
let isPlaying = false;
let intervalId;

const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');

var bgm = new Howl({
    src: ["/frontend_display/audio/bgm.mp3"],
    volume: 0.3
});

var count2 = new Howl({
    src: ["/backend/audio/20240711012206620099.wav"],
    loop: true
});

startButton.addEventListener('click', () => {
    play();
});

stopButton.addEventListener('click', () => {
    isPlaying = false;

    bgm.stop();
    count2.stop();
    audio.currentTime = 0;
});

function play() {
    bgm.play();
    count2.play()

    isPlaying = true;
}