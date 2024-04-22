/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Genre } from './Genre';
import type { ImageLink } from './ImageLink';
import type { PublicProfile } from './PublicProfile';

export type AlbumInfo = {
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
     * Ссылка на картинку альбома
     */
    picture: ImageLink;
    /**
     * Лайкнут ли альбом
     */
    liked?: boolean;
    /**
     * Количество лайков альбома
     */
    likes_count?: number;
    /**
     * Информация о музыканте
     */
    musician: PublicProfile;
};

