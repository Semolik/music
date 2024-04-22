/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { UserTypeEnum } from './UserTypeEnum';

export type UserInfo = {
    /**
     * Логин пользователя
     */
    username: string;
    /**
     * Имя пользователя
     */
    first_name?: string;
    /**
     * Фамилия пользователя
     */
    last_name?: string;
    type: UserTypeEnum;
    id: number;
    /**
     * Ccылка на аватарку пользователя
     */
    picture?: ImageLink;
};

