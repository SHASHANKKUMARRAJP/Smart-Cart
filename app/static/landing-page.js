// LANDING PAGE JAVASCRIPT

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.classList.toggle('hidden');
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
        // Close mobile menu if open
        const mobileMenu = document.getElementById('mobileMenu');
        if (!mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
        }
    });
});

// Scroll animations
function handleScrollAnimations() {
    const reveals = document.querySelectorAll('.reveal');
    const featureCards = document.querySelectorAll('.feature-stagger');
    const appCards = document.querySelectorAll('.app-grid-item');
    
    // Reveal animations
    reveals.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
    
    // Feature cards stagger animation
    featureCards.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
    
    // App cards stagger animation
    appCards.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
}

// Parallax effect for hero section
function handleParallax() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.parallax-element');
    
    parallaxElements.forEach(element => {
        const speed = element.dataset.speed || 0.5;
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px)`;
    });
}

// Add interactive hover effects
function addInteractiveEffects() {
    const cards = document.querySelectorAll('.interactive-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('glow-effect');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('glow-effect');
        });
    });
}

// Initialize page animations
function initializeAnimations() {
    // Add reveal classes to elements
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('reveal');
    });
    
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.classList.add('feature-stagger');
    });
    
    const appCards = document.querySelectorAll('.app-card');
    appCards.forEach(card => {
        card.classList.add('app-grid-item');
    });
    
    // Add interactive classes
    const interactiveElements = document.querySelectorAll('.feature-card, .app-card');
    interactiveElements.forEach(element => {
        element.classList.add('interactive-card');
    });
    
    // Add parallax classes
    const heroElements = document.querySelectorAll('.hero-section > div > *');
    heroElements.forEach(element => {
        element.classList.add('parallax-element');
        element.dataset.speed = Math.random() * 0.5 + 0.2;
    });
}

// Page load animations
function handlePageLoad() {
    // Hide page loader if exists
    const loader = document.querySelector('.page-loader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
        }, 500);
    }
    
    // Animate hero elements on load
    const heroElements = document.querySelectorAll('.hero-section .text-animate');
    heroElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Initialize animations
    initializeAnimations();
    addInteractiveEffects();
    
    // Trigger initial scroll check
    handleScrollAnimations();
}

// Video background controls (reuse from app.js)
let isVideoMuted = false;
let isVideoPaused = false;

function toggleVideoMute() {
    const video = document.querySelector('.video-background video');
    const muteBtn = document.getElementById('muteBtn');
    
    if (video) {
        video.muted = !video.muted;
        isVideoMuted = video.muted;
        
        if (muteBtn) {
            const icon = muteBtn.querySelector('i');
            if (isVideoMuted) {
                icon.setAttribute('data-lucide', 'volume-x');
            } else {
                icon.setAttribute('data-lucide', 'volume-2');
            }
            lucide.createIcons();
        }
    }
}

function toggleVideoPlay() {
    const video = document.querySelector('.video-background video');
    const playBtn = document.getElementById('playBtn');
    
    if (video) {
        if (isVideoPaused) {
            video.play();
            isVideoPaused = false;
            if (playBtn) {
                const icon = playBtn.querySelector('i');
                icon.setAttribute('data-lucide', 'pause');
            }
        } else {
            video.pause();
            isVideoPaused = true;
            if (playBtn) {
                const icon = playBtn.querySelector('i');
                icon.setAttribute('data-lucide', 'play');
            }
        }
        lucide.createIcons();
    }
}

// Initialize video when page loads
function initializeVideo() {
    const video = document.querySelector('.video-background video');
    if (video) {
        video.play().catch(function(error) {
            console.log("Auto-play was prevented. User interaction required.");
            const playBtn = document.getElementById('playBtn');
            if (playBtn) {
                const icon = playBtn.querySelector('i');
                icon.setAttribute('data-lucide', 'play');
                lucide.createIcons();
            }
        });
    }
}

// Handle visibility change for video performance
document.addEventListener('visibilitychange', function() {
    const video = document.querySelector('.video-background video');
    if (video) {
        if (document.hidden) {
            video.pause();
        } else if (!isVideoPaused) {
            video.play().catch(function(error) {
                console.log("Auto-play was prevented. User interaction required.");
            });
        }
    }
});

// Event listeners
window.addEventListener('scroll', () => {
    handleScrollAnimations();
    handleParallax();
});

window.addEventListener('load', () => {
    handlePageLoad();
    initializeVideo();
    lucide.createIcons();
});

// Add resize handler for responsive adjustments
window.addEventListener('resize', () => {
    handleScrollAnimations();
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const mobileMenu = document.getElementById('mobileMenu');
        if (!mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
        }
    }
});

// Add touch gestures for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
        const mobileMenu = document.getElementById('mobileMenu');
        if (diff > 0 && !mobileMenu.classList.contains('hidden')) {
            // Swipe left, close menu
            mobileMenu.classList.add('hidden');
        }
    }
}

// Performance optimization - throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Apply throttling to scroll handlers
window.addEventListener('scroll', throttle(() => {
    handleScrollAnimations();
    handleParallax();
}, 100));

// Add intersection observer for better performance
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, observerOptions);

// Observe elements for animations
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.reveal, .feature-stagger, .app-grid-item');
    animatedElements.forEach(element => {
        observer.observe(element);
    });
});
