// Image modal functionality
document.addEventListener('DOMContentLoaded', function() {
    // Create modal elements
    const modal = document.createElement('div');
    modal.id = 'image-modal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.8);
        cursor: pointer;
    `;
    
    const modalImg = document.createElement('img');
    modalImg.style.cssText = `
        margin: auto;
        display: block;
        max-width: 90%;
        max-height: 90%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    `;
    
    modal.appendChild(modalImg);
    document.body.appendChild(modal);
    
    // Add click handlers to figure images
    const figures = document.querySelectorAll('figure img');
    figures.forEach(function(img) {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function(e) {
            e.preventDefault();
            modalImg.src = this.src;
            modal.style.display = 'block';
        });
    });
    
    // Close modal when clicked
    modal.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            modal.style.display = 'none';
        }
    });
});