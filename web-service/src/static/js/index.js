$('#empty_doc').click(function () {
    $('#btnGroupDrop1').text("Пустой документ");
    $('#requirements').hide('slow');
    $('#requirements').empty();
    pull_settings()
});

var requirements = '#requirements';
$('#lab_doc').click(function () {
    $('#btnGroupDrop1').text("Лабораторная работа");
    if ($('#requirements').is(':hidden') || $('*').is('#field_for_course')) {
        const for_lab = '#field_for_lab';
        $(requirements).empty();
        $(requirements).append('<div class="row" id="field_for_lab"</div>');
        createLabsField(for_lab);
        $(requirements).show("slow")
    }
    pull_settings()
});

$('.dropdown-toggle').dropdown()

$('#course_doc').click(function () {
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

        $(requirements).show('show');
    }
        pull_settings()
});

function createLabsField(id) {
    $(id).append(createFieldForConfigurator('teacher', 'Преподаватель'));
    $(id).append(createFieldForConfigurator('student', 'Студент'));
    $(id).append(createFieldForConfigurator('number_group', 'Номер группы', '1111'));
    $(id).append(createFieldForConfigurator('theme', 'Тема работы'));
    $(id).append(createFieldForConfigurator('discipline', 'Название предмета'));
    $(id).append(createFieldForConfigurator('cathedra', 'Кафедра'))

}

function createFieldForConfigurator(id, name, pl = '') {
    if (!pl)
        pl = name;
    return "<div class='col-md-6 mb-3'><label for='" + id + "'>" + name + "</label><input type='text' class='form-control' id='" + id + "' placeholder='" + pl + "' value=''></div>"
}

function checkImportantData() {
    return $('#wiki_name').val() != '' && $('#repo_name').val() != '' && $('#branch').val() != ''
}

$('#btn_submit').click(function () {
    if (checkImportantData()) {
        $("div").remove("#spinner_for_answer");
        $("a").remove("#total_link");
        $('#buttons_field').append('<div id="spinner_for_answer" class="spinner-border text-success" role="status"></div>')
    }
})

$('#style_setter').click(function () {
    if ($('#style_settings').is(':hidden')) {
        $('#style_settings').show("slow")
        $("#style_setter").css("background", "#FF2400");
    } else {
        $('#style_settings').hide("slow")
        $("#style_setter").css("background", "#007bff");
    }
});


function validate(event) {
    if ((event.keyCode < 48 || event.keyCode > 57)) {
        event.returnValue = false;
    }
}

function submitForm() {
    let check_send = $('#is_send_to_github').prop('checked')
    console.log(check_send)
    if (check_send)
        $.ajax({
            type: "POST",
            crossDomain: true,
            data: get_data_from_form(),
            success: function (json, status) {
                console.log('Success for submit form');
                location.reload();
            },
        })
    else {
        console.log('to /download')
        console.log(window.location.origin + '/download')
        //window.open(window.location.origin + '/download')
        $.ajax({
                type: "POST",
                url: window.location.origin + '/download',
                data: get_data_from_md(),
                success: function(data, status){
                    window.open(window.location.origin + '/dw_report')
                    //location.reload()
                    console.log(window.location.origin + '/download_file')
                    //$.ajax({
                    //    type: 'GET',
                    //    url: window.location.origin + '/download_file',
                    //    target: true,
                    //    success: function (data, status) {
                    //        console.log(data)
                    //    }
                    //})
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

function get_data_from_form() {
    const repo_name = $('#repo_name').val();
    const wiki_name = $('#wiki_name').val();
    var branch_name = $('#branch_name').val();
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

    var result = `repo_name=${repo_name}`;
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
    result += `&pages=${pages}`;
    result += `&download=${source_files.replace(' ', '')}`;

    if ($("*").is("#teacher")) {
        var teacher = $('#teacher').val();
        result += `&teacher=${teacher}`;
    }
    if ($("*").is("#student")) {
        var student = $('#student').val();
        result += `&student=${student}`;
    }
    if ($("*").is("#number_group")) {
        var number_group = $('#number_group').val();
        result += `&number_group=${number_group}`;
    }
    if ($("*").is("#theme")) {
        var theme = $('#theme').val();
        result += `&theme=${theme}`;
    }
    if ($("*").is("#discipline")) {
        var discipline = $('#discipline').val();
        result += `&discipline=${discipline}`;
    }
    if ($("*").is("#cathedra")) {
        var cathedra = $('#cathedra').val();
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
    ;
    if ($("*").is("#number_of_pr")) {
        var number_of_pr = $('#number_of_pr').val();
        result += `&number_of_pr=${number_of_pr}`;
    }
    return result;
}

const _a = document.getElementById('repo_menu');

_a.addEventListener('click', changeRepo);

function changeRepo(e) {
    var ssh_str = 'git@github.com:' + event.target.href.substring(19) + '.git';
    $("#repo_name").val(ssh_str);
    e.preventDefault();
}

var _b = document.getElementById('wiki_menu');

_b.addEventListener('click', changeWiki);

function changeWiki(e) {
    const wiki_str = event.target.href + '.wiki.git';
    $("#wiki_name").val(wiki_str);
    e.preventDefault();
}