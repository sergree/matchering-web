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

const codes = {
    "2001": "Uploading files",
    "2002": "Queued for processing",
    "2003": "Loading and analysis",
    "2004": "Matching levels",
    "2005": "Matching frequencies",
    "2006": "Correcting levels",
    "2007": "Final processing and saving",
    "2008": "Exporting various audio formats",
    "2009": "Making previews",
    "2010": "The task is completed",
    "2101": "The TARGET audio is mono. Converting it to stereo...",
    "2201": "The REFERENCE audio is mono. Converting it to stereo...",
    "2202": "The REFERENCE audio was resampled",
    "2203": "Presumably the REFERENCE audio format is lossy",
    "3001": "Audio clipping is detected in the TARGET file. It is highly recommended to use the non-clipping version",
    "3002": "The applied limiter is detected in the TARGET file. It is highly recommended to use the version without a limiter",
    "3003": "The TARGET audio sample rate and internal sample rate were different. The TARGET audio was resampled",
    "3004": "Presumably the TARGET audio format is lossy. It is highly recommended to use lossless audio formats (WAV, FLAC, AIFF)",
    "4001": "Audio stream error in the TARGET file",
    "4002": "Track length is exceeded in the TARGET file",
    "4003": "The track length is too small in the TARGET file",
    "4004": "The number of channels exceeded in the TARGET file",
    "4005": "The TARGET and REFERENCE files are the same. They must be different so that Matchering makes sense",
    "4101": "Audio stream error in the REFERENCE file",
    "4102": "Track length is exceeded in the REFERENCE file",
    "4103": "The track length is too small in the REFERENCE file",
    "4104": "The number of channels exceeded in the REFERENCE file",
    "4201": "Unknown error",
    "4202": "Validation failed! Please let the developers know about this error!"
};