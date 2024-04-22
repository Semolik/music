/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { MusicianClipWithoutTrack } from './MusicianClipWithoutTrack';

export type AlbumTrack = {
    /**
     * Название трека
     */
    name: string;
    /**
     * Участники трека
     */
    feat?: string;
    /**
     * ID трека
     */
    id: string;
    /**
     * Ссылка на картинку трека
     */
    picture: ImageLink;
    clip?: MusicianClipWithoutTrack;
    /**
     * Длительность трека
     */
    duration: number;
    /**
     * Ссылка на трек
     */
    url?: string;
    /**
     * Лайкнут ли трек
     */
    liked?: boolean;
};

