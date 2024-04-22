/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { PublicProfileLinks } from './PublicProfileLinks';

export type PublicProfile = {
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
};

