document.addEventListener("DOMContentLoaded", ready);
function ready(){
    //if (!('md-editor' in localStorage))
    localStorage['md-editor'] = true

    let query = decodeURI(window.location.search).split('?')[1]
    let d = {}
    if (query){
        query.split('&').forEach((value) => {
        let val = value.split('=')
        d[val[0]] = val[1].replace(new RegExp("_",'g'), ' ')
    })
    }
    if (d)
        localStorage['start_dict'] = JSON.stringify(d)
}