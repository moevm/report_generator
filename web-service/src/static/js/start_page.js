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
    let defaultSettings = {}
    if ('start_dict' in localStorage)
        defaultSettings = JSON.parse(localStorage['start_dict'])
    else
        return
    console.log(defaultSettings)
    SETTINGS_CONFIGURATION.forEach((value => {
        if (value in defaultSettings){
                let el = $('#' + value)
                if (el)
                    el.val(defaultSettings[value])
            }
        }))
}

pull_settings()