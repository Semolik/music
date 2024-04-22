/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UpdateAlbumJson = {
    name?: string;
    /**
     * Дата создания альбома
     */
    open_date: string;
    /**
     * Список ID жанров
     */
    genres_ids?: Array<number>;
};

