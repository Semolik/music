/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { PublicProfileLinksUsernames } from './PublicProfileLinksUsernames';

export type PublicProfileUsernames = {
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
    links: PublicProfileLinksUsernames;
    picture?: ImageLink;
};

