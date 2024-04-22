/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { MusicianContent } from './MusicianContent';
import type { PublicProfileLinks } from './PublicProfileLinks';

export type MusicianFullInfo = {
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
     * Лайкнут ли музыкант
     */
    liked?: boolean;
    /**
     * Количество лайков музыканта
     */
    likes_count?: number;
    /**
     * Популярное
     */
    popular: MusicianContent;
};

