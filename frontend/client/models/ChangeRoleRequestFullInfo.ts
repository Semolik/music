/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ChangeRoleRequestStatus } from './ChangeRoleRequestStatus';
import type { File } from './File';
import type { RoleRequestAnswer } from './RoleRequestAnswer';
import type { UserInfo } from './UserInfo';

export type ChangeRoleRequestFullInfo = {
    /**
     * Время создания
     */
    time_created: string;
    /**
     * Файлы, прикрепленные к запросу
     */
    files: Array<File>;
    /**
     * Сообщение пользователя
     */
    message: string;
    /**
     * Статус запроса
     */
    request_status: ChangeRoleRequestStatus;
    /**
     * Ответ на запрос
     */
    answer: RoleRequestAnswer;
    /**
     * ID запроса на изменение типа аккаунта
     */
    id: number;
    /**
     * Пользователь, сделавший запрос
     */
    user: UserInfo;
};

