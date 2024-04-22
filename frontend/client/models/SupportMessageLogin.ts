/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SupportMessageStatus } from './SupportMessageStatus';
import type { SupportMessageType } from './SupportMessageType';

export type SupportMessageLogin = {
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
     * ID сообщения
     */
    id: string;
    /**
     * Статус сообщения
     */
    status: SupportMessageStatus;
    /**
     * Дата создания сообщения
     */
    created_at: string;
    /**
     * Логин пользователя
     */
    login: string;
};

