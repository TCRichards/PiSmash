//global variables
var fancyHistAxes = ["Highest KO Count per Game", "Highest Damage Done per Game"];
var fancyHistNormalization = [true, true];
var playerPlotAxes = ["KO Counts per Player", "Win Counts per Player"]
var barGraphAxis = "KO Counts per Player";


// FUNCTIONS

function average(x) {
    let sum = 0;

    for (let i = 0; i < x.length; i++) {
        sum += x[i];
    }

    return sum / x.length;
}

//Histogram(s)
function getHistBins(data) {
    let N = data.length;
    let bincount = Math.round(Math.sqrt(N));

    var arr_hist = []; //each element in this is the number of data points in the associated bin
    var bins = []; //contains arrays; each array is a bin which contains the datapoints
    var binwidth = Math.abs(Math.min(...data) - Math.max(...data)) / bincount
    var edges = [Math.min(...data)];

    for (var i = 0; i < bincount; i++) {
        edges.push(edges[i] + binwidth);
    }

    //making sure first bin starts at slightly below min (to go against rounding errors);
    edges[0] = Math.min(...data) - Math.min(...data) * 1e-9;
    //making sure last bin goes to slightly above max
    edges[bincount] = Math.max(...data) + Math.max(...data) * 1e-9;

    var left = edges.slice(0, -1);
    var right = edges.slice(1);

    var bintemp = [];

    for (var i = 0; i < bincount; i++) {
        bintemp = [];
        for (var j = 0; j < data.length - 1; j++) {
            if ((data[j] >= edges[i]) && (data[j] < edges[i + 1])) {
                bintemp.push(data[j]); //adds data to the bin if it is between the bounds of the bin
            }
        }
        if ((data[data.length - 1] > edges[i]) && (data[data.length - 1] <= edges[i + 1])) {
            bintemp.push(data[j]); //adds data to the bin if it is between the bounds of the bin
        }
        bins.push(bintemp) //adds an array of data for that bin to bins, the 2D array.
    }

    for (var i = 0; i < bincount; i++) {
        arr_hist.push(bins[i].length);
    }

    return [arr_hist, left, right];
}

function createFancyHistData() {
    let axes = [[], []];
    let hhist = [], hleft = [], hright = [];
    let vhist = [], vleft = [], vright = [];

    for (let k = 0; k < 2; k++) {
        switch (fancyHistAxes[k]) { //creates x and y
            case "Highest KO Count per Game":
                let highestKOs = [];
                for (let i = 0; i < matches.KOs.length; i++) { //for each game
                    let gameKOs = [];
                    for (let j = 0; j < matches.KOs[i][0].length; j++) { //for each player
                        gameKOs.push(matches.KOs[i][1][j]);
                    }

                    let maxKO = Math.max(...gameKOs);

                    if (fancyHistNormalization[k]) {
                        maxKO = maxKO / matches.KOs[i][0].length; //NORMALIZATION by number of players
                    }

                    highestKOs.push(maxKO);
                }
                axes[k] = highestKOs;
                break;
            case "Highest Damage Done per Game":
                let highestDams = [];
                for (let i = 0; i < matches.damPercs.length; i++) { //for each game
                    let gameDams = [];
                    for (let j = 0; j < matches.damPercs[i][0].length; j++) { //for each player
                        gameDams.push(matches.damPercs[i][1][j]);
                    }

                    let maxDam = Math.max(...gameDams);

                    if (fancyHistNormalization[k]) {
                        maxDam = maxDam / matches.damPercs[i][0].length; //NORMALIZATION by number of players
                    }

                    highestDams.push(maxDam);
                }
                axes[k] = highestDams;
                break;
            case "Average Damage Done per Game":
                let avgDams = [];
                for (let i = 0; i < matches.damPercs.length; i++) { //for each game
                    let gameDams = [];
                    for (let j = 0; j < matches.damPercs[i][0].length; j++) { //for each player
                        gameDams.push(matches.damPercs[i][1][j]);
                    }

                    let avgDam = average(gameDams);

                    if (fancyHistNormalization[k]) {
                        avgDam = avgDam / matches.damPercs[i][0].length; //NORMALIZATION by number of players
                    }

                    avgDams.push(avgDam);
                }
                axes[k] = avgDams;
                break;
            case "Player Count per Game":
                let playerCounts = [];
                for (let i = 0; i < matches.damPercs.length; i++) { //for each game

                    let playercount = matches.damPercs[i][0].length;
                    playerCounts.push(playercount);
                }
                axes[k] = playerCounts;
                break;
            default:
                break;
        }
    }



    hHistResult = getHistBins(axes[0]);
    vHistResult = getHistBins(axes[1]);

    hhist = hHistResult[0];
    hleft = hHistResult[1];
    hright = hHistResult[2];

    vhist = vHistResult[0];
    vleft = vHistResult[1];
    vright = vHistResult[2];

    return [[axes[0], axes[1]], [hhist, hleft, hright], [vhist, vleft, vright]];
}

