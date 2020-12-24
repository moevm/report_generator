correctFields = new Map()

$('#empty_doc').click(function () {
    $('#btnGroupDrop1').text("Пустой документ");
    $('#requirements').hide('slow').empty();
    pull_settings()
});

function main_settings() {
    console.log('MAIN SETTINGS');
    let settings = $('#main_settings');
    if (settings.is(':hidden'))
        settings.show('slow');
    else
        settings.hide('slow');
    return false;
}

function create_lab() {
    $('#btnGroupDrop1').text("Лабораторная работа");
    if ($('#requirements').is(':hidden') || $('*').is('#field_for_course')) {
        const for_lab = '#field_for_lab';
        $(requirements).empty();
        $(requirements).append('<div class="row" id="field_for_lab"</div>');
        createLabsField(for_lab);
        $(requirements).show("slow");
    }
    pull_settings()
}

function create_course_work() {
    $('#btnGroupDrop1').text("Курсовая работа");

    if ($(requirements).is(':hidden') || $('*').is('#field_for_lab')) {
        const for_course = '#field_for_course';
        $(requirements).empty();
        $(requirements).append('<div class="row" id="field_for_course"</div>');

        createLabsField(for_course);

        $(for_course).append(createFieldForConfigurator('min_pages', 'Минимальное количество страниц'));
        $(for_course).append(createFieldForConfigurator('date_start', 'Дата начала', '0.0.1970'));
        $(for_course).append(createFieldForConfigurator('date_finish', 'Дата сдачи', '0.0.1970'));
        $(for_course).append(createFieldForConfigurator('date_defend', 'Дата защиты', '0.0.1970'));
        $(for_course).append(createFieldForConfigurator('init_data', 'Исходные данные', 'Исходные данные в задании курсовой работы', false, true));
        $(for_course).append(createFieldForConfigurator('context_of_explanation', 'Содержание пояснительной записки', '', false, true));
        $(for_course).append(createFieldForConfigurator('annotation', 'Аннотация', 'Аннотация', false, true));
        $(for_course).append(createFieldForConfigurator('en_annotation', 'Аннотация на английском', 'Аннотация на английском', false, true));
        $(for_course).append(createFieldForConfigurator('list_of_source', 'Список источников',
            'Иванов И. И. Книга одного-трех авторов. М.: Издательство, 2010. 000 с.\n' +
               'Книга четырех авторов / И. И. Иванов, П. П. Петров, С. С. Сидоров, В. В. Васильев. СПб.: Издательство, 2010. 000 с.\n' +
               'Книга пяти и более авторов / И. И. Иванов, П. П. Петров, С. С. Сидоров и др.. СПб.: Издательство, 2010. 000 с.', false, true));
        $(requirements).show('show');
    }

    pull_settings();
}

var requirements = '#requirements';
$('#repo_name').focus(function () {
    $(this).attr("style", "box-shadow: 0px 0px 0px 0 red;")
    $('#wiki_name').attr("style", "box-shadow: 0px 0px 0px 0 red;")
})

$('#wiki_name').focus(function () {
    $(this).attr("style", "box-shadow: 0px 0px 0px 0 red;")
    $('repo_name').attr("style", "box-shadow: 0px 0px 0px 0 red;")
})

$('#lab_doc').click(function () {
    create_lab();
});

$('.dropdown-toggle').dropdown()


$('#course_doc').click(function () {
    create_course_work();
});

function setCheck(id, regex = RegExp(""), title = '', text = '') {
    correctFields[id] = false
    $(id)
        .focus(function () {
            $(this).attr("style", "box-shadow: 0px 0px 0px 0 red;")
        })
        .focusout(function() {
            let value = $(this).val()
            if (value === "") {
                $(this).attr("style", "box-shadow: 0px 0px 0px 0 red;")
                correctFields[id] = false
                return;
            }

            if (value.search(regex) !== 0) {
                $('#AlertBox').html(title + "<br>" +
                    "<div style = 'font-size: small'>" + text + "</div>").fadeIn()
                window.setTimeout(function () {
                    $('#AlertBox').fadeOut(300)
                }, 5000);
                $(this).attr("style", "box-shadow: 0px 0px 2px 0 red;")
                correctFields[id] = false
            } else {
                correctFields[id] = true
                $(this).val(value.trim())
                $(this).attr("style", "box-shadow: 0px 0px 0px 0 red;")
            }
    })
}

