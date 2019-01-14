import $ from 'jquery';


function toggleState(form) {
    const isContainerWidget = form.getWidget('is_container');
    const entityWidget = form.getWidget('entity');
    const titleWidget = form.getWidget('title');
    const pathWidget = form.getWidget('path');

    if (isContainerWidget.find('input[type=checkbox]')[0].checked) {
        entityWidget.find('select').attr('required', false);
        entityWidget.hide();

        titleWidget.show();
        titleWidget.find('input').attr('required', true);

        pathWidget.show();
    } else {
        entityWidget.show();
        entityWidget.find('select').attr('required', true);

        titleWidget.find('input').attr('required', false);
        titleWidget.hide();

        pathWidget.hide();
    }
}


$('form[name=odm_ui_modify_content_menu]').on('ready:form:pytsite', (e, form) => {
    form.getWidget('is_container').on('change', () => toggleState(form));
    toggleState(form);
});
