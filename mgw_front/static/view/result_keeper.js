const targetMAButton = $("#make-another-checkbox-target");
const referenceMAButton = $("#make-another-checkbox-reference");

function redrawMA() {
    if (connector.targetKeep) {
        targetMAButton.addClass("make-another-checkbox-selected");
    } else {
        targetMAButton.removeClass("make-another-checkbox-selected");
    }

    if (connector.referenceKeep) {
        referenceMAButton.addClass("make-another-checkbox-selected");
    } else {
        referenceMAButton.removeClass("make-another-checkbox-selected");
    }
}

function targetMAButtonHandler () {
    if (connector.referenceKeep) { connector.referenceKeep = false; }
    connector.targetKeep = !connector.targetKeep;
    redrawMA();
}

function referenceMAButtonHandler () {
    if (connector.targetKeep) { connector.targetKeep = false; }
    connector.referenceKeep = !connector.referenceKeep;
    redrawMA();
}

targetMAButton.click(targetMAButtonHandler);
referenceMAButton.click(referenceMAButtonHandler);