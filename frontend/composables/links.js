const useMusicianLink = (musicanInfo, track) => {
    var musician_id =
        track?.musician?.id ||
        musicanInfo?.id ||
        track?.album?.musician?.id ||
        null;
    if (!musician_id) return null;
    return {
        name: "musician-id",
        params: { id: musician_id },
    };
};
const useAlbumLink = (albumInfo, track) => {
    var album_id = track?.album?.id || albumInfo?.id;
    if (!album_id) return null;
    return {
        name: "album-id",
        params: { id: album_id },
    };
};
export { useAlbumLink, useMusicianLink };
