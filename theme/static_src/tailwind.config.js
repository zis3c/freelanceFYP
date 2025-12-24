module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        './node_modules/flowbite/**/*.js'
    ],
    theme: {
        extend: {
            colors: {
               // User specified: Primary Indigo (#4F46E5), Secondary Emerald (#10B981)
               primary: {
                   DEFAULT: '#4F46E5', // Indigo 600
                   50: '#eef2ff',
                   100: '#e0e7ff',
                   200: '#c7d2fe',
                   300: '#a5b4fc',
                   400: '#818cf8',
                   500: '#6366f1',
                   600: '#4f46e5', 
                   700: '#4338ca',
                   800: '#3730a3',
                   900: '#312e81',
               },
               secondary: {
                   DEFAULT: '#10B981', // Emerald 500
                   50: '#ecfdf5',
                   100: '#d1fae5',
                   200: '#a7f3d0',
                   300: '#6ee7b7',
                   400: '#34d399',
                   500: '#10b981',
                   600: '#059669',
                   700: '#047857',
                   800: '#065f46',
                   900: '#064e3b',
               }
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('flowbite/plugin'),
    ],
}
