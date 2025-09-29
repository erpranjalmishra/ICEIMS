// ICCCA Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initBackToTop();
    initCarousel();
    initSmoothScroll();
    initTimeline();
    initBackToTop();
    
    // Initialize dropdowns after a short delay to ensure DOM is ready
    setTimeout(initDropdowns, 100);
});

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Active link highlighting
    window.addEventListener('scroll', function() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
    
    // Mobile menu close on link click
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });
    
    // Enhanced dropdown functionality
    initDropdowns();
}

// Initialize dropdown functionality
function initDropdowns() {
    // Simple hover functionality without Bootstrap Dropdown API
    const dropdownElements = document.querySelectorAll('.nav-item.dropdown');
    
    dropdownElements.forEach(dropdownEl => {
        const dropdownToggle = dropdownEl.querySelector('.dropdown-toggle');
        const dropdownMenu = dropdownEl.querySelector('.dropdown-menu');
        
        if (!dropdownToggle || !dropdownMenu) return;
        
        let hoverTimeout;
        
        // Mouse enter - show dropdown
        dropdownEl.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            dropdownEl.classList.add('show');
            dropdownMenu.classList.add('show');
            dropdownToggle.setAttribute('aria-expanded', 'true');
        });
        
        // Mouse leave - hide dropdown with delay
        dropdownEl.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(() => {
                dropdownEl.classList.remove('show');
                dropdownMenu.classList.remove('show');
                dropdownToggle.setAttribute('aria-expanded', 'false');
            }, 150);
        });
        
        // Click functionality for mobile/accessibility
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isOpen = dropdownEl.classList.contains('show');
            
            // Close all other dropdowns
            document.querySelectorAll('.nav-item.dropdown.show').forEach(el => {
                if (el !== dropdownEl) {
                    el.classList.remove('show');
                    el.querySelector('.dropdown-menu').classList.remove('show');
                    el.querySelector('.dropdown-toggle').setAttribute('aria-expanded', 'false');
                }
            });
            
            // Toggle current dropdown
            if (isOpen) {
                dropdownEl.classList.remove('show');
                dropdownMenu.classList.remove('show');
                dropdownToggle.setAttribute('aria-expanded', 'false');
            } else {
                dropdownEl.classList.add('show');
                dropdownMenu.classList.add('show');
                dropdownToggle.setAttribute('aria-expanded', 'true');
            }
        });
        
        // Keyboard navigation
        dropdownToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                dropdownToggle.click();
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.nav-item.dropdown.show').forEach(dropdownEl => {
                const dropdownMenu = dropdownEl.querySelector('.dropdown-menu');
                const dropdownToggle = dropdownEl.querySelector('.dropdown-toggle');
                dropdownEl.classList.remove('show');
                dropdownMenu.classList.remove('show');
                dropdownToggle.setAttribute('aria-expanded', 'false');
            });
        }
    });
    
    console.log('Dropdowns initialized:', dropdownElements.length);
}

// Back to top button
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
    }
}

// Scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Carousel enhancements
function initCarousel() {
    const carousel = document.getElementById('heroCarousel');
    if (carousel) {
        // Initialize Bootstrap carousel
        const bsCarousel = new bootstrap.Carousel(carousel, {
            interval: 4000,
            ride: 'carousel',
            pause: 'hover',
            wrap: true,
            touch: true
        });
        
        // Pause carousel on hover
        carousel.addEventListener('mouseenter', function() {
            bsCarousel.pause();
        });
        
        carousel.addEventListener('mouseleave', function() {
            bsCarousel.cycle();
        });
        
        // Add keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                bsCarousel.prev();
            } else if (e.key === 'ArrowRight') {
                bsCarousel.next();
            }
        });
        
        // Touch/swipe support for mobile
        let startX = 0;
        let endX = 0;
        
        carousel.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        });
        
        carousel.addEventListener('touchend', function(e) {
            endX = e.changedTouches[0].clientX;
            handleSwipe();
        });
        
        function handleSwipe() {
            const threshold = 50; // minimum distance for swipe
            const diff = startX - endX;
            
            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    // Swiped left, go to next slide
                    bsCarousel.next();
                } else {
                    // Swiped right, go to previous slide
                    bsCarousel.prev();
                }
            }
        }
        
        // Ensure carousel starts immediately
        setTimeout(() => {
            bsCarousel.cycle();
            carousel.classList.add('loaded');
        }, 100);
        
        // Add slide change event listeners for analytics or other purposes
        carousel.addEventListener('slide.bs.carousel', function (event) {
            console.log('Sliding to slide:', event.to);
        });
        
        carousel.addEventListener('slid.bs.carousel', function (event) {
            console.log('Slid to slide:', event.to);
        });
    }
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if href is just "#"
            if (href === '#') return;
            
            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                
                const headerOffset = 80;
                const elementPosition = target.offsetTop;
                const offsetPosition = elementPosition - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Card hover effects
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll(
        '.date-card, .track-card, .committee-card, .highlight-card, .attraction-card'
    );
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Counter animation for statistics
function animateCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-counter'));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            counter.textContent = Math.floor(current);
            
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            }
        }, 20);
    });
}

