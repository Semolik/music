/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AlbumInfo } from './AlbumInfo';
import type { MusicianProfile } from './MusicianProfile';
import type { PlaylistInfoWithoutTracks } from './PlaylistInfoWithoutTracks';

export type HistoryItem = {
    id: string;
    type: string;
    info: (AlbumInfo | PlaylistInfoWithoutTracks | MusicianProfile);
};

