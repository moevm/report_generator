function openGithub(url) {
    if (localStorage['url'] != url)
    {
        localStorage['url'] = url;
        window.open(url, '_blank');
    }
}