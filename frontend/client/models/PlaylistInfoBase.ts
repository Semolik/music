/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';

export type PlaylistInfoBase = {
    /**
     * Название плейлиста
     */
    name: string;
    description?: string;
    /**
     * Личный плейлист или публичный
     */
    private: boolean;
    /**
     * id плейлиста
     */
    id: string;
    /**
     * Дата создания плейлиста
     */
    created_at: string;
    picture?: ImageLink;
    /**
     * Количество треков в плейлисте
     */
    tracks_count: number;
    /**
     * Понравился ли плейлист пользователю
     */
    liked?: boolean;
};

