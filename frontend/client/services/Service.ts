/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AlbumAfterUpload } from '../models/AlbumAfterUpload';
import type { AlbumInfo } from '../models/AlbumInfo';
import type { AlbumInfoUploaded } from '../models/AlbumInfoUploaded';
import type { AlbumInfoWithoutMusician } from '../models/AlbumInfoWithoutMusician';
import type { AlbumWithTracks } from '../models/AlbumWithTracks';
import type { AlbumWithTracksUploaded } from '../models/AlbumWithTracksUploaded';
import type { AllSearchItem } from '../models/AllSearchItem';
import type { Body_create_album_api_v1_albums_post } from '../models/Body_create_album_api_v1_albums_post';
import type { Body_create_clip_api_v1_clips_post } from '../models/Body_create_clip_api_v1_clips_post';
import type { Body_create_genre_api_v1_genres_post } from '../models/Body_create_genre_api_v1_genres_post';
import type { Body_create_slide_api_v1_slider_post } from '../models/Body_create_slide_api_v1_slider_post';
import type { Body_send_update_role_request_api_v1_roles_change_post } from '../models/Body_send_update_role_request_api_v1_roles_change_post';
import type { Body_update_album_api_v1_albums__album_id__put } from '../models/Body_update_album_api_v1_albums__album_id__put';
import type { Body_update_clip_api_v1_clips__clip_id__put } from '../models/Body_update_clip_api_v1_clips__clip_id__put';
import type { Body_update_genre_api_v1_genres__genre_id__put } from '../models/Body_update_genre_api_v1_genres__genre_id__put';
import type { Body_update_slide_api_v1_slider__slide_id__put } from '../models/Body_update_slide_api_v1_slider__slide_id__put';
import type { Body_update_track_by_id_api_v1_tracks__track_id__put } from '../models/Body_update_track_by_id_api_v1_tracks__track_id__put';
import type { Body_update_user_avatar_api_v1_users_me_avatar_put } from '../models/Body_update_user_avatar_api_v1_users_me_avatar_put';
import type { Body_update_user_public_avatar_api_v1_users_me_public_avatar_put } from '../models/Body_update_user_public_avatar_api_v1_users_me_public_avatar_put';
import type { Body_upload_track_api_v1_albums__album_id__track_post } from '../models/Body_upload_track_api_v1_albums__album_id__track_post';
import type { ChangePassword } from '../models/ChangePassword';
import type { ChangeRoleRequestFullInfo } from '../models/ChangeRoleRequestFullInfo';
import type { ChangeRoleRequestStatus } from '../models/ChangeRoleRequestStatus';
import type { CreateSupportMessage } from '../models/CreateSupportMessage';
import type { FilterGenreEnum } from '../models/FilterGenreEnum';
import type { Genre } from '../models/Genre';
import type { GenreFullInfo } from '../models/GenreFullInfo';
import type { GenreStats } from '../models/GenreStats';
import type { HistoryAlbum } from '../models/HistoryAlbum';
import type { HistoryItem } from '../models/HistoryItem';
import type { HistoryMusician } from '../models/HistoryMusician';
import type { HistoryPlaylist } from '../models/HistoryPlaylist';
import type { HistoryTrack } from '../models/HistoryTrack';
import type { LikesInfo } from '../models/LikesInfo';
import type { MusicianClip } from '../models/MusicianClip';
import type { MusicianFullInfo } from '../models/MusicianFullInfo';
import type { MusicianInfo } from '../models/MusicianInfo';
import type { Order } from '../models/Order';
import type { order_playlist_by } from '../models/order_playlist_by';
import type { OrderAlbums } from '../models/OrderAlbums';
import type { PlaylistBase } from '../models/PlaylistBase';
import type { PlaylistCreate } from '../models/PlaylistCreate';
import type { PlaylistInfo } from '../models/PlaylistInfo';
import type { PlaylistInfoWithoutTracks } from '../models/PlaylistInfoWithoutTracks';
import type { PlaylistTrack } from '../models/PlaylistTrack';
import type { PublicProfile } from '../models/PublicProfile';
import type { PublicProfileModifiable } from '../models/PublicProfileModifiable';
import type { PublicProfileUsernames } from '../models/PublicProfileUsernames';
import type { RoleRequestAnswer } from '../models/RoleRequestAnswer';
import type { SearchAlbum } from '../models/SearchAlbum';
import type { SearchClip } from '../models/SearchClip';
import type { SearchMusician } from '../models/SearchMusician';
import type { SearchPlaylist } from '../models/SearchPlaylist';
import type { SearchTrack } from '../models/SearchTrack';
import type { Slide } from '../models/Slide';
import type { SupportMessageLogin } from '../models/SupportMessageLogin';
import type { SupportMessageStatus } from '../models/SupportMessageStatus';
import type { SupportMessageType } from '../models/SupportMessageType';
import type { Track } from '../models/Track';
import type { TrackAfterUpload } from '../models/TrackAfterUpload';
import type { TrackStats } from '../models/TrackStats';
import type { UpdateRoleRequestAnswer } from '../models/UpdateRoleRequestAnswer';
import type { UserAuth } from '../models/UserAuth';
import type { UserBase } from '../models/UserBase';
import type { UserInfo } from '../models/UserInfo';
import type { UserInfoWithPlaylists } from '../models/UserInfoWithPlaylists';
import type { UserRegister } from '../models/UserRegister';
import type { UsersStats } from '../models/UsersStats';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class Service {

    /**
     * Login
     * Авторизация пользователя
     * @param requestBody
     * @returns UserInfo Successful Response
     * @throws ApiError
     */
    public static loginApiV1AuthLoginPost(
        requestBody: UserAuth,
    ): CancelablePromise<UserInfo> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Logout
     * Выход из системы
     * @returns any Successful Response
     * @throws ApiError
     */
    public static logoutApiV1AuthLogoutDelete(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/auth/logout',
        });
    }

    /**
     * Refresh
     * Обновление токена
     * @returns void
     * @throws ApiError
     */
    public static refreshApiV1AuthRefreshPost(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/refresh',
        });
    }

    /**
     * Create User Signup
     * Создание пользователя без необходимости последующей авторизации
     * @param requestBody
     * @returns UserInfo Successful Response
     * @throws ApiError
     */
    public static createUserSignupApiV1AuthSignupPost(
        requestBody: UserRegister,
    ): CancelablePromise<UserInfo> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change Password
     * Изменение пароля пользователя
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static changePasswordApiV1AuthChangePasswordPut(
        requestBody: ChangePassword,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/auth/change-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Users Stats
     * Получение статистики по пользователям
     * @returns UsersStats Successful Response
     * @throws ApiError
     */
    public static getUsersStatsApiV1UsersStatsGet(): CancelablePromise<UsersStats> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/stats',
        });
    }

    /**
     * Get User Info
     * Получение данных пользователя
     * @returns UserInfo Successful Response
     * @throws ApiError
     */
    public static getUserInfoApiV1UsersMeGet(): CancelablePromise<UserInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/me',
            errors: {
                401: `Unauthorized`,
            },
        });
    }

    /**
     * Update User Data
     * Обновление данных пользователя
     * @param requestBody
     * @returns UserInfo Successful Response
     * @throws ApiError
     */
    public static updateUserDataApiV1UsersMePut(
        requestBody: UserBase,
    ): CancelablePromise<UserInfo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/users/me',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Check Username Exists
     * Проверка существования логина
     * @param username
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static checkUsernameExistsApiV1UsersUsernameExistsGet(
        username: string,
    ): CancelablePromise<boolean> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/username-exists',
            query: {
                'username': username,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Avatar
     * Обновление данных пользователя
     * @param formData
     * @returns UserInfo Successful Response
     * @throws ApiError
     */
    public static updateUserAvatarApiV1UsersMeAvatarPut(
        formData?: Body_update_user_avatar_api_v1_users_me_avatar_put,
    ): CancelablePromise<UserInfo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/users/me/avatar',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get User Info By Id
     * Получение данных пользователя по ID
     * @param userId ID пользователя
     * @returns UserInfoWithPlaylists Successful Response
     * @throws ApiError
     */
    public static getUserInfoByIdApiV1UsersUserIdGet(
        userId: number,
    ): CancelablePromise<UserInfoWithPlaylists> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get User Public Profile Info
     * Получение данных публичного профиля пользователя
     * @returns PublicProfileUsernames Successful Response
     * @throws ApiError
     */
    public static getUserPublicProfileInfoApiV1UsersMePublicGet(): CancelablePromise<PublicProfileUsernames> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/me/public',
            errors: {
                401: `Unauthorized`,
            },
        });
    }

    /**
     * Update User Public Profile Data
     * Обновление данных публичного профиля пользователя
     * @param requestBody
     * @returns PublicProfileUsernames Successful Response
     * @throws ApiError
     */
    public static updateUserPublicProfileDataApiV1UsersMePublicPut(
        requestBody: PublicProfileModifiable,
    ): CancelablePromise<PublicProfileUsernames> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/users/me/public',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                401: `Unauthorized`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Public Avatar
     * Обновление данных пользователя
     * @param formData
     * @returns PublicProfile Successful Response
     * @throws ApiError
     */
    public static updateUserPublicAvatarApiV1UsersMePublicAvatarPut(
        formData?: Body_update_user_public_avatar_api_v1_users_me_public_avatar_put,
    ): CancelablePromise<PublicProfile> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/users/me/public/avatar',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get User Playlists
     * Получение списка плейлистов
     * @param userId ID пользователя
     * @param page Номер страницы
     * @param orderBy Порядок сортировки
     * @param orderOrientation Направление сортировки
     * @returns PlaylistInfoWithoutTracks Successful Response
     * @throws ApiError
     */
    public static getUserPlaylistsApiV1UsersUserIdPlaylistsGet(
        userId: number,
        page: number = 1,
        orderBy?: order_playlist_by,
        orderOrientation?: Order,
    ): CancelablePromise<Array<PlaylistInfoWithoutTracks>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/{user_id}/playlists',
            path: {
                'user_id': userId,
            },
            query: {
                'page': page,
                'order_by': orderBy,
                'order_orientation': orderOrientation,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Change Requests
     * Получение списка запросов на смену типа аккаунта
     * @param page Номер страницы
     * @returns ChangeRoleRequestFullInfo Successful Response
     * @throws ApiError
     */
    public static getChangeRequestsApiV1RolesChangeGet(
        page: number = 1,
    ): CancelablePromise<Array<ChangeRoleRequestFullInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/roles/change',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Send Update Role Request
     * Отправка запроса на смену типа аккаунта
     * @param formData
     * @returns ChangeRoleRequestFullInfo Successful Response
     * @throws ApiError
     */
    public static sendUpdateRoleRequestApiV1RolesChangePost(
        formData: Body_send_update_role_request_api_v1_roles_change_post,
    ): CancelablePromise<ChangeRoleRequestFullInfo> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/roles/change',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Has Change Requests
     * Имеется ли запросы на смену типа аккаунта
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static hasChangeRequestsApiV1RolesChangeHasGet(): CancelablePromise<boolean> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/roles/change/has',
        });
    }

    /**
     * Get Current Change Request
     * Получение текущего запроса на смену типа аккаунта
     * @returns ChangeRoleRequestFullInfo Successful Response
     * @throws ApiError
     */
    public static getCurrentChangeRequestApiV1RolesChangeCurrentGet(): CancelablePromise<ChangeRoleRequestFullInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/roles/change/current',
        });
    }

    /**
     * Get All Change Role Requests
     * Получение списка запросов на смену типа аккаунта от всех пользователей
     * @param page Номер страницы
     * @param filter Фильтр по статусу
     * @returns ChangeRoleRequestFullInfo Successful Response
     * @throws ApiError
     */
    public static getAllChangeRoleRequestsApiV1RolesChangeAllGet(
        page: number = 1,
        filter?: ChangeRoleRequestStatus,
    ): CancelablePromise<Array<ChangeRoleRequestFullInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/roles/change/all',
            query: {
                'page': page,
                'filter': filter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Change Role Request
     * Получение запроса на смену типа аккаунта
     * @param requestId
     * @returns ChangeRoleRequestFullInfo Successful Response
     * @throws ApiError
     */
    public static getChangeRoleRequestApiV1RolesChangeRequestIdGet(
        requestId: number,
    ): CancelablePromise<ChangeRoleRequestFullInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/roles/change/{request_id}',
            path: {
                'request_id': requestId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Change Role Request
     * Удаление запроса на смену типа аккаунта
     * @param requestId
     * @returns void
     * @throws ApiError
     */
    public static deleteChangeRoleRequestApiV1RolesChangeRequestIdDelete(
        requestId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/roles/change/{request_id}',
            path: {
                'request_id': requestId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Send Update Role Request Answer
     * Ответ на запрос на смену типа аккаунта
     * @param requestId
     * @param requestBody
     * @returns RoleRequestAnswer Successful Response
     * @throws ApiError
     */
    public static sendUpdateRoleRequestAnswerApiV1RolesChangeRequestIdAnswerPost(
        requestId: number,
        requestBody: UpdateRoleRequestAnswer,
    ): CancelablePromise<RoleRequestAnswer> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/roles/change/{request_id}/answer',
            path: {
                'request_id': requestId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Image
     * Получение изображения по его id
     * @param imageId ID изображения
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getImageApiV1UploadsImagesImageIdGet(
        imageId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/uploads/images/{image_id}',
            path: {
                'image_id': imageId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get File
     * Получение файла по его id
     * @param fileId ID файла
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getFileApiV1UploadsOtherFileIdGet(
        fileId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/uploads/other/{file_id}',
            path: {
                'file_id': fileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Support Messages
     * @param type
     * @param page Номер страницы
     * @returns SupportMessageLogin Successful Response
     * @throws ApiError
     */
    public static getSupportMessagesApiV1SupportMessagesGet(
        type?: SupportMessageType,
        page: number = 1,
    ): CancelablePromise<Array<SupportMessageLogin>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/support/messages',
            query: {
                'type': type,
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Support Message
     * @param requestBody
     * @returns SupportMessageLogin Successful Response
     * @throws ApiError
     */
    public static createSupportMessageApiV1SupportMessagesPost(
        requestBody: CreateSupportMessage,
    ): CancelablePromise<SupportMessageLogin> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/support/messages',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Support Message
     * @param messageId ID сообщения
     * @returns SupportMessageLogin Successful Response
     * @throws ApiError
     */
    public static getSupportMessageApiV1SupportMessagesMessageIdGet(
        messageId: string,
    ): CancelablePromise<SupportMessageLogin> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/support/messages/{message_id}',
            path: {
                'message_id': messageId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Support Message
     * @param messageId ID сообщения
     * @param messageStatus Статус сообщения
     * @returns SupportMessageLogin Successful Response
     * @throws ApiError
     */
    public static updateSupportMessageApiV1SupportMessagesMessageIdPut(
        messageId: string,
        messageStatus: SupportMessageStatus,
    ): CancelablePromise<SupportMessageLogin> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/support/messages/{message_id}',
            path: {
                'message_id': messageId,
            },
            query: {
                'message_status': messageStatus,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Liked Musician Profiles
     * Получение списка любимых музыкантов
     * @param page Номер страницы
     * @returns PublicProfile Successful Response
     * @throws ApiError
     */
    public static getLikedMusicianProfilesApiV1MusicianLikedGet(
        page: number = 1,
    ): CancelablePromise<Array<PublicProfile>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/liked',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Random Musician Profiles
     * Получение списка случайных музыкантов
     * @returns PublicProfile Successful Response
     * @throws ApiError
     */
    public static getRandomMusicianProfilesApiV1MusicianRandomGet(): CancelablePromise<Array<PublicProfile>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/random',
        });
    }

    /**
     * Get Popular Musician Profiles
     * Получение списка популярных музыкантов
     * @param page Номер страницы
     * @returns MusicianInfo Successful Response
     * @throws ApiError
     */
    public static getPopularMusicianProfilesApiV1MusicianPopularGet(
        page: number = 1,
    ): CancelablePromise<Array<MusicianInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/popular',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Like Musician
     * Лайк музыканта
     * @param profileId ID профиля
     * @returns LikesInfo Successful Response
     * @throws ApiError
     */
    public static likeMusicianApiV1MusicianProfileIdLikePut(
        profileId: number,
    ): CancelablePromise<LikesInfo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/musician/{profile_id}/like',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Public Profile Info
     * Получение информации о публичном профиле музыканта
     * @param profileId ID профиля
     * @returns MusicianFullInfo Successful Response
     * @throws ApiError
     */
    public static getPublicProfileInfoApiV1MusicianProfileIdGet(
        profileId: number,
    ): CancelablePromise<MusicianFullInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/{profile_id}',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Public Profile
     * Получение публичного профиля музыканта
     * @param profileId ID профиля
     * @returns PublicProfile Successful Response
     * @throws ApiError
     */
    public static getPublicProfileApiV1MusicianProfileIdInfoGet(
        profileId: number,
    ): CancelablePromise<PublicProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/{profile_id}/info',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Musician Clips
     * Получение клипов музыканта
     * @param profileId ID музыканта
     * @param page Страница
     * @returns MusicianClip Successful Response
     * @throws ApiError
     */
    public static getMusicianClipsApiV1MusicianProfileIdClipsGet(
        profileId: number,
        page: number = 1,
    ): CancelablePromise<Array<MusicianClip>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/{profile_id}/clips',
            path: {
                'profile_id': profileId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Musician Albums
     * Получение альбомов музыканта
     * @param profileId ID музыканта
     * @param page Страница
     * @returns AlbumInfo Successful Response
     * @throws ApiError
     */
    public static getMusicianAlbumsApiV1MusicianProfileIdAlbumsGet(
        profileId: number,
        page: number = 1,
    ): CancelablePromise<Array<AlbumInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/{profile_id}/albums',
            path: {
                'profile_id': profileId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Musician Popular Tracks
     * Получение популярных треков музыканта
     * @param profileId ID музыканта
     * @param page Страница
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static getMusicianPopularTracksApiV1MusicianProfileIdPopularGet(
        profileId: number,
        page: number = 1,
    ): CancelablePromise<Array<Track>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/{profile_id}/popular',
            path: {
                'profile_id': profileId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Musician Popular Tracks
     * Поиск популярных треков музыканта
     * @param profileId ID музыканта
     * @param search Поисковый запрос
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static searchMusicianPopularTracksApiV1MusicianProfileIdPopularSearchGet(
        profileId: number,
        search: string,
    ): CancelablePromise<Array<Track>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/musician/{profile_id}/popular/search',
            path: {
                'profile_id': profileId,
            },
            query: {
                'search': search,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Album
     * Создание альбома
     * @param formData
     * @returns AlbumAfterUpload Successful Response
     * @throws ApiError
     */
    public static createAlbumApiV1AlbumsPost(
        formData: Body_create_album_api_v1_albums_post,
    ): CancelablePromise<AlbumAfterUpload> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/albums',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                401: `Unauthorized`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Close Album Uploading
     * Закрытие альбома для загрузки треков
     * @param albumId ID альбома
     * @returns void
     * @throws ApiError
     */
    public static closeAlbumUploadingApiV1AlbumsAlbumIdCloseUploadingPut(
        albumId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/albums/{album_id}/close-uploading',
            path: {
                'album_id': albumId,
            },
            errors: {
                401: `Unauthorized`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Album By Id
     * Получение альбома по id
     * @param albumId ID альбома
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAlbumByIdApiV1AlbumsAlbumIdGet(
        albumId: number,
    ): CancelablePromise<(AlbumWithTracks | AlbumWithTracksUploaded)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/albums/{album_id}',
            path: {
                'album_id': albumId,
            },
            errors: {
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Album
     * Обновление альбома
     * @param albumId ID альбома
     * @param formData
     * @returns AlbumInfoUploaded Successful Response
     * @throws ApiError
     */
    public static updateAlbumApiV1AlbumsAlbumIdPut(
        albumId: number,
        formData: Body_update_album_api_v1_albums__album_id__put,
    ): CancelablePromise<AlbumInfoUploaded> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/albums/{album_id}',
            path: {
                'album_id': albumId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                401: `Unauthorized`,
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Album By Id
     * Удаление альбома по id
     * @param albumId ID альбома
     * @returns void
     * @throws ApiError
     */
    public static deleteAlbumByIdApiV1AlbumsAlbumIdDelete(
        albumId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/albums/{album_id}',
            path: {
                'album_id': albumId,
            },
            errors: {
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Album Tracks Order
     * Обновление порядка треков в альбоме
     * @param albumId ID альбома
     * @param tracksIds ID треков в новом порядке
     * @returns AlbumWithTracks Successful Response
     * @throws ApiError
     */
    public static updateAlbumTracksOrderApiV1AlbumsAlbumIdTracksOrderPut(
        albumId: number,
        tracksIds: Array<number>,
    ): CancelablePromise<AlbumWithTracks> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/albums/{album_id}/tracks-order',
            path: {
                'album_id': albumId,
            },
            query: {
                'tracks_ids': tracksIds,
            },
            errors: {
                401: `Unauthorized`,
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Albums
     * Получение альбомов музыканта
     * @param page Номер страницы
     * @returns AlbumInfo Successful Response
     * @throws ApiError
     */
    public static getMyAlbumsApiV1AlbumsMyGet(
        page: number = 1,
    ): CancelablePromise<Array<AlbumInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/albums/my',
            query: {
                'page': page,
            },
            errors: {
                401: `Unauthorized`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search My Albums
     * Поиск альбомов музыканта
     * @param text Строка поиска
     * @returns AlbumInfoWithoutMusician Successful Response
     * @throws ApiError
     */
    public static searchMyAlbumsApiV1AlbumsMySearchGet(
        text: string,
    ): CancelablePromise<Array<AlbumInfoWithoutMusician>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/albums/my/search',
            query: {
                'text': text,
            },
            errors: {
                401: `Unauthorized`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Album Like
     * Лайнуть альбом
     * @param albumId ID альбома
     * @returns LikesInfo Successful Response
     * @throws ApiError
     */
    public static albumLikeApiV1AlbumsAlbumIdLikePut(
        albumId: number,
    ): CancelablePromise<LikesInfo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/albums/{album_id}/like',
            path: {
                'album_id': albumId,
            },
            errors: {
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Liked Albums
     * Получение лайкнутых альбомов
     * @param orderBy Сортировка
     * @param order Порядок сортировки
     * @param page Номер страницы
     * @returns AlbumInfo Successful Response
     * @throws ApiError
     */
    public static getLikedAlbumsApiV1AlbumsLikedGet(
        orderBy?: OrderAlbums,
        order?: Order,
        page: number = 1,
    ): CancelablePromise<Array<AlbumInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/albums/liked',
            query: {
                'order_by': orderBy,
                'order': order,
                'page': page,
            },
            errors: {
                401: `Unauthorized`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Last Albums
     * Получение последних альбомов
     * @param page Номер страницы
     * @param pageSize Размер страницы
     * @returns AlbumInfo Successful Response
     * @throws ApiError
     */
    public static getLastAlbumsApiV1AlbumsLastGet(
        page: number = 1,
        pageSize: number = 100,
    ): CancelablePromise<Array<AlbumInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/albums/last',
            query: {
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Album Info By Id
     * Получение информации об альбоме по id
     * @param albumId ID альбома
     * @returns AlbumInfoUploaded Successful Response
     * @throws ApiError
     */
    public static getAlbumInfoByIdApiV1AlbumsAlbumIdInfoGet(
        albumId: number,
    ): CancelablePromise<AlbumInfoUploaded> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/albums/{album_id}/info',
            path: {
                'album_id': albumId,
            },
            errors: {
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Upload Track
     * Создание трека
     * @param albumId ID альбома
     * @param formData
     * @returns TrackAfterUpload Successful Response
     * @throws ApiError
     */
    public static uploadTrackApiV1AlbumsAlbumIdTrackPost(
        albumId: number,
        formData: Body_upload_track_api_v1_albums__album_id__track_post,
    ): CancelablePromise<TrackAfterUpload> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/albums/{album_id}/track',
            path: {
                'album_id': albumId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                401: `Unauthorized`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Playlists
     * Получение списка плейлистов
     * @param page Номер страницы
     * @param orderBy Порядок сортировки
     * @param orderOrientation Направление сортировки
     * @param ownedOnly Показывать только мои плейлисты
     * @param _private Показывать только приватные плейлисты
     * @returns PlaylistInfoWithoutTracks Successful Response
     * @throws ApiError
     */
    public static getMyPlaylistsApiV1PlaylistsGet(
        page: number = 1,
        orderBy?: order_playlist_by,
        orderOrientation?: Order,
        ownedOnly: boolean = false,
        _private: boolean = false,
    ): CancelablePromise<Array<PlaylistInfoWithoutTracks>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/playlists',
            query: {
                'page': page,
                'order_by': orderBy,
                'order_orientation': orderOrientation,
                'owned_only': ownedOnly,
                'private': _private,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Playlist
     * Создание плейлиста
     * @param requestBody
     * @returns PlaylistInfoWithoutTracks Successful Response
     * @throws ApiError
     */
    public static createPlaylistApiV1PlaylistsPost(
        requestBody: PlaylistCreate,
    ): CancelablePromise<PlaylistInfoWithoutTracks> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/playlists',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Playlist Info
     * Получение информации о плейлисте
     * @param playlistId ID плейлиста
     * @returns PlaylistInfo Successful Response
     * @throws ApiError
     */
    public static getPlaylistInfoApiV1PlaylistsPlaylistIdGet(
        playlistId: string,
    ): CancelablePromise<PlaylistInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/playlists/{playlist_id}',
            path: {
                'playlist_id': playlistId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Playlist
     * Обновление плейлиста
     * @param playlistId ID плейлиста
     * @param requestBody
     * @returns PlaylistInfo Successful Response
     * @throws ApiError
     */
    public static updatePlaylistApiV1PlaylistsPlaylistIdPut(
        playlistId: string,
        requestBody: PlaylistBase,
    ): CancelablePromise<PlaylistInfo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/playlists/{playlist_id}',
            path: {
                'playlist_id': playlistId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Playlist
     * Удаление плейлиста
     * @param playlistId ID плейлиста
     * @returns void
     * @throws ApiError
     */
    public static deletePlaylistApiV1PlaylistsPlaylistIdDelete(
        playlistId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/playlists/{playlist_id}',
            path: {
                'playlist_id': playlistId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Track To Playlist
     * Добавление трека в плейлист
     * @param trackId ID трека
     * @param playlistId ID плейлиста
     * @returns PlaylistTrack Successful Response
     * @throws ApiError
     */
    public static addTrackToPlaylistApiV1PlaylistsPlaylistIdTrackTrackIdPost(
        trackId: string,
        playlistId: string,
    ): CancelablePromise<PlaylistTrack> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/playlists/{playlist_id}/track/{track_id}',
            path: {
                'track_id': trackId,
                'playlist_id': playlistId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Track From Playlist
     * Удаление трека из плейлиста
     * @param trackId ID трека
     * @param playlistId ID плейлиста
     * @returns void
     * @throws ApiError
     */
    public static deleteTrackFromPlaylistApiV1PlaylistsPlaylistIdTrackTrackIdDelete(
        trackId: string,
        playlistId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/playlists/{playlist_id}/track/{track_id}',
            path: {
                'track_id': trackId,
                'playlist_id': playlistId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Like Playlist
     * Лайк плейлиста
     * @param playlistId ID плейлиста
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static likePlaylistApiV1PlaylistsPlaylistIdLikePut(
        playlistId: string,
    ): CancelablePromise<boolean> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/playlists/{playlist_id}/like',
            path: {
                'playlist_id': playlistId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Clip
     * Создание клипа
     * @param formData
     * @returns MusicianClip Successful Response
     * @throws ApiError
     */
    public static createClipApiV1ClipsPost(
        formData: Body_create_clip_api_v1_clips_post,
    ): CancelablePromise<MusicianClip> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/clips',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Clip By Id
     * Получение клипа
     * @param clipId ID клипа
     * @returns MusicianClip Successful Response
     * @throws ApiError
     */
    public static getClipByIdApiV1ClipsClipIdGet(
        clipId: number,
    ): CancelablePromise<MusicianClip> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/clips/{clip_id}',
            path: {
                'clip_id': clipId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Clip
     * Изменение клипа
     * @param clipId ID клипа
     * @param formData
     * @returns MusicianClip Successful Response
     * @throws ApiError
     */
    public static updateClipApiV1ClipsClipIdPut(
        clipId: number,
        formData: Body_update_clip_api_v1_clips__clip_id__put,
    ): CancelablePromise<MusicianClip> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/clips/{clip_id}',
            path: {
                'clip_id': clipId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Clip
     * Удаление клипа
     * @param clipId ID клипа
     * @returns void
     * @throws ApiError
     */
    public static deleteClipApiV1ClipsClipIdDelete(
        clipId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/clips/{clip_id}',
            path: {
                'clip_id': clipId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Clips
     * Получение моих клипов
     * @param page Страница
     * @returns MusicianClip Successful Response
     * @throws ApiError
     */
    public static getMyClipsApiV1ClipsMyGet(
        page: number = 1,
    ): CancelablePromise<Array<MusicianClip>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/clips/my',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search My Clips
     * Поиск моих клипов
     * @param search Строка поиска
     * @returns MusicianClip Successful Response
     * @throws ApiError
     */
    public static searchMyClipsApiV1ClipsMySearchGet(
        search: string,
    ): CancelablePromise<Array<MusicianClip>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/clips/my/search',
            query: {
                'search': search,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Genres
     * Получение  жанров отсортированных по популярности
     * @param page
     * @param filter
     * @returns Genre Successful Response
     * @throws ApiError
     */
    public static getGenresApiV1GenresGet(
        page: number = 1,
        filter?: FilterGenreEnum,
    ): CancelablePromise<Array<Genre>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres',
            query: {
                'page': page,
                'filter': filter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Genre
     * Создание жанра
     * @param formData
     * @returns GenreStats Successful Response
     * @throws ApiError
     */
    public static createGenreApiV1GenresPost(
        formData: Body_create_genre_api_v1_genres_post,
    ): CancelablePromise<GenreStats> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/genres',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                403: `Forbidden`,
                409: `Conflict`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Random Genres
     * Получение случайных жанров
     * @returns Genre Successful Response
     * @throws ApiError
     */
    public static getRandomGenresApiV1GenresRandomGet(): CancelablePromise<Array<Genre>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/random',
        });
    }

    /**
     * Like Genre
     * Лайк жанра
     * @param genreId ID жанра
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static likeGenreApiV1GenresGenreIdLikePut(
        genreId: number,
    ): CancelablePromise<boolean> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/genres/{genre_id}/like',
            path: {
                'genre_id': genreId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Genre
     * Получение информации о жанре
     * @param genreId ID жанра
     * @returns GenreFullInfo Successful Response
     * @throws ApiError
     */
    public static getGenreApiV1GenresGenreIdGet(
        genreId: number,
    ): CancelablePromise<GenreFullInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}',
            path: {
                'genre_id': genreId,
            },
            errors: {
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Genre
     * Обновление жанра
     * @param genreId ID жанра
     * @param formData
     * @returns GenreStats Successful Response
     * @throws ApiError
     */
    public static updateGenreApiV1GenresGenreIdPut(
        genreId: number,
        formData: Body_update_genre_api_v1_genres__genre_id__put,
    ): CancelablePromise<GenreStats> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/genres/{genre_id}',
            path: {
                'genre_id': genreId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Genre
     * Удаление жанра
     * @param genreId ID жанра
     * @returns void
     * @throws ApiError
     */
    public static deleteGenreApiV1GenresGenreIdDelete(
        genreId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/genres/{genre_id}',
            path: {
                'genre_id': genreId,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Genre Info
     * Получение информации о жанре
     * @param genreId ID жанра
     * @returns Genre Successful Response
     * @throws ApiError
     */
    public static getGenreInfoApiV1GenresGenreIdInfoGet(
        genreId: number,
    ): CancelablePromise<Genre> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}/info',
            path: {
                'genre_id': genreId,
            },
            errors: {
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Popular Albums By Genre Id
     * Получение популярных альбомов по жанру
     * @param genreId ID жанра
     * @param page
     * @returns AlbumInfo Successful Response
     * @throws ApiError
     */
    public static getPopularAlbumsByGenreIdApiV1GenresGenreIdAlbumsGet(
        genreId: number,
        page: number = 1,
    ): CancelablePromise<Array<AlbumInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}/albums',
            path: {
                'genre_id': genreId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get New Albums By Genre Id
     * Получение новых альбомов по жанру
     * @param genreId ID жанра
     * @param page
     * @returns AlbumInfo Successful Response
     * @throws ApiError
     */
    public static getNewAlbumsByGenreIdApiV1GenresGenreIdAlbumsNewGet(
        genreId: number,
        page: number = 1,
    ): CancelablePromise<Array<AlbumInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}/albums/new',
            path: {
                'genre_id': genreId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Popular Tracks By Genre Id
     * Получение популярных треков по жанру
     * @param genreId ID жанра
     * @param page
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static getPopularTracksByGenreIdApiV1GenresGenreIdTracksGet(
        genreId: number,
        page: number = 1,
    ): CancelablePromise<Array<Track>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}/tracks',
            path: {
                'genre_id': genreId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Popular Musicians By Genre Id
     * Получение популярных музыкантов по жанру
     * @param genreId ID жанра
     * @param page
     * @returns MusicianInfo Successful Response
     * @throws ApiError
     */
    public static getPopularMusiciansByGenreIdApiV1GenresGenreIdMusiciansGet(
        genreId: number,
        page: number = 1,
    ): CancelablePromise<Array<MusicianInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}/musicians',
            path: {
                'genre_id': genreId,
            },
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Genre Info
     * Получение статистики по жанру
     * @param genreId
     * @returns GenreStats Successful Response
     * @throws ApiError
     */
    public static getGenreInfoApiV1GenresGenreIdStatsGet(
        genreId: number,
    ): CancelablePromise<GenreStats> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/genres/{genre_id}/stats',
            path: {
                'genre_id': genreId,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Like Track
     * Лайк трека
     * @param trackId ID трека
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static likeTrackApiV1TracksTrackIdLikePut(
        trackId: string,
    ): CancelablePromise<boolean> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/tracks/{track_id}/like',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Liked Tracks
     * Получение лайкнутых треков
     * @param page Номер страницы
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static getLikedTracksApiV1TracksLikedGet(
        page: number = 1,
    ): CancelablePromise<Array<Track>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/liked',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Popular Tracks
     * Получение популярных треков
     * @param page Номер страницы
     * @param pageSize Размер страницы
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static getPopularTracksApiV1TracksPopularGet(
        page: number = 1,
        pageSize: number = 20,
    ): CancelablePromise<Array<Track>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/popular',
            query: {
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Popular Tracks Period
     * Получение популярных треков за месяц
     * @param startDate Дата начала периода
     * @param endDate Дата конца периода
     * @param pageSize Размер страницы
     * @param page Номер страницы
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static getPopularTracksPeriodApiV1TracksPopularPeriodGet(
        startDate: string,
        endDate: string,
        pageSize: number = 20,
        page: number = 1,
    ): CancelablePromise<Array<Track>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/popular/period',
            query: {
                'page_size': pageSize,
                'page': page,
                'start_date': startDate,
                'end_date': endDate,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Track
     * Получение трека
     * @param trackId ID трека
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static getTrackApiV1TracksTrackIdGet(
        trackId: string,
    ): CancelablePromise<Track> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/{track_id}',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Track By Id
     * Обновление трека
     * @param trackId ID трека
     * @param formData
     * @returns Track Successful Response
     * @throws ApiError
     */
    public static updateTrackByIdApiV1TracksTrackIdPut(
        trackId: string,
        formData: Body_update_track_by_id_api_v1_tracks__track_id__put,
    ): CancelablePromise<Track> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/tracks/{track_id}',
            path: {
                'track_id': trackId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Track
     * Удаление трека
     * @param trackId ID трека
     * @returns void
     * @throws ApiError
     */
    public static deleteTrackApiV1TracksTrackIdDelete(
        trackId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/tracks/{track_id}',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Track Playlists
     * Получение ваших плейлистов, в которых есть трек
     * @param trackId ID трека
     * @returns PlaylistInfoWithoutTracks Successful Response
     * @throws ApiError
     */
    public static getTrackPlaylistsApiV1TracksTrackIdPlaylistsMyGet(
        trackId: string,
    ): CancelablePromise<Array<PlaylistInfoWithoutTracks>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/{track_id}/playlists/my',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Track Statistics
     * Получение статистики по треку
     * @param trackId ID трека
     * @returns TrackStats Successful Response
     * @throws ApiError
     */
    public static getTrackStatisticsApiV1TracksTrackIdStatsGet(
        trackId: string,
    ): CancelablePromise<TrackStats> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/{track_id}/stats',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Set Listened Track
     * Установка прослушанного трека
     * @param trackId ID трека
     * @returns void
     * @throws ApiError
     */
    public static setListenedTrackApiV1TracksTrackIdListeningPut(
        trackId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/tracks/{track_id}/listening',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Start Listening Track
     * Начало прослушивания трека
     * @param trackId ID трека
     * @returns void
     * @throws ApiError
     */
    public static startListeningTrackApiV1TracksTrackIdListeningPost(
        trackId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/tracks/{track_id}/listening',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Track File
     * Получение трека по его id
     * @param trackId ID трека
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getTrackFileApiV1TracksTrackIdFileGet(
        trackId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tracks/{track_id}/file',
            path: {
                'track_id': trackId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search
     * Поиск по всему
     * @param text Поисковый запрос
     * @returns AllSearchItem Successful Response
     * @throws ApiError
     */
    public static searchApiV1SearchAutocompleteGet(
        text: string,
    ): CancelablePromise<Array<AllSearchItem>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/autocomplete',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Musician
     * Поиск по музыкантам
     * @param text Поисковый запрос
     * @returns SearchMusician Successful Response
     * @throws ApiError
     */
    public static searchMusicianApiV1SearchMusicianGet(
        text: string,
    ): CancelablePromise<Array<SearchMusician>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/musician',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Album
     * Поиск по альбомам
     * @param text Поисковый запрос
     * @returns SearchAlbum Successful Response
     * @throws ApiError
     */
    public static searchAlbumApiV1SearchAlbumGet(
        text: string,
    ): CancelablePromise<Array<SearchAlbum>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/album',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Track
     * Поиск по трекам
     * @param text Поисковый запрос
     * @returns SearchTrack Successful Response
     * @throws ApiError
     */
    public static searchTrackApiV1SearchTrackGet(
        text: string,
    ): CancelablePromise<Array<SearchTrack>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/track',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Clip
     * Поиск по клипам
     * @param text Поисковый запрос
     * @returns SearchClip Successful Response
     * @throws ApiError
     */
    public static searchClipApiV1SearchClipGet(
        text: string,
    ): CancelablePromise<Array<SearchClip>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/clip',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Playlist
     * Поиск по плейлистам
     * @param text Поисковый запрос
     * @returns SearchPlaylist Successful Response
     * @throws ApiError
     */
    public static searchPlaylistApiV1SearchPlaylistGet(
        text: string,
    ): CancelablePromise<Array<SearchPlaylist>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/playlist',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Genres
     * Поиск по жанрам
     * @param text Поисковый запрос
     * @returns Genre Successful Response
     * @throws ApiError
     */
    public static getGenresApiV1SearchGenresGet(
        text: string,
    ): CancelablePromise<Array<Genre>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/search/genres',
            query: {
                'text': text,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Slides
     * Получение всех слайдов
     * @returns Slide Successful Response
     * @throws ApiError
     */
    public static getSlidesApiV1SliderGet(): CancelablePromise<Array<Slide>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/slider',
        });
    }

    /**
     * Create Slide
     * Создание слайда
     * @param formData
     * @returns Slide Successful Response
     * @throws ApiError
     */
    public static createSlideApiV1SliderPost(
        formData: Body_create_slide_api_v1_slider_post,
    ): CancelablePromise<Slide> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/slider',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get All Slides
     * Получение всех слайдов
     * @param page
     * @returns Slide Successful Response
     * @throws ApiError
     */
    public static getAllSlidesApiV1SliderAllGet(
        page: number = 1,
    ): CancelablePromise<Array<Slide>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/slider/all',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Slide By Id
     * Получение слайда по id
     * @param slideId
     * @returns Slide Successful Response
     * @throws ApiError
     */
    public static getSlideByIdApiV1SliderSlideIdGet(
        slideId: string,
    ): CancelablePromise<Slide> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/slider/{slide_id}',
            path: {
                'slide_id': slideId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Slide
     * Обновление слайда
     * @param slideId
     * @param formData
     * @returns Slide Successful Response
     * @throws ApiError
     */
    public static updateSlideApiV1SliderSlideIdPut(
        slideId: string,
        formData: Body_update_slide_api_v1_slider__slide_id__put,
    ): CancelablePromise<Slide> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/slider/{slide_id}',
            path: {
                'slide_id': slideId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Slide
     * Удаление слайда
     * @param slideId
     * @returns void
     * @throws ApiError
     */
    public static deleteSlideApiV1SliderSlideIdDelete(
        slideId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/slider/{slide_id}',
            path: {
                'slide_id': slideId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get History
     * Получение последних прослушанных плейлистов, альбомов и музыкантов
     * @returns HistoryItem Successful Response
     * @throws ApiError
     */
    public static getHistoryApiV1HistoryGet(): CancelablePromise<Array<HistoryItem>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/history',
        });
    }

    /**
     * Get History Tracks
     * Получение треков из истории
     * @param page
     * @returns HistoryTrack Successful Response
     * @throws ApiError
     */
    public static getHistoryTracksApiV1HistoryTracksGet(
        page: number = 1,
    ): CancelablePromise<Array<HistoryTrack>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/history/tracks',
            query: {
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Playlist To History
     * Добавление плейлиста в историю
     * @param playlistId ID плейлиста
     * @returns HistoryPlaylist Successful Response
     * @throws ApiError
     */
    public static addPlaylistToHistoryApiV1HistoryPlaylistsPlaylistIdPost(
        playlistId: string,
    ): CancelablePromise<HistoryPlaylist> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/history/playlists/{playlist_id}',
            path: {
                'playlist_id': playlistId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Album To History
     * Добавление альбома в историю
     * @param albumId ID альбома
     * @returns HistoryAlbum Successful Response
     * @throws ApiError
     */
    public static addAlbumToHistoryApiV1HistoryAlbumsAlbumIdPost(
        albumId: string,
    ): CancelablePromise<HistoryAlbum> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/history/albums/{album_id}',
            path: {
                'album_id': albumId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Musician To History
     * Добавление музыканта в историю
     * @param musicianId ID музыканта
     * @returns HistoryMusician Successful Response
     * @throws ApiError
     */
    public static addMusicianToHistoryApiV1HistoryMusiciansMusicianIdPost(
        musicianId: string,
    ): CancelablePromise<HistoryMusician> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/history/musicians/{musician_id}',
            path: {
                'musician_id': musicianId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Track From History
     * Удаление трека из истории
     * @param historyItemId ID элемента истории
     * @returns void
     * @throws ApiError
     */
    public static deleteTrackFromHistoryApiV1HistoryTracksHistoryItemIdDelete(
        historyItemId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/history/tracks/{history_item_id}',
            path: {
                'history_item_id': historyItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