// Initialize counters when they come into view
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', function() {
    const statsSection = document.querySelector('.university-stats');
    if (statsSection) {
        counterObserver.observe(statsSection);
    }
});

// Loading animation
window.addEventListener('load', function() {
    const loading = document.querySelector('.loading');
    if (loading) {
        loading.style.opacity = '0';
        setTimeout(() => {
            loading.style.display = 'none';
        }, 500);
    }
    
    // Force carousel initialization after page load
    setTimeout(() => {
        const carousel = document.getElementById('heroCarousel');
        if (carousel && !bootstrap.Carousel.getInstance(carousel)) {
            initCarousel();
        }
    }, 500);
});

// Form handling (if forms are added later)
function handleFormSubmission(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Add form validation and submission logic here
            const formData = new FormData(form);
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Submitting...';
            submitBtn.disabled = true;
            
            // Simulate form submission (replace with actual API call)
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                // Show success message
                showNotification('Form submitted successfully!', 'success');
                form.reset();
            }, 2000);
        });
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Image lazy loading
function initLazyLoading() {
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
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);

// Error handling for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Replace with placeholder image if original fails to load
            this.src = '/static/images/placeholder.svg';
        });
    });
});

// Contact form handling
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactFormSubmission);
    }
});

function handleContactFormSubmission(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    submitBtn.disabled = true;
    
    // Validate form
    if (!validateContactForm(form)) {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        return;
    }
    
    // Simulate form submission (replace with actual API call)
    setTimeout(() => {
        submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Message Sent!';
        
        // Show success message
        showNotification('Thank you for your message! We will get back to you within 24 hours.', 'success');
        
        // Reset form
        form.reset();
        
        // Reset button after 3 seconds
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 3000);
        
    }, 2000);
}

function validateContactForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Email validation
    const email = form.querySelector('#email');
    if (email.value && !isValidEmail(email.value)) {
        email.classList.add('is-invalid');
        isValid = false;
    }
    
    if (!isValid) {
        showNotification('Please fill in all required fields correctly.', 'danger');
    }
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Form field validation on blur
document.addEventListener('DOMContentLoaded', function() {
    const formFields = document.querySelectorAll('.form-control, .form-select');
    
    formFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
            
            // Email validation
            if (this.type === 'email' && this.value && !isValidEmail(this.value)) {
                this.classList.add('is-invalid');
            }
        });
        
        field.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
});

// Performance optimization - Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Timeline animation
function initTimeline() {
    const timelineSection = document.querySelector('.timeline-section');
    if (!timelineSection) return;
    
    const timelineItems = document.querySelectorAll('.timeline-item');
    const timelineLine = document.querySelector('.timeline-line');
    
    const timelineObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Animate timeline items with staggered delay
                timelineItems.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, index * 200);
                });
                
                // Animate the timeline line
                if (timelineLine) {
                    timelineLine.style.animation = 'drawLine 2s ease-out forwards';
                }
                
                timelineObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });
    
    // Initially hide timeline items
    timelineItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        item.style.transition = 'all 0.6s ease-out';
    });
    
    timelineObserver.observe(timelineSection);
}

// Add CSS animation for timeline line drawing
const timelineStyles = document.createElement('style');
timelineStyles.textContent = `
    @keyframes drawLine {
        0% {
            background: linear-gradient(90deg, 
                #28a745 0%, 
                #28a745 0%, 
                #e9ecef 0%, 
                #e9ecef 100%);
        }
        50% {
            background: linear-gradient(90deg, 
                #28a745 0%, 
                #28a745 15%, 
                #e9ecef 15%, 
                #e9ecef 100%);
        }
        100% {
            background: linear-gradient(90deg, 
                #28a745 0%, 
                #28a745 30%, 
                #e9ecef 30%, 
                #e9ecef 100%);
        }
    }
`;
document.head.appendChild(timelineStyles);

// Optimized Chatbot Initialization - Lazy Loading
function initChatbot() {
    let chatbotInstance = null;
    let initialized = false;
    
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbotWindow = document.querySelector('.chatbot-window');
    const closeBtn = document.querySelector('.chatbot-close');
    
    if (!chatbotToggle || !chatbotWindow) return;
    
    // Initialize chatbot only when first opened
    chatbotToggle.addEventListener('click', async function() {
        if (!initialized) {
            // Show loading state
            const originalContent = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span class="chatbot-name">Loading...</span>';
            
            try {
                // Create chatbot instance lazily
                chatbotInstance = new GeminiChatbot();
                await chatbotInstance.initializeWhenNeeded();
                initialized = true;
            } catch (error) {
                console.warn('Chatbot initialization failed:', error);
                // Continue with basic functionality
            }
            
            // Restore button
            this.innerHTML = originalContent;
        }
        
        // Toggle window
        chatbotWindow.classList.toggle('active');
    });
    
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            chatbotWindow.classList.remove('active');
        });
    }
}

// Initialize chatbot when DOM is ready with delay for performance
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initChatbot, 1000);
});

