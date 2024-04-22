/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';
import type { MusicianInfo } from './MusicianInfo';
import type { TrackWithoutMusician } from './TrackWithoutMusician';

export type SearchClip = {
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
    /**
     * Информация о треке
     */
    track?: TrackWithoutMusician;
    musician: MusicianInfo;
};

