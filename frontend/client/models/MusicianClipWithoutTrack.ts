/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';

export type MusicianClipWithoutTrack = {
    /**
     * Название клипа
     */
    name: string;
    /**
     * ID видео на YouTube
     */
    video_id: string;
    /**
     * ID трека
     */
    track_id?: string;
    /**
     * ID клипа
     */
    id: number;
    /**
     * Ссылка на картинку клипа
     */
    picture: ImageLink;
    video?: string;
};

