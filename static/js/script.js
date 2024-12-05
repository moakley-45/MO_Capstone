document.addEventListener('DOMContentLoaded', function() {
    /** Declare and initialize variables inside DOMContentLoaded */
    const recipeSlug = "{{ recipe.slug }}"; // Make sure this is included in your template
    const editReviewButtons = document.getElementsByClassName("btn-edit-review");
    const deleteReviewButtons = document.getElementsByClassName("btn-delete-review");
    const editReviewForm = document.getElementById("editReviewForm");
    const deleteReviewConfirm = document.getElementById("deleteReviewConfirm");
    const editReviewModalElement = document.getElementById("editReviewModal");
    const deleteReviewModalElement = document.getElementById("deleteReviewModal");

    // Initialize Bootstrap modals only if elements exist
    const editReviewModal = editReviewModalElement ? new bootstrap.Modal(editReviewModalElement) : null;

    /** Check if editReviewButtons exist before adding event listeners */
    // if (editReviewButtons.length > 0) {
    //     for (let button of editReviewButtons) {
    //         button.addEventListener("click", (e) => {
    //             let reviewId = e.target.getAttribute("data-review-id");
    //             let reviewContent = document.getElementById(`review${reviewId}`).innerText;

    //             // Populate the form fields in the modal
    //             document.getElementById("id_content").value = reviewContent; // Assuming your form has an input with this ID
    //             document.getElementById("review_id").value = reviewId; // Set the hidden input value

    //             // Set action URL for form submission using recipeSlug
    //             editReviewForm.setAttribute("action", `/recipes/${recipeSlug}/review/${reviewId}/edit/`);

    //             // Show the modal
    //             if (editReviewModal) {
    //                 editReviewModal.show();
    //             } else {
    //                 console.error("Edit Review Modal is not initialized");
    //             }
    //         });
    //     }
    // } else {
    //     console.log("No edit review buttons found"); // Debugging log
    // }

    /** Check if deleteReviewButtons exist before adding event listeners */
    // if (deleteReviewButtons.length > 0) {
    //     for (let button of deleteReviewButtons) {
    //         console.log("Adding event listener to delete review button:", button); // Debugging log
    //         button.addEventListener("click", (e) => {
    //             console.log("Delete review button clicked:", e.target); // Debugging log
    //             let reviewId = e.target.getAttribute("data-review-id");
    //             deleteReviewConfirm.href = `delete_review/${reviewId}`;
    //             if (deleteReviewModal) {
    //                 deleteReviewModal.show();
    //             } else {
    //                 console.error("Delete Review Modal is not initialized");
    //             }
    //         });
    //     }
    // } else {
    //     console.log("No delete review buttons found"); // Debugging log
    // }

    /*
     * Initializes deletion functionality for the provided comment delete buttons.
     */
    // const deleteButtons = document.getElementsByClassName("btn-delete");
    // const deleteConfirm = document.getElementById("deleteConfirm");
    // const deleteModalElement = document.getElementById("deleteModal");
    // const deleteModal = deleteModalElement ? new bootstrap.Modal(deleteModalElement) : null;

    // if (deleteButtons.length > 0) {
    //     for (let button of deleteButtons) {
    //         console.log("Adding event listener to comment delete button:", button); // Debugging log
    //         button.addEventListener("click", (e) => {
    //             let commentId = e.target.getAttribute("comment_id");
    //             deleteConfirm.href = `delete_comment/${commentId}`;
    //             if (deleteModal) {
    //                 deleteModal.show();
    //             } else {
    //                 console.error("Delete Modal is not initialized");
    //             }
    //         });
    //     }
    // } else {
    //     console.log("No comment delete buttons found"); // Debugging log
    // }

    /*
     * Adds a dynamic update for the Recipe Submission form, on smaller screen sizes.
     */
    function checkScreenSize() {
        var warning = document.querySelector('.mobile-warning');
        var form = document.querySelector('.form-container');
        if (window.innerWidth <= 450) {
            warning.style.display = 'block';
            form.style.display = 'none';
        } else {
            warning.style.display = 'none';
            form.style.display = 'block';
        }
    }

    // Run on page load
    checkScreenSize();

    // Run on window resize
    window.addEventListener('resize', checkScreenSize);
});