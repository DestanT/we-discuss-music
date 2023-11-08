// Spotiy iFrame Embed
window.onSpotifyIframeApiReady = (IFrameAPI) => {
    const element = document.getElementById('embed-iframe');

    if (element) {
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
        }
};


document.addEventListener("DOMContentLoaded", function (e) {
    
    /**
     * If reply-links exist and the user clicks on it:
     * will hide the 'comment form' section and inject custom inner HTML in its place for replies.
     * URL path is set based on the comment being replied to and season post user is in.
    */
    const replyLinks = document.querySelectorAll(".reply-link");
    if (replyLinks) {

        replyLinks.forEach(function (link) {
            link.addEventListener("click", function (e) {

                // Season slug from current URL in window
                const pathArray = window.location.pathname.split("/");
                const seasonSlug = pathArray[pathArray.length - 2];

                // comment.id and comment.user from data- attribute
                let commentId = link.getAttribute("data-comment-id");
                let commentUser = link.getAttribute("data-comment-user");

                // Set URL accordingly
                let url = `/season/${seasonSlug}/${commentId}/reply`;

                // Hide commentForm and display replyForm instead
                const replyFormDiv = document.getElementById("reply-form");
                const commentFormDiv = document.getElementById("comment-form");
                commentFormDiv.classList.add("d-none");
                replyFormDiv.classList.remove("d-none");

                // Custom innerHTML for replyForm
                replyFormDiv.innerHTML = `
                <div class="row">
                    <div class="col">
                        replying to ${commentUser}
                    </div>
                    <div class="col-auto">
                        <button type="button" class="btn btn-sm btn-close" id="close-reply-form" aria-label="Close"></button>
                    </div>
                </div>
                <div class="d-flex">
                    <div class="flex-shrink-0 mt-2">
                        <img class="rounded-circle" src="https://dummyimage.com/50x50/ced4da/6c757d.jpg" alt="...">
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <form method="post" action="${url}" class="mt-3">
                            {% csrf_token %}
                            <div class="row d-flex g-0">
                                <div class="col">
                                    {{ reply_form | crispy }}
                                </div>
                                <div class="col-auto">
                                    <button type="submit" class="btn btn-outline-success">Reply</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                `;

                // Close replyForm and display the default commentForm again
                const closeReplyFormButton = document.getElementById("close-reply-form");
                closeReplyFormButton.addEventListener("click", function (e) {
                    replyFormDiv.classList.add("d-none");
                    commentFormDiv.classList.remove("d-none");
                });
            });
        });
    }

    // Event listeners for editing comments
    const editCommentButtons = document.querySelectorAll(".edit-comment")
    if (editCommentButtons) {

        editCommentButtons.forEach(function (button) {
            button.addEventListener("click", function (e) {
                
                // comment.id from data- attribute
                let commentId = button.getAttribute("data-comment-id");
                let commentDiv = document.getElementById(`comment${commentId}`)
                let editCommentDiv = document.getElementById(`edit-comment${commentId}`);
                
                // Hide the comment itself and replace with the update form
                commentDiv.classList.add("d-none");
                editCommentDiv.classList.remove("d-none");
            });
        });
    }
});