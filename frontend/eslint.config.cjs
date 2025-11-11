const reactPlugin = require('eslint-plugin-react');
const reactHooksPlugin = require('eslint-plugin-react-hooks');

module.exports = [
  {
    files: ['src/**/*.js', 'src/**/*.jsx'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    plugins: { react: reactPlugin, 'react-hooks': reactHooksPlugin },
    // Merge recommended rules from ESLint core + plugins into flat config rules
    rules: {
      // eslint:recommended rules are already applied by ESLint by default for flat configs,
      // but we prioritize plugin recommended rules here by spreading them.
      ...(reactPlugin && reactPlugin.configs && reactPlugin.configs.recommended
        ? reactPlugin.configs.recommended.rules
        : {}),
      ...(reactHooksPlugin && reactHooksPlugin.configs && reactHooksPlugin.configs.recommended
        ? reactHooksPlugin.configs.recommended.rules
        : {}),

      // Project overrides
      'react/prop-types': 'off',
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'react/react-in-jsx-scope': 'off',
    },
    settings: { react: { version: 'detect' } },
  },
];
