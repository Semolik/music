/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { PublicProfileLinks } from './PublicProfileLinks';

export type MusicianProfile = {
    /**
     * Оторажаемое имя
     */
    name: string;
    /**
     * Описание профиля
     */
    description?: string;
    /**
     * ID публичного профиля
     */
    id: number;
    /**
     * Ссылки на соц. сети
     */
    links: PublicProfileLinks;
    picture?: ImageLink;
    /**
     * Лайкнут ли профиль
     */
    liked?: boolean;
};

