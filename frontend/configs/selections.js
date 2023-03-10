import { routesNames } from "@typed-router";
import { IconsNames } from "./icons";
const { playlistIcon, albumIcon, trackIcon, userIcon, historyIcon } =
    IconsNames;
const menuSelections = [
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
                icon: userIcon,
                to: { name: routesNames.favoriteArtists },
                text: "Исполнители",
            },
            {
                icon: playlistIcon,
                to: { name: routesNames.favoritePlaylists },
                text: "Плейлисты",
            },
            {
                icon: historyIcon,
                to: { name: routesNames.history },
                text: "История",
            },
        ],
    },
];
export { menuSelections };
