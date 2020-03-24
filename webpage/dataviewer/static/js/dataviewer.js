//global variables
var matches = { //this needs to be global so that bokeh callbacks can access it (I think)
    numbers: [],
    winners: [],
    KOs: [],
    damPercs: []
};
//numbers is array enumerating all matches; winners is array with the winner of each match; 
//KOs is an array full of arrays where each sub-array (for each game) contains (1) an ordered array of players and (2) their corresponding KO count.
//similar construction for damPercs (damage percentages).



//Data Handling

function getData(test) { //pulls raw .db data, loads it to usable format
    //execute this whenever the page loads
    let rawData;
    if (test){
        rawData = "1,BEEF,BEEF:2 Thomato:8 curt:1 postmabone:10,Thomato:559 BEEF:200 postmabone:999 curt:10\n2,Thomato,Thomato:3 BEEF:2 postmabone:8 curt:9,postmabone:119 BEEF:100 Thomato:980 curt:2\n3,curt,Thomato:1 BEEF:5 postmabone:7 curt:2 LONG:2,LONG:456 postmabone:119 BEEF:100 Thomato:980 curt:2\n4,postmabone,Thomato:2 BEEF:3 postmabone:1 curt:3 LONG:1 sivad:4,LONG:456 sivad:890 postmabone:119 BEEF:100 Thomato:980 curt:2\n5,postmabone,BEEF:2 postmabone:3,BEEF:780 postmabone:10\n6,sivad,Thomato:7 BEEF:3 postmabone:11 curt:2 LONG:7 sivad:4,LONG:230 sivad:891 postmabone:1119 BEEF:102 Thomato:98 curt:890";
    }

    //rawData = ...
    return rawData;
}

function initializeData(rawData) { //converts pulled data into usable format
    matches.numbers = [], matches.winners = [], matches.KOs = [], matches.damPercs = []; //clears old data

    let matchArr = rawData.split("\n");
    let matchTemp = [], KOStrTemp = [], KOTemp = [[], []], KOPair = [], damPercStrTemp = [], damPercTemp = [[], []], damPercPair = [];
    for (let i = 0; i < matchArr.length; i++) {
        KOStrTemp = [], KOTemp = [[], []], damPercStrTemp = [], damPercTemp = [[],[]];

        matchTemp = matchArr[i].split(",");

        matches.numbers.push(Number(matchTemp[0]));
        matches.winners.push(matchTemp[1]);

        //organizes KO data
        KOStrTemp = matchTemp[2].split(" ");
        for (let j = 0; j < KOStrTemp.length; j++) {
            KOPair = KOStrTemp[j].split(":");

            KOTemp[0].push(KOPair[0]);
            KOTemp[1].push(Number(KOPair[1]));
        }

        matches.KOs.push(KOTemp);

        //organizes damage percentage data
        damPercStrTemp = matchTemp[3].split(" ");
        for (let j = 0; j < damPercStrTemp.length; j++) {
            damPercPair = damPercStrTemp[j].split(":");

            damPercTemp[0].push(damPercPair[0]);
            damPercTemp[1].push(Number(damPercPair[1]));
        }

        matches.damPercs.push(damPercTemp);

    }

    return;

}