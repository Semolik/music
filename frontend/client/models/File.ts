/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type File = {
    id: string;
    /**
     * ID пользователя
     */
    user_id: number;
    url?: string;
    /**
     * Имя файла, как оно было на компьютере пользователя
     */
    original_file_name: string;
};

