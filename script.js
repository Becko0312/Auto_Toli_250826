class MongolianDictionary {
    constructor() {
        this.dictionary = [];
        this.searchInput = document.getElementById('searchInput');
        this.clearButton = document.getElementById('clearButton');
        this.resultsGrid = document.getElementById('resultsGrid');
        this.resultsCount = document.getElementById('resultsCount');
        this.noResults = document.getElementById('noResults');
        this.loadingMessage = document.getElementById('loadingMessage');
        
        this.initializeEventListeners();
        this.showLoadingMessage();
        this.loadDictionary();
    }
    
    initializeEventListeners() {
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });
        
        this.clearButton.addEventListener('click', () => {
            this.searchInput.value = '';
            this.clearResults();
            this.searchInput.focus();
        });
        
        document.querySelectorAll('input[name="searchDirection"]').forEach(radio => {
            radio.addEventListener('change', () => {
                if (this.searchInput.value.trim()) {
                    this.handleSearch(this.searchInput.value);
                }
            });
        });
        
        // Focus search input on page load
        this.searchInput.focus();
    }
    
    async loadDictionary() {
        try {
            const response = await fetch('dictionary.json');
            if (response.ok) {
                this.dictionary = await response.json();
                this.hideLoadingMessage();
                console.log(`Loaded ${this.dictionary.length} dictionary entries`);
            } else {
                this.showLoadingMessage();
            }
        } catch (error) {
            console.log('Dictionary file not found. Please upload dictionary.json');
            this.showLoadingMessage();
        }
    }
    
    showLoadingMessage() {
        this.loadingMessage.style.display = 'block';
        this.resultsGrid.style.display = 'none';
        this.noResults.style.display = 'none';
        this.resultsCount.textContent = '';
    }
    
    hideLoadingMessage() {
        this.loadingMessage.style.display = 'none';
    }
    
    handleSearch(query) {
        const trimmedQuery = query.trim().toLowerCase();
        
        if (!trimmedQuery) {
            this.clearResults();
            return;
        }
        
        if (this.dictionary.length === 0) {
            this.showLoadingMessage();
            return;
        }
        
        const searchDirection = document.querySelector('input[name="searchDirection"]:checked').value;
        const results = this.searchDictionary(trimmedQuery, searchDirection);
        this.displayResults(results, trimmedQuery);
    }
    
    searchDictionary(query, direction) {
        return this.dictionary.filter(entry => {
            const mongolian = entry.mongolian.toLowerCase();
            const english = entry.english.toLowerCase();
            
            switch (direction) {
                case 'mongolian':
                    return mongolian.includes(query);
                case 'english':
                    return english.includes(query);
                case 'both':
                default:
                    return mongolian.includes(query) || english.includes(query);
            }
        });
    }
    
    displayResults(results, query) {
        this.hideLoadingMessage();
        
        if (results.length === 0) {
            this.showNoResults();
            return;
        }
        
        this.hideNoResults();
        this.updateResultsCount(results.length);
        
        // Sort results by relevance (exact matches first, then starts with, then contains)
        const sortedResults = this.sortResultsByRelevance(results, query);
        
        this.resultsGrid.innerHTML = sortedResults
            .slice(0, 100) // Limit to first 100 results for performance
            .map(entry => this.createResultCard(entry, query))
            .join('');
        
        this.resultsGrid.style.display = 'grid';
    }
    
    sortResultsByRelevance(results, query) {
        return results.sort((a, b) => {
            const aScore = this.getRelevanceScore(a, query);
            const bScore = this.getRelevanceScore(b, query);
            return bScore - aScore;
        });
    }
    
    getRelevanceScore(entry, query) {
        const mongolian = entry.mongolian.toLowerCase();
        const english = entry.english.toLowerCase();
        let score = 0;
        
        // Exact match gets highest score
        if (mongolian === query || english === query) score += 100;
        // Starts with query gets high score
        if (mongolian.startsWith(query) || english.startsWith(query)) score += 50;
        // Contains query gets base score
        if (mongolian.includes(query) || english.includes(query)) score += 10;
        
        return score;
    }
    
    createResultCard(entry, query) {
        const mongolianHighlighted = this.highlightText(entry.mongolian, query);
        const englishHighlighted = this.highlightText(entry.english, query);
        
        return `
            <div class="result-card">
                <div class="mongolian-text">${mongolianHighlighted}</div>
                <div class="english-text">${englishHighlighted}</div>
            </div>
        `;
    }
    
    highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${this.escapeRegExp(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    updateResultsCount(count) {
        const plural = count === 1 ? '' : 's';
        this.resultsCount.textContent = `${count} result${plural}`;
    }
    
    showNoResults() {
        this.noResults.style.display = 'block';
        this.resultsGrid.style.display = 'none';
        this.resultsCount.textContent = '';
    }
    
    hideNoResults() {
        this.noResults.style.display = 'none';
    }
    
    clearResults() {
        this.resultsGrid.innerHTML = '';
        this.resultsGrid.style.display = 'none';
        this.hideNoResults();
        this.resultsCount.textContent = '';
    }
}

// Initialize the dictionary app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MongolianDictionary();
});