function get_sv(name) {
    let ls = JSON.parse(localStorage['start_dict'])
    console.log(ls)
    if ('start_dict' in localStorage && name in localStorage['start_dict'])
        $(name).val(localStorage['start_dict'][name])
}

const SETTINGS_CONFIGURATION = ['general_font', 'general_size', 'code_font', 'code_size', 'for_h1', 'for_h1',
    'for_h2', 'for_h3', 'for_h4', 'for_h5', 'for_h6', 'teacher', 'student', 'number_group', 'theme', 'discipline', 'cathedra',
    'min_pages', 'date_start', 'date_finish', 'date_defend', 'md']


function pull_settings() {

    let query = decodeURI(window.location.search).split('?')[1]
    let d = {}
    if (query){
        query.split('&').forEach((value) => {
        let val = value.split('=')
        d[val[0]] = val[1].replace(new RegExp("_",'g'), ' ')
    })
    }

    let defaultSettings = d
    if (defaultSettings){
        console.log(defaultSettings)
        SETTINGS_CONFIGURATION.forEach((value => {
            if (value in defaultSettings){
                    let el = $('#' + value)
                    if (el)
                        el.val(defaultSettings[value])
                }
            }))
    }
}

pull_settings()
