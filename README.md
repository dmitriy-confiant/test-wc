# test-wc

## client/test.js

`client/test.js` is an immediately-invoked function expression that runs as
soon as the script loads. It checks whether `document.URL` is a string that
starts with `chrome-devtools://`. If it does, meaning the script has been
injected into a Chrome DevTools page, it throws
`Error("Don't inject into devtools.")` to stop running there. On any other
page it does nothing.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
