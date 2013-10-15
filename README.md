# cefp

A CEF-ish parser, accepting CEF input and returning a native hash, written in
about 30 lines of clojure and compiling to a native Java jar for use in your
jvm related projects.

## Why CEF-ish?

The fields themselves aren't inspected so everything gets returned as a string
for now and leaves it to the application to work with the data.

## Next Todos

- detect dates and make them native
- detect numeric data (?)

# Running Tests

You'll need Leiningen to build this.  If you have lein installed, in the base
of the project, just run `lein test`.

# Usage

Coming soon.

# License

See accompanying LICENSE file.

tl;dr - MIT

