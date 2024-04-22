/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AlbumInfo } from './AlbumInfo';
import type { ImageLink } from './ImageLink';
import type { MusicianInfo } from './MusicianInfo';
import type { Track } from './Track';

export type GenreFullInfo = {
    /**
     * Название жанра
     */
    name: string;
    /**
     * ID жанра
     */
    id: number;
    /**
     * Ссылка на картинку жанра
     */
    picture: ImageLink;
    /**
     * Количество лайков жанра
     */
    likes?: number;
    /**
     * Лайкнут ли жанр
     */
    liked?: boolean;
    /**
     * Список популярных альбомов
     */
    popular_albums?: Array<AlbumInfo>;
    /**
     * Список популярных треков
     */
    popular_tracks?: Array<Track>;
    /**
     * Список популярных музыкантов
     */
    popular_musicians?: Array<MusicianInfo>;
    /**
     * Список новых альбомов
     */
    new_albums?: Array<AlbumInfo>;
};

