/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AlbumInfoWithoutMusician } from './AlbumInfoWithoutMusician';
import type { MusicianClipWithoutMusician } from './MusicianClipWithoutMusician';
import type { TrackWithoutMusician } from './TrackWithoutMusician';

export type MusicianContent = {
    /**
     * Клипы музыканта
     */
    clips: Array<MusicianClipWithoutMusician>;
    /**
     * Альбомы музыканта
     */
    albums: Array<AlbumInfoWithoutMusician>;
    /**
     * Треки музыканта
     */
    tracks: Array<TrackWithoutMusician>;
};

