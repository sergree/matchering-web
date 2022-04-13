/*
 * Matchering WEB - Handy Matchering 2.0 Containerized Web Application
 * Copyright (C) 2016-2022 Sergree
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

function crossfade(from, to) {
    $(from).fadeOut(1000).promise().done(
        function () {
            $(to).fadeIn(1000);
        }
    );
}

function redrawProcess() {
    $("#stage-process").removeClass("process-error");
}

function redrawUpload(file_type) {
    $(`#upload-${file_type}`)
        .removeClass("upload-cell-uploading upload-cell-uploaded")
        .addClass("upload-cell-active");
}

function redrawAll(keep_target = false, keep_reference = false) {
    if (!keep_target) { redrawUpload("target"); }
    if (!keep_reference) { redrawUpload("reference"); }

    redrawProcess();

    let from;
    if ($("#stage-process").is(":visible")) {
        from = "#stage-process";
    } else {
        from = "#stage-result";
    }

    audioPause();

    crossfade(from, "#stage-upload");
}

const warning = $("#warning");
let warningText = "";

function updateWarningText(warningCodes) {
    let warnings = ["Warning!"];
    warningCodes.forEach(
        function (entry) {
            warnings.push(`${codes[entry]}.`);
        }
    );
    warningText = warnings.join("<br><br>");
}

function showStageResult(json) {
    $("#track-target").html(json.target);
    $("#track-reference").html(json.reference);
    $("#result16").attr("href", json.result16);
    $("#result24").attr("href", json.result24);
    $("#player-original").attr("src", json.preview_target);
    $("#player-matchered").attr("src", json.preview_result);
    if (json.warnings.length > 0) {
        updateWarningText(json.warnings);
        warning.addClass("warning-visible");
    } else {
        warning.removeClass("warning-visible");
    }
    crossfade("#stage-process", "#stage-result");
}

function showError() {
    $("#stage-process").addClass("process-error");
}

function updateStatus(code) {
    $("#process-text").html(codes[code]);
}

function showStageProcess() {
    crossfade("#stage-upload", "#stage-process");
}

function success(file_type) {
    $(`#upload-${file_type}`)
        .removeClass("upload-cell-uploading")
        .addClass("upload-cell-uploaded");
    $(`#upload-${file_type}-text`).html("OK");
}

function uploadFunc(file_type) {
    return function (uploadProgress, totalBytes, totalBytesSent) {
        $(`#upload-${file_type}-text`).html(`${uploadProgress.toFixed(0)}%`);
    };
}

const upload = {
    target: uploadFunc("target"),
    reference: uploadFunc("reference")
};

function addedFunc(file_type) {
    return function () {
        $(`#upload-${file_type}`)
            .removeClass("upload-cell-active")
            .addClass("upload-cell-uploading");
    };
}

const added = {
    target: addedFunc("target"),
    reference: addedFunc("reference")
};

function showPage() {
    $("#page-preloader .spinner").fadeOut();
    $("#page-preloader").delay(150).fadeOut("slow");
}

function myAlert(text) {
    $("#main-modal-text").html(text);
    const mainModal = $("#main-modal");
    if (mainModal.css("display") === "none") {
        mainModal.modal({
            fadeDuration: 250
        });
    }
}

function showWarning() {
    myAlert(warningText);
}

function genHandler(where, from, to) {
    return function () {
        $(where).stop().css("opacity", "0").html(function (_, oldText) {
            return (
                oldText === to ? from : to
            );
        }).animate({
            opacity: 1
        }, 500);
    };
}

const uploadTipText = $("#upload-tip").html();

$("#upload-target").hover(
    genHandler(
        "#upload-tip",
        uploadTipText,
        "The Track You Want to Master"
    )
);
$("#upload-reference").hover(
    genHandler(
        "#upload-tip",
        uploadTipText,
        "Some <span class=\"accent\">Wet</span> Reference Track"
    )
);

warning.click(showWarning);