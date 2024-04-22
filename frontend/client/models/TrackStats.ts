/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { StatsDay } from './StatsDay';

export type TrackStats = {
    /**
     * Общее количество прослушиваний
     */
    total_listens: number;
    /**
     * Статистика по дням
     */
    calendar: Array<StatsDay>;
    /**
     * ID трека
     */
    track_id: string;
};

