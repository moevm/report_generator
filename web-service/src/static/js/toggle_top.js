function toggle_top() {
    let btn = $('#md-editor-github')
    let name  = btn.html()
    let isMarkDownEditor = name === "Markdown Editor";
    btn.html( isMarkDownEditor? "GitHub" : "Markdown Editor")
    $('#markdown-place-editor').toggle('show')
    $('#github-manager').toggle('show')
    localStorage['md-editor'] = !isMarkDownEditor
}