// Initialize Lucide icons
lucide.createIcons();

// Global state
let currentResults = [];
let isLoading = false;
let smartCart = JSON.parse(localStorage.getItem('smartCart')) || [];

// DOM elements (some only exist on certain pages)
const searchInput = document.getElementById('searchInput');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const productGrid = document.getElementById('productGrid');
const noResults = document.getElementById('noResults');
const sortSelect = document.getElementById('sortSelect');

// Platform configuration
const platformConfig = {
    'Blinkit': {
        color: '#fcd34d', // amber-300
        bg: 'rgba(245, 158, 11, 0.2)',
        border: 'rgba(245, 158, 11, 0.6)',
        shadow: 'rgba(245, 158, 11, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(245,158,11,0.6)]',
        hoverBorder: 'hover:border-amber-400/50',
        textHover: 'group-hover:text-amber-300',
        domain: 'blinkit.com',
        logo: 'https://upload.wikimedia.org/wikipedia/commons/1/18/Blinkit_logo.png'
    },
    'BigBasket Now': {
        color: '#bef264', // lime-300
        bg: 'rgba(132, 204, 34, 0.2)',
        border: 'rgba(132, 204, 34, 0.6)',
        shadow: 'rgba(132, 204, 34, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(132,204,34,0.6)]',
        hoverBorder: 'hover:border-lime-400/50',
        textHover: 'group-hover:text-lime-300',
        domain: 'bigbasket.com',
        logo: 'https://upload.wikimedia.org/wikipedia/en/1/16/Bigbasket_Logo.png'
    },
    'Dunzo Daily': {
        color: '#c4b5fd', // violet-300
        bg: 'rgba(139, 92, 246, 0.2)',
        border: 'rgba(139, 92, 246, 0.6)',
        shadow: 'rgba(139, 92, 246, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(139,92,246,0.6)]',
        hoverBorder: 'hover:border-violet-400/50',
        textHover: 'group-hover:text-violet-300',
        domain: 'dunzo.com',
        logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Dunzo_Logo.svg/1200px-Dunzo_Logo.svg.png'
    },
    'Flipkart Minutes': {
        color: '#93c5fd', // blue-300
        bg: 'rgba(59, 130, 246, 0.2)',
        border: 'rgba(59, 130, 246, 0.6)',
        shadow: 'rgba(59, 130, 246, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(59,130,246,0.6)]',
        hoverBorder: 'hover:border-blue-400/50',
        textHover: 'group-hover:text-blue-300',
        domain: 'flipkart.com',
        logo: 'https://upload.wikimedia.org/wikipedia/en/7/7a/Flipkart_logo.svg'
    },
    'Amazon Fresh': {
        color: '#86efac', // green-300
        bg: 'rgba(34, 197, 94, 0.2)',
        border: 'rgba(34, 197, 94, 0.6)',
        shadow: 'rgba(34, 197, 94, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(34,197,94,0.6)]',
        hoverBorder: 'hover:border-green-400/50',
        textHover: 'group-hover:text-green-300',
        domain: 'amazon.in',
        logo: 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg'
    },
    'Zepto': {
        color: '#d8b4fe', // purple-300
        bg: 'rgba(168, 85, 247, 0.2)',
        border: 'rgba(168, 85, 247, 0.6)',
        shadow: 'rgba(168, 85, 247, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(168,85,247,0.6)]',
        hoverBorder: 'hover:border-purple-400/50',
        textHover: 'group-hover:text-purple-300',
        domain: 'zeptonow.com',
        logo: 'https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/Zepto_Logo.svg/1024px-Zepto_Logo.svg.png'
    },
    'Instamart': {
        color: '#fdba74', // orange-300
        bg: 'rgba(249, 115, 22, 0.2)',
        border: 'rgba(249, 115, 22, 0.6)',
        shadow: 'rgba(249, 115, 22, 0.3)',
        blurShadow: 'drop-shadow-[0_0_10px_rgba(249,115,22,0.6)]',
        hoverBorder: 'hover:border-orange-400/50',
        textHover: 'group-hover:text-orange-300',
        domain: 'swiggy.com',
        logo: 'https://upload.wikimedia.org/wikipedia/en/1/12/Swiggy_logo.svg'
    }
};

// Search functions
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        searchProducts();
    }
}

function quickSearch(product) {
    searchInput.value = product;
    searchProducts();
}

