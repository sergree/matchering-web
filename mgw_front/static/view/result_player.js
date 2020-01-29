function playerIsPlaying(player) {
    return !player.paused && !player.ended && 0 < player.currentTime;
}

const playerTarget = $("#player-original")[0];
const playerResult = $("#player-matchered")[0];
const previewPause = $("#preview-pause");
const previewOriginal = $("#preview-original");
const previewMatchered = $("#preview-matchered");
const previewPlayer = $("#preview-player");

function toggleVolume(result = true) {
    playerTarget.volume = +!result;
    playerResult.volume = +result;
}

function togglesWereNotTouched() {
    return playerTarget.volume === 1 && playerResult.volume === 1;
}

function audioPlay() {
    playerTarget.play();
    playerResult.play();
    previewPlayer.addClass("preview-player-playing");
}

function audioPause() {
    playerTarget.pause();
    playerResult.pause();
    previewPlayer.removeClass("preview-player-playing");
}

function audioIsPlaying() {
    return playerIsPlaying(playerTarget) || playerIsPlaying(playerResult);
}

function pauseHandler() {
    if (!audioIsPlaying()) {
        if (togglesWereNotTouched()) {
            toggleVolume(true);
        }
        audioPlay();
    } else {
        audioPause();
    }
}

function originalHandler() {
    previewPlayer.addClass("preview-player-original");
    toggleVolume(false);
}

function matcheredHandler() {
    previewPlayer.removeClass("preview-player-original");
    toggleVolume(true);
}

previewPause.click(pauseHandler);
previewOriginal.click(originalHandler);
previewMatchered.click(matcheredHandler);