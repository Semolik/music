/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ImageLink } from './ImageLink';

export type Slide = {
    name: string;
    is_active: boolean;
    active_from: string;
    active_to?: string;
    order?: number;
    url?: string;
    id: string;
    picture: ImageLink;
};

