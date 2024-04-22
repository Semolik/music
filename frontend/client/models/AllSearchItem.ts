/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SearchAlbum } from './SearchAlbum';
import type { SearchClip } from './SearchClip';
import type { SearchMusician } from './SearchMusician';
import type { SearchPlaylist } from './SearchPlaylist';
import type { SearchTrack } from './SearchTrack';

export type AllSearchItem = {
    type: string;
    info: (SearchMusician | SearchAlbum | SearchTrack | SearchClip | SearchPlaylist);
    likes_count: number;
};