function createLabsField(id) {

    $(id).append(createFieldForConfigurator('teacher', 'Преподаватель', 'Иванов И.И.', true))
    setCheck('#teacher', /[А-Я][а-я]+\s[А-Я].[А-Я].\s*$/,
        "Некорректное имя преподавателя",
        "Hint: имя преподавателя должно состоять из кириллицы и начинаться с заглавной буквы")

    $(id).append(createFieldForConfigurator('student', 'Студент', 'Иванов И.И.', true))
    setCheck('#student', /[А-Я][а-я]+\s[А-Я].[А-Я].\s*$/,
        "Некорректное имя студента",
        "Hint: имя студента должно состоять из кириллицы и начинаться с заглавной буквы")


    $(id).append(createFieldForConfigurator('number_group', 'Номер группы', '6392', true));
    setCheck('#number_group', /\d\d\d\d\s*$/,
        "Некорректный номер группы",
        "Hint: номер группы должен состоять из 4 цифр")

    $(id).append(createFieldForConfigurator('number_of_report', 'Номер работы', '1', true));
    setCheck('#number_of_report', /([1-9]|[1-9]\d)\s*$/,
        "Некорректный номер работы",
        "Hint: номер работы лежит в диапазоне 1-99")

    $(id).append(createFieldForConfigurator('theme', 'Тема работы', '', true));
    $(id).append(createFieldForConfigurator('discipline', 'Название предмета', '',true));
    $(id).append(createFieldForConfigurator('cathedra', 'Кафедра', '', true));
    $(id).append(createFieldForConfigurator('md_pages', 'Список wiki страниц', 'без расширения .md', true));
    $(id).append(createFieldForConfigurator('source_files', 'Файлы для приложения', '/src/example.c'));

    $(id).append(createFieldForConfigurator('branch_name', 'Название ветки', 'master'));
    $(id).append(createFieldForConfigurator('number_of_pr', 'Комментарии из пулл реквеста', 'Нужно вести номер пулл реквеста', true));
    setCheck('#number_of_pr', /([1-9]|[1-9]\d*)\s*$/,
        "Некорректный номер пулл реквеста",
        "Hint: номер пулл реквеста принимает значения > 1")

}

function createFieldForConfigurator(id, name, pl = '', isRequire=false, textArea=false) {
    if (!pl)
        pl = name;
    if (isRequire) {
        return "<div class='col-md-6 mb-3'><label for='" + id + "'>" + name + "</label>" +
            "<input type='text' class='form-control' id='" + id + "' placeholder='" + pl + "' value=''></div>";

    } else if (textArea) {
        return "<div class='col-md-6 mb-3'><label for='" + id + "'>" + name + "</label><textarea class='form-control' id='" + id + "' placeholder='" + pl + "' aria-label='With textarea'></textarea></div>"
    } else {
        return "<div class='col-md-6 mb-3'><label for='" + id + "'>" + name + "</label><input type='text' class='form-control' id='" + id + "' placeholder='" + pl + "' value=''></div>"
    }
}

function isCorrectImportantData() {
    return correctFields['#teacher'] && correctFields['#student'] && correctFields['#number_group'] &&
        correctFields['#number_of_report'] && correctFields['#number_of_pr']
}
//oninvalid="this.setCustomValidity('Please Enter valid email')"
$('#btn_submit').click(function () {
    if (isCorrectImportantData()) {
        $("div").remove("#spinner_for_answer");
        $("a").remove("#total_link");

    }
})

$('#google_drive_button').click(function () {
    $('#buttons_field').append('<div id="spinner_for_answer" class="spinner-border text-primary" style="width: 5rem; height: 5rem;" role="status"></div>')
})

$('#style_setter').click(function () {
    if ($('#style_settings').is(':hidden')) {
        $('#style_settings').show("slow");
        $("#style_setter").css("background", "#FF2400");
    } else {
        $('#style_settings').hide("slow");
        $("#style_setter").css("background", "#007bff");
    }
});


