/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./_src/templates/**/*','./_src/templates/*/*'],
    theme: {
    colors: {
        base: {
            '50': '#fff4ed',
            '100': '#ffe7d4',
            '200': '#ffcaa8',
            '300': '#ffa571',
            '400': '#ff7438',
            '500': '#fe4909',
            '600': '#ef3407',
            '700': '#c62308',
            '800': '#9d1d0f',
            '900': '#7e1c10',
            '950': '#440a06',
        },
        white: '#fff',
        black: '#000'
    },
},
    plugins: [],
}
