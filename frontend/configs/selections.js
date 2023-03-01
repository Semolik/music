import { routesNames } from "@typed-router";
import { IconsNames } from "./icons";
const { playlistIcon, albumIcon, trackIcon, musicianIcon, historyIcon } =
    IconsNames;
const menuSelections = [
    {
        name: null,
        links: [
            {
                icon: historyIcon,
                to: { name: routesNames.history },
                text: "История",
            },
        ],
    },
    {
        name: "Библиотека",
        links: [
            {
                icon: trackIcon,
                to: { name: routesNames.favoriteTracks },
                text: "Треки",
            },
            {
                icon: albumIcon,
                to: { name: routesNames.favoriteAlbums },
                text: "Альбомы",
            },
            {
                icon: musicianIcon,
                to: { name: routesNames.favoriteArtists },
                text: "Исполнители",
            },
            {
                icon: playlistIcon,
                to: { name: routesNames.favoritePlaylists },
                text: "Плейлисты",
            },
        ],
    },
];
export { menuSelections };
