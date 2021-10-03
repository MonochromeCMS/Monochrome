module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    'eslint:recommended',
    '@vue/typescript/recommended',
    '@vue/prettier',
    '@vue/prettier/@typescript-eslint',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // clean code
    complexity: ['error', { max: 10 }],
    'max-lines': ['error', { max: 300, skipBlankLines: true, skipComments: true }],
    'max-lines-per-function': ['error', { max: 80, skipBlankLines: true, skipComments: true }],
    'max-depth': ['error', 4],
    // /. clean code
    // vue compiler macros
    'no-undef': 'off',
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': 'off',
    // /. vue compiler macros
    // vue base
    'vue/eqeqeq': 'error',
    'vue/component-definition-name-casing': ['warn', 'kebab-case'],
    'vue/match-component-file-name': 'warn',
    'vue/component-name-in-template-casing': [
      'error',
      'kebab-case',
      {
        registeredComponentsOnly: false,
      },
    ],
    // /.vue base
    // typescript
    '@typescript-eslint/prefer-ts-expect-error': 'warn',
    '@typescript-eslint/no-var-requires': 'off',
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/consistent-type-imports': [
      'error',
      {
        prefer: 'type-imports',
        disallowTypeAnnotations: true,
      },
    ],
    '@typescript-eslint/no-explicit-any': 'off',
    '@typescript-eslint/ban-types': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/array-type': 'warn',
    '@typescript-eslint/no-empty-function': 'off',
    '@typescript-eslint/member-ordering': [
      'warn',
      {
        default: [
          'public-method', // = ["public-static-method", "public-instance-method"]
          'protected-method', // = ["protected-static-method", "protected-instance-method"]
          'private-method', // = ["private-static-method", "private-instance-method"]
        ],
      },
    ],
    'lines-between-class-members': 'off',
    '@typescript-eslint/lines-between-class-members': 'warn',
    // https://github.com/typescript-eslint/typescript-eslint/blob/master/packages/eslint-plugin/docs/rules/strict-boolean-expressions.md
    '@typescript-eslint/strict-boolean-expressions': ['off'],
    // /. typescript
  },
  overrides: [
    {
      files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
      env: {
        jest: true,
      },
    },
  ],
};
