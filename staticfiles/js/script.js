document.addEventListener('DOMContentLoaded', function() {
    const editReviewButtons = document.getElementsByClassName("btn-edit-review");
    const editCommentButtons = document.getElementsByClassName("btn-edit");
    const deleteCommentButtons = document.getElementsByClassName("btn-delete");
    const deleteModal = document.getElementById("deleteModal");
    const deleteConfirmLink = document.getElementById("deleteConfirm");

    // Function to handle button clicks for editing
    function handleEditButtonClick(e) {
        e.preventDefault();
        let editUrl = e.target.getAttribute("data-url"); // Use data-url attribute
        console.log('editUrl', editUrl);
        window.location.href = editUrl;  // Redirect to edit URL
    }

    // Handle edit review buttons
    if (editReviewButtons.length > 0) {
        for (let button of editReviewButtons) {
            button.addEventListener("click", handleEditButtonClick);
        }
    } else {
        console.log("No edit review buttons found");
    }

    // Handle edit comment buttons
    if (editCommentButtons.length > 0) {
        for (let button of editCommentButtons) {
            button.addEventListener("click", handleEditButtonClick);
        }
    } else {
        console.log("No edit comment buttons found");
    }

    // Handle delete comment buttons
    if (deleteCommentButtons.length > 0) {
        for (let button of deleteCommentButtons) {
            button.addEventListener("click", function(e) {
                e.preventDefault();
                const commentId = this.getAttribute('data-comment-id');
                const deleteUrl = this.getAttribute('data-url'); // Get URL from data-url attribute

                // Set the confirmation link for deletion
                deleteConfirmLink.href = deleteUrl;

                // Show the delete confirmation modal
                const modalInstance = new bootstrap.Modal(deleteModal);
                modalInstance.show();
            });
        }
    } else {
        console.log("No delete comment buttons found");
    }

    function checkScreenSize() {
        var warning = document.querySelector('.mobile-warning');
        var form = document.querySelector('.form-container');
        if (warning && form) {
            if (window.innerWidth <= 450) {
                warning.style.display = 'block';
                form.style.display = 'none';
            } else {
                warning.style.display = 'none';
                form.style.display = 'block';
            }
        }
    }
    
    // Only run if both elements exist
    if (document.querySelector('.mobile-warning') && document.querySelector('.form-container')) {
        // Run on page load
        checkScreenSize();
    
        // Run on window resize
        window.addEventListener('resize', checkScreenSize);
    }
});