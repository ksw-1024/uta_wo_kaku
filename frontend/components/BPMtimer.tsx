import React, { useState } from "react";

const MINUTES = 60 * 1000;
const BASE_BEAT = 4; // BPMが4分音符換算なので定数的に扱う
const bpm = 120;
const beat = 4; // 実際にカウントするベースになる音符
const beatRate = MINUTES / (bpm * beat / MINUTES);
let section = 1;
let requestID;
let time = 0;
let preBeatCount = 0;


const timerId = setInterval(() => {
    preBeatCount = preBeatCount + 1
}, beatRate)


return <div>{preBeatCount}</div>
}

export default BPMtimer