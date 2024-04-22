/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Body_update_clip_api_v1_clips__clip_id__put = {
    /**
     * Картинка клипа
     */
    clipPicture?: Blob;
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
     * Использовать ли картинку с YouTube
     */
    image_from_youtube: boolean;
};

