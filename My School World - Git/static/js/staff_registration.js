tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                },
                secondary: {
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                }
            },
            fontFamily: {
                times: ['"Times New Roman"', 'serif'],
              },

        }
    }
}
const profileDropdown = document.getElementById('profileDropdown');
const dropdownMenu = document.getElementById('dropdownMenu');

profileDropdown.addEventListener('click', () => {
    dropdownMenu.classList.toggle('hidden');
});

// Close dropdown when clicking outside
window.addEventListener('click', (e) => {
    if (!profileDropdown.contains(e.target)) {
        dropdownMenu.classList.add('hidden');
    }
});


// Custom dropdown for Standard
const standardDropdownButton = document.getElementById('dropdownButton');
const standardDropdownMenu = document.querySelector('#custom-standard-dropdown #dropdownMenu');
const standardSelectedOption = document.getElementById('selectedOption');
const standardInput = document.getElementById('standardInput');

standardDropdownButton.addEventListener('click', function(e) {
    e.stopPropagation();
    standardDropdownMenu.classList.toggle('hidden');
});
standardDropdownMenu.querySelectorAll('li').forEach(function(item) {
    item.addEventListener('click', function() {
        standardSelectedOption.textContent = this.textContent;
        standardInput.value = this.textContent;
        standardDropdownMenu.classList.add('hidden');
    });
});
window.addEventListener('click', function(e) {
    if (!standardDropdownButton.contains(e.target)) {
        standardDropdownMenu.classList.add('hidden');
    }
});