//Scatter Plot(s)
function createPlayerPlotData() {
    let axes = [[], []];
    let players = [], bars = [];

    for (let k = 0; k < 2; k++) {
        switch (playerPlotAxes[k]) { //creates x and y
            case "KO Counts per Player":
                bars = createKOBars()
                players = bars[0];
                axes[k] = bars[1];
                break;
            case "Win Counts per Player":
                bars = createWinBars()
                players = bars[0];
                axes[k] = bars[1];
                break;
            case "Damage Done per Player":
                bars = createDamPercBars()
                players = bars[0];
                axes[k] = bars[1];
                break;
            default:
                break;
        }
    }
    return [players, axes[0], axes[1]];
}

//Bar Graph(s)

function createBars() {
    let players = [], bars = [], counts = [];

    switch (barGraphAxis) { //creates x and y
        case "KO Counts per Player":
            bars = createKOBars()
            players = bars[0];
            counts = bars[1];
            break;
        case "Win Counts per Player":
            bars = createWinBars()
            players = bars[0];
            counts = bars[1];
            break;
        case "Damage Done per Player":
            bars = createDamPercBars()
            players = bars[0];
            counts = bars[1];
            break;
        default:
            break;
    }
    return [players, counts];
}

function sortBars(players, counts) {

    let dict = {}; //convert data to a "dict" object
    players.forEach((key, i) => dict[key] = counts[i]);

    // Create items array
    var items = Object.keys(dict).map(function (key) {
        return [key, dict[key]];
    });

    // Sort the array based on the second element
    items.sort(function (first, second) {
        return second[1] - first[1];
    });

    let sortedNames = [], sortedCounts = [];

    for (let i = 0; i < items.length; i++) {
        sortedNames.push(items[i][0]);
        sortedCounts.push(items[i][1]);
    }

    return [sortedNames, sortedCounts];
}

function createWinBars() {
    //players is arr of str, wincounts is (same order) of win count

    let uniqueWinnersSet = new Set(matches.winners);

    let players = [...uniqueWinnersSet];
    let wincounts = new Array(players.length).fill(0);

    for (let i = 0; i < matches.winners.length; i++) {
        for (let j = 0; j < players.length; j++) {
            if (matches.winners[i] === players[j]) {
                wincounts[j] += 1;
            }
        }
    }


    let sorted = sortBars(players, wincounts);

    return sorted;
}

function createKOBars() {

    let allplayers = [];

    for (let i = 0; i < matches.KOs.length; i++) { //from every match, ever, creates a list of every player, then removes duplicates
        for (let j = 0; j < matches.KOs[i][0].length; j++) {
            allplayers.push(matches.KOs[i][0][j]);
        }
    }

    let uniquePlayersSet = new Set(allplayers);

    let players = [...uniquePlayersSet];
    let KOcounts = new Array(players.length).fill(0);

    for (let i = 0; i < matches.KOs.length; i++) {
        for (let j = 0; j < matches.KOs[i][0].length; j++) {
            for (let k = 0; k < players.length; k++) {
                if (matches.KOs[i][0][j] === players[k]) {
                    KOcounts[k] += matches.KOs[i][1][j]
                }
            }
        }
    }

    let sorted = sortBars(players, KOcounts);

    return sorted;
}

function createDamPercBars() {

    let allplayers = [];

    for (let i = 0; i < matches.damPercs.length; i++) { //from every match, ever, creates a list of every player, then removes duplicates
        for (let j = 0; j < matches.damPercs[i][0].length; j++) {
            allplayers.push(matches.damPercs[i][0][j]);
        }
    }

    let uniquePlayersSet = new Set(allplayers);

    let players = [...uniquePlayersSet];
    let damPercCounts = new Array(players.length).fill(0);

    for (let i = 0; i < matches.damPercs.length; i++) {
        for (let j = 0; j < matches.damPercs[i][0].length; j++) {
            for (let k = 0; k < players.length; k++) {
                if (matches.damPercs[i][0][j] === players[k]) {
                    damPercCounts[k] += matches.damPercs[i][1][j]
                }
            }
        }
    }

    let sorted = sortBars(players, damPercCounts);

    return sorted;
}