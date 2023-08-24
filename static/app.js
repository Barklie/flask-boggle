// const { default: axios } = require("axios");

// collect the elements needed 
const startButton = document.getElementById('start-button');
const form = document.querySelector('form')
const timerDisplay = document.getElementById('timer');

// set up variables for timer and remaining time
let timer;
let remainingTime = 60;
let nPlays = 0
let score = 0

// start time function
function startTimer() {
    // first clear timer
    if (timer) {
        clearInterval(timer);
    }

    // set timer to 
    timer = setInterval(updateTimer, 1000);
    updateTimer();
}

// function to update the timer as needed to be called in the startTimer function
function updateTimer() {
    if (remainingTime > 0) {
        remainingTime--;
        timerDisplay.textContent = `Time Remaining: ${remainingTime} seconds`;
    } else {
        clearInterval(timer);
        timerDisplay.textContent = 'Time is up!'
        remainingTime = 60
        const wordInput = document.getElementById("word");
        const submitButton = document.getElementById("submit-button");
        let newPlays = nPlays += 1
        console.log(score)



        postStats(score, newPlays)


    }
}

async function postStats(playerScore, nplays) {
    res = await axios.post('http://127.0.0.1:5000/post-score', { "score": playerScore, "nplays": nplays })
    console.log(res.data.brokeRecord)
    console.log(res)

    $('#nplays').text(`Number of Games Played: ${res.data.nplays}`)

    if (res.data.brokeRecord === true) {
        $('#highScore').text(`High Score: ${playerScore}`)
    }
    // else{
    //     $('#highScore').text(`High Score: ${}`)
    // }

}

startButton.addEventListener('click', startTimer);



form.addEventListener("submit", function (e) {
    e.preventDefault()

    userGuess = $('#form-guess').val()

    handleSubmit(userGuess)
})


//function to check user's guess, update score, and notify user if their guess is valid
async function handleSubmit(guess) {

    const res = await axios.post('http://127.0.0.1:5000/validate-guess',
        { word: `${guess}` })

    console.log(res)

    if (res.data.result === "ok") {
        console.log('ok')
        $('#result').text(`Your Guess is: ${res.data.result} `)
        let newScore = score += 1
        console.log(newScore)
        $('#score').text(`Score: ${newScore} `)
    }

    if (res.data.result === "not-a-word") {
        console.log('no')
        $('#result').text(`Your Guess is: ${res.data.result} `)
    }

    if (res.data.result === "not-on-board") {
        console.log('no')
        $('#result').text(`Your Guess is: ${res.data.result} `)
    }

}