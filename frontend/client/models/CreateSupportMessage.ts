/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SupportMessageType } from './SupportMessageType';

export type CreateSupportMessage = {
    /**
     * Email пользователя
     */
    email: string;
    /**
     * Сообщение
     */
    message: string;
    /**
     * Тип сообщения
     */
    type?: SupportMessageType;
    /**
     * Логин пользователя
     */
    login: string;
};