function validate(event) {
    if ((event.keyCode < 48 || event.keyCode > 57)) {
        event.returnValue = false;
    }
}

function submitForm() {
    if (!isCorrectImportantData()) {
        $('#AlertBox').html("Данные заполнены некорректно!").fadeIn()
        window.setTimeout(function () {
            $('#AlertBox').fadeOut(300)
        }, 5000);

        for (id in correctFields) {
            if (correctFields.hasOwnProperty(id)) {
                if (!correctFields[id]) {
                    $(id).attr("style", "box-shadow: 0px 0px 2px 0 red;")
                }
            }
        }

        return;
    }

    let check_send = false; // TODO: add markdown editor
    console.log('LOG DATA');
    console.log(check_send);

    $('#buttons_field').append('<div id="spinner_for_answer" class="spinner-border text-success" style="width: 5rem; height: 5rem;" role="status"></div>')
    if (check_send) {
        $.ajax({
            type: "POST",
            crossDomain: true,
            data: get_data_from_form(),
            success: function (json, status) {
                console.log('Success for submit form');
                location.reload();
            },
        })
    } else {
        console.log('to /download')
        console.log(window.location.origin + '/download')
        let data = get_data_from_form();
        let student, pdf;

        if ($("*").is("#student")) {
            student = $('#student').val();
        }
        //window.open(window.location.origin + '/download')
        $.ajax({
            type: "POST",
            url: window.location.origin + '/download',
            data: data,
            success: function(data, status){
                window.open(window.location.origin + '/dw_report?name=' + student)

                $('#wiki_name').attr("style", "box-shadow: 0px 0px 0px 0 red;")
                $('#repo_name').attr("style", "box-shadow: 0px 0px 0px 0 red;")
                $('#spinner_for_answer').remove()
            },
            error: function (data) {
                $('#AlertBox').html(
                    "<div style = 'font-size: small'>" + data.responseText + "</div>").fadeIn()
                window.setTimeout(function () {
                    $('#AlertBox').fadeOut(300)
                }, 5000);
                $('#repo_name').attr("style", "box-shadow: 0px 0px 2px 0 red;")
                $('#wiki_name').attr("style", "box-shadow: 0px 0px 2px 0 red;")

                $('#spinner_for_answer').remove()
            }
        })
    }
}

function get_data_from_md() {
    console.log(simplemde.value())
    let info = get_data_from_form()
    let mdText = simplemde.value()
    info += `&md=${mdText}`
    info += `&is_md_editor=${localStorage['md-editor']}`
    return info
}

function google_drive() {
    $.ajax({
                type: "POST",
                url: window.location.origin + '/download',
                data: get_data_from_form(),
                success: function(data, status){
                    console.log('go google drive');
                    window.location = window.location.origin + '/googleauthorize';
                    //window.open(window.location.origin + '/dw_report?name=' + student)
                }
    })
}

