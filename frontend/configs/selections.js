import { IconsNames } from "./icons";
const { playlistIcon, albumIcon, trackIcon, userIcon, historyIcon } =
    IconsNames;
const menuSelections = [
    {
        name: "Библиотека",
        links: [
            {
                icon: trackIcon,
                to: { name: "favorite-tracks" },
                text: "Треки",
            },
            {
                icon: albumIcon,
                to: { name: "favorite-albums" },
                text: "Альбомы",
            },
            {
                icon: userIcon,
                to: { name: "favorite-artists" },
                text: "Исполнители",
            },
            {
                icon: playlistIcon,
                to: { name: "favorite-playlists" },
                text: "Плейлисты",
            },
            {
                icon: historyIcon,
                to: { name: "history" },
                text: "История",
            },
        ],
    },
];
export { menuSelections };
