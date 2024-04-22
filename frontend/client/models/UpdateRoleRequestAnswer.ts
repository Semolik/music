/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ChangeRoleRequestStatus } from './ChangeRoleRequestStatus';

export type UpdateRoleRequestAnswer = {
    /**
     * Ответное сообщение
     */
    message: string;
    /**
     * Статус запроса
     */
    request_status: ChangeRoleRequestStatus;
};

