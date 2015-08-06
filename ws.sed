# Only within the body:
/<body>/,/<\/body>/ {

    # Remove the current <pre>s
    /^<\/\?pre/ d

    # For plain-text lines:
    /^[^<>]\+$/ {
        # Wrap up to the last double-space in <pre>
        s/^\(.*  \)/<span xml:space="preserve">\1<\/span>/

        # Append <br>
        a\
        <br/>
    }

}

