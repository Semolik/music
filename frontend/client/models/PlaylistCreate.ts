/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type PlaylistCreate = {
    /**
     * Список id треков
     */
    tracks_ids: Array<string>;
    /**
     * Название плейлиста
     */
    name: string;
    description?: string;
    /**
     * Личный плейлист или публичный
     */
    private: boolean;
};

