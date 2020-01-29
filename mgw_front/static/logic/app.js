function dropzone(file_type) {
    return new Dropzone(
        `#upload-${file_type}>.upload-zone`, {
            url: `dummy`,
            maxFilesize: 256,
            previewTemplate: "<div style=\"display:none\"></div>",
            previewsContainer: false,
            createImageThumbnails: false,
            acceptedFiles: ".wav,.flac,.aif,.aiff,.aifc,.mp3,.m4a," +
                ".mp4,.ogg,.mp2,.aac,.3gp,.ape",
            init: function () {
                this.on("error", function (file, response) {
                    if (!file.accepted) {
                        this.removeFile(file);
                        myAlert("The file format is not supported or the max" +
                            "imum file size (256 MB) has been exceeded.");
                        redrawUpload(file_type);
                    } else {
                        myAlert(response);
                    }
                });
            },
            fallback: function () {
                myAlert("Your browser doesn't support file upload");
            },
            addedfile: added[file_type],
            totaluploadprogress: upload[file_type],
            success: function () {
                success(file_type);
                connector.uploadSuccess(file_type);
            }
        }
    );
}

const connector = {
    token: null,
    alreadyShown: false,
    targetUploaded: false,
    referenceUploaded: false,
    checker: null,
    targetDropzone: null,
    referenceDropzone: null,
    targetKeep: false,
    referenceKeep: false,

    initializeDropZones: function () {
        connector.targetDropzone = dropzone("target");
        connector.referenceDropzone = dropzone("reference");
    },

    updateDropZoneUrl: function (fileType) {
        let dz = connector[`${fileType}Dropzone`];
        dz.removeAllFiles(true);
        dz.options.url = `/api/upload/${connector.token}/${fileType}/`;
    },

    createSession: function (targetKeep = false, referenceKeep = false) {
        $.post({
            url: "/api/session/",
            data: JSON.stringify({
                "previous": connector.token,
                "keep_target": targetKeep,
                "keep_reference": referenceKeep
            }),
            success: function (json) {
                connector.token = json.token;
                if (connector.token && !connector.alreadyShown) {
                    showPage();
                    connector.alreadyShown = true;
                }
                if (connector.token) {
                    if (!targetKeep) {
                        connector.updateDropZoneUrl("target");
                        connector.targetUploaded = false;
                    }
                    if (!referenceKeep) {
                        connector.updateDropZoneUrl("reference");
                        connector.referenceUploaded = false;
                    }
                } else {
                    myAlert("System error! The token is not issued by the " +
                        "server side. Try restarting the container.");
                }
            }
        });
    },

    uploadSuccess: function (fileType) {
        this[`${fileType}Uploaded`] = true;
        if (this.targetUploaded && this.referenceUploaded) {
            showStageProcess();
            connector.checker = setInterval(connector.checkSession, 1000);
        }
    },

    checkSession: function () {
        $.getJSON(`/api/session/${connector.token}/`, function (json) {
            updateStatus(json.code);
            if (json.code === 2010) {
                showStageResult(json);
                clearInterval(connector.checker);
            } else if (Math.floor(json.code / 1000) === 4) {
                showError();
                clearInterval(connector.checker);
            }
        });
    },

    restart: function (targetKeep = false, referenceKeep = false) {
        redrawAll(targetKeep, referenceKeep);
        connector.createSession(targetKeep, referenceKeep);
    },

    restartNoKeep: function () {
        connector.restart(false, false);
    },

    restartKeep: function () {
        connector.restart(connector.targetKeep, connector.referenceKeep);
    }
};

$(window).on("load", function () {
    $.when(connector.initializeDropZones()).then(function () {
        connector.createSession(false, false);
    });
});

$("#process_cancel").click(function () {
    connector.restartNoKeep();
});

$("#another").click(function () {
    connector.restartKeep();
});
