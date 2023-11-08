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

                // comment.id and comment.user from data- attribute in comments.html 'reply' link
                let commentId = link.getAttribute("data-comment-id");
                let commentUser = link.getAttribute("data-comment-user");

                // Hide commentForm and display replyForm instead
                const replyFormDiv = document.getElementById("reply-form");
                const commentFormDiv = document.getElementById("comment-form");
                commentFormDiv.classList.add("d-none");
                replyFormDiv.classList.remove("d-none");
                
                // Set innerHTML 'replying to {commentUser}'
                const replyingTo = document.getElementById("js-injection-replying-to");
                replyingTo.innerHTML = `replying to ${commentUser}`;
                
                // Set reply form action URL
                const replyForm = document.getElementById("js-injection-reply-form");
                let url = `/season/${seasonSlug}/${commentId}/reply`;
                replyForm.action = url;

                // Close button - close replyForm and display the default commentForm again
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