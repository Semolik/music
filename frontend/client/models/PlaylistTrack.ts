/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlaylistInfoWithoutTracks } from './PlaylistInfoWithoutTracks';
import type { Track } from './Track';

export type PlaylistTrack = {
    /**
     * Трек
     */
    track: Track;
    /**
     * Плейлист
     */
    playlist: PlaylistInfoWithoutTracks;
};

