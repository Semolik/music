/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AlbumInfoWithoutMusician } from './AlbumInfoWithoutMusician';
import type { ImageLink } from './ImageLink';
import type { MusicianClipWithoutTrack } from './MusicianClipWithoutTrack';
import type { PublicProfile } from './PublicProfile';

export type SearchTrack = {
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
    /**
     * Информация об альбоме
     */
    album: AlbumInfoWithoutMusician;
    /**
     * Информация о музыканте
     */
    musician: PublicProfile;
};

