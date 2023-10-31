window.onSpotifyIframeApiReady = (IFrameAPI) => {
    const element = document.getElementById('embed-iframe');
    const options = {
        width: '100%',
    };
    const callback = (EmbedController) => {
        document.querySelectorAll('.spotify-iframe').forEach(
            playlist => {
                playlist.addEventListener('click', () => {
                    EmbedController.loadUri(playlist.dataset.spotifyId)
                });
            })
    };
    IFrameAPI.createController(element, options, callback);
};  