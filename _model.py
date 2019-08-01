"""PytSite Content Menu Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import form, odm, content, widget
from plugins.menu import Menu


class ContentMenu(Menu):
    @property
    def is_container(self) -> bool:
        return self.f_get('is_container')

    @is_container.setter
    def is_container(self, value: bool):
        self.f_set('is_container', value)

    @property
    def entity(self) -> content.ContentWithURL:
        return self.f_get('entity')

    @entity.setter
    def entity(self, value: content.ContentWithURL):
        self.f_set('entity', value)

    def _setup_fields(self):
        super()._setup_fields()

        self.get_field('title').is_required = False

        self.define_field(odm.field.Bool('is_container'))
        self.define_field(odm.field.Ref('entity', model_cls=content.ContentWithURL))

    def _on_f_get(self, field_name: str, value, **kwargs):
        if field_name in ('title', 'path') and self.entity:
            if field_name == 'title':
                return self.entity.title
            if field_name == 'path':
                return self.entity.route_alias.alias

        return super()._on_f_get(field_name, value)

    def _on_after_save(self, first_save: bool = False, **kwargs):
        if self.is_container:
            if self.entity:
                self.f_set('entity', None).save()

    def odm_ui_m_form_setup(self, frm: form.Form):
        super().odm_ui_m_form_setup(frm)

        # Add CSS class to let JS code work with forms of inherited models
        if self.model != 'content_menu':
            frm.css += ' odm-ui-form-content_menu'

    def odm_ui_m_form_setup_widgets(self, frm: form.Form):
        super().odm_ui_m_form_setup_widgets(frm)

        if frm.has_widget('_parent'):
            frm.remove_widget('_parent')

        frm.add_widget(widget.select.Checkbox(
            uid='is_container',
            weight=25,
            label=self.t('is_container'),
            value=self.is_container,
        ))

        frm.add_widget(content.widget.EntitySelect(
            uid='entity',
            weight=150,
            label=self.t('content'),
            required=self.get_field('entity').is_required,
            value=self.entity,
        ))