async function searchProducts() {
    const query = searchInput.value.trim();
    if (!query) return;

    if (isLoading) return;

    isLoading = true;
    showLoading();

    try {
        const isEcommerce = window.location.pathname.includes('ecommerce');
        const endpoint = isEcommerce ? '/search/ecommerce' : '/search';

        const response = await fetch(`${endpoint}?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        currentResults = data;
        displayResults(data);
    } catch (error) {
        console.error('Search error:', error);
        showError();
    } finally {
        isLoading = false;
        hideLoading();
    }
}

// === SMART CART LOGIC ===
function addProductToSmartCart(productName, productImg) {
    const resultsToUse = (window.currentResults && window.currentResults.length > 0) ? window.currentResults : currentResults;
    if (!resultsToUse || resultsToUse.length === 0) {
        console.error("Smart Cart Add Failed: No search results found in scope.");
        return;
    }

    const platformPrices = {};
    let amazonPrice = null;
    let fallbackBasePrice = 0;

    // Aggregate prices for this product across all platforms found in the search
    // We filter by productName to ensure we only get prices for the specific item clicked
    resultsToUse.forEach(item => {
        if (item.product !== productName && !productName.includes(item.product) && !item.product.includes(productName)) return;

        const price = parseFloat(item.price);
        if (isNaN(price)) return;

        platformPrices[item.platform] = price;

        // Identify Amazon as the base if present (for ecommerce)
        if (item.platform.toLowerCase().includes('amazon')) {
            amazonPrice = price;
        }

        // Fallback base: Just track the highest price or Blinkit
        if (price > fallbackBasePrice) {
            fallbackBasePrice = price;
        }
        if (item.platform.toLowerCase() === 'blinkit' && !amazonPrice) {
            amazonPrice = price;
        }
    });

    // Use Amazon/Blinkit price if available, otherwise use highest price found as the "baseline" to compare against
    const basePrice = amazonPrice || fallbackBasePrice;

    const cartItem = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 5),
        product: productName,
        image: productImg,
        prices: platformPrices,
        basePrice: basePrice
    };

    smartCart.push(cartItem);
    saveAndRenderCart();

    // Use Toast instead of Alert for better UX
    if (typeof showToast === 'function') {
        showToast(`Added ${productName} to Smart Cart!`, 'success');
    } else {
        alert(`Successfully added ${productName} to Smart Cart! Savings updated.`);
    }
}

function proceedToCheckout() {
    if (smartCart.length === 0) {
        if (typeof showToast === 'function') {
            showToast('Your cart is empty!', 'warning');
        } else {
            alert('Your cart is empty!');
        }
        return;
    }

    let baseTotal = 0;
    let mixedTotal = 0;

    smartCart.forEach(item => {
        const prices = Object.values(item.prices);
        const bestPrice = prices.length > 0 ? Math.min(...prices) : item.basePrice;

        baseTotal += item.basePrice;
        mixedTotal += bestPrice;
    });

    localStorage.setItem('checkout_total', mixedTotal.toString());
    localStorage.setItem('checkout_original', baseTotal.toString());

    window.location.href = '/payment';
}

function removeFromSmartCart(index) {
    smartCart.splice(index, 1);
    saveAndRenderCart();
}

function clearSmartCart() {
    smartCart = [];
    saveAndRenderCart();
}

function saveAndRenderCart() {
    localStorage.setItem('smartCart', JSON.stringify(smartCart));
    updateCartUI();
}

function updateCartUI() {
    const listEl = document.getElementById('smartCartItemsList');
    const baseTotalEl = document.getElementById('smartCartBaseTotal');
    const mixedTotalEl = document.getElementById('smartCartMixedTotal');
    const savingsEl = document.getElementById('smartCartSavings');
    const baseLabel = document.getElementById('smartCartBaseLabel');

    if (!listEl) return; // Smart Cart banner isn't on this page

    let baseTotal = 0;
    let mixedTotal = 0;

    listEl.innerHTML = '';

    if (smartCart.length === 0) {
        listEl.innerHTML = '<div class="text-sm text-gray-400 italic text-center py-2" id="emptyCartMessage">Your cart is empty</div>';
        baseTotalEl.textContent = '₹0';
        mixedTotalEl.textContent = '₹0';
        savingsEl.textContent = '₹0';
        return;
    }

    smartCart.forEach((item, index) => {
        // Find the absolute lowest price across all platforms for this specific item
        const prices = Object.values(item.prices);
        const bestPrice = prices.length > 0 ? Math.min(...prices) : item.basePrice;

        baseTotal += item.basePrice;
        mixedTotal += bestPrice;

        const itemHTML = `
            <div class="flex justify-between items-center bg-white/5 rounded-lg p-2 border border-white/10">
                <div class="flex items-center gap-2 overflow-hidden">
                    <img src="${item.image}" alt="${item.product}" class="w-8 h-8 rounded shrink-0 object-contain bg-white/10 p-1 filter mix-blend-screen brightness-110 contrast-125">
                    <span class="text-sm text-white font-medium truncate w-32" title="${item.product}">${item.product}</span>
                </div>
                <div class="flex items-center gap-3 shrink-0">
                    <span class="text-xs text-green-400 font-bold">₹${bestPrice}</span>
                    <button onclick="removeFromSmartCart(${index})" class="text-gray-500 hover:text-red-400 text-xs transition p-1 bg-white/5 rounded-full hover:bg-red-500/20">
                        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
            </div>
        `;
        listEl.insertAdjacentHTML('beforeend', itemHTML);
    });

    baseTotalEl.textContent = `₹${baseTotal}`;
    mixedTotalEl.textContent = `₹${mixedTotal}`;
    savingsEl.textContent = `₹${Math.max(0, baseTotal - mixedTotal)}`;

    // Dynamic label
    if (baseLabel) {
        if (window.location.pathname.includes('ecommerce')) {
            baseLabel.innerHTML = 'Total on Amazon';
        } else {
            baseLabel.innerHTML = 'Standard Platform Total';
        }
    }

    // Re-initialize Lucide icons for dynamically added trash buttons
    if (window.lucide) {
        lucide.createIcons();
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
});
// ==========================

function showLoading() {
    if (loadingState) loadingState.classList.remove('hidden');
    if (resultsSection) resultsSection.classList.add('hidden');
    if (noResults) noResults.classList.add('hidden');
}

function hideLoading() {
    if (loadingState) loadingState.classList.add('hidden');
}

function closeResults() {
    if (resultsSection) resultsSection.classList.add('hidden');
    if (noResults) noResults.classList.add('hidden');
}

function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

function showError() {
    if (noResults) noResults.classList.remove('hidden');
    if (resultsSection) resultsSection.classList.add('hidden');
}

function displayResults(results) {
    if (results.length === 0) {
        showError();
        return;
    }

    if (resultsSection) resultsSection.classList.remove('hidden');
    if (noResults) noResults.classList.add('hidden');

    renderProductCards(results);
}

function renderProductCards(results) {
    productGrid.innerHTML = '';

    results.forEach((item, index) => {
        const isCheapest = index === 0;
        const card = createProductCard(item, isCheapest);
        productGrid.appendChild(card);
    });

    lucide.createIcons();
}

function createProductCard(item, isCheapest) {
    const config = platformConfig[item.platform] || {
        color: '#94a3b8', bg: 'rgba(255,255,255,0.05)', border: 'rgba(255,255,255,0.2)', shadow: 'rgba(255,255,255,0.1)',
        blurShadow: '', hoverBorder: 'hover:border-white/30', textHover: 'group-hover:text-gray-300', domain: 'google.com',
        logo: `https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${item.platform.toLowerCase().replace(' ', '')}.com&size=128`
    };

    let productImg = 'https://cdn-icons-png.flaticon.com/512/3233/3233483.png'; // Generic Package box icon
    if (item && item.product) {
        const productName = item.product.toLowerCase();
        if (productName.includes('milk')) {
            productImg = '/static/images/amul_milk.png';
        } else if (productName.includes('bread')) {
            productImg = '/static/images/brown_bread.png';
        } else if (productName.includes('egg')) {
            productImg = '/static/images/farm_eggs.png';
        } else if (productName.includes('coke') || productName.includes('cola')) {
            productImg = '/static/images/coke_can.png';
        } else if (productName.includes('headphone') || productName.includes('earbud') || productName.includes('audio') || productName.includes('headphones')) {
            productImg = 'https://www.sony.co.in/image/6145c1d32e6ac8e63a46c912dc33c5bb?fmt=pjpeg&wid=330&bgcolor=FFFFFF&bgc=FFFFFF';
        } else if (productName.includes('lipstick') || productName.includes('mac')) {
            productImg = '/static/images/mac_lipstick.png';
        }
    }

    const card = document.createElement('div');
    card.className = `glass-card-premium rounded-xl p-5 hover-lift-premium flex flex-col h-full group transition-all duration-300 ${config.hoverBorder} bg-[#0a0f1c]/90 border border-white/10 border-t-2 shadow-lg`;
    card.style.borderTopColor = config.color;

    card.innerHTML = `
        ${isCheapest ? `
            <div class="inline-block savings-highlight-premium text-xs px-2 py-1 rounded-full font-bold mb-3 self-start bg-green-500/20 border border-green-500/50 text-white shadow-[0_0_10px_rgba(34,197,94,0.3)]">
                🏆 Best Price
            </div>
        ` : ''}
        
        <div class="flex flex-col items-center mb-4 text-center">
            <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-3 overflow-hidden p-2 backdrop-blur-md transition-all duration-500 group-hover:scale-110" 
                 style="background: ${config.bg}; border: 1px solid ${config.border}; box-shadow: 0 0 15px ${config.shadow};">
                <img src="${config.logo}" onerror="this.src='https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${config.domain}&size=128'" alt="${item.platform}"
                     class="w-full h-full object-contain rounded-lg drop-shadow-md bg-white/95 p-1">
            </div>
            <div>
                <h4 class="font-bold text-xl mb-1 text-white ${config.textHover} transition-colors">${item.platform}</h4>
                <div class="text-3xl font-extrabold ${config.blurShadow} my-2" style="color: ${config.color}; text-shadow: 0 0 10px rgba(255,255,255,0.1);">
                    ₹${item.price}
                </div>
                <p class="text-xs text-gray-300 tracking-wider uppercase mb-2 font-medium">${item.delivery_time || 'Standard Delivery'}</p>
            </div>
        </div>
        
        <div class="mb-4 flex-grow flex items-center gap-3 bg-white/5 p-3 rounded-xl border border-white/10 mt-2">
            <div class="w-12 h-12 bg-white/10 rounded-lg flex items-center justify-center p-1 shrink-0">
                <img src="${productImg}" alt="${item.product}" class="w-full h-full object-contain filter drop-shadow-md mix-blend-screen brightness-110 contrast-125">
            </div>
            <div>
                <h3 class="font-medium text-white text-sm line-clamp-2" title="${item.product}">${item.product}</h3>
                <div class="flex items-center gap-2 mt-1">
                    <span class="text-xs ${item.source === 'scraped' ? 'text-green-400' : 'text-yellow-400'} px-2 py-0.5 rounded-full" style="background: rgba(255,255,255,0.05)">
                        ${item.source === 'scraped' ? '● Live Price' : '● Estimated'}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="flex gap-2 mt-auto pt-4 border-t border-white/10">
            <a href="${item.url}" target="_blank" 
               class="flex-1 glass-button-premium text-white py-2 px-3 rounded-xl font-semibold transition text-center text-sm" style="background: rgba(255,255,255,0.05)">
                Visit Store
            </a>
            <button onclick="addProductToSmartCart('${item.product.replace(/'/g, "\\'")}', '${productImg}')" class="flex-[2] glass-button-premium text-green-400 border border-green-500/30 hover:bg-green-500/20 hover:border-green-400 py-2 rounded-xl text-sm font-bold flex justify-center items-center transition shadow-[0_4px_14px_rgba(34,197,94,0.15)] group-hover:shadow-[0_6px_20px_rgba(34,197,94,0.3)]">
                <i data-lucide="shopping-cart" class="w-4 h-4 mr-2"></i> Add to Smart Cart
            </button>
        </div>
    `;

    return card;
}

function copyLink(url) {
    navigator.clipboard.writeText(url);
    alert('Link copied to clipboard!');
}

function sortResults() {
    if (!sortSelect) return;
    const sortBy = sortSelect.value;
    let sortedResults = [...currentResults];

    if (sortBy === 'price') {
        sortedResults.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'delivery') {
        sortedResults.sort((a, b) => parseInt(a.delivery_time) - parseInt(b.delivery_time));
    }

    renderProductCards(sortedResults);
}

// Animation styles removed