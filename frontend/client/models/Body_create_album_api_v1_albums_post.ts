/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CreateAlbumJson } from './CreateAlbumJson';

export type Body_create_album_api_v1_albums_post = {
    albumData: CreateAlbumJson;
    /**
     * Картинка альбома
     */
    albumPicture: Blob;
};

