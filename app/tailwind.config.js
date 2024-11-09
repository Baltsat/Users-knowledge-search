/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {},
		screens: {
			xl: { max: '1279px' },
			// => @media (max-width: 1279px) { ... }

			lg: { max: '1023px' },
			// => @media (max-width: 1023px) { ... }

			md: { max: '767px' },
			// => @media (max-width: 767px) { ... }

			sm: { max: '639px' }
			// => @media (max-width: 639px) { ... }
		}
	},
	plugins: [
		require('daisyui'),
		require('@tailwindcss/container-queries'),
		require('@tailwindcss/typography')
	],
	daisyui: {
    styled: true,
    // base: true,
    logs: false,
    darkTheme: 'dark',
    themes: [
      {
        light: {
          primary: '#3030FF',
          secondary: '#36D399',
          accent: '#3dfbcd',
          neutral: '#363853',
          'base-100': '#ffffff',
          'base-200': '#f3f3f4',
          'base-300': '#e6e5e8',

          info: '#64B5F6',
          success: '#26BB00',
          warning: '#fbbd23',
          error: '#F32051',
        },
      },
      {
        dark: {
          primary: '#4747FF',
          secondary: '#3dfbcd',
          accent: '#1fb2a6',
          neutral: '#DFE1E5',
          'base-100': '#232326',
          'base-200': '#191A1C',
          'base-300': '#101010',

          info: '#64B5F6',
          success: '#04BB00',
          warning: '#FBBD23',
          error: '#F2466E',
        },
      },
    ],
  },
};
