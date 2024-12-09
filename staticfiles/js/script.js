document.addEventListener('DOMContentLoaded', function() {
    const editReviewButtons = document.getElementsByClassName("btn-edit-review");
    const editReviewModalElement = document.getElementById("editReviewModal");

    if (editReviewButtons.length > 0) {
        for (let button of editReviewButtons) {
            button.addEventListener("click", (e) => {
                e.preventDefault();
                let reviewId = e.target.getAttribute("data-review-id");
                let editUrl = e.target.getAttribute("href");
                
                window.location.href = editUrl;
            });
        }
    } else {
        console.log("No edit review buttons found");
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