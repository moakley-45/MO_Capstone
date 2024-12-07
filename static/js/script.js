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
    if (editReviewButtons.length > 0) {
        for (let button of editReviewButtons) {
            button.addEventListener("click", (e) => {
                e.preventDefault();
                let reviewId = e.target.getAttribute("data-review-id");
                let editUrl = e.target.getAttribute("href");
                
                // Redirect to the edit page
                window.location.href = editUrl;
            });
        }
    } else {
        console.log("No edit review buttons found"); // Debugging log
    }

    // ... rest of your existing code ...

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