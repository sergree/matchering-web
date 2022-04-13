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