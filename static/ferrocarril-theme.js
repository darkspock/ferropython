(function() {
    'use strict';

    // Mobile menu toggle
    document.addEventListener('DOMContentLoaded', function() {
        const menuToggle = document.querySelector('.menu-toggle');
        const primaryMenu = document.querySelector('#primary-menu');
        
        if (menuToggle && primaryMenu) {
            menuToggle.addEventListener('click', function() {
                this.classList.toggle('toggled');
                primaryMenu.classList.toggle('toggled');
            });
        }

        // Submenu toggles for mobile
        const menuItemsWithChildren = document.querySelectorAll('.menu-item-has-children > a');
        menuItemsWithChildren.forEach(function(item) {
            item.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const subMenu = this.nextElementSibling;
                    if (subMenu && subMenu.classList.contains('sub-menu')) {
                        subMenu.classList.toggle('toggled');
                    }
                }
            });
        });

        // Search form enhancement
        const searchForms = document.querySelectorAll('.search-form');
        searchForms.forEach(function(form) {
            const input = form.querySelector('.search-field');
            const button = form.querySelector('.search-submit');
            
            if (input && button) {
                input.addEventListener('focus', function() {
                    form.classList.add('search-focused');
                });
                
                input.addEventListener('blur', function() {
                    if (!this.value) {
                        form.classList.remove('search-focused');
                    }
                });
            }
        });

        // Smooth scroll for anchor links
        const anchorLinks = document.querySelectorAll('a[href^="#"]');
        anchorLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId !== '#') {
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });

        // Add loading class to images
        const images = document.querySelectorAll('img');
        images.forEach(function(img) {
            img.addEventListener('load', function() {
                this.classList.add('loaded');
            });
            
            // Handle error state
            img.addEventListener('error', function() {
                this.classList.add('error');
                this.src = '/static/images/placeholder.jpg';
            });
        });

        // Table of contents for long posts (if needed)
        const postContent = document.querySelector('.entry-content');
        if (postContent) {
            const headings = postContent.querySelectorAll('h2, h3, h4');
            if (headings.length > 3) {
                createTableOfContents(headings);
            }
        }

        // Back to top button
        createBackToTopButton();

        // Lazy loading for images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    });

    // Create table of contents
    function createTableOfContents(headings) {
        const toc = document.createElement('div');
        toc.className = 'table-of-contents';
        toc.innerHTML = '<h3>Índice</h3><ul></ul>';
        
        const tocList = toc.querySelector('ul');
        headings.forEach((heading, index) => {
            const id = heading.id || `heading-${index}`;
            heading.id = id;
            
            const li = document.createElement('li');
            li.innerHTML = `<a href="#${id}">${heading.textContent}</a>`;
            tocList.appendChild(li);
        });

        const postContent = document.querySelector('.entry-content');
        if (postContent) {
            postContent.insertBefore(toc, postContent.firstChild);
        }
    }

    // Create back to top button
    function createBackToTopButton() {
        const button = document.createElement('button');
        button.className = 'back-to-top';
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.setAttribute('aria-label', 'Volver arriba');
        document.body.appendChild(button);

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                button.classList.add('show');
            } else {
                button.classList.remove('show');
            }
        });

        button.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Handle responsive videos
    function wrapVideos() {
        const videos = document.querySelectorAll('iframe[src*="youtube"], iframe[src*="vimeo"]');
        videos.forEach(function(video) {
            if (!video.parentElement.classList.contains('video-wrapper')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'video-wrapper';
                video.parentNode.insertBefore(wrapper, video);
                wrapper.appendChild(video);
            }
        });
    }

    // Initialize video wrappers
    wrapVideos();

    // Accessibility enhancements
    function enhanceAccessibility() {
        // Add focus indicators
        const focusableElements = document.querySelectorAll('a, button, input, textarea, select');
        focusableElements.forEach(function(element) {
            element.addEventListener('focus', function() {
                document.body.classList.add('keyboard-navigation');
            });
            
            element.addEventListener('blur', function() {
                document.body.classList.remove('keyboard-navigation');
            });
        });

        // Skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.focus();
                    target.scrollIntoView();
                }
            });
        }
    }

    enhanceAccessibility();

})();