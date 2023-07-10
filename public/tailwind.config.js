/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './**/*.html',
        '../**/*.html'
    ],
    darkMode: 'class',
    theme: {
        screens: {
            'phone': '480px',
            'tablet': '640px',
            'laptop': '960px',
            'desktop': '1024px',
        },
    }
}

