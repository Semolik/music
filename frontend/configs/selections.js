import { IconsNames } from "./icons";
const { playlistIcon, albumIcon, trackIcon, userIcon, historyIcon } =
    IconsNames;
const menuSelections = [
    {
        name: "Библиотека",
        links: [
            {
                icon: trackIcon,
                to: { name: "library-tracks" },
                text: "Треки",
            },
            {
                icon: albumIcon,
                to: { name: "library-albums" },
                text: "Альбомы",
            },
            {
                icon: userIcon,
                to: { name: "library-artists" },
                text: "Исполнители",
            },
            {
                icon: playlistIcon,
                to: { name: "library-playlists" },
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
