# Syntax error - Support for the experimental syntax 'decorators-legacy' isn't currently enabled



我的解决方法是在vite.config.js中将plugins . preact放到后面去就行了







web3.js无法引入，各种错误

npm install agent-base process

修改vite.config.js:

```
    resolve: {
        alias: {
            process: 'process/browser',
            util: 'util',
            https: 'agent-base',
            http: 'agent-base',
            zlib: 'browserify-zlib'
        }
    },
        optimizeDeps: {        esbuildOptions: {
            define: {
                global: 'globalThis',
            },
            plugins: [
                GlobalsPolyfills({
                    process: true,
                    buffer: true,
                }),
            ],
        },
    },
```

