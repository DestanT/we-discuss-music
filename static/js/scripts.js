window.onSpotifyIframeApiReady = (IFrameAPI) => {
    const element = document.getElementById('embed-iframe');
    // Get parent div of 'element' - for d-none toggle
    const parent = element.parentElement;

    const options = {
        width: '100%',
    };

    const callback = (EmbedController) => {
        document.querySelectorAll('.spotify-iframe').forEach(
            playlist => {
                playlist.addEventListener('click', () => {
                    parent.classList.remove('d-none');
                    EmbedController.loadUri(playlist.dataset.spotifyId)
                });
            })
    };
    IFrameAPI.createController(element, options, callback);
};  