/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type PlaylistBase = {
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

