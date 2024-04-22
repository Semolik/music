/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Genre } from './Genre';

export type AlbumAfterUpload = {
    name?: string;
    /**
     * Дата создания альбома
     */
    open_date: string;
    id: number;
    /**
     * Год выпуска альбома
     */
    year?: number;
    /**
     * Список жанров альбома
     */
    genres: Array<Genre>;
    /**
     * ID музыканта
     */
    musician_id: number;
};