// Morphing University Gallery
class MorphingGallery {
    constructor() {
        this.currentIndex = 0;
        this.totalImages = 5;
        this.autoPlayInterval = null;
        this.progressInterval = null;
        this.isPlaying = true;
        this.intervalTime = 4500; // 4.5 seconds
        this.isTransitioning = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.startAutoPlay();
        this.updateProgressRing();
    }
    
    setupEventListeners() {
        const container = document.querySelector('.morphing-gallery-container');
        const dots = document.querySelectorAll('.nav-dot');
        
        if (!container) return;
        
        // Pause on hover
        container.addEventListener('mouseenter', () => this.pauseAutoPlay());
        container.addEventListener('mouseleave', () => this.resumeAutoPlay());
        
        // Dot navigation
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                if (!this.isTransitioning) {
                    this.goToImage(index);
                }
            });
        });
        
        // Touch/swipe support for mobile
        let startX = 0;
        let endX = 0;
        
        container.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        }, { passive: true });
        
        container.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            this.handleSwipe(startX, endX);
        }, { passive: true });
    }
    
    handleSwipe(startX, endX) {
        const diff = startX - endX;
        const minSwipe = 50;
        
        if (Math.abs(diff) > minSwipe) {
            if (diff > 0) {
                this.nextImage();
            } else {
                this.previousImage();
            }
        }
    }
    
    goToImage(index) {
        if (this.isTransitioning || index === this.currentIndex) return;
        
        this.isTransitioning = true;
        const containers = document.querySelectorAll('.morphing-image-container');
        const dots = document.querySelectorAll('.nav-dot');
        
        // Remove active classes
        containers[this.currentIndex].classList.remove('active');
        dots[this.currentIndex].classList.remove('active');
        
        // Add morphing animation classes
        containers[this.currentIndex].style.animation = 'morphOut 0.8s cubic-bezier(0.23, 1, 0.320, 1) forwards';
        
        setTimeout(() => {
            this.currentIndex = index;
            
            // Activate new image with morphing animation
            containers[this.currentIndex].style.animation = 'morphIn 1.2s cubic-bezier(0.23, 1, 0.320, 1) forwards';
            containers[this.currentIndex].classList.add('active');
            dots[this.currentIndex].classList.add('active');
            
            this.updateProgressRing();
            
            setTimeout(() => {
                containers[this.currentIndex].style.animation = '';
                this.isTransitioning = false;
            }, 1200);
        }, 400);
    }
    
    nextImage() {
        const nextIndex = (this.currentIndex + 1) % this.totalImages;
        this.goToImage(nextIndex);
    }
    
    previousImage() {
        const prevIndex = (this.currentIndex - 1 + this.totalImages) % this.totalImages;
        this.goToImage(prevIndex);
    }
    
    startAutoPlay() {
        if (!this.isPlaying) {
            this.isPlaying = true;
            this.autoPlayInterval = setInterval(() => {
                if (!this.isTransitioning) {
                    this.nextImage();
                }
            }, this.intervalTime);
        }
    }
    
    pauseAutoPlay() {
        this.isPlaying = false;
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    resumeAutoPlay() {
        if (!this.isPlaying) {
            setTimeout(() => {
                this.startAutoPlay();
            }, 1000);
        }
    }
    
    updateProgressRing() {
        const progressText = document.querySelector('.progress-text');
        const progressCircle = document.querySelector('.progress-ring-circle');
        
        if (progressText) {
            progressText.textContent = `${this.currentIndex + 1}/${this.totalImages}`;
        }
        
        if (progressCircle) {
            const circumference = 2 * Math.PI * 28; // r=28
            const progress = (this.currentIndex + 1) / this.totalImages;
            const offset = circumference - (progress * circumference);
            
            progressCircle.style.strokeDasharray = circumference;
            progressCircle.style.strokeDashoffset = offset;
        }
    }
    
    // Public methods for external control
    pause() {
        this.pauseAutoPlay();
    }
    
    play() {
        this.startAutoPlay();
    }
    
    getCurrentIndex() {
        return this.currentIndex;
    }
}

// Initialize morphing gallery
let morphingGallery = null;

document.addEventListener('DOMContentLoaded', function() {
    const galleryContainer = document.querySelector('.morphing-gallery-container');
    
    if (galleryContainer) {
        morphingGallery = new MorphingGallery();
        
        // Intersection Observer for performance
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        if (morphingGallery && !morphingGallery.isPlaying) {
                            morphingGallery.play();
                        }
                    } else {
                        if (morphingGallery) {
                            morphingGallery.pause();
                        }
                    }
                });
            },
            { threshold: 0.3 }
        );
        
        observer.observe(galleryContainer);
    }
});

// Handle visibility changes
document.addEventListener('visibilitychange', () => {
    if (morphingGallery) {
        if (document.hidden) {
            morphingGallery.pause();
        } else {
            morphingGallery.play();
        }
    }
});

// Expose global functions for external access
window.nextGalleryImage = () => {
    if (morphingGallery) morphingGallery.nextImage();
};

window.prevGalleryImage = () => {
    if (morphingGallery) morphingGallery.previousImage();
};

window.goToGalleryImage = (index) => {
    if (morphingGallery) morphingGallery.goToImage(index);
};