function get_data_from_form() {
    const repo_name = $('#repo_name').val();
    const wiki_name = $('#wiki_name').val();
    let branch_name = $('#branch_name').val();
    if (branch_name === '')
        branch_name = 'master';
    const general_font = $('#general_font').val();
    const general_size = $('#general_size').val();
    const code_font = $('#code_font').val();
    const code_size = $('#code_size').val();
    const for_h1 = $('#for_h1').val();
    const for_h2 = $('#for_h2').val();
    const for_h3 = $('#for_h3').val();
    const for_h4 = $('#for_h4').val();
    const for_h5 = $('#for_h5').val();
    const for_h6 = $('#for_h6').val();
    const pages = $('#md_pages').val();
    const source_files = $('#source_files').val();

    let result = `repo_name=${repo_name}`;
    result += `&wiki_name=${wiki_name}`;
    result += `&branch_name=${branch_name}`;
    result += `&general_font=${general_font}`;
    result += `&general_size=${general_size}`;
    result += `&code_font=${code_font}`;
    result += `&code_size=${code_size}`;
    result += `&h1=${for_h1}`;
    result += `&h2=${for_h2}`;
    result += `&h3=${for_h3}`;
    result += `&h4=${for_h4}`;
    result += `&h5=${for_h5}`;
    result += `&h6=${for_h6}`;
    result += `&pages=${pages.replace(new RegExp(' ', 'g'), '')}`;
    result += `&download=${source_files.replace(new RegExp(' ', 'g'), '')}`;


    let check_val = (value) => {
        if (value === '')
            return 'unknown';
        return value;
    }
    if ($("*").is("#teacher")) {
        var teacher = check_val($('#teacher').val());
        result += `&teacher=${teacher}`;
    }
    if ($("*").is("#student")) {
        var student = check_val($('#student').val());
        result += `&student=${student}`;
    }
     if ($("*").is("#number_of_report")) {
        var number_of_report = check_val($('#number_of_report').val());
        result += `&number=${number_of_report}`;
    }
    if ($("*").is("#number_group")) {
        var number_group = $('#number_group').val();
        if (number_group === '')
            number_group = '0'
        result += `&number_group=${number_group}`;
    }
    if ($("*").is("#theme")) {
        var theme = check_val($('#theme').val());
        result += `&theme=${theme}`;
    }
    if ($("*").is("#discipline")) {
        var discipline = check_val($('#discipline').val());
        result += `&discipline=${discipline}`;
    }
    if ($("*").is("#cathedra")) {
        var cathedra = check_val($('#cathedra').val());
        result += `&cathedra=${cathedra}`;
    }
    if ($("*").is("#min_pages")) {
        var min_pages = $('#min_pages').val();
        result += `&min_pages=${min_pages}`;
    }
    if ($("*").is("#date_start")) {
        var date_start = $('#date_start').val();
        result += `&date_start=${date_start}`;
    }
    if ($("*").is("#date_finish")) {
        var date_finish = $('#date_finish').val();
        result += `&date_finish=${date_finish}`;
    }
    if ($("*").is("#date_defend")) {
        var date_defend = $('#date_defend').val();
        result += `&date_defend=${date_defend}`;
    }
    if ($("*").is("#number_of_pr")) {
        var number_of_pr = $('#number_of_pr').val();
        result += `&number_of_pr=${number_of_pr}`;
    }
    if ($("*").is("#annotation")) {
        var annotation = check_val($('#annotation').val());
        result += `&annotation=${annotation}`;
    }
    if ($("*").is("#list_of_source")) {
        var list_of_source = check_val($('#list_of_source').val());
        result += `&list_of_source=${list_of_source}`;
    }
    if ($("*").is("#en_annotation")) {
        var en_annotation = check_val($('#en_annotation').val());
        result += `&en_annotation=${en_annotation}`;
    }
    if ($("*").is("#init_data")) {
        var init_data = check_val($('#init_data').val());
        result += `&init_data=${init_data}`;
    }
    if ($("*").is("#context_of_explanation")) {
        var context_of_explanation = check_val($('#context_of_explanation').val());
        result += `&context_of_explanation=${context_of_explanation}`;
    }
    if ($("*").is('#is_pdf')) {
        var pdf = check_val($('#is_pdf').is(':checked'));
        result += `&PDF=${pdf ? "True" : "False"}`;
    }
    console.log(result)
    return result;
}

const _a = document.getElementById('repo_menu');

//_a.addEventListener('click', changeRepo);

function changeRepo(e) {
    const ssh_str = 'git@github.com:' + event.target.href.substring(19) + '.git';
    $("#repo_name").val(ssh_str);
    e.preventDefault();
}

var _b = document.getElementById('wiki_menu');

//_b.addEventListener('click', changeWiki);

function changeWiki(e) {
    const wiki_str = event.target.href + '.wiki.git';
    $("#wiki_name").val(wiki_str);
    e.preventDefault();
}

function check_type() {
    let query = decodeURI(window.location.search).split('?')[1];
    let d = {}

    if (query) {
        query.split('&').forEach((value) => {
            let val = value.split('=')
            d[val[0]] = val[1].replace(new RegExp("_",'g'), ' ')
        })
    }

    if ('type' in d && d['type'].toLowerCase() === 'lr'){
        create_lab();
    }
    else if ('type' in d && d['type'].toLowerCase() === 'kr'){
        create_course_work();
    }

}

check_type();