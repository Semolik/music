/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';

export type GenreStats = {
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
     * Количество альбомов
     */
    album_count?: number;
};

